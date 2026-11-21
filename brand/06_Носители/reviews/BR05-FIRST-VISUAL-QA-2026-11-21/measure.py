"""Read-only art-direction QA evidence from existing v0.73/v0.75/v0.62 sources.
Do not edit or install brand masters, working font or production website.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import asyncio,base64,hashlib,json,re,subprocess,tempfile,urllib.request
import websockets
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
A=ROOT/'brand/06_Носители/GoldenStep-Applications-v0.73'
T=ROOT/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.75'
OPT=ROOT/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.62/audit.json'
assert A.is_dir() and T.is_dir() and OPT.is_file()
async def issue(ws,i,method,params=None):
 await ws.send(json.dumps({'id':i,'method':method,'params':params or {}}))
 while True:
  v=json.loads(await ws.recv())
  if v.get('id')==i:
   if 'error' in v:raise RuntimeError(v['error'])
   return v.get('result',{})
async def measure_cover():
 chrome='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
 with tempfile.TemporaryDirectory(prefix='arvectum-first-review-') as d:
  flags=[chrome,'--headless','--disable-gpu','--disable-dev-shm-usage','--allow-file-access-from-files',
         '--remote-debugging-port=0','--remote-debugging-address=127.0.0.1','--remote-allow-origins=*',
         '--no-first-run','--user-data-dir='+d,'--window-size=1440,980','about:blank']
  with (Path(d)/'chrome.log').open('wb') as log:proc=subprocess.Popen(flags,stdout=subprocess.DEVNULL,stderr=log)
  try:
   portfile=Path(d)/'DevToolsActivePort'
   for _ in range(80):
    if portfile.is_file():break
    await asyncio.sleep(.1)
   assert portfile.exists()
   port=int(portfile.read_text().splitlines()[0]);targets=json.loads(urllib.request.urlopen(f'http://127.0.0.1:{port}/json',timeout=5).read())
   wsurl=next(x['webSocketDebuggerUrl'] for x in targets if x['type']=='page')
   async with websockets.connect(wsurl,max_size=None,proxy=None) as ws:
    i=0;i+=1;await issue(ws,i,'Page.navigate',{'url':(A/'slides/deck.html').as_uri()})
    await asyncio.sleep(1.0)
    query='''JSON.stringify((()=>{
      const a=document.querySelector('.cover .watermark').getBoundingClientRect();
      const b=document.querySelector('.cover .foot').getBoundingClientRect();
      const txt=document.querySelector('.cover .foot').innerText;
      return {artwork:{x:a.x,y:a.y,width:a.width,height:a.height,right:a.right,bottom:a.bottom},
        footer:{x:b.x,y:b.y,width:b.width,height:b.height,right:b.right,bottom:b.bottom,text:txt},
        overlap:{width:Math.max(0,Math.min(a.right,b.right)-Math.max(a.left,b.left)),
                 height:Math.max(0,Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top))}};
    })())'''
    i+=1;res=await issue(ws,i,'Runtime.evaluate',{'expression':query,'returnByValue':True})
    j=json.loads(res['result']['value']);j['overlap']['area']=round(j['overlap']['width']*j['overlap']['height'],2)
    assert j['overlap']['area']>10,'Unexpected cover no-overlap; reevaluate this review'
    return j
  finally:
   proc.terminate()
   try:proc.wait(timeout=5)
   except subprocess.TimeoutExpired:proc.kill()

content=asyncio.run(measure_cover())
opt=json.loads(OPT.read_text())
sim={}
for style in ('Display','Text'):
 a=opt['styles'][style]['pair_similarity']['3/З']
 sim[style]={str(x['px']):x['intersection_over_union'] for x in a if x['px'] in (10,12,14,16,20,40)}
css=(A/'tokens.css').read_text()
assert 'h1{font-size:clamp(38px,5.5vw,72px)' in css
fontscale=json.loads((T/'design-tokens.json').read_text())
assert fontscale['responsive_web_px']['desktop']['H1']==68
visual_pdf=T/'proofs/Brandbook-Typeface-v075-Pages.pdf'
def pdftext(pageno):
 return subprocess.check_output(['pdftotext','-f',str(pageno),'-l',str(pageno),'-layout',str(visual_pdf),'-'],text=True)
pg3=pdftext(3);pg4=pdftext(4)
assert '5. Числа' in pg3 and 'Схемы' not in pg3 and pg4.lstrip().startswith('Схемы')
assert '6. Цвет' in pg4
card=A/'proofs/business-card.pdf';slides=A/'proofs/slides.pdf'
assert int(re.search(r'^Pages:\s*(\d+)',subprocess.check_output(['pdfinfo',str(slides)],text=True),re.M).group(1))==3
p=(P/'evidence/cover-footer-collision.png')
# Evidentiary image: crop of the existing 16:9 PDF proof, with no modifications to source files.
im=Image.open(A/'proofs/render-slides-1.png').convert('RGB')
# Crop around lower-right footer where exact overlay is visibly present.
roi=(int(im.width*.57),int(im.height*.72),im.width,im.height)
part=im.crop(roi)
part.save(p)
summary={
 'status':'FIRST_INTERNAL_ART_DIRECTOR_REVIEW_NOT_OWNER_APPROVAL',
 'sources':{'carriers':'GoldenStep-Applications-v0.73','guide':'Arvectum-Typeface-v0.75','optical_audit':'Arvectum-Typeface-v0.62','provenance':'Arvectum-Typeface-v0.74'},
 'visual_reviewed':['site desktop/mobile','Pages native letter and proposal two pages','slide PDF three pages','business card two sides','typography guide five A4 pages'],
 'cover_overlap_chrome_css_rectangles':content,
 '3_vs_cyrillic_Z_mask_IoU_at_selected_px':sim,
 'design_token_mismatch':{'v0.73_site_desktop_H1_max_px':72,'v0.75_typography_desktop_H1_px':68,'difference_px':4},
 'typography_guide_page_break':{'section_5_heading_page':3,'section_5_continuation_without_heading_page':4,'physical_crop_or_text_loss_established':False},
 'presentation_equivalence':{'HTML_slide_PDF_rendered':True,'editable_PPTX_exists':True,'native_Keynote_PPTX_rendered':False,'pixel_parity_claim':False},
 'retained_source_logo':{'approved_geometry_originals_modified':False,'wordmark_cyrillic_r_and_e_open_review':True,'full_lockup_and_colors_owner_approved':False},
 'release_flag':{'OFL_inter_derived':True,'v0.64_fsType_preview_print':4,'fsType0_experimental_installed':False},
 'limitations':['High raster glyph IoU is not human-reading study','HTML slide rect overlap does not establish same problem in PPTX',
                'No changes to previous version, original master, customer material or live site',
                'Typography style guide page flow is editorial issue, not proof of PDF text clipping']}
(P/'evidence/facts.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print('COVER_OBSTRUCTION',content['overlap'])
print('SIMILARITY_3_Z',sim)
print('SCALE_MISMATCH 72 vs 68 px (desktop site vs guide)')
print('SECTION_BREAK page 3->4, no proven crop')
print('PASS first-review factual measurement saved')
