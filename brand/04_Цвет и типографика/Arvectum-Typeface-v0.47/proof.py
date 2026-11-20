from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,subprocess
P=Path(__file__).resolve().parent
fonts=sorted((P/'experimental').glob('*.otf'))
assert len(fonts)==2
W,H=1800,1580
im=Image.new('RGB',(W,H),'white');dr=ImageDraw.Draw(im)
system='/System/Library/Fonts/Supplemental/Arial.ttf'
lab=lambda size:ImageFont.truetype(system,size)
navy='#001432';mint='#41B599'
dr.text((40,24),'ARVECTUM  /  v0.47 COMPLETE PRIMARY REPERTOIRE',font=lab(36),fill=navy)
dr.text((40,77),'182 encoded positions per font  •  unapproved draft contours  •  no kerning',font=lab(22),fill='#475569')
reports={}
for i,p in enumerate(fonts):
    y=135+i*720;style='Display' if 'Display' in p.name else 'Text'
    dr.line((40,y,W-40,y),fill='#cbd5e1',width=2)
    dr.text((40,y+12),style+' / draft OTF',font=lab(26),fill=navy)
    dr.text((40,y+50),'Arvectum  Арвектум',font=ImageFont.truetype(str(p),83),fill=navy)
    for j,(size,s) in enumerate([(44,'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),(44,'abcdefghijklmnopqrstuvwxyz'),(39,'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'),(39,'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'),(39,'0123456789  ₽ $ € £ ¥ ₴ ¢  №  17,5%  + − × ÷'),(26,'Съешь ещё этих мягких французских булок, да выпей чаю.'),(22,'The quick brown fox jumps over the lazy dog.  AV VA  лл дл ере рер'),(16,'Арвектум — разработка программного обеспечения. 1 250 000 ₽.')]):
        f=ImageFont.truetype(str(p),size)
        assert dr.textlength(s,font=f)<W-80,(style,size,s,dr.textlength(s,font=f))
        dr.text((40,y+165+j*62),s,font=f,fill=navy)
    checks={}
    for size in [12,16,24,40,72]:
        f=ImageFont.truetype(str(p),size)
        word='Arvectum Арвектум Ёё 0123456789'
        bbox=f.getbbox(word);assert bbox[2]>bbox[0] and bbox[3]>bbox[1]
        mask=f.getmask(word);assert mask.getbbox()
        checks[str(size)]={'width':f.getlength(word),'bbox':bbox}
    hb=subprocess.run(['hb-shape','--output-format=json',str(p),'Arvectum Арвектум Ёё 0123456789 ₽'],check=True,capture_output=True,text=True)
    glyphs=json.loads(hb.stdout);assert all(x['g']!='.notdef' for x in glyphs)
    reports[style]={'freetype':checks,'harfbuzz_shaped_glyphs':len(glyphs),'notdef':0}
im.save(P/'proof.png')
(P/'render-qa.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n')
im.thumbnail((1050,950));im.save('/tmp/arvectum-v047-proof.jpg',quality=82,optimize=True)
print(reports)
