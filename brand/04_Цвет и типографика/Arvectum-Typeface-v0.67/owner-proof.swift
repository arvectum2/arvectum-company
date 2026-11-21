import AppKit
import Foundation
import CoreGraphics
import CoreText

let root=URL(fileURLWithPath:CommandLine.arguments[1],isDirectory:true)
let dest=URL(fileURLWithPath:CommandLine.arguments[2])
let navy=CGColor(red:0.07,green:0.16,blue:0.22,alpha:1)
let gray=CGColor(red:0.28,green:0.37,blue:0.42,alpha:1)
let teal=CGColor(red:0.16,green:0.61,blue:0.54,alpha:1)
func font(_ path:String,_ size:CGFloat)->CTFont {
 let url=root.appendingPathComponent(path)
 var err:Unmanaged<CFError>?
 guard CTFontManagerRegisterFontsForURL(url as CFURL,.process,&err),
       let descriptors=CTFontManagerCreateFontDescriptorsFromURL(url as CFURL) as? [CTFontDescriptor],
       let descriptor=descriptors.first else {
    fatalError("Font registration failed: \(path) \(String(describing:err))")
 }
 let f=CTFontCreateWithFontDescriptor(descriptor,size,nil)
 guard String(CTFontCopyPostScriptName(f)).contains("Draft") else {fatalError("Font fallback: \(path)")}
 return f
}
let d61=font("Arvectum-Typeface-v0.61/experimental/ArvectumDisplayGoldenStepDraft061-Medium.otf",28)
let t61=font("Arvectum-Typeface-v0.61/experimental/ArvectumTextGoldenStepDraft061-Regular.otf",16)
let d63=font("Arvectum-Typeface-v0.63/experimental/ArvectumDisplayGoldenStepDraft063-Medium.otf",28)
let t63=font("Arvectum-Typeface-v0.63/experimental/ArvectumTextGoldenStepDraft063-Regular.otf",16)
let d64=font("Arvectum-Typeface-v0.64/experimental/ArvectumDisplayGoldenStepDraft064-Medium.otf",28)
let t64=font("Arvectum-Typeface-v0.64/experimental/ArvectumTextGoldenStepDraft064-Regular.otf",16)
let helv=CTFontCreateWithName("Arial" as CFString,12,nil)
let helvB=CTFontCreateWithName("Arial-BoldMT" as CFString,15,nil)
func sized(_ f:CTFont,_ size:CGFloat)->CTFont {
 return CTFontCreateCopyWithAttributes(f,size,nil,nil)
}
var media=CGRect(x:0,y:0,width:595,height:842)
guard let context=CGContext(dest as CFURL,mediaBox:&media,nil) else {fatalError("PDF unavailable")}
func draw(_ text:String,_ f:CTFont,_ x:CGFloat,_ y:CGFloat,
          _ color:CGColor=navy,_ maxw:CGFloat=560) {
 let str=NSAttributedString(string:text,attributes:[
     NSAttributedString.Key(kCTFontAttributeName as String):f,
     NSAttributedString.Key(kCTForegroundColorAttributeName as String):color])
 let line=CTLineCreateWithAttributedString(str)
 let width=CTLineGetTypographicBounds(line,nil,nil,nil)
 guard width <= Double(maxw)+1 else {
   fatalError("Text exceeds region: \(text), width \(width), max \(maxw)")
 }
 context.textMatrix=CGAffineTransform.identity
 context.textPosition=CGPoint(x:x,y:y)
 CTLineDraw(line,context)
}
func rule(_ y:CGFloat) {
 context.setStrokeColor(teal);context.setLineWidth(1.5)
 context.move(to:CGPoint(x:33,y:y));context.addLine(to:CGPoint(x:562,y:y));context.strokePath()
}
func start(_ title:String,_ num:Int) {
 context.beginPDFPage(nil)
 draw("ARVECTUM / GOLDEN STEP / INTERNAL OPTICAL REVIEW",sized(helvB,9),33,807,gray)
 draw(title,sized(helvB,16),33,776)
 draw("DRAFT 2026-11-21 · NOT RELEASED · owner decision pending",sized(helv,9),33,755,gray)
 rule(742)
 draw("PAGE \(num) / 4",sized(helv,9),494,25,gray)
}
func finish(){context.endPDFPage()}
func colHead(_ text:String,_ x:CGFloat,_ y:CGFloat) {
 draw(text,sized(helvB,12),x,y,gray,255)
}

// Page 1: current roles and typography hierarchy.
start("1 / Три направления разработки",1)
colHead("v0.61 / исходная геометрия",34,712)
draw("Интеллект в действии.",sized(d61,29),35,661)
draw("Арвектум — программное обеспечение и цифровые продукты.",sized(t61,14),35,627)
draw("71 пара кернинга; базовые вертикальные метрики.",sized(helv,10),35,604,gray)
rule(570)
colHead("v0.63 / варианты букв, без утверждения",34,542)
draw("ЗАРПЛАТА 3 / З · для дела",sized(d63,26),35,498)
draw("Изменены только З, д, л; на части кеглей результат хуже.",sized(helv,10),35,469,gray)
rule(440)
colHead("v0.64 / расширенный кернинг",34,413)
draw("Интеллект в действии.",sized(d64,29),35,372)
draw("Структура, учёт, технологии и ключевые задачи.",sized(t64,17),35,339)
draw("85 пар; контуры и базовые метрики не менялись.",sized(helv,10),35,310,gray)
rule(278)
draw("Для следующих тестов: кернинг v0.64 с исходными формами.",sized(helv,11),35,246)
draw("Рекомендация не является утверждением или релизом.",sized(helv,10),35,224,gray)
draw("Предыдущие версии сохранены вместе с исходниками.",sized(helv,10),35,202,gray)
finish()

// Page 2: optical variants in identical typography sizes.
start("2 / Альтернативы букв и цифр",2)
colHead("v0.61 / исходные формы",36,707)
colHead("v0.63 / варианты З / д / л",308,707)
for (idx,sz) in [12,14,16,20,28,40,58].enumerated() {
 let y:CGFloat=671-CGFloat(idx)*72
 draw(String(format:"%02d px",sz),sized(helv,9),36,y+23,gray)
 draw(String(format:"%02d px",sz),sized(helv,9),308,y+23,gray)
 draw("3 З  д л",sized(t61,CGFloat(sz)),52,y,navy,235)
 draw("3 З  д л",sized(t63,CGFloat(sz)),323,y,navy,235)
}
rule(145)
draw("14px 3/З: Display 0.926→0.852; Text 0.880→0.679.",sized(helv,10),35,116)
draw("Но на 12px Display и 16px Text сходство увеличивается.",sized(helv,10),35,99,gray)
draw("Метрика сходства не заменяет визуальное решение.",sized(helv,10),35,82,gray)
finish()

// Page 3: kerning comparisons; same curves and widths, only GPOS changes.
start("3 / Межбуквенные интервалы",3)
colHead("v0.61 / 71 пара",35,707)
colHead("v0.64 / 85 пар",306,707)
let samples=["ту ку уч жд оч","ct ty rv Co Pr AI","Структура • учёт","Служба учёта","Creative company","Corporate activities","1 250 000,00 ₽"]
for (idx,s) in samples.enumerated() {
 let y:CGFloat=658-CGFloat(idx)*79
 draw(s,sized(t61,idx==6 ? 15 : 20),35,y,navy,250)
 draw(s,sized(t64,idx==6 ? 15 : 20),306,y,navy,250)
}
rule(88)
draw("В Pages абзац v0.64 перенёсся компактнее.",sized(helv,10),35,64,gray)
finish()

// Page 4: explicit approvals, exceptions and evidence ownership.
start("4 / Предмет согласования",4)
let rows=[
 ("Статус","Эксперимент. Исходные мастера не изменены."),
 ("A. Кернинг","v0.64: 85 пар, рабочий кандидат."),
 ("Б. Формы","v0.63 отложена: недостатки на части кеглей."),
 ("В. Текст","Нужна оценка кириллицы 10–16px на экранах."),
 ("Г. Документы","Pages: 2 A4, шрифты встроены, один перенос."),
 ("Д. Права","Производный от Inter, OFL 1.1, пакет v0.66."),
 ("Е. Название","Метаданные и окончательное имя не утверждены."),
 ("Ж. Windows","Отложено. Метрики v0.59 непригодны."),
 ("З. Выпуск","Требует решения собственника о дизайне.")
]
for (idx,r) in rows.enumerated() {
 let y:CGFloat=696-CGFloat(idx)*64
 draw(r.0,sized(helvB,11),35,y)
 draw(r.1,sized(helv,11),150,y,navy,408)
}
rule(97)
draw("Материалы для рассмотрения, не решение собственника.",sized(helv,10),35,72,gray)
finish()
context.closePDF()
print("PASS process-only CoreText: 4 A4 pages; fonts drawn with exact versioned CFF sources.")
