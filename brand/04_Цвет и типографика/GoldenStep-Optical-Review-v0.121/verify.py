"""Independent cross-check of the constrained optical/financial/native QA artifact."""
from pathlib import Path
import json,hashlib,subprocess
from fontTools.ttLib import TTFont
P=Path(__file__).resolve().parent;ROOT=P.parent/'Arvectum-Typeface-v0.121'
origins=json.loads((P/'evidence/input-fonts.json').read_text())
assert origins['source_commit'].startswith('3098566')
for e in origins['font_sources'].values():
 q=P.parents[2]/e['path']
 assert hashlib.sha256(q.read_bytes()).hexdigest()==e['sha256']
a=json.loads((P/'evidence/measurements.json').read_text())
b=json.loads((P/'evidence/browser-qa.json').read_text())
c=json.loads((P/'evidence/coretext-qa.json').read_text())
assert a['font']=='v0.121' and set(a['faces'])=={'Display','Text'}
for face,weight in [('Display','Medium'),('Text','Regular')]:
 fpath=ROOT/'otf'/f'ArvectumGoldenStep{face}PhraseRhythmWorking0121-{weight}.otf'
 font=TTFont(fpath);assert len(font.getGlyphOrder())==2937 and len(font.getBestCmap())==2852
 m=a['faces'][face]
 assert 1.25 < m['ratio_W_over_M'] <1.32
 assert m['default_digits_have_variable_widths']
 assert len(m['pairs_gap_px'])==12 and all(gap>0 for gap in m['pairs_gap_px'].values())
 assert m['pairs_gap_px']['WĄ']==m['pairs_gap_px']['WA']==m['pairs_gap_px']['WÁ']
 assert m['pairs_gap_px']['MĄ']==m['pairs_gap_px']['MA']
 assert m['A_bounds'][1]==0 and m['Aogonek_bounds'][1] < -300
 for s,d in m['finance'].items():
  assert len(d['tnum']['digit_advances_upm'])>=5
  assert set(d['tnum']['digit_advances_upm'])=={1320}
 assert (P/'proofs'/f'{face}-Aogonek-WAM-12-76px.png').stat().st_size>30000
 print('PASS GLYPH/FEATURE',face,'12 non-colliding sample pairs, Aogonek descent and tabular digits')
assert set(b)=={'390','768','1440'}
for width,entry in b.items():
 met=entry['metrics']
 assert met['vw']==met['docWidth']==int(width)
 assert {'ArvectumTextAudit','ArvectumDisplayAudit'}<=set(met['loaded'])
 assert met['bodyLen']==next(iter(b.values()))['metrics']['bodyLen']
 assert abs(met['default888']-met['default111'])>40
 assert abs(met['table888']-met['table111'])<0.01
 assert all(met['sampleLetters'])
 assert all(p['width']<=p['clientWidth']+1 for p in met['pages'])
 assert (P/'proofs'/f'finance-optical-{width}px.png').stat().st_size>20000
 print('PASS CHROME',width,'correct font loads, numeric features and no overflow')
assert len(c['masters'])==2
for t in c['masters']:
 assert t['mapped_required_unicode']==13 and len(t['checked_lines'])==5
 assert '0121' in t['postscript_name']
 assert all(x['glyph_count']>0 and x['width_pt']>0 for x in t['checked_lines'])
assert 'Pages:           2' in subprocess.check_output(['pdfinfo',str(P/'proofs/GoldenStep-v0121-Financial-and-Optical-Review.pdf')],text=True)
assert 'Pages:           1' in subprocess.check_output(['pdfinfo',str(P/'proofs/NativeCoreText-v0121-proof.pdf')],text=True)
chrome_fonts=subprocess.check_output(['pdffonts',str(P/'proofs/GoldenStep-v0121-Financial-and-Optical-Review.pdf')],text=True)
quartz_fonts=subprocess.check_output(['pdffonts',str(P/'proofs/NativeCoreText-v0121-proof.pdf')],text=True)
assert 'Type 3' in chrome_fonts and 'Type 1C' in quartz_fonts
assert all((P/'proofs'/q).stat().st_size>35000 for q in ('review-a4-1.jpg','review-a4-2.jpg','native-coretext-page-1.jpg'))
print('PASS NATIVE+PDF','CoreText loaded two actual OTF, 1-page Quartz Type 1C and 2-page Chrome Type 3 classified separately')
manifest=P/'SHA256SUMS.txt'
if manifest.exists():
 for entry in manifest.read_text().splitlines():
  expected,rel=entry.split('  ',1)
  assert hashlib.sha256((P/rel).read_bytes()).hexdigest()==expected,rel
 print('PASS IMMUTABLE REVIEW SHA256',len(manifest.read_text().splitlines()),'files')
