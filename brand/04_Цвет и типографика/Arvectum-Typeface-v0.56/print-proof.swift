import Foundation
import AppKit
import CoreText
import CoreGraphics
func load(_ path: String) -> CTFont {
    let url=URL(fileURLWithPath:path)
    var error: Unmanaged<CFError>?
    guard CTFontManagerRegisterFontsForURL(url as CFURL, .process, &error),
          let descs=CTFontManagerCreateFontDescriptorsFromURL(url as CFURL) as? [CTFontDescriptor],
          let desc=descs.first else { fatalError("CoreText registration failed: \(path)") }
    return CTFontCreateWithFontDescriptor(desc,12,nil)
}
var box=CGRect(x:0,y:0,width:595,height:842)
let url=URL(fileURLWithPath:CommandLine.arguments[1])
guard let context=CGContext(url as CFURL,mediaBox:&box,nil) else { fatalError("cannot create PDF") }
func makeLine(_ s:String,_ font:CTFont) -> CTLine {
    let dict: [NSAttributedString.Key: Any] = [NSAttributedString.Key(kCTFontAttributeName as String):font,
              NSAttributedString.Key(kCTForegroundColorAttributeName as String):CGColor(red:0,green:0.075,blue:0.18,alpha:1)]
    return CTLineCreateWithAttributedString(NSAttributedString(string:s,attributes:dict))
}
func measure(_ s:String,_ font:CTFont) -> Double {
    let line=makeLine(s,font)
    return CTLineGetTypographicBounds(line,nil,nil,nil)
}
func draw(_ text:String,_ font:CTFont,_ x:CGFloat,_ y:CGFloat) {
    let line=makeLine(text,font)
    context.textPosition=CGPoint(x:x,y:y)
    CTLineDraw(line,context)
}
let texts=[
    ("Arvectum — Арвектум",28.0),
    ("Интеллект в действии. Intelligence in action.",13.0),
    ("Системность, надёжность, ясность, интеллект.",12.0),
    ("Профессиональная автоматизация бизнес-процессов",12.0),
    ("A AV VA To Te Ty АУ ЛТ ДА",21.0),
    ("I l 1  O О 0  S 5  З 3",20.0),
    ("1 250 000,00 ₽  /  12 000 €  /  $ 800",17.0),
    ("№ 17 — 2026  •  44-ФЗ  /  223-ФЗ",16.0),
    ("info@arvectum.com",14.0),
    ("https://arvectum.com",14.0),
    ("© ® ™  + − × ÷ ≠ ≤ ≥ ≈ ← → ↔",15.0),
    ("а́ à ä â ç  ё й  № 17",17.0)
]
for (i,name) in ["Display","Text"].enumerated() {
    let font=load(CommandLine.arguments[i+2])
    context.beginPDFPage(nil)
    context.textMatrix=CGAffineTransform.identity
    draw("ARVECTUM GOLDEN STEP / v0.56 / PRINT PROOF",CTFontCreateWithName("Helvetica" as CFString,13,nil),32,805)
    draw("Page \(i+1) — \(name) / draft, not approved",CTFontCreateWithName("Helvetica" as CFString,10,nil),32,787)
    var y:CGFloat=748
    for (s,size) in texts {
        let f=CTFontCreateCopyWithAttributes(font,size,nil,nil)
        if measure(s,f)>530 {
            var left="";var right=""
            for word in s.split(separator:" ") {
                let candidate=left.isEmpty ? String(word) : left+" "+word
                if !left.isEmpty && measure(candidate,f)>530 { right=right.isEmpty ? String(word) : right+" "+word }
                else if right.isEmpty { left=candidate }
                else { right+=" "+word }
            }
            guard !right.isEmpty, measure(left,f)<=530, measure(right,f)<=530 else { fatalError("Cannot wrap: "+s) }
            draw(left,f,32,y);y-=CGFloat(size+18);draw(right,f,32,y);y-=CGFloat(size+18)
        } else {
            draw(s,f,32,y);y-=CGFloat(size+21)
        }
    }
    context.endPDFPage()
}
context.closePDF()
print("PDF created",CommandLine.arguments[1])
