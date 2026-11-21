import AppKit
import WebKit
import Foundation

final class Nav: NSObject, WKNavigationDelegate {
    var ended = false
    var error: String? = nil
    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) { ended=true }
    func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
        self.error=error.localizedDescription;ended=true
    }
    func webView(_ webView: WKWebView, didFailProvisionalNavigation navigation: WKNavigation!, withError error: Error) {
        self.error=error.localizedDescription;ended=true
    }
}
func spin(_ seconds: TimeInterval, _ condition: () -> Bool) -> Bool {
    let limit=Date().addingTimeInterval(seconds)
    while !condition() && Date() < limit { _ = RunLoop.current.run(mode:.default,before:Date().addingTimeInterval(0.05)) }
    return condition()
}
func js(_ web:WKWebView,_ source:String) -> Any? {
    var done=false;var result:Any?=nil;var problem:Error?=nil
    web.evaluateJavaScript(source) { value,error in result=value;problem=error;done=true }
    guard spin(10,{done}) else {fatalError("evaluateJavaScript timeout: \(source.prefix(60))")}
    if let problem=problem {fatalError("JS \(problem)")}
    return result
}
func png(_ image:NSImage, _ dest:URL) {
    guard let tiff=image.tiffRepresentation, let bmp=NSBitmapImageRep(data:tiff), let data=bmp.representation(using:.png,properties:[:]) else {fatalError("PNG encode failure")}
    try! data.write(to:dest)
}
let repoURL=URL(fileURLWithPath:CommandLine.arguments[1],isDirectory:true)
let document=repoURL.appendingPathComponent("Arvectum-Typeface-v0.72/proofs/webkit-type-specimen.html")
let output=URL(fileURLWithPath:CommandLine.arguments[2],isDirectory:true)
let app=NSApplication.shared
app.setActivationPolicy(.prohibited)
var reports:[[String:Any]]=[]
for (label,width,height) in [("mobile",390,970),("tablet",768,1000),("desktop",1440,1000)] {
    let cfg=WKWebViewConfiguration()
    cfg.websiteDataStore = .nonPersistent()
    let web=WKWebView(frame:NSRect(x:0,y:0,width:width,height:height),configuration:cfg)
    let nav=Nav();web.navigationDelegate=nav
    web.loadFileURL(document, allowingReadAccessTo:repoURL)
    guard spin(20,{nav.ended}) else {fatalError("WebKit did not finish \(label)")}
    if let problem=nav.error {fatalError("WebKit \(label): \(problem)")}
    _ = spin(1.8,{false})
    let script="""
    (() => {
      const doc = document.documentElement, styles = getComputedStyle(document.body);
      const header = document.querySelector('h1').getBoundingClientRect();
      const table=document.querySelector('.table-wrap');
      const textSize=parseFloat(styles.fontSize);
      const retval={engine: navigator.userAgent, viewport:innerWidth, scrollWidth:doc.scrollWidth,
       textSize, h1Size:parseFloat(getComputedStyle(document.querySelector('h1')).fontSize),
       fontText:document.fonts.check('18px GoldenText'),fontDisplay:document.fonts.check('36px GoldenDisplay'),
       titleFits:header.right <= document.querySelector('.page').getBoundingClientRect().right+1,
       moneySideScroll:table.scrollWidth>table.clientWidth,
       rowsStacked:getComputedStyle(document.querySelector('tbody tr')).display === 'flex',
       tableWidth:table.clientWidth, contentHeight:doc.scrollHeight};
      return JSON.stringify(retval);
    })()
    """
    guard let value=js(web,script) as? String, let data=value.data(using:.utf8), let stats=try? JSONSerialization.jsonObject(with:data) as? [String:Any] else {fatalError("No metrics \(label)")}
    print("WKWebKit",label,stats)
    let observed=stats["viewport"] as? Int ?? -1
    guard observed==width else {fatalError("Wrong CSS viewport: \(observed), expected \(width)")}
    let scroll=stats["scrollWidth"] as? Int ?? 9999
    guard scroll<=width+1 else {fatalError("Viewport horizontal overflow \(label): \(scroll)")}
    guard (stats["fontText"] as? Bool)==true,(stats["fontDisplay"] as? Bool)==true else {fatalError("Font failed WebKit \(label)")}
    guard (stats["titleFits"] as? Bool)==true else {fatalError("Title overflows \(label)")}
    if label == "mobile" {
        guard (stats["rowsStacked"] as? Bool)==true,(stats["moneySideScroll"] as? Bool)==false else {fatalError("Mobile money fails")}
    }
    var entry=stats
    entry["label"]=label
    entry["status"]="PASS_SCOPE"
    let captureHeight=CGFloat(min(3200,(stats["contentHeight"] as? Int ?? 2000)+10))
    web.frame=NSRect(x:0,y:0,width:CGFloat(width),height:captureHeight)
    _ = spin(0.7,{false})
    let conf=WKSnapshotConfiguration()
    conf.rect=CGRect(x:0,y:0,width:CGFloat(width),height:captureHeight)
    var image:NSImage?=nil;var end=false;var error:Error?
    web.takeSnapshot(with:conf) { result,issue in image=result;error=issue;end=true }
    if spin(15,{end}),let image=image {
       png(image,output.appendingPathComponent("webkit-\(label).png"))
       print("SNAPSHOT_OK",label,Int(image.size.width),Int(image.size.height))
    } else {print("SNAPSHOT_UNAVAILABLE",label,String(describing:error))}
    web.pageZoom=2.0
    _ = spin(0.8,{false})
    let zoomSource="""
    (() => {const t=document.querySelector('.table-wrap'),p=document.querySelector('.page').getBoundingClientRect(),h=document.querySelector('h1').getBoundingClientRect();
      return JSON.stringify({innerWidth,scrollWidth:document.documentElement.scrollWidth,bodyText:parseFloat(getComputedStyle(document.body).fontSize),
      titleFits:h.right<=p.right+1,tableOverflow:t.scrollWidth>t.clientWidth,rowsStacked:getComputedStyle(document.querySelector('tbody tr')).display==='flex',
      outliers:[...document.querySelectorAll('body *')].filter(n=>n.getBoundingClientRect().right>innerWidth+1).slice(0,8).map(n=>({element:n.tagName,cl:n.className,text:n.textContent.trim().slice(0,30),right:Math.round(n.getBoundingClientRect().right),scroll:n.scrollWidth}))});})()
    """
    if let zoomValue=js(web,zoomSource) as? String, let raw=zoomValue.data(using:.utf8), let zoom=try? JSONSerialization.jsonObject(with:raw) as? [String:Any] {
        entry["zoom200"] = zoom
        print("WKWebKit_ZOOM200",label,zoom)
    }
    reports.append(entry)
    web.stopLoading()
}
let doc:[String:Any]=["runner":"macOS WKWebView (Safari/WebKit engine, not Safari.app UI)","results":reports,"user_safari_windows_modified":false,
 "actual_iPhone_run":false,"simulator_run":false,"production_changes":false]
let data=try! JSONSerialization.data(withJSONObject:doc,options:[.prettyPrinted,.sortedKeys,.fragmentsAllowed])
try! data.write(to:output.appendingPathComponent("webkit-report.json"))
print("WEBKIT_QA_FINISHED")
