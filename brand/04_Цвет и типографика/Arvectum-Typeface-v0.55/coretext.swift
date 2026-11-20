import Foundation
import CoreText
import AppKit
let fontURL = URL(fileURLWithPath: CommandLine.arguments[1])
var error: Unmanaged<CFError>?
let ok = CTFontManagerRegisterFontsForURL(fontURL as CFURL, .process, &error)
guard ok, let descs = CTFontManagerCreateFontDescriptorsFromURL(fontURL as CFURL) as? [CTFontDescriptor], let desc = descs.first else {
    print("ERROR: CoreText process registration failed", error?.takeRetainedValue() as Any)
    exit(2)
}
let font = CTFontCreateWithFontDescriptor(desc, 12, nil)
print("CoreText loaded", CTFontCopyPostScriptName(font), "ascent", CTFontGetAscent(font), "descent", CTFontGetDescent(font))
func typeset(_ str: String) -> CTTypesetter {
    let s = NSAttributedString(string: str, attributes: [NSAttributedString.Key(kCTFontAttributeName as String):font])
    return CTTypesetterCreateWithAttributedString(s as CFAttributedString)
}
func width(_ s: String) -> Double {
    let t = typeset(s)
    return CTTypesetterSuggestClusterBreak(t,0,10000) > 0 ? CTTypesetterCreateLine(t,CFRangeMake(0,s.utf16.count)).typographicBounds() : -1
}
extension CTLine {
    func typographicBounds() -> Double {
        var ascent: CGFloat = 0;var descent: CGFloat = 0;var leading: CGFloat = 0
        return CTLineGetTypographicBounds(self,&ascent,&descent,&leading)
    }
}
let narrow = width("A ") + 0.05
for s in ["A A", "A\u{00A0}A", "A\u{202F}A", "1 250", "1\u{00A0}250", "1\u{202F}250"] {
    let t=typeset(s)
    let n=CTTypesetterSuggestLineBreak(t,0,narrow)
    print("linebreak", s.unicodeScalars.map{String(format:"%04X",$0.value)}.joined(separator:" "),n,"of",s.utf16.count)
}
for s in ["0","1","2","3","4","5","6","7","8","9"] { print("fig",s,width(s)) }
