"""Independent saved-font QA v0.112; nine W accent outlines, 20 mark anchors, 160 kerning pairs."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.pointPen import PointToSegmentPen
from fontTools.ufoLib.glifLib import readGlyphFromString
from fontTools.ttLib.tables.otBase import OTTableWriter
import uharfbuzz as hb
import hashlib,math,json,copy
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
W_VARIANTS=('Wcircumflex','Wgrave','Wacute','Wdieresis','uni1E86','uni1E88',
            'Wdieresis.ss07','uni1E86.ss07','uni1E88.ss07')
ALL_W=('W',)+W_VARIANTS
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def rec(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
def tab(t,f):
 w=OTTableWriter(tableTag='GPOS');t.compile(w,f);return w.getAllData()
def angles(f,n,minlen=130):
 path=rec(f,n);start=prior=None;out=[]
 for idx,(op,pts) in enumerate(path):
  if op=='moveTo':start=prior=pts[0]
  elif op in ('lineTo','closePath'):
   curr=pts[0] if op=='lineTo' else start
   dx=curr[0]-prior[0];dy=curr[1]-prior[1]
   if abs(dx)>20 and abs(dy)>20 and math.hypot(dx,dy)>minlen:
    out.append(math.degrees(math.atan2(abs(dy),abs(dx))))
   prior=curr
  elif op in ('curveTo','qCurveTo'):prior=pts[-1]
 return out
def shaped(f,word,features={'kern':True}):
 font=hb.Font(hb.Face(f.read_bytes()));font.scale=(2048,2048)
 buf=hb.Buffer();buf.add_str(word);buf.guess_segment_properties()
 hb.shape(font,buf,features)
 return [(g.codepoint,p.x_advance,p.x_offset,p.y_offset) for g,p in zip(buf.glyph_infos,buf.glyph_positions)]
q={'version':'0.112','engineering_working':True,'production':False,'owner_art_signoff':'OPEN',
 'preserved_owner_angles':{'W_alpha':69.0948425521,'X_CyrX_beta':58.2825255885},
 'masters':{}}
for face,x in m['masters'].items():
 source=R/x['source'];target=P/x['output']
 assert sha(source)==x['source_sha256'] and sha(target)==x['output_sha256']
 a,b=TTFont(source),TTFont(target)
 assert a.getGlyphOrder()==b.getGlyphOrder() and len(a.getGlyphOrder())==2937
 assert a.getBestCmap()==b.getBestCmap() and len(a.getBestCmap())==2852
 for t in ('cmap','hhea','OS/2','GSUB','GDEF'):
  assert a[t].compile(a)==b[t].compile(b),(face,t)
 changed={n for n in a.getGlyphOrder() if rec(a,n)!=rec(b,n)}
 assert changed==set(W_VARIANTS),(face,'changed contour scope',changed)
 assert rec(b,'W')==rec(a,'W') and rec(b,'X')==rec(b,'uni0425')
 changed_hmtx={n for n in a.getGlyphOrder() if a['hmtx'][n]!=b['hmtx'][n]}
 assert changed_hmtx==set(W_VARIANTS),(face,'advance changed too much',changed_hmtx)
 for n in W_VARIANTS:
  assert b['hmtx'][n][0]==b['hmtx']['W'][0] and b['hmtx'][n][1]==a['hmtx'][n][1]
  old,new=rec(a,n),rec(b,n)
  assert len(new)==len(old) and new[:20]==rec(b,'W')
  for (op1,points1),(op2,points2) in zip(old[20:],new[20:]):
   assert op1==op2
   assert len(points1)==len(points2)
   for (u,v),(xx,yy) in zip(points1,points2):
    assert abs((xx-u)-x['accent_shift_x_UPM'])<.00001,(face,n,'accent moved wrong X')
    assert abs(yy-v)<.00001,(face,n,'accent moved wrong Y')
 for glyph in ('W','X','uni0425')+W_VARIANTS:
  name=f'{glyph}-{face}.glif'
  pp=P/'source-glyphs'/name
  p=RecordingPen();readGlyphFromString(pp.read_text(),pointPen=PointToSegmentPen(p))
  assert p.value==rec(b,glyph),(face,'GLIF/source divergence',glyph)
 assert len(angles(b,'W'))==8 and max(abs(deg-q['preserved_owner_angles']['W_alpha']) for deg in angles(b,'W'))<.00001
 for glyph in ('X','uni0425'):
  aa=angles(b,glyph)
  assert len(aa)==8 and max(abs(deg-q['preserved_owner_angles']['X_CyrX_beta']) for deg in aa)<.00001
 # Differential rollback of GPOS mark + last kern lookup must restore exactly original GPOS.
 rollback=TTFont(target)
 k=rollback['GPOS'].table.LookupList.Lookup
 src_lookup=a['GPOS'].table.LookupList.Lookup
 assert len(k)==len(src_lookup)==11
 last=k[-1].SubTable[0]
 assert last.Format==1 and last.PairSetCount==len(last.Coverage.glyphs)
 count=sum(len(p.PairValueRecord) for p in last.PairSet)
 assert count==160,(face,'expected 10x16 pair overlay',count)
 oldlast=src_lookup[-1].SubTable[0]
 before={(left,pr.SecondGlyph):pr.Value1.XAdvance for left,set_ in zip(oldlast.Coverage.glyphs,oldlast.PairSet)
        for pr in set_.PairValueRecord}
 after={(left,pr.SecondGlyph):pr.Value1.XAdvance for left,set_ in zip(last.Coverage.glyphs,last.PairSet)
        for pr in set_.PairValueRecord}
 assert len(before)==16 and all(after[pair]==value for pair,value in before.items())
 for (left,right),value in before.items():
  for v in W_VARIANTS:
   pair=(v,right) if left=='W' else (left,v)
   assert after[pair]==value,(face,pair,'variant kerning absent')
 k[-1]=copy.deepcopy(src_lookup[-1])
 mark_updated=0
 for ix,lk in enumerate(k):
  if lk.LookupType!=4:continue
  for sub in lk.SubTable:
   cov=getattr(getattr(sub,'BaseCoverage',None),'glyphs',[])
   if not cov:continue
   for name in ALL_W:
    if name not in cov:continue
    n=cov.index(name)
    for ank in sub.BaseArray.BaseRecord[n].BaseAnchor:
     if ank is None:continue
     assert ank.XCoordinate==x['alpha_W_center_UPM'],(face,'wrong new anchor',name,ank.XCoordinate)
     ank.XCoordinate-=x['accent_shift_x_UPM']
     assert ank.XCoordinate==x['source_center_UPM']
     mark_updated+=1
 assert mark_updated==20,(face,mark_updated)
 assert a['GPOS'].compile(a)==rollback['GPOS'].compile(rollback),(face,'unscoped GPOS mutation')
 # HarfBuzz: W+combining mark must shift by exactly new W center, retaining vertical placement.
 for example in ('W\u0304','W\u0306'):
  bef,aft=shaped(source,example),shaped(target,example)
  assert len(bef)==len(aft)==2,(face,example)
  assert aft[1][2]-bef[1][2]==x['accent_shift_x_UPM'],(face,'mark x positioning',example,bef,aft)
  assert aft[1][3]==bef[1][3]
 for base,code in [('Wacute','Ẃ'),('Wcircumflex','Ŵ'),('Wdieresis','Ẅ'),
                   ('Wgrave','Ẁ'),('uni1E86','Ẇ'),('uni1E88','Ẉ')]:
  assert b.getBestCmap()[ord(code)]==base
  assert shaped(target,code)[0][1]==b['hmtx']['W'][0],(face,code)
 for example in ('WA','AW','WO','OW','WT','WV','WY','WX','WW','XХ','АРВЕКТУМ'):
  assert shaped(source,example)==shaped(target,example),(face,'unintended shape regression',example)
 for code,other in [('Ẃ','A'),('Ŵ','O'),('Ẅ','E'),('Ẁ','N'),('Ẇ','L')]:
  oldshape,newshape=shaped(source,code+other),shaped(target,code+other)
  assert len(oldshape)==len(newshape)==2
  assert newshape[0][1]-oldshape[0][1]==(b['hmtx']['W'][0]-a['hmtx'][b.getBestCmap()[ord(code)]][0])+before[('W',other)]
 q['masters'][face]={
  'only_modified_glyphs':list(W_VARIANTS),'unchanged_glyphs':2937-len(W_VARIANTS),
  'new_advance':b['hmtx']['W'][0],'shift_UPM':x['accent_shift_x_UPM'],
  'mark_anchor_records_updated':mark_updated,
  'same_original_GPOS_except_scoped_mark_kern_changes':True,
  'old_pair_records':16,'new_pair_records':160,
  'full_GLIF_saved_CFF_roundtrip':True,
  'W_alpha_8_of_8':True,'X_CyrX_beta_8_of_8':True}
 print('PASS',face,'9 W accents exact α base; 20 anchor records; 160 scoped kerning pairs; others unchanged')
(P/'evidence/qa-report.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
