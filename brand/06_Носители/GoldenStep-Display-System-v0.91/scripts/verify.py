"""Verify both typography studies, source lineage, live browser outputs and clear scope."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from PIL import Image
import hashlib,json,subprocess
P=Path(__file__).resolve().parent.parent
R=P.parents[2]
manifest=json.loads((P/'evidence/source-manifest.json').read_text())
browser=json.loads((P/'evidence/browser-report.json').read_text())
system_browser=json.loads((P/'evidence/browser-system-report.json').read_text())
diff=json.loads((P/'evidence/pixel-difference-report.json').read_text())
system_diff=json.loads((P/'evidence/system-pixel-difference-report.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def ops(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
assert sha(R/manifest['approved_logo_source'])==manifest['approved_logo_sha256']
assert sha(P/'assets/lockup_ru.svg')==manifest['approved_logo_sha256']
assert sha(P/'assets/monogram_navy.svg')==manifest['monogram_sha256']
assert sha(R/manifest['token_source'])==manifest['token_source_sha256']
src_text=R/manifest['fonts']['inter-text']['source']
assert sha(src_text)==manifest['fonts']['inter-text']['source_sha256']
assert (P/'OFL-LICENSE.txt').read_bytes()==(R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.91/OFL-LICENSE.txt').read_bytes()
report={'technical_status':'PASS','approval_status':'experiment, owner design release pending',
        'font_only':{},'system_level':{},'fonts':{},'origins':manifest,'scope':'isolated design copies, no website or native templates'}
for key,spec in manifest['fonts'].items():
 src=R/spec['source'];dst=P/'fonts'/f'{key}.woff2'
 assert sha(src)==spec['source_sha256'] and sha(dst)==spec['output_sha256'],key
 a,b=TTFont(src),TTFont(dst)
 assert a.getBestCmap()==b.getBestCmap() and len(b.getBestCmap())==2852
 assert a['hmtx'].metrics==b['hmtx'].metrics
 assert len(a.getGlyphOrder())==len(b.getGlyphOrder())==2937
 assert all(ops(a,n)==ops(b,n) for n in a.getGlyphOrder())
 report['fonts'][key]={'num_glyphs':2937,'identical_source_outlines':True}
pure=TTFont(P/'fonts/inter-display.woff2')
trial=TTFont(P/'fonts/golden-display.woff2')
changed={n for n in pure.getGlyphOrder() if ops(pure,n)!=ops(trial,n)}
assert changed=={'A','uni0410','uni0417','uni0437','uni0412','uni0432','B','uni0411','uni0431'}
assert pure['hmtx'].metrics==trial['hmtx'].metrics
report['fonts']['golden_vs_inter']={'changed':sorted(changed),'unchanged':2937-len(changed)}
fontonly_css=(P/'tokens-inter.css').read_text()
golden_css=(P/'tokens-golden.css').read_text()
system_css=(P/'tokens-system.css').read_text()
assert fontonly_css.replace('fonts/inter-display.woff2','fonts/ANY-display.woff2')==golden_css.replace('fonts/golden-display.woff2','fonts/ANY-display.woff2')
assert golden_css==system_css
assert "fonts/inter-text.woff2" in fontonly_css and "fonts/inter-text.woff2" in golden_css and "fonts/inter-text.woff2" in system_css
for case in ('letter','proposal','mobile'):
 html={}
 for variant in ('inter','golden','system'):
  h=(P/'cases'/case/f'{variant}.html').read_text();html[variant]=h
 # Different fonts only for font-only A/B.
 assert html['inter'].replace('tokens-inter.css','tokens-ONE.css')==html['golden'].replace('tokens-golden.css','tokens-ONE.css'),case
 # Applied system: identical copy/images, one extra scoped heading CSS block.
 s=html['system'].replace('tokens-system.css','tokens-golden.css')
 assert '<style id="golden-display-composition">' in s
 begin=s.index('<style id="golden-display-composition">')
 end=s.index('</style>',begin)+len('</style>')
 assert s[:begin]+s[end:]==html['golden'],case
 for variant,stats in [('inter',browser[f'{case}-inter']['metrics']),
                       ('golden',browser[f'{case}-golden']['metrics']),
                       ('system',system_browser[f'{case}-system']['metrics'])]:
  assert stats['bodyText']==browser[f'{case}-inter']['metrics']['bodyText']
  assert 'GSDisplay' in stats['families'] and 'GSText' in stats['families']
  assert all(im['natural']>0 for im in stats['images'])
  if case=='mobile':
   assert stats['viewport']==stats['docWidth']==390,(case,variant,stats)
  assert stats['height']>=1800 if case=='mobile' else stats['height']>=1000
 if case in ('letter','proposal'):
  for variant in ('inter','golden','system'):
   pdf=P/'proofs'/f'{case}-{variant}.pdf'
   info=subprocess.check_output(['pdfinfo',str(pdf)],text=True)
   expected=1 if case=='letter' else 2
   assert f'Pages:           {expected}' in info,(case,variant)
 report['font_only'][case]={'identical_html_except_display_font':True,
    'same_height':browser[f'{case}-inter']['metrics']['height']==browser[f'{case}-golden']['metrics']['height']}
 report['system_level'][case]={'heading_style_addition_only':True,
    'height_baseline':browser[f'{case}-inter']['metrics']['height'],
    'height_system':system_browser[f'{case}-system']['metrics']['height']}
for k,v in diff.items():
 assert 0<v['pixel_change_pct_threshold12']<.5,(k,v)
for k,v in system_diff.items():
 assert 0<v['pixel_change_pct_threshold12']<30,(k,v)
for pdf,pages in [('SIDE-BY-SIDE-REVIEW.pdf',4),('SYSTEM-SIDE-BY-SIDE-REVIEW.pdf',4),
 ('VECTOR-ORIGINALS-A4.pdf',6),('SYSTEM-VECTOR-ORIGINALS-A4.pdf',6)]:
 info=subprocess.check_output(['pdfinfo',str(P/'proofs'/pdf)],text=True)
 assert f'Pages:           {pages}' in info,pdf
for variant in ('inter','golden','system'):
 im=Image.open(P/'proofs'/f'mobile-{variant}.png')
 assert im.width==390 and im.height>=1800
report['font_only_pixel_diff_full_image']=diff
report['applied_system_pixel_diff_full_image']=system_diff
report['open']=['Human design and legibility judgement', 'Official company brand release',
 'Commercial font licensing/attribution review', 'PDF/X printing preflight', 'Windows']
(P/'evidence/qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS 3 font WOFF2 2937 outlines each; 9 Display changes from Inter, Text exact Inter')
print('PASS 3 identical-case A/B pairs; system has heading CSS only, no extra copy changes')
print('PASS 4+4 review PDF pages and 6+6 A4 pages; 390px mobile no overflow')
print('FONT-ONLY', {k:v['pixel_change_pct_threshold12'] for k,v in diff.items()})
print('SYSTEM', {k:v['pixel_change_pct_threshold12'] for k,v in system_diff.items()})
