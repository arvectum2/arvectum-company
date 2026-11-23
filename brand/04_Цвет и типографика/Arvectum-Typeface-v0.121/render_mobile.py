"""Chrome CDP actual local 390px / 768px font fixture A/B, with font load check."""
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
   if 'error' in obj:raise RuntimeError((method,obj['error']))
   return obj.get('result',{})
async def main():
 results={}
 with tempfile.TemporaryDirectory(prefix='gs-v0121-mobile-') as d:
  chrome=[CHROME,'--headless=new','--no-sandbox','--disable-gpu',
    '--disable-dev-shm-usage','--no-first-run','--allow-file-access-from-files',
    '--remote-debugging-port=0','--remote-debugging-address=127.0.0.1',
    '--remote-allow-origins=*','--user-data-dir='+d,'--window-size=1250,980','about:blank']
  with (Path(d)/'chrome.log').open('wb') as err:
   proc=subprocess.Popen(chrome,stdout=subprocess.DEVNULL,stderr=err)
  try:
   portfile=Path(d)/'DevToolsActivePort'
   for _ in range(70):
    if portfile.is_file():break
    await asyncio.sleep(.12)
   assert portfile.exists(),'Chrome did not initialize'
   port=int(portfile.read_text().splitlines()[0])
   targets=json.loads(urllib.request.urlopen(f'http://127.0.0.1:{port}/json',timeout=4).read())
   url=next(t['webSocketDebuggerUrl'] for t in targets if t['type']=='page')
   k=0
   async with websockets.connect(url,proxy=None,max_size=None) as ws:
    for width in (390,768):
     for version in ('before','after'):
      k+=1;await ask(ws,k,'Emulation.setDeviceMetricsOverride',
        {'width':width,'height':950,'deviceScaleFactor':1,'mobile':True})
      k+=1;await ask(ws,k,'Page.enable')
      file=P/'cases'/f'mobile-{version}.html'
      k+=1;await ask(ws,k,'Page.navigate',{'url':file.as_uri()})
      k+=1;await ask(ws,k,'Runtime.evaluate',{'expression':'document.fonts.ready.then(()=>true)',
        'awaitPromise':True,'returnByValue':True})
      await asyncio.sleep(.28)
      k+=1;resp=await ask(ws,k,'Runtime.evaluate',{'expression':"""JSON.stringify({
        viewport:innerWidth,docWidth:document.documentElement.scrollWidth,
        docHeight:document.documentElement.scrollHeight,
        families:[...document.fonts].filter(x=>x.status==='loaded').map(x=>x.family),
        wordCount:document.body.innerText.length,
        maxBoxWidth:Math.max(...[...document.querySelectorAll('.card')]
          .map(el=>el.getBoundingClientRect().width))
      })""",'returnByValue':True})
      vals=json.loads(resp['result']['value'])
      assert vals['viewport']==width and vals['docWidth']<=width,(width,version,vals)
      assert 'GSD' in vals['families'] and 'GST' in vals['families'],(version,vals)
      k+=1;pic=await ask(ws,k,'Page.captureScreenshot',
         {'format':'png','captureBeyondViewport':True})
      name=P/'proofs'/f'mobile-{width}px-{version}.png'
      name.write_bytes(base64.b64decode(pic['data']))
      assert name.stat().st_size>15000,(name,name.stat().st_size)
      results[f'{width}-{version}']={'source':str(file.relative_to(P)),
         'screenshot':str(name.relative_to(P)),'bytes':name.stat().st_size,'metrics':vals}
      print('PASS CHROME',width,version,'docWidth',vals['docWidth'],
        'fonts',vals['families'],'height',vals['docHeight'])
   (P/'evidence/mobile-browser-qa.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
  finally:
   proc.terminate()
   try:proc.wait(timeout=7)
   except subprocess.TimeoutExpired:proc.kill()
asyncio.run(main())
