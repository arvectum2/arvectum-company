"""Render six truly equivalent local carrier fixtures through Chrome CDP."""
from pathlib import Path
import asyncio,base64,json,subprocess,tempfile,urllib.request
import websockets
P=Path(__file__).resolve().parent.parent
CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
async def ask(ws,i,method,params=None):
 await ws.send(json.dumps({'id':i,'method':method,'params':params or {}}))
 while True:
  obj=json.loads(await ws.recv())
  if obj.get('id')==i:
   if 'error' in obj:raise RuntimeError((method,obj['error']))
   return obj.get('result',{})
async def main():
 results={}
 with tempfile.TemporaryDirectory(prefix='golden-v0104-alpha-cdp-') as d:
  chrome=[CHROME,'--headless=new','--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--no-first-run',
    '--allow-file-access-from-files','--remote-debugging-port=0','--remote-debugging-address=127.0.0.1',
    '--remote-allow-origins=*','--user-data-dir='+d,'--window-size=1250,1100','about:blank']
  with (Path(d)/'chrome.log').open('wb') as err:
   proc=subprocess.Popen(chrome,stdout=subprocess.DEVNULL,stderr=err)
  try:
   portfile=Path(d)/'DevToolsActivePort'
   for _ in range(80):
    if portfile.is_file():break
    await asyncio.sleep(.1)
   assert portfile.is_file(),'Chrome failed to open debugging port'
   port=int(portfile.read_text().splitlines()[0])
   targets=json.loads(urllib.request.urlopen(f'http://127.0.0.1:{port}/json',timeout=5).read())
   url=next(t['webSocketDebuggerUrl'] for t in targets if t['type']=='page')
   k=0
   async with websockets.connect(url,proxy=None,max_size=None) as ws:
    for carrier in ('letter','proposal','mobile'):
     for variant in ('old0103','new0104'):
      mobile=carrier=='mobile';width,height=(390,920) if mobile else (1160,1080)
      k+=1;await ask(ws,k,'Emulation.setDeviceMetricsOverride',{'width':width,'height':height,'deviceScaleFactor':1,'mobile':mobile})
      k+=1;await ask(ws,k,'Page.enable')
      file=P/'cases'/carrier/f'{variant}.html'
      k+=1;await ask(ws,k,'Page.navigate',{'url':file.as_uri()})
      k+=1;await ask(ws,k,'Runtime.evaluate',{'expression':'document.fonts.ready.then(()=>true)','awaitPromise':True,'returnByValue':True})
      await asyncio.sleep(.35)
      k+=1;stats=await ask(ws,k,'Runtime.evaluate',{'expression':"""JSON.stringify({viewport:innerWidth,docWidth:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight,
        families:[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family),
        images:[...document.images].map(i=>({url:i.getAttribute('src'),natural:i.naturalWidth,loaded:i.complete})),
        bodyText:document.body.innerText.length,caseTitle:document.title})""",'returnByValue':True})
      data=json.loads(stats['result']['value'])
      assert 'GSDisplay' in data['families'] and 'GSText' in data['families'],(carrier,variant,data['families'])
      assert all(x['natural']>0 and x['loaded'] for x in data['images']),(carrier,variant,data['images'])
      if mobile:assert data['viewport']==390 and data['docWidth']<=390,(carrier,variant,data)
      if not mobile:
       k+=1;pdf=await ask(ws,k,'Page.printToPDF',{'printBackground':True,'preferCSSPageSize':True,
         'marginTop':0,'marginBottom':0,'marginLeft':0,'marginRight':0})
       target=P/'proofs'/f'{carrier}-{variant}.pdf'
       target.write_bytes(base64.b64decode(pdf['data']))
      else:
       k+=1;snap=await ask(ws,k,'Page.captureScreenshot',{'format':'png','captureBeyondViewport':True})
       target=P/'proofs'/f'mobile-{variant}.png'
       target.write_bytes(base64.b64decode(snap['data']))
      assert target.stat().st_size>10000,(carrier,variant,target.stat().st_size)
      results[f'{carrier}-{variant}']={'source':str(file.relative_to(P)),
       'output':str(target.relative_to(P)),'bytes':target.stat().st_size,'metrics':data}
      print('RENDER',carrier,variant,target.stat().st_size,'viewport',data['viewport'],'images',len(data['images']))
   (P/'evidence/browser-report.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
  finally:
   proc.terminate()
   try:proc.wait(timeout=7)
   except subprocess.TimeoutExpired:proc.kill()
 print('READY',len(results))
asyncio.run(main())
