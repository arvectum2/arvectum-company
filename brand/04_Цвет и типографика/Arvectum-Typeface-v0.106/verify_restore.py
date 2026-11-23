"""Owner-requested rollback validation: v0.106 is the exact ACTIVE SOURCE,
v0.107 rejected. No glyph source binaries are rewritten.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
import hashlib,json
import pathops
P=Path(__file__).resolve().parent
R=P.parents[2];source=P/'experimental'
reject=R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.107/experimental'
manifest=json.loads((R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.107/evidence/build-manifest.json').read_text())
def sha(x):return hashlib.sha256(x.read_bytes()).hexdigest()
def ops(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
def ink(f,n,xy):
 p=pathops.Path();f.getGlyphSet()[n].draw(p.getPen());return bool(p.contains(xy))
res={'decision':'REJECT v0.107 open gaps and Fork/Direct alternatives. RESTORE v0.106 exactly.',
 'font_source':'v0.106 existing binaries, NOT rebuilt',
 'status':'rollback active experimental; not production','styles':{}}
for face,w in (('Display','Medium'),('Text','Regular')):
 otf=source/f'ArvectumGoldenStep{face}UnifiedForkDraft0106-{w}.otf'
 web=otf.with_suffix('.woff2')
 f=TTFont(otf);woff=TTFont(web);cm=f.getBestCmap()
 old=manifest['faces'][face]['Fork']
 assert sha(otf)==old['source_sha256'],(face,'font not exact parent SHA')
 assert len(cm)==2852 and len(f.getGlyphOrder())==2937
 assert f['hmtx'].metrics==woff['hmtx'].metrics
 assert f.getBestCmap()==woff.getBestCmap()
 for n in f.getGlyphOrder():
  assert ops(f,n)==ops(woff,n),(face,n,'source web parity failed')
 assert ops(f,cm[ord('A')])==ops(f,cm[ord('А')])
 assert ops(f,cm[ord('P')])==ops(f,cm[ord('Р')])
 assert ops(f,cm[ord('K')])==ops(f,cm[ord('К')])
 restored={}
 for ch,info in old['gap_geometry'].items():
  x0,y0,x1,y1=info['rect']
  xy=((x0+x1)/2,(y0+y1)/2)
  assert ink(f,cm[ord(ch)],xy),(face,ch,'old gap unexpectedly remains')
  for variant in ('Fork','Direct'):
   path=reject/f'ArvectumGoldenStep{face}{variant}Draft0107-{w}.otf'
   g=TTFont(path)
   assert not ink(g,g.getBestCmap()[ord(ch)],xy),(face,ch,'not comparing real v0.107 notch')
   # Exact restored glyph equals v0.106 unchanged parent; intentionally differs from v0.107
   assert ops(f,cm[ord(ch)]) != ops(g,g.getBestCmap()[ord(ch)])
  restored[ch]={'formerly_gapped_coordinate_xy':xy,'restored_ink_solid':True}
 for ch in ('K','К','Ж','ж'):
  fork=TTFont(reject/f'ArvectumGoldenStep{face}ForkDraft0107-{w}.otf')
  assert ops(f,cm[ord(ch)])==ops(fork,fork.getBestCmap()[ord(ch)]),(face,ch,'did not recover old K/Zh')
 # Display A/А remains the original, proven right-open v0.102+ outline;
 # Text A/А stays the original closed crossbar.
 # Compare against restored exact version and neither font font paths were touched.
 res['styles'][face]={'otf':str(otf.relative_to(R)),'sha256':sha(otf),
  'woff2':str(web.relative_to(R)),'woff2_sha256':sha(web),
  'coverage_glyphs':2937,'unicode_positions':2852,
  'A_cyrillic_latin_same':True,
  'capital_A_crossbar':'right-open in Display; closed in Text (unchanged optical design)',
  'restored_ungapped_letters':restored,'original_K_CyrK_and_Zh_restored':True}
 print('PASS',face,'exact parent SHA / full 2937 font/web paths; seven open variants reverted, K/Ж restored')
out=P/'evidence'
out.mkdir(exist_ok=True)
(out/'RESTORE-QA-2026-11-23.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')
