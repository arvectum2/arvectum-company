from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from fontTools.ttLib import TTFont
import numpy as np,json,subprocess
P=Path(__file__).resolve().parent;ROOT=P.parent
STYLES=('Display','Text');PX=(10,12,14,16,20,28,40,64)
def mask(f,c,sz):
    ft=ImageFont.truetype(str(f),sz)
    im=Image.new('L',(sz*3,sz*3))
    ImageDraw.Draw(im).text((sz,sz*2),c,font=ft,fill=255,anchor='ls')
    return np.array(im)>=128
def similarity(font,a,b,size):
    x,y=mask(font,a,size),mask(font,b,size)
    u=np.count_nonzero(x|y)
    return round(float(np.count_nonzero(x&y))/u,4) if u else 0
def overlap(font,pair,size):
    ft=ImageFont.truetype(str(font),size)
    masks=[]
    for c in pair:
        v,o=ft.getmask2(c,mode='L',anchor='ls')
        masks.append((np.asarray(v,dtype=np.uint8).reshape(v.size[1],v.size[0]),o))
    sh=json.loads(subprocess.check_output(['hb-shape','--output-format=json',str(font),pair],text=True))
    if len(sh)!=2:return None
    (a,(x1,y1)),(b,(xb,y2))=masks
    x2=xb+int(round(sh[0]['ax']*size/2048))
    lx,rx=max(x1,x2),min(x1+a.shape[1],x2+b.shape[1])
    ty,by=max(y1,y2),min(y1+a.shape[0],y2+b.shape[0])
    if lx>=rx or ty>=by:return 0
    return int(np.count_nonzero((a[ty-y1:by-y1,lx-x1:rx-x1]>=128)&
        (b[ty-y2:by-y2,lx-x2:rx-x2]>=128)))
results={}
for sty in STYLES:
    old=next((ROOT/'Arvectum-Typeface-v0.61/experimental').glob('Arvectum'+sty+'*.otf'))
    new=next((P/'experimental').glob('Arvectum'+sty+'*.otf'))
    comparisons={}
    for pair in ('3З','дл','лд','З3'):
        comparisons[pair]=[dict(px=s,old=similarity(old,*pair,s),new=similarity(new,*pair,s)) for s in PX]
    # Controlled neighbor mask tests around revised glyphs. Do not assume no collision outside these pairs.
    collide={}
    scope=['дл','лд','од','до','ад','да','дл','ил','ли','ЗА','АЗ','ЗО','ОЗ','З3','3З']
    for size in (12,16,24,40,72,128):
        for pair in sorted(set(scope)):
            count=overlap(new,pair,size)
            if count:collide[f'{pair}:{size}']=count
    results[sty]={'similarity':comparisons,'candidate_ink_collisions':collide}
    print(sty,'3/З IoU',[(v['px'],v['old'],v['new']) for v in comparisons['3З'] if v['px'] in (12,14,16,40)])
    print('candidate collisions',collide)
    assert comparisons['3З'][2]['new']<comparisons['3З'][2]['old'],('3/З did not improve at 14px',sty)
    # Current optical revision only experimental; note any intersections rather than auto-approve.
    im=Image.new('RGB',(1850,1410),'white');d=ImageDraw.Draw(im)
    regular=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',21)
    title=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',32)
    d.text((30,24),'ARVECTUM v0.63 — '+sty+' / optical candidate vs v0.61 baseline',font=title,fill='#122a38')
    labels=[('Original v0.61',old),('Alternative v0.63',new)]
    for idx,(lab,font) in enumerate(labels):
        x=30+idx*920
        d.text((x,80),lab,font=regular,fill='#445665')
        d.line((x,118,x+885,118),fill='#ced8df')
        y=145
        for phrase,size in [
            ('3  З  3З  33З  ЗАРПЛАТА',50),
            ('дл  лд  Договор  для  лица',43),
            ('Статус дела · 3 заявки · 3З',34),
            ('д л  З  3   14px original sizes shown below',23),
            ('Здравствуйте! Сроки, задачи, доходы.',33),
            ('взгляд, длина, лад, здание, должность',30)
        ]:
            f=ImageFont.truetype(str(font),size)
            assert d.textlength(phrase,font=f)<875,(sty,phrase)
            d.text((x,y),phrase,font=f,fill='#112b38')
            y+=104
        for i,sz in enumerate((10,12,14,16,20,28,40,64)):
            f=ImageFont.truetype(str(font),sz*2)
            yy=790+i*68
            d.text((x,yy),str(sz)+'px ×2:',font=regular,fill='#75838f')
            d.text((x+155,yy),'3 З / д л',font=f,fill='#112b38')
    im.save(P/'proofs'/('optical-alternatives-'+sty.lower()+'.png'))
(P/'optical-qa.json').write_text(json.dumps({'status':'PROPOSAL_ONLY','styles':results,
 'safety_scope':'12–128px tested subset, original 212 Unicode mapping maintained',
 'no_default_approval':True,'Windows':'deferred'},ensure_ascii=False,indent=2)+'\n')
im=Image.open(P/'proofs/optical-alternatives-display.png');im.thumbnail((1150,880))
im.save('/tmp/arvectum-v063-alternatives.png')
print('PASS v0.63 measurements; visual candidate awaiting editorial review')
