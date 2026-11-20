from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from PIL import Image,ImageFont,ImageDraw
import json,subprocess
P=Path(__file__).resolve().parent;old=P.parent/'Arvectum-Typeface-v0.45'
scope='+=−×÷±≠≤≥≈%‰°№'
im=Image.new('RGB',(1800,1400),'white');dr=ImageDraw.Draw(im)
label='/System/Library/Fonts/Supplemental/Arial.ttf'
def tx(x,y,s,sz=23,col='#334155'):dr.text((x,y),s,font=ImageFont.truetype(label,sz),fill=col)
def rec(f,n):
    p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
def glyphs(f,x,y,s,size):
    cmap=TTFont(f).getBestCmap();assert all(ord(c) in cmap for c in s),s
    ft=ImageFont.truetype(str(f),size);assert dr.textlength(s,font=ft)<=820,(s,size)
    dr.text((x,y),s,font=ft,fill='#001432')
tx(40,25,'ARVECTUM GOLDEN STEP / v0.46',36,'#001432')
tx(40,82,'Mathematical and business symbols / same optical size, no kerning',22)
results={}
for i,style in enumerate(('Display','Text')):
    a=next((old/'experimental').glob(f'Arvectum{style}*.otf'));b=next((P/'experimental').glob(f'Arvectum{style}*.otf'))
    fa,fb=TTFont(a),TTFont(b);cm=fa.getBestCmap();assert cm==fb.getBestCmap()
    changed=[]
    for cp,n in cm.items():
        if chr(cp) not in scope:assert rec(fa,n)==rec(fb,n) and fa['hmtx'][n]==fb['hmtx'][n],(style,cp)
        else:
            assert rec(fa,n)!=rec(fb,n) or fa['hmtx'][n]!=fb['hmtx'][n],(style,cp);changed.append(chr(cp))
    assert len(changed)==14
    adv={fb['hmtx'][cm[ord(c)]][0] for c in '+=−×÷±≠≤≥≈'}
    assert adv=={1323 if style=='Display' else 1266}
    for sz in (12,16,24,40,72):
        ft=ImageFont.truetype(str(b),sz);assert all(ft.getmask(c).getbbox() for c in scope)
    shaped=json.loads(subprocess.run(['hb-shape','--output-format=json',str(b),scope],capture_output=True,text=True,check=True).stdout)
    assert len(shaped)==14 and all(g['g']!='.notdef' for g in shaped)
    results[style]={'changed':changed,'unchanged':168,'operator_advance':next(iter(adv)),'raster_sizes':[12,16,24,40,72],'hb_nonmissing':14}
    top=145+i*610;dr.line((40,top,1760,top),fill='#cbd5e1',width=2);tx(40,top+14,style,28,'#001432')
    for j,(f,name) in enumerate(((a,'v0.45 / before'),(b,'v0.46 / after'))):
        x=40+j*880;tx(x,top+64,name,21,'#475569')
        for y,s,sz in [(105,'+ = − × ÷ ± ≠',82),(220,'≤ ≥ ≈ % ‰ ° №',72),(340,'125 × 8 = 1 000',56),(420,'x ≤ 12,5%  |  20 °C',50),(495,'№ 17 — ± 0,5 ‰',42)]:
            glyphs(f,x,top+y,s,sz)
im.save(P/'symbol-comparison.png');im.thumbnail((1100,900));im.save('/tmp/arvectum-v046-symbols.jpg',quality=84,optimize=True)
(P/'comparison-qa.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(results)
