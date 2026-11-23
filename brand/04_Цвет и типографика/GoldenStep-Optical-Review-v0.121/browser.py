"""Real locally-served font loading/layout, tabular numeral and PDF tests via Chrome CDP."""
from pathlib import Path
import asyncio,json,subprocess,tempfile,urllib.request,base64
import websockets
P=Path(__file__).resolve().parent
CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
async def ask(ws,i,method,params=None):
 await ws.send(json.dumps({'id':i,'method':method,'params':params or {}}))
 while True:
  obj=json.loads(await ws.recv())
  if obj.get('id')==i:
   if 'error' in obj: raise RuntimeError((method,obj['error']))
   return obj.get('result',{})
async def main():
 results={}
 with tempfile.TemporaryDirectory(prefix='arv-v121-financial-',ignore_cleanup_errors=True) as temp:
  flags=[CHROME,'--headless=new','--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--no-first-run',
    '--allow-file-access-from-files','--remote-debugging-port=0','--remote-debugging-address=127.0.0.1',
    '--remote-allow-origins=*','--user-data-dir='+temp,'--window-size=1450,1100','about:blank']
  with (Path(temp)/'chrome.log').open('wb') as err: proc=subprocess.Popen(flags,stdout=subprocess.DEVNULL,stderr=err)
  try:
   portfile=Path(temp)/'DevToolsActivePort'
   for i in range(90):
    if portfile.is_file(): break
    await asyncio.sleep(.1)
   assert portfile.is_file(),'no Chrome endpoint'
   port=int(portfile.read_text().splitlines()[0])
   target=json.loads(urllib.request.urlopen(f'http://127.0.0.1:{port}/json',timeout=6).read())
   uri=next(t['webSocketDebuggerUrl'] for t in target if t['type']=='page')
   k=0
   async with websockets.connect(uri,proxy=None,max_size=None) as ws:
    for width in (390,768,1440):
     k+=1;await ask(ws,k,'Emulation.setDeviceMetricsOverride',{'width':width,'height':1100,'deviceScaleFactor':1,'mobile':width==390})
     k+=1;await ask(ws,k,'Page.enable')
     k+=1;await ask(ws,k,'Page.navigate',{'url':(P/'financial-specimen.html').as_uri()})
     k+=1;await ask(ws,k,'Runtime.evaluate',{'expression':'document.fonts.ready.then(()=>true)','awaitPromise':True})
     await asyncio.sleep(.4)
     js="""JSON.stringify((() => {
       const test=document.createElement('span');
       test.style.cssText='position:absolute;left:-10000px;top:0;white-space:nowrap;font-size:36px;font-family:"ArvectumTextAudit"';
       document.body.appendChild(test);
       function measure(s,tnum) { test.style.fontVariantNumeric=tnum?'tabular-nums':'normal';
         test.style.fontFeatureSettings=tnum?'"tnum" 1':'normal'; test.textContent=s;
         return test.getBoundingClientRect().width; }
       const res={
         vw:innerWidth,docWidth:document.documentElement.scrollWidth,docHeight:document.documentElement.scrollHeight,
         loaded:[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family),
         bodyLen:document.body.innerText.length,
         variant:getComputedStyle(document.querySelector('.arv-financial-column')).fontVariantNumeric,
         feature:getComputedStyle(document.querySelector('.arv-financial-column')).fontFeatureSettings,
         default111:measure('111111',false),default888:measure('888888',false),
         table111:measure('111111',true),table888:measure('888888',true),
         sampleLetters:['Ą','W','А','М'].map(s=>document.fonts.check('16px ArvectumTextAudit',s)),
         pages:[...document.querySelectorAll('.page')].map(p=>({width:p.scrollWidth,clientWidth:p.clientWidth,height:p.scrollHeight}))
       };test.remove();return res;})())"""
     k+=1;resp=await ask(ws,k,'Runtime.evaluate',{'expression':js,'returnByValue':True})
     met=json.loads(resp['result']['value'])
     assert met['vw']==width and met['docWidth']<=width,(width,met)
     assert set(['ArvectumTextAudit','ArvectumDisplayAudit']).issubset(set(met['loaded'])),met['loaded']
     assert abs(met['default111']-met['default888'])>3,met
     assert abs(met['table111']-met['table888'])<.01,met
     assert met['variant']=='tabular-nums'
     assert '"tnum"' in met['feature'] or 'tnum' in met['feature']
     assert all(met['sampleLetters'])
     assert all(p['width']<=p['clientWidth']+1 for p in met['pages'])
     k+=1;pic=await ask(ws,k,'Page.captureScreenshot',{'format':'png','captureBeyondViewport':True})
     dest=P/'proofs'/f'finance-optical-{width}px.png'
     dest.write_bytes(base64.b64decode(pic['data']))
     assert dest.stat().st_size>12000
     results[str(width)]={'metrics':met,'image_bytes':dest.stat().st_size}
     print('PASS CHROME',width,'loaded fonts',met['loaded'],'proportional variance',round(met['default888']-met['default111'],1),'tabular delta',met['table888']-met['table111'],'no overflow')
     if width==1440:
      k+=1;pdf=await ask(ws,k,'Page.printToPDF',{'printBackground':True,'preferCSSPageSize':True,'marginTop':0,'marginBottom':0,'marginLeft':0,'marginRight':0})
      dst=P/'proofs/GoldenStep-v0121-Financial-and-Optical-Review.pdf'
      dst.write_bytes(base64.b64decode(pdf['data']))
      print('SAVED TRUE PDF',dst.stat().st_size)
   (P/'evidence/browser-qa.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
  finally:
   proc.terminate()
   try:proc.wait(timeout=7)
   except subprocess.TimeoutExpired:proc.kill()
asyncio.run(main())
