"""Opt-in-free build of deliberately isolated *NOT FOR INSTALL* fsType metadata variants.
No font name, glyph, GPOS, GDEF, OS/2 metrics or original OTF is changed.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
import hashlib,json
P=Path(__file__).resolve().parent;ROOT=P.parent;OUT=P/'experimental'
def digest(x):return hashlib.sha256(Path(x).read_bytes()).hexdigest()
report={}
for sty in ('Display','Text'):
 source=next((ROOT/'Arvectum-Typeface-v0.64/experimental').glob('Arvectum'+sty+'*.otf'))
 f=TTFont(source)
 assert f['OS/2'].fsType==4
 f['OS/2'].fsType=0
 f.recalcTimestamp=False
 target=OUT/(source.stem+'-fsType0-TEST-ONLY.otf')
 f.save(target)
 old=TTFont(source);new=TTFont(target)
 assert new['OS/2'].fsType==0 and old['OS/2'].fsType==4
 assert old.getBestCmap()==new.getBestCmap() and len(new.getBestCmap())==212
 assert old['hmtx'].metrics==new['hmtx'].metrics
 # Metadata-only change MUST preserve exact base source names; do not install concurrently.
 assert old['name'].compile(old)==new['name'].compile(new)
 for t in ('CFF ','GPOS','GDEF','hhea','cmap','name'):
  assert old[t].compile(old)==new[t].compile(new),(sty,t)
 # Compare compiled OS/2 payload after reverting the *test object* flag.
 # This proves the only semantic OS/2 change is fsType, despite identity-different Panose objects.
 new['OS/2'].fsType=4
 assert old['OS/2'].compile(old)==new['OS/2'].compile(new)
 new['OS/2'].fsType=0
 for cp,n in old.getBestCmap().items():
  p=RecordingPen();q=RecordingPen()
  old.getGlyphSet()[n].draw(p);new.getGlyphSet()[n].draw(q)
  assert p.value==q.value,(sty,cp)
 report[sty]=dict(source=source.name,source_sha256=digest(source),probe=target.name,
  probe_sha256=digest(target),fsType_before=4,fsType_after=0,
  outlines_unchanged=212,metrics_and_GPOS_GDEF_unchanged=True,
  family_name_unchanged_collision_if_installed_together=True,
  actual_Windows_or_Word_embedded_editing_untested=True)
(P/'evidence/embedding-probe.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS fsType0 metadata-only OTF test binaries, two styles; NO user installation or release')
