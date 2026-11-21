"""Optical baseline audit; no glyph or font asset changed."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
import numpy as np,math,json
from fontTools.ttLib import TTFont
P=Path(__file__).resolve().parent;ROOT=P.parent
SIZES=(10,12,14,16,20,28,40,64)
GROUPS=[('Cyrillic reading','д л ч ж и п т г о а р'),
('Latin bowls','s g e a c o p q'),
('Figures versus lookalikes','0 O О 3 З 1 I l'),
('English+Russian','System Arvectum АРВЕКТУМ'),
('Real wording','Интеллект в действии.'),
('Technical wording','Договор, статус, закупка, графика, аналитика.')]
PAIRS=[('0','O'),('0','О'),('3','З'),('1','I'),('1','l'),('I','l'),('д','л'),('s','g')]
def glyph_img(font,ch,size):
    f=ImageFont.truetype(str(font),size)
    # Fixed baseline point in a normalized canvas; shapes may have distinct x advances
    v=Image.new('L',(size*3,size*3),0)
    x=size;baseline=size*2
    ImageDraw.Draw(v).text((x,baseline),ch,font=f,fill=255,anchor='ls')
    return v
result={}
for sty in ('Display','Text'):
    font=next((ROOT/'Arvectum-Typeface-v0.61/experimental').glob('Arvectum'+sty+'*.otf'))
    tt=TTFont(font);cm=tt.getBestCmap()
    metrics={}
    for ch in 'длчжsgeacopq0OО3З1Il':
        if ord(ch) not in cm:continue
        m=ImageFont.truetype(str(font),40)
        mask,offset=m.getmask2(ch,mode='L',anchor='ls')
        arr=np.asarray(mask,dtype=np.uint8).reshape(mask.size[1],mask.size[0])
        metrics[ch]={'advance_40px':round(m.getlength(ch),3),'mask_size':mask.size,'offset':offset,
                     'dark_pixels_40px':int(np.count_nonzero(arr>=128)),
                     'dark_fraction_40px':round(float(np.mean(arr>=128)),4)}
    comparison={}
    for a,b in PAIRS:
        observations=[]
        for s in SIZES:
            ai=np.asarray(glyph_img(font,a,s),dtype=np.uint8)>127
            bi=np.asarray(glyph_img(font,b,s),dtype=np.uint8)>127
            union=int(np.count_nonzero(ai|bi));inter=int(np.count_nonzero(ai&bi))
            observations.append({'px':s,'intersection_over_union':round(inter/max(1,union),4),
                'dark_count_a':int(ai.sum()),'dark_count_b':int(bi.sum())})
        comparison[a+'/'+b]=observations
    result[sty]={'metric':metrics,'pair_similarity':comparison,'sizes':SIZES}
    w=2300;h=1500
    im=Image.new('RGB',(w,h),'#fff');d=ImageDraw.Draw(im)
    title=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',32)
    label=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',18)
    d.text((50,24),'GOLDEN STEP v0.62   /   '+sty+'   /   optical grid (baseline v0.61)',font=title,fill='#112c3b')
    # Visible rows are 4 focus groups x 8 sizes.
    for r,(group,txt) in enumerate(GROUPS[:4]):
        y=96+r*305
        d.text((52,y),group,font=title,fill='#173442')
        d.line((52,y+48,2240,y+48),fill='#d5dfe3',width=2)
        for j,sz in enumerate(SIZES):
            x=55+j*280
            d.text((x,y+65),str(sz)+' px',font=label,fill='#74838c')
            f=ImageFont.truetype(str(font),sz)
            # glyph sample individually, ensure no overflow in 275px cell
            if r<3:
                shown=txt.replace(' ','')
                shown=shown[:10] if r==0 else shown[:8]
                maxlen=d.textlength(shown,font=f)
                if maxlen>260:shown=shown[:int(len(shown)*260/maxlen)]
                d.text((x,y+130),shown,font=f,fill='#112c3b')
                enlarged=ImageFont.truetype(str(font),max(24,min(45,sz)))
                d.text((x,y+203),shown[:5],font=enlarged,fill='#112c3b')
            else:
                # text sample clipped to cell, but the crop is documented
                excerpt='Arvectum' if j%2 else 'АРВЕКТУМ'
                d.text((x,y+130),excerpt,font=f,fill='#112c3b')
    y=1320
    d.text((55,y),'Reading at small sizes must be judged by people; IoU is only a shape-similarity diagnostic.',font=label,fill='#41515f')
    im.save(P/'proofs'/('optical-grid-'+sty.lower()+'.png'))
# Extra legible full-width specimen, at 12 / 14 / 18px and 40px to inspect golden-style angular кириллица in actual paragraphs.
im=Image.new('RGB',(2200,1410),'#fff');d=ImageDraw.Draw(im)
title=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',31)
label=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',20)
for idx,sty in enumerate(('Display','Text')):
    font=next((ROOT/'Arvectum-Typeface-v0.61/experimental').glob('Arvectum'+sty+'*.otf'))
    y0=35+idx*680
    d.text((45,y0),sty+' · 12/14/16/24/42px',font=title,fill='#112c3b')
    y=y0+60
    samples=['Арвектум — Интеллект в действии. Сложная геометрия: д, л, ч, ж, з.',
             'Цена предложения 1\u202f250\u202f000 ₽. 0/O/О, 3/З и 1/I/l — отличить.',
             'Договор, поставщик, консультант, статус, номер заявки, отчёт.',
             'Arvectum Intelligent Solutions. System, software and data.']
    for size,sample in zip((12,14,16,24),samples):
        ft=ImageFont.truetype(str(font),size*2)
        d.text((55,y),str(size)+'px [2×]:',font=label,fill='#526776')
        d.text((260,y),sample,font=ft,fill='#112c3b')
        y+=111
    ft=ImageFont.truetype(str(font),50)
    d.text((55,y+35),'дл  лд  жч  s g  0 O О  3 З  1 I l',font=ft,fill='#112c3b')
im.save(P/'proofs/reading-specimen.png')
(P/'audit.json').write_text(json.dumps({'baseline':'v0.61','font_outlines_changed':False,'styles':result,
  'limitations':['IoU uses a fixed baseline, not forced shape normalization',
   'small-screen anti-aliasing and reader accuracy not proven',
   'similarity threshold cannot substitute for editorial review',
   'Windows explicitly deferred by owner']},ensure_ascii=False,indent=2)+'\n')
for st,records in result.items():
 print(st, 'mean similarity 0/O at 14px',records['pair_similarity']['0/O'][2]['intersection_over_union'],
   '3/З at 14px',records['pair_similarity']['3/З'][2]['intersection_over_union'],
   '1/I at 14px',records['pair_similarity']['1/I'][2]['intersection_over_union'])
print('PASS audit+3 PNG sheets, no changes to fonts')
