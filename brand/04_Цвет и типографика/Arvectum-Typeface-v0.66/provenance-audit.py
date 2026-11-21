"""Trace original licensed Inter sources and glyph-level source/metadata evidence."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
import json,csv,hashlib,shutil,collections
P=Path(__file__).resolve().parent;ROOT=P.parent
src=ROOT/'Arvectum-Typeface-v0.36/sources'
prov=json.loads((src/'provenance.json').read_text())
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
for name,meta in prov['files'].items():
    path=src/name
    assert path.is_file() and sha(path)==meta['sha256'],('Original Inter file missing or modified',name)
license_source=src/'LICENSE.txt'
license_text=license_source.read_text()
assert license_text.startswith('Copyright (c) 2016 The Inter Project Authors')
assert 'SIL OPEN FONT LICENSE Version 1.1' in license_text
assert 'nor any of its individual components' in license_text
assert 'must not be distributed under any other license' in ' '.join(license_text.split())
shutil.copy2(license_source,P/'internal-kit/LICENSE.txt')
original_provenance=list(csv.DictReader((ROOT/'Arvectum-Typeface-v0.47/glyph-provenance.csv').open()))
known={ (r['style'],int(r['unicode'][2:],16)):r for r in original_provenance}
assert len(known)==364
chain=(36,37,38,39,40,41,42,43,44,45,46,47,49,50,51,52,53,54,55,56,57,58,61,64)
results={}
rows=[]
for style in ('Display','Text'):
  typeface={}
  for rev in chain:
    files=list((ROOT/f'Arvectum-Typeface-v0.{rev}/experimental').glob(f'Arvectum{style}*.otf'))
    if len(files)!=1:
      raise RuntimeError(f'Unexpected source for v0.{rev} {style}: {files}')
    path=files[0];f=TTFont(path)
    outlines={}
    for cp,name in f.getBestCmap().items():
      pen=RecordingPen();f.getGlyphSet()[name].draw(pen)
      outlines[cp]=hashlib.sha256(repr(pen.value).encode()).hexdigest()
    typeface[rev]={'path':path,'sha256':sha(path),'font':f,'outlines':outlines}
  current=typeface[64];f=current['font']
  assert len(f.getBestCmap())==212
  id0=f['name'].getDebugName(0) or ''
  id13=f['name'].getDebugName(13) or ''
  id14=f['name'].getDebugName(14) or ''
  cff=f['CFF '].cff.topDictIndex[0]
  assert 'Inter Project Authors' in id0 and 'OFL 1.1' in id0
  assert 'SIL Open Font License' in id13 and 'openfontlicense.org' in id14
  assert 'Inter Project Authors' in (cff.Notice or '')
  assert 'Arvectum' in (f['name'].getDebugName(1) or '')
  assert 'Inter' not in (f['name'].getDebugName(1) or '')
  # Exact contour match to licensed Inter does NOT measure derivative rights;
  # blank space outlines can be bytewise identical by design.
  licensed=TTFont(src/('InterDisplay-Medium.otf' if style=='Display' else 'InterDisplay-Regular.otf'))
  exact_source=[]
  for cp,name in f.getBestCmap().items():
    nm=licensed.getBestCmap().get(cp)
    if nm is None:continue
    lhs=RecordingPen();rhs=RecordingPen()
    licensed.getGlyphSet()[nm].draw(lhs);f.getGlyphSet()[name].draw(rhs)
    if lhs.value==rhs.value:exact_source.append(f'U+{cp:04X}')
  assert exact_source==['U+0020','U+00A0','U+202F'],(style,exact_source)
  summary={'revisions_in_chain':[f'v0.{i}' for i in chain],
    'historical_font_source_sha256':{f'v0.{rev}':data['sha256'] for rev,data in typeface.items()},
    'current_codepoints':len(current['outlines']), 'name_copyright':id0, 'name_license':id13,'name_license_url':id14,
    'CFF_notice':cff.Notice,'vendor_id':f['OS/2'].achVendID,
    'metadata_missing_manufacturer_ID8':f['name'].getDebugName(8) is None,
    'metadata_missing_designer_ID9':f['name'].getDebugName(9) is None,
    'source_is_derived_OFL_not_proven_exclusive_original':True,
    'exact_Inter_source_contour_codepoints':exact_source,
    'only_three_identical_empty_space_contours':True}
  found=collections.Counter()
  for cp,name in f.getBestCmap().items():
    fingerprint=current['outlines'][cp]
    matching=[rev for rev in chain if typeface[rev]['outlines'].get(cp)==fingerprint]
    assert matching and matching[-1]==64
    first=matching[0]
    origin=known.get((style,cp))
    rows.append(dict(style=style,codepoint=f'U+{cp:04X}',char=chr(cp),glyph_name=name,
      advance=f['hmtx'][name][0],outline_sha256=fingerprint,earliest_matching_version=f'v0.{first}',
      v047_source_origin=(origin['origin'] if origin else 'post_v047_added_or_changed'),
      v047_source_version=(origin['source_version'] if origin else ''),
      independent_originality_not_proven=True))
    found[f'v0.{first}']+=1
  summary['earliest_matching_outline_counts']=dict(sorted(found.items()))
  results[style]=summary
with (P/'evidence/glyph-outline-provenance.csv').open('w',newline='') as out:
 writer=csv.DictWriter(out,fieldnames=list(rows[0]),lineterminator='\n')
 writer.writeheader();writer.writerows(rows)
(P/'evidence/licensing-and-source-audit.json').write_text(json.dumps({
 'source_release':prov['release'],'source_url':prov['url'],'original_archive_sha256_documented':prov['archive_sha256'],
 'source_files_sha256_verified':{name:sha(src/name) for name in prov['files']},
 'license_sha256':sha(license_source),'styles':results,'glyph_rows':len(rows),
 'readiness':'INTERNAL_REVIEW_ONLY, NOT LEGAL CERTIFICATION',
 'rights_limitations':['OFL applies to derived font regardless of modified outlines',
                       'No claim of exclusive authorship of every glyph',
                       'Some historical original Arvectum ZIP archives are not recovered',
                       'Need authorized owner sign-off on public font naming and notices',
                       'Full license must accompany distributed font copy',
                       'No Reserved Font Name is explicitly listed after the copyright statement of bundled LICENSE; trademark/name review still open']},ensure_ascii=False,indent=2)+'\n')
print('PASS bundled source OFL, exact source hashes, 424 current glyph lineage rows, font license metadata')
for st in results:print(st,results[st]['earliest_matching_outline_counts'])
