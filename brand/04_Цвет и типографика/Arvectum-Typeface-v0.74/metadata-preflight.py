"""OFL font release diagnostic, no source font modifications or external deployment."""
from pathlib import Path
from fontTools.ttLib import TTFont
import hashlib,json
P=Path(__file__).resolve().parent;BASE=P.parent/'Arvectum-Typeface-v0.64/experimental'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
result={'status':'RELEASE_GATES_OPEN','input':'Golden Step v0.64 experimental OTF',
'fsType_spec':'https://learn.microsoft.com/typography/opentype/spec/os2',
'license_source':'v0.36/sources/LICENSE.txt, exact source release Inter 4.1',
'ofl_faq':'https://openfontlicense.org/ofl-faq/',
'font_software_rights':'Derived Inter SIL OFL 1.1; no exclusive proprietary font software claim',
'styles':{},'required_decisions':[]}
for style in ('Display','Text'):
 source=next(BASE.glob('Arvectum'+style+'*.otf'))
 f=TTFont(source)
 cmap=f.getBestCmap()
 names={str(i):f['name'].getDebugName(i) for i in (0,1,2,3,4,5,6,8,9,11,13,14,16,17)}
 assert len(cmap)==212 and names['0'] and 'Inter Project Authors' in names['0']
 assert names['13'] and 'SIL Open Font License' in names['13']
 assert names['14'] and 'openfontlicense.org' in names['14']
 assert f['CFF '].cff.topDictIndex[0].Notice
 width=len(names['1'])
 assert width>31
 embedding=f['OS/2'].fsType
 assert embedding==4,(style,embedding)
 m=dict(source=source.name,source_sha256=sha(source),font_family=names['1'],family_chars=width,
  legacy_GDI_family_name_length_over_31=width>31,PostScriptName=names['6'],
  name_ids=names,cff_notice=str(f['CFF '].cff.topDictIndex[0].Notice),
  vendor_id=f['OS/2'].achVendID,fsType_raw=embedding,fsType_meaning='Preview & Print only',
  codepoints=len(cmap),gpos=[r.FeatureTag for r in f['GPOS'].table.FeatureList.FeatureRecord],
  embedding_permissions_candidate='fsType 0 requested for separate technical test, not legal signoff',
  manufacturer_name_missing=not names['8'],designer_name_missing=not names['9'],
  typeface_family_ID16_missing=not names['16'],typeface_style_ID17_missing=not names['17'])
 assert all(x in m['gpos'] for x in ('kern','mark','mkmk'))
 result['styles'][style]=m
result['required_decisions']=[
 'Owner approve final glyphs, kerning, font naming and brand use',
 'Legal/licensing review of SIL OFL 1.1 derivative and copyright attribution',
 'Resolve actual rights/attribution for manufacturer ID8 and designer ID9; do not invent',
 'Evaluate embedding fsType 0 in controlled editable office documents before public release',
 'Maintain separate temporary test names to avoid installed font cache collisions',
 'Resolve 38/35-character GDI family names later in deferred Windows qualification',
 'Review legal trademark/name and distribution jurisdiction/technology sovereignty',
 'Do not publish or sign a release before reserved owner approval']
(P/'evidence/metadata-preflight.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('PREFLIGHT: fsType=4 both; long family names, missing manufacturer/designer IDs; licensed OFL attribution found')
