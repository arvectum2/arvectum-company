from pathlib import Path
import json,csv,collections
from PIL import Image,ImageDraw,ImageFont
from fontTools.ttLib import TTFont
P=Path(__file__).resolve().parent;V=P.parent/'Arvectum-Typeface-v0.47'
label='/System/Library/Fonts/Supplemental/Arial.ttf'
font=lambda sz:ImageFont.truetype(label,sz)
rows=list(csv.DictReader((P/'glyph-audit.csv').open()))
navy='#001432';teal='#41B599';muted='#475569'
for st in ('Display','Text'):
    p=next((V/'experimental').glob(f'Arvectum{st}*.otf'));f=TTFont(p);cm=f.getBestCmap()
    r=[x for x in rows if x['style']==st]
    # Fixed baseline and point size, with wide cells sufficient for em dash and broad A.
    im=Image.new('RGB',(1680,1940),'white');dr=ImageDraw.Draw(im)
    dr.text((26,18),f'ARVECTUM GOLDEN STEP / {st} / v0.48 AUDIT',font=font(32),fill=navy)
    dr.text((26,61),'All 182 encoded positions, actual v0.47 outlines / 88 px / red: metric triage',font=font(19),fill=muted)
    ft=ImageFont.truetype(str(p),88)
    for i,x in enumerate(r):
        xx=25+(i%14)*116;yy=105+(i//14)*140
        dr.rectangle((xx,yy,xx+113,yy+136),outline='#dedfe3')
        dr.text((xx+4,yy+3),x['unicode'][2:],font=font(13),fill='#b45309' if x['flags'] else muted)
        dr.line((xx+3,yy+101,xx+110,yy+101),fill='#b9ddd5')
        c=x['char'];w=ft.getlength(c)
        assert w<=113,(st,c,w)
        if c.isspace():dr.rectangle((xx+int((113-w)/2),yy+56,xx+int((113+w)/2),yy+77),outline=teal)
        else:dr.text((xx+(113-w)/2,yy+101),c,font=ft,fill=navy,anchor='ls')
        dr.text((xx+4,yy+124),x['advance'],font=font(11),fill=muted)
    im.save(P/f'{st.lower()}-glyph-grid.png')
    im.thumbnail((780,900));im.save(f'/tmp/arvectum-v048-{st.lower()}-grid.jpg',quality=55,optimize=True)
# Mixed-script proof uses actual excerpts where all characters are mapped.
corpus=json.loads((P/'corpus.json').read_text())
original=corpus[0]['text']
lines=['Arvectum — Арвектум','Интеллект в действии. Intelligence in action.','Системность, надёжность, ясность, интеллект.','AV AW VA WA TA To Te Ty LT LY','АВ ВА АУ УА ТА То Те Ту ЛТ ДА','yу kк  I l 1  O О 0  З 3  S 5  Б 6','1 250 000,00 ₽   1\u202f250\u202f000 ₽','Срок исполнения — 20 рабочих дней.']
im=Image.new('RGB',(1600,1560),'white');dr=ImageDraw.Draw(im)
dr.text((36,22),'ARVECTUM GOLDEN STEP / OPTICAL REVIEW',font=font(34),fill=navy)
dr.text((36,70),'Baseline v0.47 / no kerning / draft, not approved',font=font(20),fill=muted)
def wrap(s,ft,w):
    out=[];line=''
    for word in s.split():
        nxt=(line+' '+word).strip()
        if ft.getlength(nxt)>w and line:out.append(line);line=word
        else:line=nxt
    if line:out.append(line)
    return out
for i,st in enumerate(('Display','Text')):
    p=next((V/'experimental').glob(f'Arvectum{st}*.otf'));cm=TTFont(p).getBestCmap()
    x=36+i*785;y=122
    dr.text((x,y),st,font=font(26),fill=navy);y+=42
    for j,line in enumerate(lines):
        assert all(ord(c) in cm for c in line)
        ft=ImageFont.truetype(str(p),[50,27,25,36,36,35,36,26][j])
        for l in wrap(line,ft,750):dr.text((x,y),l,font=ft,fill=navy);y+=ft.size+14
    y+=12
    dr.line((x,y,x+740,y),fill='#ccd9dd');y+=16
    paragraph=next(l.split(': ',1)[-1] for l in original.splitlines() if l.startswith('Позиционирование:'))
    assert all(ord(c) in cm for c in paragraph)
    for sz in (16,22,30):
        ft=ImageFont.truetype(str(p),sz)
        dr.text((x,y),f'{sz}px / actual brand-platform excerpt',font=font(14),fill=muted);y+=22
        for l in wrap(paragraph,ft,735):dr.text((x,y),l,font=ft,fill=navy);y+=sz+8
        y+=17
    assert y<1560,(st,y)
im=im.crop((0,0,1600,max(y+35,1050)));im.save(P/'mixed-script-proof.png');im.thumbnail((900,760));im.save('/tmp/arvectum-v048-mixed.jpg',quality=65,optimize=True)
print('PASS: full fixed-baseline grids and mixed-script proof')
