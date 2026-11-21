"""Create preview-only transparent PNGs from byte-exact approved source SVG; never edit originals."""
from pathlib import Path
import asyncio,base64,json,subprocess,tempfile,urllib.request
from PIL import Image
import websockets
P=Path(__file__).resolve().parent.parent
CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
async def call(ws,i,method,params=None):
 await ws.send(json.dumps({'id':i,'method':method,'params':params or {}}))
 while True:
  v=json.loads(await ws.recv())
  if v.get('id')==i:
   if 'error' in v:raise RuntimeError(v['error'])
   return v.get('result',{})
async def main():
 with tempfile.TemporaryDirectory(prefix='arvectum-logo-') as work:
  cmd=[CHROME,'--headless','--disable-gpu','--disable-dev-shm-usage','--allow-file-access-from-files',
  '--remote-debugging-port=0','--remote-allow-origins=*','--no-first-run','--user-data-dir='+work,'about:blank']
  with (Path(work)/'chrome.log').open('wb') as log:proc=subprocess.Popen(cmd,stdout=subprocess.DEVNULL,stderr=log)
  try:
   port=Path(work)/'DevToolsActivePort'
   for _ in range(50):
    if port.exists():break
    await asyncio.sleep(.1)
   assert port.exists()
   portnum=int(port.read_text().splitlines()[0])
   targets=json.loads(urllib.request.urlopen(f'http://127.0.0.1:{portnum}/json',timeout=5).read())
   target=next(v['webSocketDebuggerUrl'] for v in targets if v['type']=='page')
   async with websockets.connect(target,proxy=None,max_size=None) as ws:
    i=0
    for name,width,height in [('logo',1500,236),('monogram',900,559)]:
     i+=1;await call(ws,i,'Emulation.setDeviceMetricsOverride',{'width':width,'height':height,'deviceScaleFactor':1,'mobile':False})
     i+=1;await call(ws,i,'Emulation.setDefaultBackgroundColorOverride',{'color':{'r':255,'g':255,'b':255,'a':0}})
     i+=1;await call(ws,i,'Page.navigate',{'url':(P/'assets'/f'{name}-raster.html').as_uri()})
     await asyncio.sleep(.8)
     i+=1
     r=await call(ws,i,'Page.captureScreenshot',{'format':'png','captureBeyondViewport':True,
                                                'clip':{'x':0,'y':0,'width':width,'height':height,'scale':1}})
     out=P/'assets'/f'{name}-preview.png';out.write_bytes(base64.b64decode(r['data']))
     im=Image.open(out).convert('RGBA')
     assert im.size==(width,height)
     box=im.getbbox()
     assert box and box[2]>width*.5 and box[3]>height*.3,(name,box)
     print('RASTER_PNG',name,im.size,'alpha extrema',im.getchannel('A').getextrema(),out.stat().st_size)
  finally:
   proc.terminate()
   try:proc.wait(timeout=5)
   except subprocess.TimeoutExpired:proc.kill()
asyncio.run(main())
