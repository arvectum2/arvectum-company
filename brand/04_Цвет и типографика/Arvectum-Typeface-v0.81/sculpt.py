"""Golden Step v0.81 — natural numeric 3 with smooth narrow inside waist.
Source-exact CFF v0.80; keep original outside numeral bowl and all Cyrillic З/з.
Selected from 10 sampled non-crossing optical candidates; trial, no owner approval.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import json,hashlib
P=Path(__file__).resolve().parent;SRC=P.parent/'Arvectum-Typeface-v0.80/experimental'
sha=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
report={'base':'v0.80','approved':False,'target':'U+0033','design':'G1 smooth inner-waist only, original external numeral contours',
 'reference_untouched':['U+0417','U+0437','U+0440','U+0435','U+0070','U+0065'],
 'tested_variants':['old','inner480','inner505','inner530','inner550','inner575','S_outer_I510','S_outer_I540','S_outer_I560','S_outer_I580'],
 'selected':'inner575','styles':{}}
for st,sub in (('Display','Medium'),('Text','Regular')):
 old=SRC/f'Arvectum{st}GoldenStepDraft080-{sub}.otf';f=TTFont(old);g=f.getGlyphSet();name=f.getBestCmap()[0x33]
 rec=RecordingPen();g[name].draw(rec);ops=list(rec.value)
 assert len(ops)==19 and all(ops[i][0]=='lineTo' for i in (5,6,7))
 start=ops[4][1][-1];finish=ops[7][1][-1]
 ix=575 if st=='Display' else 554
 inside_y=921
 # Cubics share a downward vertical tangent at x=ix. There is no rectangular
 # horizontal bar as on the Cyrillic З. No external bowl changes and no overlaps.
 enter=('curveTo',((start[0]-45,start[1]),(ix,983),(ix,inside_y)))
 leave=('curveTo',((ix,851),(finish[0]-80,finish[1]),finish))
 ops=ops[:5]+[enter,leave]+ops[8:]
 new=RecordingPen();new.value=ops
 bboxpen=BoundsPen(None);new.replay(bboxpen);bbox=bboxpen.bounds
 oldbp=BoundsPen(g);g[name].draw(oldbp)
 assert bbox==oldbp.bounds,(st,bbox,oldbp.bounds)
 assert all(rec.value[j]==new.value[j-1] for j in range(8,19))
 pen=SVGPathPen(None);new.replay(pen);x0,y0,x1,y1=bbox
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.4f} {-y1:.4f} {x1-x0:.4f} {y1-y0:.4f}"><title>Golden Step v0.81 {st} U+0033 smooth inside waist</title><path fill="#001432" fill-rule="nonzero" transform="scale(1 -1)" d="{pen.getCommands()}"/></svg>\n'
 path=P/'glyphs'/st/'U+0033.svg';path.write_text(svg)
 report['styles'][st]={'source_otf':old.name,'source_sha256':sha(old),'source_advance':f['hmtx'][name][0],
  'source_lsb':f['hmtx'][name][1],'bbox':bbox,'candidate_svg_sha256':sha(path),
  'old_commands':len(rec.value),'new_commands':len(new.value),'inner_waist':(ix,inside_y),
  'outer_bowl_unchanged':True}
 print(st,'numeric 3',len(ops),'ops','inner waist',(ix,inside_y),'no outer changes')
(P/'evidence/sculpt.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
