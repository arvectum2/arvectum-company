"""Golden Step v0.80: repair inherited Cyrillic б shoulder with C1/G1 and G2 continuity.
Source exact v0.79 glyph; preserve positions, other contours, all font tables.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import math,json,hashlib
P=Path(__file__).resolve().parent;SRC=P.parent/'Arvectum-Typeface-v0.79/experimental'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
report={'status':'experimental_not_approved','source_version':'v0.79','selection':'B_G2 based on prototypes old,A,A_G2,B,B_G2,C,C_G2',
 'adjustment_only':'U+0431 Cyrillic lowercase б','styles':{}}
for sty,sub in (('Display','Medium'),('Text','Regular')):
 source=SRC/f'Arvectum{sty}GoldenStepDraft079-{sub}.otf'
 f=TTFont(source);n=f.getBestCmap()[0x0431];pen=RecordingPen();f.getGlyphSet()[n].draw(pen)
 raw=list(pen.value)
 assert len(raw)==17 and raw[4][0]=='curveTo' and raw[5][0]=='curveTo'
 original_joint=raw[4][1][-1]
 j=(original_joint[0],975)
 u=(-45.,65.)
 first=raw[4][1][0];last=raw[5][1][1]
 # Equality of signed curvature at the join for cubics sharing tangent u:
 # alpha^2 = cross(u,P2_next - J) / cross(u,P1_prev - J).
 numerator=cross(u,(last[0]-j[0],last[1]-j[1]))
 denominator=cross(u,(first[0]-j[0],first[1]-j[1]))
 assert numerator*denominator>0
 alpha=math.sqrt(numerator/denominator)
 before_control=(j[0]-u[0],j[1]-u[1]);after_control=(j[0]+alpha*u[0],j[1]+alpha*u[1])
 old4=raw[4][1];old5=raw[5][1]
 raw[4]=('curveTo',(old4[0],before_control,j))
 raw[5]=('curveTo',(after_control,old5[1],old5[2]))
 new=RecordingPen();new.value=raw
 b=BoundsPen(None);new.replay(b);xmin,ymin,xmax,ymax=b.bounds
 assert abs(xmin-f['hmtx'][n][1])<1 and xmax<f['hmtx'][n][0],(sty,b.bounds)
 sv=SVGPathPen(None);new.replay(sv)
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{xmin:.4f} {-ymax:.4f} {xmax-xmin:.4f} {ymax-ymin:.4f}"><title>Golden Step v0.80 {sty} U+0431 G2 rounded shoulder</title><path fill="#001432" fill-rule="nonzero" transform="scale(1 -1)" d="{sv.getCommands()}"/></svg>\n'
 out=P/'glyphs'/sty/'U+0431.svg';out.write_text(svg)
 report['styles'][sty]={'source_file':source.name,'source_sha256':sha(source),'source_advance':f['hmtx'][n][0],
 'source_lsb':f['hmtx'][n][1],'original_joint':original_joint,'candidate_joint':j,
 'incoming_second_control':before_control,'outgoing_first_control':after_control,'curvature_handle_scale':alpha,
 'bbox':b.bounds,'original_curve_commands':len(pen.value),'candidate_curve_commands':len(new.value),
 'glyph_svg_sha256':sha(out)}
 print(sty,'source metrics',f['hmtx'][n],'G2 joint',j,'alpha',round(alpha,6),'SVG',out.name)
(P/'evidence/sculpt-geometry.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
