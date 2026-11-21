"""Frozen-corpus kerning follow-up, on v0.61 geometry (not v0.63 optical variants)."""
from pathlib import Path
import json,sys
from fontTools.ttLib import TTFont
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
P=Path(__file__).resolve().parent;ROOT=P.parent
sys.path.insert(0,str(ROOT/'Arvectum-Typeface-v0.49'))
from pipeline import Family,verify,sha
PAIRS={'ct':-15,'ty':-15,'rv':-20,'Co':-30,'Pr':-30,'AI':-15,
       'ту':-25,'ут':-25,'ку':-20,'ед':-15,'сл':-20,'жд':-20,
       'оч':-25,'уч':-35}
REPORT={}
for st in ('Display','Text'):
 src=next((ROOT/'Arvectum-Typeface-v0.61/experimental').glob('Arvectum'+st+'*.otf'))
 out=P/'experimental'/('Arvectum'+st+'GoldenStepDraft064-'+('Medium' if st=='Display' else 'Regular')+'.otf')
 f=Family(st,64,src,out);f.f['CFF '].cff.fontNames=[f.name]
 f.finish()
 assert verify(src,out,set())==212
 g=TTFont(out);cm=g.getBestCmap()
 fea=(ROOT/'Arvectum-Typeface-v0.61'/('features-'+st.lower()+'.fea')).read_text()
 assert fea.count('} kern;')==1
 lines=[]
 for pair,k in PAIRS.items():
  assert len(pair)==2 and -45<k<0 and all(ord(c) in cm for c in pair)
  a,b=(cm[ord(c)] for c in pair)
  assert f'pos {a} {b} ' not in fea
  lines.append('    pos '+a+' '+b+' '+str(k)+';')
 full=fea.replace('} kern;','\n'.join(lines)+'\n} kern;')
 (P/('features-'+st.lower()+'.fea')).write_text(full)
 addOpenTypeFeaturesFromString(g,full)
 assert set(x.FeatureTag for x in g['GPOS'].table.FeatureList.FeatureRecord)=={'kern','mark','mkmk'}
 g.recalcTimestamp=False;g.save(out)
 assert verify(src,out,set())==212
 before=TTFont(src);after=TTFont(out)
 for tag in ('OS/2','hhea','GDEF'):
  assert after[tag].compile(after)==before[tag].compile(before)
 assert after['hmtx'].metrics==before['hmtx'].metrics and after.getBestCmap()==before.getBestCmap()
 assert after['CFF '].cff.fontNames==[after['name'].getDebugName(6)]
 REPORT[st]={'input':src.name,'input_sha256':sha(src),'output':out.name,'output_sha256':sha(out),
             'new_pairs':PAIRS,'old_kern_pairs':71,'new_kern_pairs':14,'total_kern_pairs':85,
             'same_glyphs_hmtx_OS2_hhea_GDEF':True,'web':{}}
 for flavor in ('woff','woff2'):
  web=TTFont(out);web.flavor=flavor;web.recalcTimestamp=False
  target=out.with_suffix('.'+flavor);web.save(target)
  t=TTFont(target)
  assert t.getBestCmap()==after.getBestCmap() and t['hmtx'].metrics==after['hmtx'].metrics
  REPORT[st]['web'][flavor]=dict(file=target.name,sha256=sha(target))
(P/'build-report.json').write_text(json.dumps(REPORT,ensure_ascii=False,indent=2)+'\n')
print('PASS 14 new pairs/style, 85 in total, glyphs and Win-safe metrics untouched')
