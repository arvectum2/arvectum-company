"""Arvectum original constructivist Cyrillic Z/z: straight flats + local smooth quarter turns.
Three independent parametric optical variations, not derived from other fonts' outlines.
All geometric input derives from Arvectum source glyph metrics/anchors, no outlines copied.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from PIL import Image,ImageDraw,ImageFont
import math,json,hashlib
ROOT=Path(__file__).resolve().parent.parent
BASE=ROOT/'Arvectum-Typeface-v0.83/experimental/S';OUT=Path(__file__).resolve().parent
# radius share is expressed relative to available counterform height.
VARIANTS={
  'A':{'upper':0.28,'lower':0.21,'outer':0.18,'transition':0.16,'terminal':0.62,'label':'A · Structural'},
  'B':{'upper':0.42,'lower':0.34,'outer':0.31,'transition':0.30,'terminal':0.51,'label':'B · Balanced'},
  'C':{'upper':0.33,'lower':0.27,'outer':0.23,'transition':0.23,'terminal':0.57,'label':'C · Arvectum Main'},
}
K=4/3*(math.sqrt(2)-1) # quarter circle cubic handle factor

def M(p):return ('moveTo',(p,))
def L(p):return ('lineTo',(p,))
def C(p1,p2,p3):return ('curveTo',(p1,p2,p3))
Z=('closePath',())
def synth(st,ch,pr,source):
 f=TTFont(source);gs=f.getGlyphSet();n=f.getBestCmap()[ord(ch)];rec=RecordingPen();gs[n].draw(rec);op=rec.value
 assert len(op)==19, (st,ch,len(op))
 start=op[0][1][-1];inner_entry=op[1][1][-1]
 # Original bounding structure but newly authored straight/round sequence
 uCent=op[16][1][-1][0];upperOuterTop=op[16][1][-1][1]
 yUtop=op[2][1][-1][1];yUbottom=op[4][1][-1][1]
 xInnerUpper=op[3][1][-1][0];xOuterUpper=op[15][1][-1][0]
 xInsideLow=op[8][1][-1][0];xOuterLow=op[13][1][-1][0]
 yInsideLowTop=op[7][1][-1][1];yInsideLowBottom=op[9][1][-1][1]
 xInsideLowStart=op[7][1][-1][0];xInsideLowEnd=op[9][1][-1][0]
 outerBottom=op[12][1][-1][1];outerWaist=op[14][1][-1]
 xInsideUpperEnd=op[4][1][-1][0];xWaistUpperLeft=op[5][1][-1][0]
 xWaistLowerLeft=op[6][1][-1][0];bottomTerminal=op[10][1][-1];lowerLeft=op[11][1][-1]
 # Core sizing must not cause radii to intersect.
 up_h=yUtop-yUbottom;lo_h=yInsideLowTop-yInsideLowBottom
 ru=min(up_h*.49,up_h*pr['upper'])
 rl=min(lo_h*.46,lo_h*pr['lower'])
 o_up=min((upperOuterTop-outerWaist[1])*.37,(upperOuterTop-outerWaist[1])*pr['outer']*.85)
 o_low=min((outerWaist[1]-outerBottom)*.38,(outerWaist[1]-outerBottom)*pr['outer']*.9)
 # Outer lower cut must extend a meaningful horizontal bottom and top.
 waistx=outerWaist[0];waisty=outerWaist[1]
 lower_outer_right_top_y=waisty-0.035*(waisty-outerBottom)
 upper_outer_left_start_y=waisty
 upper_outer_start_y=waisty + 0.05*(upperOuterTop-waisty)
 o_upper_bottom=max(52, (upperOuterTop-waisty)*pr['transition']*.65)
 o_upper_top=max(60,(upperOuterTop-waisty)*pr['transition'])
 xup_start=uCent-pr['terminal']*(uCent-inner_entry[0])*.13
 xlower_inner_bottom=min(xInsideLowEnd,xInsideLow-rl-35)
 ops=[M(start),L(inner_entry),
      L((xup_start,yUtop)),L((xInnerUpper-ru,yUtop)),
      # horizontal right -> down, smoothly
      C((xInnerUpper-ru+K*ru,yUtop),(xInnerUpper,yUtop-ru+K*ru),(xInnerUpper,yUtop-ru)),
      L((xInnerUpper,yUbottom+ru)),
      C((xInnerUpper,yUbottom+ru-K*ru),(xInnerUpper-ru+K*ru,yUbottom),(xInnerUpper-ru,yUbottom)),
      L((xInsideUpperEnd,yUbottom)),
      L((xWaistUpperLeft,yUbottom)),L((xWaistLowerLeft,yInsideLowTop)),
      L((xInsideLowStart,yInsideLowTop)),L((xInsideLow-rl,yInsideLowTop)),
      C((xInsideLow-rl+K*rl,yInsideLowTop),(xInsideLow,yInsideLowTop-rl+K*rl),(xInsideLow,yInsideLowTop-rl)),
      L((xInsideLow,yInsideLowBottom+rl)),
      C((xInsideLow,yInsideLowBottom+rl-K*rl),(xInsideLow-rl+K*rl,yInsideLowBottom),(xInsideLow-rl,yInsideLowBottom)),
      L((xlower_inner_bottom,yInsideLowBottom)),L(bottomTerminal),L(lowerLeft)]
 # Lower outer: small local entry round to long baseline straight.
 lbcorner=min(115,(yInsideLowBottom-outerBottom)*pr['outer']*1.2)
 lbstart=(lowerLeft[0]+max(60,lbcorner*.75),outerBottom+max(10,lbcorner*.15))
 lbend=(lowerLeft[0]+max(135,lbcorner*1.7),outerBottom)
 ops.extend([C((lowerLeft[0]+lbcorner*.25,outerBottom+lbcorner*.42),(lbstart[0]-lbcorner*.15,lbend[1]),lbend),
             L((xOuterLow-o_low,outerBottom)),
             C((xOuterLow-o_low+K*o_low,outerBottom),(xOuterLow,outerBottom+o_low-K*o_low),(xOuterLow,outerBottom+o_low)),
             L((xOuterLow,lower_outer_right_top_y-o_low)),
             C((xOuterLow,lower_outer_right_top_y-o_low+K*o_low),(xOuterLow-o_low+K*o_low,lower_outer_right_top_y),(xOuterLow-o_low,lower_outer_right_top_y)),
             L((waistx,waisty)),
             # Avoid retracing on the waist: one ascending straight facet, not S wave
             L((xOuterUpper-o_upper_bottom,upper_outer_start_y)),
             C((xOuterUpper-o_upper_bottom+K*o_upper_bottom,upper_outer_start_y),
               (xOuterUpper,upper_outer_start_y+o_upper_bottom-K*o_upper_bottom),
               (xOuterUpper,upper_outer_start_y+o_upper_bottom)),
             L((xOuterUpper,upperOuterTop-o_upper_top)),
             C((xOuterUpper,upperOuterTop-o_upper_top+K*o_upper_top),
               (xOuterUpper-o_upper_top+K*o_upper_top,upperOuterTop),
               (xOuterUpper-o_upper_top,upperOuterTop)),
             L((uCent,upperOuterTop)),L(start),Z])
 r=RecordingPen();r.value=ops
 bb=BoundsPen(None);r.replay(bb)
 return r,bb.bounds

manifest={'kind':'experimental_new_original_Z_construction','baseline':'v0.83 S','variants':VARIANTS,'sources':{},'styles':{}}
for st,sub in (('Display','Medium'),('Text','Regular')):
 orig=next(BASE.glob(f'Arvectum{st}*.otf'))
 manifest['sources'][st]=hashlib.sha256(orig.read_bytes()).hexdigest()
 manifest['styles'][st]={}
 for variation,prop in VARIANTS.items():
  f=TTFont(orig);f.recalcTimestamp=False;td=f['CFF '].cff.topDictIndex[0];rows=[]
  for ch in 'Зз':
   pen,bounds=synth(st,ch,prop,orig)
   n=f.getBestCmap()[ord(ch)];width,lsb=f['hmtx'][n]
   t=T2CharStringPen(width,None);pen.replay(t)
   td.CharStrings[n]=t.getCharString(private=td.Private,globalSubrs=f['CFF '].cff.GlobalSubrs)
   svg=SVGPathPen(None);pen.replay(svg);x0,y0,x1,y1=bounds
   loc=OUT/'glyphs'/variation/st/f'U+{ord(ch):04X}.svg';loc.parent.mkdir(parents=True,exist_ok=True)
   loc.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.4f} {-y1:.4f} {x1-x0:.4f} {y1-y0:.4f}"><path fill="#001432" fill-rule="nonzero" transform="scale(1 -1)" d="{svg.getCommands()}"/></svg>')
   rows.append({'ch':ch,'bbox':bounds,'advance':width,'svg':str(loc.relative_to(OUT))})
  ps=f'Arvectum{st}GoldenStepArchitect{variation}Draft084-{sub}';family=f'Arvectum {st} Golden Step Architect {variation} Draft 084'
  for plat,enc,lang in ((3,1,1033),(1,0,0)):
   for nid,value in ((1,family),(3,ps+';0.84'),(4,family+' '+sub),(5,'Version 0.084'),(6,ps)):f['name'].setName(value,nid,plat,enc,lang)
  td.FamilyName=family;td.FullName=family+' '+sub;f['CFF '].cff.fontNames=[ps];f['head'].fontRevision=.084
  path=OUT/'experimental'/f'{st}-{variation}.otf';f.save(path)
  manifest['styles'][st][variation]={'otf':str(path.relative_to(OUT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'glyphs':rows}
  print(st,variation,'new original glyphs',rows)
(OUT/'evidence/build-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('READY',OUT)
