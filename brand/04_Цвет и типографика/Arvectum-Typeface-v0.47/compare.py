from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from PIL import Image,ImageFont,ImageDraw
import json,subprocess
P=Path(__file__).resolve().parent;old=P.parent/'Arvectum-Typeface-v0.46'
scope='₽$€£¥₴¢';spaces=' \u00a0\u202f'
im=Image.new('RGB',(1800,1400),'white');dr=ImageDraw.Draw(im)
label='/System/Library/Fonts/Supplemental/Arial.ttf'
def tx(x,y,s,sz=23,col='#334155'):dr.text((x,y),s,font=ImageFont.truetype(label,sz),fill=col)
def rec(f,n):
    p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
def glyphs(f,x,y,s,size):
    cmap=TTFont(f).getBestCmap();assert all(ord(c) in cmap for c in s),s
    ft=ImageFont.truetype(str(f),size);assert dr.textlength(s,font=ft)<=820,(s,size)
    dr.text((x,y),s,font=ft,fill='#001432')
tx(40,25,'ARVECTUM GOLDEN STEP / v0.47',36,'#001432')
tx(40,82,'Currency and whitespace / same optical size, no kerning',22)
results={}
for i,style in enumerate(('Display','Text')):
    a=next((old/'experimental').glob(f'Arvectum{style}*.otf'));b=next((P/'experimental').glob(f'Arvectum{style}*.otf'))
    fa,fb=TTFont(a),TTFont(b);cm=fa.getBestCmap();assert cm==fb.getBestCmap()
    changed=[]
    for cp,n in cm.items():
        if chr(cp) not in scope+spaces:assert rec(fa,n)==rec(fb,n) and fa['hmtx'][n]==fb['hmtx'][n],(style,cp)
        elif chr(cp) in scope:
            assert rec(fa,n)!=rec(fb,n);changed.append(chr(cp))
        else:assert not any(op!='closePath' for op,pts in rec(fb,n))
    assert len(changed)==7
    widths={f'U+{ord(c):04X}':fb['hmtx'][cm[ord(c)]][0] for c in spaces}
    assert widths=={'U+0020':512,'U+00A0':512,'U+202F':316}
    all_ink=''.join(chr(c) for c in sorted(cm) if chr(c) not in spaces)
    assert len(all_ink)==179
    for sz in (12,16,24,40,72):
        ft=ImageFont.truetype(str(b),sz);assert all(ft.getmask(c).getbbox() for c in all_ink)
        assert all(ft.getmask(c).getbbox() is None for c in spaces)
        assert ft.getlength(' ')==ft.getlength('\u00a0')>ft.getlength('\u202f')>0
    shaped=json.loads(subprocess.run(['hb-shape','--output-format=json',str(b),all_ink],capture_output=True,text=True,check=True).stdout)
    assert len(shaped)==179 and all(g['g']!='.notdef' for g in shaped)
    for c in spaces:
        shaped=json.loads(subprocess.run(['hb-shape','--output-format=json',str(b),c],capture_output=True,text=True,check=True).stdout)
        assert len(shaped)==1 and shaped[0]['g']!='.notdef' and shaped[0]['ax']==widths[f'U+{ord(c):04X}'],(style,c,shaped)
    results[style]={'currency_changed':changed,'unchanged_outside_scope':172,'whitespace':widths,'raster_sizes':[12,16,24,40,72],'tested_visible_codepoints':179}
    top=145+i*610;dr.line((40,top,1760,top),fill='#cbd5e1',width=2);tx(40,top+14,style,28,'#001432')
    for j,(f,name) in enumerate(((a,'v0.46 / before'),(b,'v0.47 / after'))):
        x=40+j*880;tx(x,top+64,name,21,'#475569')
        for y,s,sz in [(105,'₽ $ € £ ¥ ₴ ¢',105),(230,'1 250 000,00 ₽',60),(315,'$ 12 345,67  |  € 890',46),(397,'£ 250  |  ¥ 1 200  |  ₴ 500',40),(480,'1\u00a0250\u00a0000 ₽  |  1\u202f250\u202f000 ₽',36)]:
            glyphs(f,x,top+y,s,sz)
im.save(P/'currency-comparison.png');im.thumbnail((1100,900));im.save('/tmp/arvectum-v047-currency.jpg',quality=84,optimize=True)
(P/'comparison-qa.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(results)
