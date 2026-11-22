from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import hashlib,csv,json
P=Path(__file__).resolve().parent
S=P.parent/'Arvectum-Typeface-v0.36'/'sources'
expected={'InterDisplay-Medium.otf':'9a17712bbd6da13b7ce9beb056d19fe15648799a11d5c35f8086a1270a0d13b2','InterDisplay-Regular.otf':'35c1f7437dd6d63f4e60a49144df4b4e4edc190e13ffc1e54b86083747fe3acf','LICENSE.txt':'262481e844521b326f5ecd053e59b98c8b2da78c8ee1bdbb6e8174305e54935a'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for n,v in expected.items():assert sha(S/n)==v,n
(P/'OFL-LICENSE.txt').write_bytes((S/'LICENSE.txt').read_bytes())
m={'version':'0.85','kind':'experimental/unapproved','source':'Inter 4.1 InterDisplay static CFF','unchanged_outlines':True,'source_hashes':expected,'styles':{}}
for sty,weight,name in [('Display','Medium','InterDisplay-Medium.otf'),('Text','Regular','InterDisplay-Regular.otf')]:
 f=TTFont(S/name,recalcTimestamp=False)
 family=f'Arvectum Golden Step {sty} Base Draft 085'
 ps=f'ArvectumGoldenStep{sty}BaseDraft085-{weight}'
 for plat,enc,lang in [(3,1,1033),(1,0,0)]:
  for nid,val in {1:family,2:weight,3:ps+';0.85;Inter-4.1-source',4:family+' '+weight,5:'Version 0.085; experimental',6:ps,16:family,17:weight}.items():
   f['name'].setName(val,nid,plat,enc,lang)
 f['CFF '].cff.topDictIndex[0].FamilyName=family
 f['CFF '].cff.topDictIndex[0].FullName=family+' '+weight
 f['CFF '].cff.fontNames=[ps]
 f['head'].fontRevision=.085
 out=P/'experimental'/f'{ps}.otf';out.parent.mkdir(parents=True,exist_ok=True)
 f.save(out)
 cm=f.getBestCmap()
 for ch in 'Зз3ВвАЕМ':
  g=f.getGlyphSet()[cm[ord(ch)]]
  sp=SVGPathPen(f.getGlyphSet());g.draw(sp)
  bp=BoundsPen(f.getGlyphSet());g.draw(bp);x0,y0,x1,y1=bp.bounds
  p=P/'glyphs'/sty/f'U+{ord(ch):04X}.svg';p.parent.mkdir(parents=True,exist_ok=True)
  p.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.3f} {-y1:.3f} {x1-x0:.3f} {y1-y0:.3f}"><path fill="#001432" transform="scale(1 -1)" d="{sp.getCommands()}"/></svg>\n')
 m['styles'][sty]={'source':name,'output':str(out.relative_to(P)),'sha256':sha(out),'unicode_positions':len(cm),'glyph_count':len(f.getGlyphOrder())}
 print('BUILT',sty,len(cm),len(f.getGlyphOrder()),sha(out)[:14])
alphabet=[('Cyrillic capitals','АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'),('Cyrillic lowercase','абвгдеёжзийклмнопрстуфхцчшщъыьэюя'),('Latin capitals','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),('Latin lowercase','abcdefghijklmnopqrstuvwxyz'),('Numerals','0123456789')]
with (P/'GLYPH-REVIEW-LEDGER.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['codepoint','glyph','group','base','status','next','approved'])
 for group,chars in alphabet:
  for ch in chars:w.writerow([f'U+{ord(ch):04X}',ch,group,'Inter 4.1 exact','BASELINE','Review З/з' if ch in 'Зз' else 'Individual optical review','NO'])
(P/'evidence').mkdir(exist_ok=True)
(P/'evidence/build-manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')

