"""Kern-only typeface regression gate for existing Golden Step Mac drafts; never promotes fonts."""
from pathlib import Path
import argparse,ast,hashlib,json,subprocess,sys
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
P=Path(__file__).resolve().parent;ROOT=P.parent
def parse_var(path,key):
 tree=ast.parse(path.read_text())
 for n in tree.body:
  if isinstance(n,ast.Assign) and any(isinstance(v,ast.Name) and v.id==key for v in n.targets):
   return ast.literal_eval(n.value)
 raise KeyError(key)
prior=parse_var(ROOT/'Arvectum-Typeface-v0.53/kerning.py','pairs')
stage61=parse_var(ROOT/'Arvectum-Typeface-v0.61/kerning-candidate.py','ADDITIONS')
stage64=parse_var(ROOT/'Arvectum-Typeface-v0.64/kerning-candidate.py','PAIRS')
assert len(prior)==57 and len(stage61)==14 and len(stage64)==14
assert len(set(prior)|set(stage61)|set(stage64))==85
def glyph(p,font,name):
 pen=RecordingPen()
 font.getGlyphSet()[name].draw(pen)
 return pen.value
def digest(p):
 return hashlib.sha256(p.read_bytes()).hexdigest()
def shape(file,s,kern=True):
 out=subprocess.check_output(['hb-shape','--features=kern='+str(int(kern)),
      '--output-format=json',str(file),s],text=True)
 o=json.loads(out)
 if any(x['g']=='.notdef' for x in o):raise ValueError('Missing glyph for '+repr(s))
 return o
def check_style(st,version,expected):
 base=next((ROOT/'Arvectum-Typeface-v0.58/experimental').glob('Arvectum'+st+'*.otf'))
 path=next((ROOT/f'Arvectum-Typeface-v0.{version}/experimental').glob('Arvectum'+st+'*.otf'))
 ff=TTFont(path);old=TTFont(base)
 assert ff.getBestCmap()==old.getBestCmap() and len(ff.getBestCmap())==212,'Unicode coverage changed'
 for cp,n in old.getBestCmap().items():
  m=ff.getBestCmap()[cp]
  if glyph(path,old,n)!=glyph(path,ff,m):
   raise AssertionError('Contour differs: '+st+' U+'+format(cp,'04X'))
  if old['hmtx'][n]!=ff['hmtx'][m]:
   raise AssertionError('Advance/bearing differs: '+st+' U+'+format(cp,'04X'))
 for table in ('OS/2','hhea','GDEF'):
  if old[table].compile(old)!=ff[table].compile(ff):
   raise AssertionError(table+' changed relative to v0.58: '+st)
 assert set(x.FeatureTag for x in ff['GPOS'].table.FeatureList.FeatureRecord)=={'kern','mark','mkmk'}
 assert ff['CFF '].cff.fontNames==[ff['name'].getDebugName(6)]
 assert 'Inter Project Authors' in (ff['name'].getDebugName(0) or '')
 assert 'SIL Open Font License' in (ff['name'].getDebugName(13) or '')
 assert 'openfontlicense.org' in (ff['name'].getDebugName(14) or '')
 assert 'Inter Project Authors' in str(ff['CFF '].cff.topDictIndex[0].Notice)
 for flavor in ('woff','woff2'):
  w=path.with_suffix('.'+flavor)
  assert w.exists(),'missing '+str(w)
  loaded=TTFont(w)
  assert loaded.getBestCmap()==ff.getBestCmap() and loaded['hmtx'].metrics==ff['hmtx'].metrics
  assert set(x.FeatureTag for x in loaded['GPOS'].table.FeatureList.FeatureRecord)=={'kern','mark','mkmk'}
 zero=[ff['hmtx'][ff.getBestCmap()[ord(c)]][0] for c in '0123456789']
 assert len(set(zero))==1,'tabular figures lost'
 assert {c:ff['hmtx'][ff.getBestCmap()[ord(c)]][0] for c in (' ','\u00a0','\u202f')}=={
     ' ':512,'\u00a0':512,'\u202f':316}
 for pair,val in expected.items():
  a=sum(x['ax'] for x in shape(path,pair,True))
  b=sum(x['ax'] for x in shape(path,pair,False))
  assert a-b==val,(st,pair,a-b,val)
 for s in ('01','00','90','1\u202f250\u202f000,00 ₽','a\u0308\u0301','c\u0327\u0327',
            'Арвектум — Arvectum','№ 17/2026'):
  before=shape(base,s,True)
  after=shape(path,s,True)
  if s.startswith('01') or s in ('00','90','1\u202f250\u202f000,00 ₽','a\u0308\u0301','c\u0327\u0327','№ 17/2026'):
   assert before==after,('Control shaping changed',st,s)
 return dict(font=path.name,sha256=digest(path),style=st,
    codepoints=212,outlines_and_hmtx_unchanged=212,
    tables_unchanged=['OS/2','hhea','GDEF'],pairs_validated=len(expected),
    features=['kern','mark','mkmk'],tabular_figure_width=zero[0],
    space_advances={'space':512,'nbsp':512,'nnbsp':316},
    source_attribution_preserved=True,woff_roundtrip=True,woff2_roundtrip=True)
def main():
 parser=argparse.ArgumentParser()
 parser.add_argument('--candidate',type=int,required=True)
 parser.add_argument('--output',type=Path)
 opt=parser.parse_args()
 assert opt.candidate>=58
 expected=dict(prior)
 if opt.candidate>=61:expected.update(stage61)
 if opt.candidate>=64:expected.update(stage64)
 dest=opt.output or (P/'evidence'/f'gate-v0.{opt.candidate}.json')
 result=dict(candidate=f'v0.{opt.candidate}',baseline='v0.58',mode='kerning-only',
     status='NOT_RUN',styles={},expected_pairs=len(expected),
     production_approved=False,windows_device_test_performed=False)
 try:
  for style in ('Display','Text'):
   result['styles'][style]=check_style(style,opt.candidate,expected)
  result['status']='PASS_TECHNICAL_KERN_ONLY'
 except Exception as err:
  result['status']='BLOCKED_SCOPE_VIOLATION'
  result['reason']=str(err)
 dest.parent.mkdir(parents=True,exist_ok=True)
 dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(result['candidate'],result['status'],result.get('reason',''),result['expected_pairs'])
 return 0 if result['status'].startswith('PASS_') else 1
if __name__=='__main__':sys.exit(main())
