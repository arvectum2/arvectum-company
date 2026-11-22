"""QA for identical branded carrier fixtures with font-only A/B."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from PIL import Image
import subprocess,json,hashlib
P=Path(__file__).resolve().parent.parent
R=P.parents[2]
m=json.loads((P/'evidence/source-manifest.json').read_text())
browser=json.loads((P/'evidence/browser-report.json').read_text())
diff=json.loads((P/'evidence/pixel-difference-report.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected={'B','uni0412','uni0432','uni0411','uni0431','uni0417','uni0437'}
def outline(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
report={'status':'PASS technical carrier QA, not visual or release approval',
 'case_control':'identical source HTML and branding, font face files only differ',
 'source_hashes':{},'fonts':{},'layout':{},'pixel_differences':diff,'open':[]}
for k,path in [('wordmark',m['original_wordmark']),
 ('tokens',m['reference_tokens']),('monogram',m['monogram_svg'])]:
 original=R/path;current=m['original_wordmark_sha256'] if k=='wordmark' else m['reference_tokens_sha256'] if k=='tokens' else m['monogram_sha256']
 assert sha(original)==current,(k,sha(original),current)
 report['source_hashes'][k]=current
assert sha(P/'assets/lockup_ru.svg')==m['original_wordmark_sha256']
assert sha(P/'assets/monogram_navy.svg')==m['monogram_sha256']
assert (P/'OFL-LICENSE.txt').read_bytes()==(R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.89/OFL-LICENSE.txt').read_bytes()
for carrier in ('letter','proposal','mobile'):
 src=R/m['cases'][carrier]['source']
 assert sha(src)==m['cases'][carrier]['source_sha256']
 a=(P/'cases'/carrier/'inter.html').read_text()
 b=(P/'cases'/carrier/'golden.html').read_text()
 assert a.replace('tokens-inter.css','tokens-ANY.css')==b.replace('tokens-golden.css','tokens-ANY.css'),carrier
 aa=browser[f'{carrier}-inter']['metrics'];bb=browser[f'{carrier}-golden']['metrics']
 assert aa['bodyText']==bb['bodyText'] and aa['height']==bb['height'] and aa['docWidth']==bb['docWidth'],(carrier,aa,bb)
 assert 'GSDisplay' in aa['families'] and 'GSText' in aa['families']
 assert 'GSDisplay' in bb['families'] and 'GSText' in bb['families']
 assert all(x['natural']>0 and x['loaded'] for x in aa['images']+bb['images'])
 if carrier=='mobile':assert aa['viewport']==bb['viewport']==390 and aa['docWidth']<=390
 report['layout'][carrier]={'body_characters':aa['bodyText'],'scrollheight':aa['height'],'docwidth':aa['docWidth'],'font_both_loaded':True,'logo_images_loaded':True}
for style in ('display','text'):
 orig=P/'fonts'/f'inter-{style}.woff2'
 cand=P/'fonts'/f'golden-{style}.woff2'
 for v in ('inter','golden'):
  x=P/'fonts'/f'{v}-{style}.woff2'
  assert sha(x)==m['fonts'][v][style]['webfont_sha256']
  upstream=R/m['fonts'][v][style]['src']
  assert sha(upstream)==m['fonts'][v][style]['source_sha256']
  s=TTFont(upstream);out=TTFont(x)
  assert s.getBestCmap()==out.getBestCmap() and s['hmtx'].metrics==out['hmtx'].metrics
  assert len(s.getGlyphOrder())==2937
  for n in s.getGlyphOrder():
   assert outline(s,n)==outline(out,n),(style,v,n)
 a=TTFont(orig);b=TTFont(cand)
 assert a.getBestCmap()==b.getBestCmap() and a['hmtx'].metrics==b['hmtx'].metrics
 changed={n for n in a.getGlyphOrder() if outline(a,n)!=outline(b,n)}
 assert changed==expected,(style,changed)
 report['fonts'][style]={'from_Inter_modified_glyph_count':len(changed),'modified_names':sorted(changed),'unchanged':2930,'cmap_positions':2852}
 print('FONT',style,'exactly seven modified glyphs, 2930 unchanged')
for case,n in [('letter',1),('proposal',2)]:
 for version in ('inter','golden'):
  info=subprocess.check_output(['pdfinfo',str(P/'proofs'/f'{case}-{version}.pdf')],text=True)
  assert f'Pages:           {n}' in info,(case,version,info)
  text=subprocess.check_output(['pdftotext',str(P/'proofs'/f'{case}-{version}.pdf'),'-'],text=True)
  assert 'Арвектум' in text and 'МАКЕТ' in text.upper() or 'ОБРАЗЕЦ' in text.upper()
for f,n in [('SIDE-BY-SIDE-REVIEW.pdf',4),('VECTOR-ORIGINALS-A4.pdf',6)]:
 info=subprocess.check_output(['pdfinfo',str(P/'proofs'/f)],text=True)
 assert f'Pages:           {n}' in info
for version in ('inter','golden'):
 im=Image.open(P/'proofs'/f'mobile-{version}.png')
 assert im.width==390 and im.height>1200
for k,v in diff.items():
 assert 0<v['pixel_change_pct_threshold12']<.5,(k,v)
report['open']=['Human optical/legibility evaluation not performed',
 'Chrome PDF uses subset Type3; no commercial print preflight',
 'Font release/rights and approved brand tokens remain out of scope']
(P/'evidence/qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS controls + layout + 6 vector document pages + mobile 390 px + 4-page review')
