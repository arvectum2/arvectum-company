"""Measure corrected HTML cover watermark/footer in Chrome: no overlap."""
from pathlib import Path
import asyncio,json,subprocess,tempfile,urllib.request
import websockets
P=Path(__file__).resolve().parent.parent
CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
async def call(ws,i,method,params=None):
 await ws.send(json.dumps({'id':i,'method':method,'params':params or {}}))
 while True:
  msg=json.loads(await ws.recv())
  if msg.get('id')==i:
   if 'error' in msg:raise RuntimeError(msg['error'])
   return msg.get('result',{})
async def main():
 with tempfile.TemporaryDirectory(prefix='arvectum-v076-qa-') as td:
  args=[CHROME,'--headless','--disable-gpu','--disable-dev-shm-usage','--allow-file-access-from-files',
   '--remote-debugging-port=0','--remote-allow-origins=*','--no-first-run','--user-data-dir='+td,'about:blank']
  with (Path(td)/'chrome.log').open('wb') as err: proc=subprocess.Popen(args,stdout=subprocess.DEVNULL,stderr=err)
  try:
   portfile=Path(td)/'DevToolsActivePort'
   for _ in range(50):
    if portfile.exists():break
    await asyncio.sleep(.1)
   assert portfile.exists()
   port=int(portfile.read_text().splitlines()[0])
   targets=json.loads(urllib.request.urlopen(f'http://127.0.0.1:{port}/json',timeout=5).read())
   wsurl=next(t['webSocketDebuggerUrl'] for t in targets if t.get('type')=='page')
   async with websockets.connect(wsurl,proxy=None,max_size=None) as ws:
    await call(ws,1,'Page.navigate',{'url':(P/'slides/deck.html').as_uri()})
    await asyncio.sleep(1)
    code="""(()=>{const a=document.querySelector('.cover .watermark').getBoundingClientRect(),b=document.querySelector('.cover .foot').getBoundingClientRect();return JSON.stringify({watermarkBottom:a.bottom,footerTop:b.top,verticalGap:b.top-a.bottom,overlapWidth:Math.max(0,Math.min(a.right,b.right)-Math.max(a.left,b.left)),overlapHeight:Math.max(0,Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top))})})()"""
    x=await call(ws,2,'Runtime.evaluate',{'expression':code,'returnByValue':True})
    result=json.loads(x['result']['value'])
    assert result['verticalGap']>35 and result['overlapHeight']==0,result
    (P/'evidence/cover-layout.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('FIXED COVER GAP',round(result['verticalGap'],1),'CSS px; NO OVERLAP')
  finally:
   proc.terminate()
   try:proc.wait(timeout=5)
   except subprocess.TimeoutExpired:proc.kill()
asyncio.run(main())
