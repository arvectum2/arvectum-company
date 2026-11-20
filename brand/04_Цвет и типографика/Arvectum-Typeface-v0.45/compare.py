from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from PIL import Image,ImageFont,ImageDraw
import json,subprocess
P=Path(__file__).resolve().parent;old=P.parent/'Arvectum-Typeface-v0.44'
geometry=json.loads((P/'punctuation-geometry.json').read_text());im=Image.new('RGB',(1800,1400),'white');dr=ImageDraw.Draw(im)
label='/System/Library/Fonts/Supplemental/Arial.ttf'
def tx(x,y,s,sz=23,col='#334155'):dr.text((x,y),s,font=ImageFont.truetype(label,sz),fill=col)
def rec(f,n):
    p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
def glyphs(f,x,y,s,size):
    cmap=TTFont(f).getBestCmap();assert all(ord(c) in cmap for c in s),s
    ft=ImageFont.truetype(str(f),size);assert dr.textlength(s,font=ft)<=820,(s,size)
    dr.text((x,y),s,font=ft,fill='#001432')
tx(40,25,'ARVECTUM GOLDEN STEP / v0.45',36,'#001432')
tx(40,82,'Punctuation / same optical size, no kerning',22)
results={}
for i,style in enumerate(('Display','Text')):
    a=next((old/'experimental').glob(f'Arvectum{style}*.otf'));b=next((P/'experimental').glob(f'Arvectum{style}*.otf'))
    fa,fb=TTFont(a),TTFont(b);cm=fa.getBestCmap();cb=fb.getBestCmap()
    scope=set(map(ord,geometry[style]['glyphs']));assert set(cb)-set(cm)=={0xb7,0x7c} and set(cm)<=set(cb)
    changed=[]
    for cp,n in cm.items():
        if cp not in scope:assert rec(fa,n)==rec(fb,cb[cp]) and fa['hmtx'][n]==fb['hmtx'][cb[cp]],(style,cp)
        else:
            assert rec(fa,n)!=rec(fb,cb[cp]) or fa['hmtx'][n]!=fb['hmtx'][cb[cp]],(style,cp);changed.append(chr(cp))
    assert len(changed)==28
    for ch,width in [('–',1024),('—',2048)]:assert fb['hmtx'][cb[ord(ch)]][0]==width
    assert len({fb['hmtx'][cb[ord(c)]] for c in '-‐‑'})==1
    assert rec(fb,cb[ord('-')])==rec(fb,cb[ord('‐')])==rec(fb,cb[ord('‑')])
    for sz in (12,16,24,40,72):
        ft=ImageFont.truetype(str(b),sz);assert all(ft.getmask(chr(c)).getbbox() for c in scope)
    # Test independent code points, without HarfBuzz normalization or bidi reordering affecting count.
    for c in scope:
        shaped=json.loads(subprocess.run(['hb-shape','--output-format=json',str(b),chr(c)],capture_output=True,text=True,check=True).stdout)
        assert len(shaped)==1 and shaped[0]['g']!='.notdef',(style,c,shaped)
    results[style]={'changed':changed,'added':['U+00B7','U+007C'],'unchanged':152,'raster_sizes':[12,16,24,40,72],'hb_nonmissing':30}
    top=145+i*610;dr.line((40,top,1760,top),fill='#cbd5e1',width=2);tx(40,top+14,style,28,'#001432')
    for j,(f,name) in enumerate(((a,'v0.44 / before'),(b,'v0.45 / after'))):
        x=40+j*880;tx(x,top+64,name,21,'#475569')
        for y,s,sz in [(105,'.,:;!?… – — - ‐ ‑',77),(220,'«» “ ” ‘ ’ „ ‚ " \'',70),(330,'( ) [ ] { }',74),(430,'«Арвектум»: проект (2026).',40),(493,'“Quality” — 1 234,56 ₽;',35)]:
            glyphs(f,x,top+y,s,sz)
        if j:glyphs(f,x,top+550,'A · B | C',30)
im.save(P/'punctuation-comparison.png');im.thumbnail((1100,900));im.save('/tmp/arvectum-v045-punctuation.jpg',quality=84,optimize=True)
(P/'comparison-qa.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(results)
