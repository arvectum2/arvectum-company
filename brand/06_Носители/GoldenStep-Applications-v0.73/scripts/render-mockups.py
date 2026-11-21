"""Isolated Chrome CDP rendering of five draft carriers; no website or app changes."""
from pathlib import Path
import asyncio,base64,json,subprocess,tempfile,urllib.request
import websockets
P=Path(__file__).resolve().parent.parent
CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
async def call(ws,i,name,params=None):
    await ws.send(json.dumps({'id':i,'method':name,'params':params or {}}))
    while True:
      m=json.loads(await ws.recv())
      if m.get('id')==i:
        if 'error' in m:raise RuntimeError((name,m['error']))
        return m.get('result',{})
async def run():
  with tempfile.TemporaryDirectory(prefix='arvectum-v073-') as work:
    args=[CHROME,'--headless','--disable-gpu','--disable-dev-shm-usage','--no-first-run',
      '--allow-file-access-from-files','--remote-debugging-port=0','--remote-debugging-address=127.0.0.1',
      '--remote-allow-origins=*','--user-data-dir='+work,'--window-size=1440,1000','about:blank']
    with (Path(work)/'chrome.log').open('wb') as log:
      proc=subprocess.Popen(args,stdout=subprocess.DEVNULL,stderr=log)
    try:
      portfile=Path(work)/'DevToolsActivePort'
      for _ in range(60):
        if portfile.is_file():break
        await asyncio.sleep(.1)
      assert portfile.is_file(),'Chrome did not start'
      port=int(portfile.read_text().splitlines()[0])
      targets=json.loads(urllib.request.urlopen(f'http://127.0.0.1:{port}/json',timeout=5).read())
      url=next(t['webSocketDebuggerUrl'] for t in targets if t['type']=='page')
      result={};counter=0
      async with websockets.connect(url,proxy=None,max_size=None) as ws:
        for label,rel,w,h,kind in [
          ('site-desktop','site/home.html',1440,1000,'screenshot'),
          ('site-mobile','site/home.html',390,920,'screenshot'),
          ('letterhead','office/letterhead.html',1100,920,'pdf'),
          ('proposal','office/proposal.html',1100,920,'pdf'),
          ('slides','slides/deck.html',1440,900,'pdf'),
          ('business-card','card/business-card.html',980,850,'pdf')]:
          counter+=1
          await call(ws,counter,'Emulation.setDeviceMetricsOverride',{'width':w,'height':h,'deviceScaleFactor':1,'mobile':label=='site-mobile'})
          counter+=1;await call(ws,counter,'Page.enable')
          counter+=1;await call(ws,counter,'Page.navigate',{'url':(P/rel).as_uri()})
          await asyncio.sleep(1.2)
          counter+=1
          expr="new Promise(r=>document.fonts.ready.then(()=>r(JSON.stringify({width:innerWidth,docWidth:document.documentElement.scrollWidth,fonts:{Display:document.fonts.check('24px GSDisplay'),Text:document.fonts.check('16px GSText')},images:[...document.images].map(i=>({src:i.getAttribute('src'),complete:i.complete,ok:i.naturalWidth>0,width:i.naturalWidth}))}))))"
          metric=await call(ws,counter,'Runtime.evaluate',{'expression':expr,'returnByValue':True,'awaitPromise':True})
          stats=json.loads(metric['result']['value'])
          assert stats['fonts']['Display'] and stats['fonts']['Text'],(label,stats)
          assert all(x['ok'] for x in stats['images']),(label,stats)
          if kind=='screenshot':
            assert stats['width']==w and stats['docWidth']<=w+1,(label,stats)
            counter+=1
            snap=await call(ws,counter,'Page.captureScreenshot',{'format':'png','captureBeyondViewport':True})
            target=P/'proofs'/f'{label}.png'
            target.write_bytes(base64.b64decode(snap['data']))
          else:
            counter+=1
            res=await call(ws,counter,'Page.printToPDF',{'printBackground':True,'preferCSSPageSize':True,
              'marginTop':0,'marginBottom':0,'marginLeft':0,'marginRight':0})
            target=P/'proofs'/f'{label}.pdf'
            target.write_bytes(base64.b64decode(res['data']))
          assert target.stat().st_size>5000,(label,target.stat().st_size)
          result[label]={'source':rel,'proof':str(target.relative_to(P)),'proof_size':target.stat().st_size,
                         'viewport':w,'content_metrics':stats,'kind':kind,'status':'PASS_RENDER'}
          print(label,'PASS',target.name,target.stat().st_size,stats['images'])
      (P/'evidence/browser-report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    finally:
      proc.terminate()
      try:proc.wait(timeout=7)
      except subprocess.TimeoutExpired:proc.kill()
  print('ALL MOCKUPS RENDERED',len(result))
asyncio.run(run())
