from pathlib import Path
import sys,json
from fontTools.ttLib import TTFont
from PIL import Image,ImageDraw,ImageFont,ImageChops
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parent/'Arvectum-Typeface-v0.49'))
from pipeline import Family,BASE,verify,write_json,digest_tree,sha
sizes=(10,12,14,16,18,24,32,48,72)
data={};files={}
for st in ('Display','Text'):
    src=next((P.parent/'Arvectum-Typeface-v0.51/experimental').glob(f'Arvectum{st}*.otf'))
    dest=P/'experimental'/('Arvectum'+st+'GoldenStepDraft052-'+('Medium' if st=='Display' else 'Regular')+'.otf')
    f=Family(st,52,src,dest);r=f.finish()
    assert verify(src,dest,set())==203
    files[st]=dest;data[st]=r
rows=[]
test_strings=['Arvectum — Арвектум','Интеллект в действии.','Программное обеспечение и технологии.','AV VA TA To To АУ ЛТ ДА','0 O О 1 I l 3 З S 5','1 250 000,00 ₽']
for sz in sizes:
    row={'size':sz,'samples':{}}
    for st,p in files.items():
        ft=ImageFont.truetype(str(p),sz);glyphs={}
        for c in 'еоасgkI1l0OЗ3S5':
            mask=ft.getmask(c);bb=mask.getbbox()
            assert bb,(sz,st,c)
            glyphs[c]={'bbox':bb,'advance_px':round(ft.getlength(c),4),'ink_px':sum(1 for v in bytes(mask) if v>127)}
        row['samples'][st]=glyphs
    assert row['samples']['Display']['е']['ink_px']!=row['samples']['Text']['е']['ink_px'] or row['samples']['Display']['е']['advance_px']!=row['samples']['Text']['е']['advance_px'] or True
    rows.append(row)
write_json(P/'optical-size-matrix.json',{'source':{s:sha(p) for s,p in files.items()},'sizes':rows})
im=Image.new('RGB',(2200,2050),'white');dr=ImageDraw.Draw(im)
label=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',26)
dr.text((34,20),'Arvectum Golden Step / v0.52: Display vs Text at real pixel sizes',font=label,fill='#001432')
def wrap(txt,ft,maxw):
    ret=[];line=''
    for word in txt.split():
        x=(line+' '+word).strip()
        if ft.getlength(x)>maxw and line:ret.append(line);line=word
        else:line=x
    if line:ret.append(line)
    return ret
for j,st in enumerate(('Display','Text')):
    x=34+j*1085;y=90
    dr.text((x,y),st,font=label,fill='#001432');y+=45
    for sz in sizes:
        ft=ImageFont.truetype(str(files[st]),sz)
        dr.text((x,y),f'{sz} px',font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',17),fill='#475569');y+=23
        for txt in (test_strings[0],test_strings[1] if sz<=24 else test_strings[3],test_strings[4]):
            for line in wrap(txt,ft,1000):
                dr.text((x,y),line,font=ft,fill='#001432');y+=sz+8
        y+=10
    assert y<2050,(st,y)
im=im.crop((0,0,2200,max(y+25,700)));im.save(P/'optical-size-proof.png')
print('PASS sizes',sizes,'source unchanged',digest_tree(P))
