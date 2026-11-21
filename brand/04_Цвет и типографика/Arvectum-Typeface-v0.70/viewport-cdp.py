"""Reproducible actual 390px Chrome device metrics emulation, independent of Chrome min window."""
from pathlib import Path
import subprocess,asyncio,json,tempfile,urllib.request,time,base64,html,os
import websockets
P=Path(__file__).resolve().parent
CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
URL=(P/'proofs/responsive-type.html').as_uri()
async def issue(ws,i,method,params=None):
    await ws.send(json.dumps({'id':i,'method':method,'params':params or {}}))
    while True:
      msg=json.loads(await ws.recv())
      if msg.get('id')==i:
        if 'error' in msg:raise RuntimeError((method,msg['error']))
        return msg.get('result',{})
async def do():
    with tempfile.TemporaryDirectory(prefix='arvectum-v070-cdp-') as t:
      args=[CHROME,'--headless','--disable-gpu','--disable-dev-shm-usage','--no-first-run',
            '--remote-debugging-port=0','--remote-debugging-address=127.0.0.1',
            '--remote-allow-origins=*','--allow-file-access-from-files',
            '--user-data-dir='+t,'--window-size=900,1450','about:blank']
      logfile=Path(t)/'stderr.log'
      proc=subprocess.Popen(args,stdout=subprocess.DEVNULL,stderr=logfile.open('wb'))
      try:
        portfile=Path(t)/'DevToolsActivePort'
        for _ in range(40):
          if portfile.exists():break
          await asyncio.sleep(.1)
        assert portfile.exists(),('No CDP port',logfile.read_text()[-300:])
        port=int(portfile.read_text().splitlines()[0])
        targets=json.loads(urllib.request.urlopen(f'http://127.0.0.1:{port}/json',timeout=5).read())
        wsurl=next(x['webSocketDebuggerUrl'] for x in targets if x.get('type')=='page')
        results={}
        async with websockets.connect(wsurl,max_size=None,proxy=None) as ws:
          i=0
          for label,w,h,mobile in (('mobile',390,1120,True),('tablet',768,1420,False),('desktop',1440,1480,False)):
            i+=1;await issue(ws,i,'Emulation.setDeviceMetricsOverride',{
              'width':w,'height':h,'deviceScaleFactor':1,'mobile':mobile})
            i+=1;await issue(ws,i,'Page.enable')
            i+=1;await issue(ws,i,'Page.navigate',{'url':URL})
            await asyncio.sleep(1.4)
            i+=1
            query="new Promise(r => document.fonts.ready.then(() => r(document.getElementById('qa')?.textContent || 'MISSING')))"
            data=await issue(ws,i,'Runtime.evaluate',{'expression':query,'awaitPromise':True,'returnByValue':True})
            observed=data['result']['value']
            assert observed.startswith('GS070_VIEWPORT PASS '),(label,observed)
            metrics=json.loads(observed.split(' ',2)[2])
            assert metrics['viewport']==w and metrics['documentWidth']<=w+1,(label,metrics)
            assert metrics['bodySize']>=16 and metrics['displayLoaded'] and metrics['textLoaded']
            if label=='mobile':
                assert metrics['tableScroll'] is False and metrics['mobileRowsStacked'] is True,('mobile table must show full amount rows without side-scroll',metrics)
                assert metrics['titleSize']>=38
            elif label=='desktop':
                assert metrics['titleSize']==68
                assert metrics['tableScroll'] is False
            i+=1;photo=await issue(ws,i,'Page.captureScreenshot',{'format':'png','captureBeyondViewport':True})
            out=P/'proofs'/f'viewport-{label}.png'
            out.write_bytes(base64.b64decode(photo['data']))
            assert out.stat().st_size>10000
            results[label]=dict(test='PASS',inner_width=w,inner_height=h,web_font_loaded=True,
                                actual_metrics=metrics,screenshot=out.name,engine='Chrome DevTools device metrics')
            print(label,'width',w,'doc',metrics['documentWidth'],'title',metrics['titleSize'],
                'tableScroll',metrics['tableScroll'],'screenshot',out.stat().st_size)
        (P/'viewport-report.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
        print('PASS precise Chrome viewport coverage 390/768/1440px')
      finally:
        proc.terminate()
        try:proc.wait(timeout=6)
        except subprocess.TimeoutExpired:proc.kill()
asyncio.run(do())
