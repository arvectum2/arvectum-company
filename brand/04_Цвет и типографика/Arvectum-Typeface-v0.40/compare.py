from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from PIL import Image, ImageFont, ImageDraw
import json,hashlib,subprocess
P=Path(__file__).resolve().parent
old=P.parent/'Arvectum-Typeface-v0.39'
common='KXYZkwxyzУХжх'
label='/System/Library/Fonts/Supplemental/Arial.ttf'
im=Image.new('RGB',(1800,1400),'white');dr=ImageDraw.Draw(im)
def text(x,y,s,sz=23,col='#334155'):
    dr.text((x,y),s,font=ImageFont.truetype(label,sz),fill=col)
def glyphs(f,x,y,s,size):
    font=ImageFont.truetype(str(f),size)
    assert dr.textlength(s,font=font)<=820,(s,size)
    dr.text((x,y),s,font=font,fill='#001432')
def record(f,n):
    pen=RecordingPen();f.getGlyphSet()[n].draw(pen);return pen.value
text(40,25,'ARVECTUM GOLDEN STEP   /   v0.40',36,'#001432')
text(40,82,'Diagonal and branch family   /   same optical size, no kerning',22)
results={}
for i,style in enumerate(('Display','Text')):
    changed=set(common+('ку' if style=='Text' else ''))
    a=next((old/'experimental').glob(f'Arvectum{style}*.otf'));b=next((P/'experimental').glob(f'Arvectum{style}*.otf'))
    fa,fb=TTFont(a),TTFont(b)
    assert fa.getBestCmap()==fb.getBestCmap()
    cm=fa.getBestCmap();same=[];diff=[]
    for cp,n in cm.items():
        sameoutline=record(fa,n)==record(fb,n)
        samemetrics=fa['hmtx'][n]==fb['hmtx'][n]
        if chr(cp) not in changed:
            assert sameoutline and samemetrics,(style,chr(cp))
            same.append(chr(cp))
        elif not (sameoutline and samemetrics):diff.append(chr(cp))
    assert len(same)==180-len(changed)
    for a1,b1 in [('K','К'),('X','Х'),('x','х')]+([('y','у')] if style=='Text' else []):
        assert record(fb,cm[ord(a1)])==record(fb,cm[ord(b1)]) and fb['hmtx'][cm[ord(a1)]]==fb['hmtx'][cm[ord(b1)]],(style,a1,b1)
    for ch in '0123456789':assert fa['hmtx'][cm[ord(ch)]]==fb['hmtx'][cm[ord(ch)]]
    qa={}
    for sz in (12,16,24,40,72):
        font=ImageFont.truetype(str(b),sz)
        assert all(font.getmask(c).getbbox() for c in changed)
        qa[str(sz)]=len(changed)
    shaped=json.loads(subprocess.run(['hb-shape','--output-format=json',str(b),''.join(sorted(changed))],capture_output=True,text=True,check=True).stdout)
    assert len(shaped)==len(changed) and all(x['g']!='.notdef' for x in shaped)
    results[style]={'unchanged_outside_family':len(same),'actually_changed':sorted(diff),'same_within_family':sorted(changed-set(diff)),'raster_nonempty':qa,'hb_nonmissing':len(changed)}
    top=145+i*610
    dr.line((40,top,1760,top),fill='#cbd5e1',width=2);text(40,top+14,style,28,'#001432')
    for j,(f,name) in enumerate(((a,'v0.39 / before'),(b,'v0.40 / after'))):
        x=40+j*880
        text(x,top+64,name,21,'#475569')
        glyphs(f,x,top+99,'K X Y Z k w x y z',62)
        glyphs(f,x,top+218,'У Х ж х к у',70)
        glyphs(f,x,top+350,'KEY — XYZ — Network',42)
        glyphs(f,x,top+414,'ЖУК — ХУДОЖНИК — УЗЕЛ',36)
        glyphs(f,x,top+474,'Arvectum  Арвектум',38)
        glyphs(f,x,top+530,'Согласование  12 000 ₽  Core concept',18)
im.save(P/'diagonal-comparison.png')
im.thumbnail((1100,900));im.save('/tmp/arvectum-v040-diagonal.jpg',quality=83,optimize=True)
(P/'comparison-qa.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False))
