import Foundation
import CoreText
import CoreGraphics

// Native macOS/CoreText check. Loads OTF from file without installing or registering fonts.
let root = URL(fileURLWithPath: CommandLine.arguments[1], isDirectory: true)
let proof = URL(fileURLWithPath: CommandLine.arguments[2])
let evidence = URL(fileURLWithPath: CommandLine.arguments[3])
let items = [
 ("Display", "ArvectumGoldenStepDisplayPhraseRhythmWorking0121-Medium.otf"),
 ("Text", "ArvectumGoldenStepTextPhraseRhythmWorking0121-Regular.otf")
]
let samples = [
 "WĄTEK · MĄKA · WĄSKI · WAM",
 "ĄW · WĄ · WÁ · WA · WM · MW",
 "Гибридная система · Главный инженер",
 "125 000 ₽ · 6% · № 123/26 · 2026",
 "ARVECTUM · WORKFLOW · PAYMENT"
]
var records: [[String: Any]] = []
var media = CGRect(x: 0, y: 0, width: 842, height: 595)
guard let pdf = CGContext(proof as CFURL, mediaBox: &media, nil) else { fatalError("Cannot open PDF graphics context") }
pdf.beginPDFPage(nil)
pdf.setFillColor(red: 0.07, green: 0.19, blue: 0.28, alpha: 1)
var y: CGFloat = 555
for (face, filename) in items {
 let url = root.appendingPathComponent(filename)
 guard let prov = CGDataProvider(url: url as CFURL), let cgfont = CGFont(prov) else { fatalError("Cannot load actual OTF \(filename)") }
 let font = CTFontCreateWithGraphicsFont(cgfont, 20, nil, nil)
 let name = CTFontCopyPostScriptName(font) as String
 precondition(name.contains("0121"),"Not Golden Step current OTF")
 let keys = Array("AĄÁaąWẂMМГиР₽".utf16)
 var glyphs = Array(repeating: CGGlyph(0),count:keys.count)
 let mapped = keys.withUnsafeBufferPointer { src in
   glyphs.withUnsafeMutableBufferPointer { dest in
     CTFontGetGlyphsForCharacters(font,src.baseAddress!,dest.baseAddress!,src.count)
   }
 }
 precondition(mapped && glyphs.allSatisfy{$0 != 0},"Native font misses required glyphs: \(face)")
 var checked: [[String: Any]] = []
 let headingFont = CTFontCreateWithGraphicsFont(cgfont, 16, nil, nil)
 let heading = CTLineCreateWithAttributedString(NSAttributedString(string:"\(face) · actual macOS CoreText", attributes: [NSAttributedString.Key(kCTFontAttributeName as String): headingFont]))
 pdf.textPosition = CGPoint(x:35,y:y)
 CTLineDraw(heading,pdf)
 y -= 42
 for s in samples {
  let txt = NSAttributedString(string:s,attributes:[NSAttributedString.Key(kCTFontAttributeName as String):font])
  let line = CTLineCreateWithAttributedString(txt)
  var ascent:CGFloat=0;var descent:CGFloat=0;var leading:CGFloat=0
  let advance = CTLineGetTypographicBounds(line,&ascent,&descent,&leading)
  let n = (CTLineGetGlyphRuns(line) as NSArray).reduce(0) { (x:Int, el:Any) in x+CTRunGetGlyphCount(el as! CTRun) }
  precondition(advance.isFinite && advance>0 && n>0 && n<=s.utf16.count,"Bad native layout")
  pdf.textPosition = CGPoint(x:35,y:y)
  CTLineDraw(line,pdf)
  checked.append(["sample":s,"width_pt":advance,"glyph_count":n,"ascent":ascent,"descent":descent])
  y -= 35
 }
 records.append(["face":face,"postscript_name":name,"mapped_required_unicode":keys.count,"checked_lines":checked])
 y -= 36
}
pdf.endPDFPage()
pdf.closePDF()
let data: [String:Any] = ["scope":"native CoreText OTF file load/layout and one-page Quartz PDF; no font registration or PDF/X claim","masters":records]
let json=try JSONSerialization.data(withJSONObject:data,options:[.prettyPrinted,.sortedKeys])
try json.write(to:evidence)
print("PASS native CoreText:",records.map{($0["face"] as! String)+": "+($0["postscript_name"] as! String)}.joined(separator:"; "))
print("PASS native Quartz PDF:",proof.path)
