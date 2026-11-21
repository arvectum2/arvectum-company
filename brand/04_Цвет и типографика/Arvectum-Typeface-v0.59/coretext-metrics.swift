import Foundation
import AppKit
import CoreText
import CoreGraphics

func registeredFont(_ source:String,_ pts:CGFloat) -> CTFont {
 let url=URL(fileURLWithPath:source)
 var err:Unmanaged<CFError>?
 guard CTFontManagerRegisterFontsForURL(url as CFURL,.process,&err),
       let descs=CTFontManagerCreateFontDescriptorsFromURL(url as CFURL) as? [CTFontDescriptor],
       let desc=descs.first
 else {fatalError("Registration failed: \(source) \(String(describing:err))")}
 let font=CTFontCreateWithFontDescriptor(desc,pts,nil)
 guard String(CTFontCopyPostScriptName(font)).contains(source.contains("059") ? "Draft059" : "Draft058") else {fatalError("unexpected fallback \(CTFontCopyPostScriptName(font))")}
 return font
}
func line(_ text:String,_ font:CTFont) -> CTLine {
 let attrs:[NSAttributedString.Key:Any]=[
 NSAttributedString.Key(kCTFontAttributeName as String):font,
 NSAttributedString.Key(kCTForegroundColorAttributeName as String):CGColor(red:0,green:0.075,blue:0.18,alpha:1)
 ]
 return CTLineCreateWithAttributedString(NSAttributedString(string:text,attributes:attrs))
}
let base=URL(fileURLWithPath:CommandLine.arguments[1])
let out=URL(fileURLWithPath:CommandLine.arguments[2])
var measure:[String:Any]=[:]
var page=CGRect(x:0,y:0,width:595,height:842)
guard let cg=CGContext(out as CFURL,mediaBox:&page,nil) else {fatalError("PDF output unavailable")}
let hd=CTFontCreateWithName("Helvetica" as CFString,12,nil)
func draw(_ s:String,_ f:CTFont,_ x:CGFloat,_ y:CGFloat) {
 cg.textMatrix=CGAffineTransform.identity
 cg.textPosition=CGPoint(x:x,y:y)
 CTLineDraw(line(s,f),cg)
}
for style in ["Display","Text"] {
 let regular=style=="Display" ? "Medium" : "Regular"
 let p58=base.appendingPathComponent("Arvectum-Typeface-v0.58/experimental/Arvectum\(style)GoldenStepDraft058-\(regular).otf")
 let p59=base.appendingPathComponent("Arvectum-Typeface-v0.59/experimental/Arvectum\(style)GoldenStepDraft059-\(regular).otf")
 let pair=[registeredFont(p58.path,52),registeredFont(p59.path,52)]
 let diag=pair.map { f -> [String:Double] in
    let font12=CTFontCreateCopyWithAttributes(f,12,nil,nil)
    var asct:CGFloat=0;var desct:CGFloat=0;var lead:CGFloat=0
    let l=line("Арвектум — Arvectum 1 250 000,00 ₽",font12)
    _=CTLineGetTypographicBounds(l,&asct,&desct,&lead)
    return [
      "ct_ascent_52":Double(CTFontGetAscent(f)), "ct_descent_52":Double(CTFontGetDescent(f)), "ct_leading_52":Double(CTFontGetLeading(f)),
      "ct_ascent_12":Double(CTFontGetAscent(font12)),"ct_descent_12":Double(CTFontGetDescent(font12)),
      "line_ascent_12":Double(asct),"line_descent_12":Double(desct),"line_leading_12":Double(lead),
      "line_width_12":CTLineGetTypographicBounds(l,nil,nil,nil)
    ]
 }
 for k in diag[0].keys {
    guard let a=diag[0][k],let b=diag[1][k],abs(a-b)<0.00001 else {fatalError("Unexpected CoreText line metric reflow \(style) \(k) \(diag)")}
 }
 measure[style]=["baseline":diag[0],"candidate":diag[1],"line_measurements_equal":true]
 cg.beginPDFPage(nil)
 draw("ARVECTUM GOLDEN STEP  /  v0.59  /  \(style)",hd,30,809)
 draw("CoreText process fonts; simulated OS/2 win clipping boundaries, NOT a Windows test",CTFontCreateWithName("Helvetica" as CFString,9,nil),30,792)
 for (idx,font) in pair.enumerated() {
    let top=idx==0 ? 670.0 : 320.0
    let name=idx==0 ? "v0.58 / Win +2160 / -760" : "v0.59 / Win +2400 / -1200; typo unchanged"
    draw(name,hd,34,top+88)
    draw("ã̃̃",font,55,top-25)
    draw("ç̧̧",font,285,top-25)
    let asc=idx==0 ? 2160.0 : 2400.0
    let desc=idx==0 ? 760.0 : 1200.0
    let factor:CGFloat=52/2048
    let topy=top-25+asc*factor
    let bottomy=top-25-desc*factor
    cg.setStrokeColor(CGColor(red:0.72,green:0.22,blue:0.18,alpha:1))
    cg.setLineWidth(0.7)
    cg.setLineDash(phase:0,lengths:[4,4])
    cg.move(to:CGPoint(x:40,y:topy));cg.addLine(to:CGPoint(x:540,y:topy))
    cg.move(to:CGPoint(x:40,y:bottomy));cg.addLine(to:CGPoint(x:540,y:bottomy))
    cg.strokePath()
    cg.setLineDash(phase:0,lengths:[])
    draw("The red guides show declared Win clipping, not native clipping.",CTFontCreateWithName("Helvetica" as CFString,9,nil),40,top-90)
    let f12=CTFontCreateCopyWithAttributes(font,12,nil,nil)
    draw("Арвектум — 1 250 000 ₽   AV To Te   ç̧  ä́",f12,42,top-125)
 }
 cg.endPDFPage()
 print("CORETEXT \(style) line metrics baseline == candidate: \(diag[0])")
}
cg.closePDF()
let data=try JSONSerialization.data(withJSONObject:measure,options:[.prettyPrinted,.sortedKeys])
try data.write(to:out.deletingLastPathComponent().appendingPathComponent("coretext-metrics.json"))
print("PDF created",out.path)
