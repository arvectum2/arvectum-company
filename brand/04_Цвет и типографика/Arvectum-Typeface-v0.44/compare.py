from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from PIL import Image,ImageFont,ImageDraw
import json,subprocess,string
P=Path(__file__).resolve().parent;old=P.parent/'Arvectum-Typeface-v0.43'
im=Image.new('RGB',(1800,1400),'white');dr=ImageDraw.Draw(im)
label='/System/Library/Fonts/Supplemental/Arial.ttf'
def tx(x,y,s,sz=23,col='#334155'):dr.text((x,y),s,font=ImageFont.truetype(label,sz),fill=col)
def rec(f,n):
    p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
def glyphs(f,x,y,s,size):
    cmap=TTFont(f).getBestCmap();assert all(ord(c) in cmap for c in s),s
    ft=ImageFont.truetype(str(f),size);assert dr.textlength(s,font=ft)<=820
    dr.text((x,y),s,font=ft,fill='#001432')
tx(40,25,'ARVECTUM GOLDEN STEP / v0.44',36,'#001432')
tx(40,82,'Tabular digits / same optical size, no kerning',22)
results={}
for i,style in enumerate(('Display','Text')):
    a=next((old/'experimental').glob(f'Arvectum{style}*.otf'));b=next((P/'experimental').glob(f'Arvectum{style}*.otf'))
    fa,fb=TTFont(a),TTFont(b);cm=fa.getBestCmap();assert cm==fb.getBestCmap()
    ds=set(map(ord,string.digits));changed=[]
    for cp,n in cm.items():
        assert fa['hmtx'][n][0]==fb['hmtx'][n][0],(style,cp)
        if cp not in ds:assert rec(fa,n)==rec(fb,n) and fa['hmtx'][n]==fb['hmtx'][n],(style,cp)
        else:
            assert rec(fa,n)!=rec(fb,n),(style,cp);changed.append(chr(cp))
    adv={fb['hmtx'][cm[c]][0] for c in ds};assert adv=={1323 if style=='Display' else 1266}
    for sz in (12,16,24,40,72):
        ft=ImageFont.truetype(str(b),sz)
        assert all(ft.getmask(c).getbbox() for c in string.digits)
        assert len({ft.getlength(c) for c in string.digits})==1
        assert bytes(ft.getmask('0'))!=bytes(ft.getmask('O')) and bytes(ft.getmask('0'))!=bytes(ft.getmask('О'))
        assert bytes(ft.getmask('1'))!=bytes(ft.getmask('I'))
    shaped=json.loads(subprocess.run(['hb-shape','--output-format=json',str(b),string.digits],capture_output=True,text=True,check=True).stdout)
    assert len(shaped)==10 and all(g['g']!='.notdef' and g['ax']==next(iter(adv)) for g in shaped)
    results[style]={'changed':changed,'unchanged':170,'advance':next(iter(adv)),'raster_sizes':[12,16,24,40,72],'hb_tabular':True}
    top=145+i*610;dr.line((40,top,1760,top),fill='#cbd5e1',width=2);tx(40,top+14,style,28,'#001432')
    for j,(f,name) in enumerate(((a,'v0.43 / before'),(b,'v0.44 / after'))):
        x=40+j*880;tx(x,top+64,name,21,'#475569')
        glyphs(f,x,top+105,'0123456789',105)
        glyphs(f,x,top+245,'0 O О   1 I l   3 З   5 S',56)
        glyphs(f,x,top+351,'1 234 567,89 ₽',56)
        glyphs(f,x,top+425,'9 876 543,21 ₽',56)
        glyphs(f,x,top+515,'2026–2027  —  01.12.2026',24)
im.save(P/'digit-comparison.png');im.thumbnail((1100,900));im.save('/tmp/arvectum-v044-digits.jpg',quality=84,optimize=True)
(P/'comparison-qa.json').write_text(json.dumps(results,indent=2)+'\n')
print(results)
