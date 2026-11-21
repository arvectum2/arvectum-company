"""Exact path-line segment audit of phi angle; CFF cubic curves not classified."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from PIL import Image,ImageDraw,ImageFont
import math,json,statistics,numpy as np
P=Path(__file__).resolve().parent;ROOT=P.parent
phi=(1+math.sqrt(5))/2
target=math.degrees(math.atan(phi))
rev=64
focus='АVМЛДлджКxУКXWЗ3'
MIN_LENGTH=280
def segments(path):
  p=RecordingPen();f.getGlyphSet()[f.getBestCmap()[ord(path)]].draw(p)
  p0=None;pt=None;out=[]
  def line(x,y,closed=False):
    nonlocal pt
    if pt is None:return
    dx=x-pt[0];dy=y-pt[1];n=math.hypot(dx,dy)
    angle=math.degrees(math.atan2(abs(dy),abs(dx))) if n else 0
    if n>=MIN_LENGTH and 5<angle<85:
      out.append(dict(angle=round(angle,4),length=round(n,4),
                      start=[round(v,4) for v in pt],end=[round(x,4),round(y,4)],
                      implicit_close=closed))
    pt=(x,y)
  for op,args in p.value:
    if op=='moveTo':pt=p0=args[0]
    elif op=='lineTo':line(*args[0])
    elif op=='curveTo':pt=args[-1]
    elif op=='qCurveTo':pt=args[-1]
    elif op=='closePath':
      if p0 is not None:line(*p0,closed=True)
  return out
reports={}
for style in ('Display','Text'):
    source=next((ROOT/f'Arvectum-Typeface-v0.{rev}/experimental').glob('Arvectum'+style+'*.otf'))
    f=TTFont(source);glyphs={}
    for cp,name in f.getBestCmap().items():
      char=chr(cp);segs=segments(char)
      if segs:glyphs[char]=segs
    total=[x for ss in glyphs.values() for x in ss]
    strict=[x for x in total if abs(x['angle']-target)<=0.35]
    optical=[x for x in total if 0.35<abs(x['angle']-target)<=3.5]
    outliers=[x for x in total if abs(x['angle']-target)>3.5]
    focus_data={}
    for char in list(dict.fromkeys(focus)):
      if char not in f.getBestCmap().values() and ord(char) not in f.getBestCmap():continue
      segs=glyphs.get(char,[])
      if segs:
        focus_data[char]=dict(angles=[v['angle'] for v in segs],
          median_angle=round(statistics.median(v['angle'] for v in segs),3),
          near_phi_035=sum(abs(v['angle']-target)<=.35 for v in segs),
          segments=len(segs))
    reports[style]={'input':source.name,'count_eligible_glyphs':len(glyphs),
      'long_diagonal_segment_count':len(total),
      'phi_angle_deg':round(target,6),
      'strict_phi_035deg_count':len(strict),
      'optical_035_to_35deg_count':len(optical),
      'outliers_gt_35deg_count':len(outliers),
      'strict_share_pct':round(len(strict)/max(1,len(total))*100,2),
      'angle_round_1_histogram':{str(v):sum(round(x['angle'])==v for x in total) for v in range(5,86)},
      'focus':focus_data,
      'outlier_samples':[{'ch':ch,'angle':x['angle'],'len':x['length']}
        for ch,ss in glyphs.items() for x in ss if abs(x['angle']-target)>3.5][:75]}
    print(style,'eligible long diagonals',len(total),'strict phi',len(strict),
          'optical',len(optical),'outliers',len(outliers))
    print('focused medians',[(k,v['median_angle']) for k,v in focus_data.items()])
# Analyze only the actual altered 3 contours of v0.63, no default merging.
optical={}
for style in ('Display','Text'):
    local={}
    for rv in (61,63):
      f=TTFont(next((ROOT/f'Arvectum-Typeface-v0.{rv}/experimental').glob('Arvectum'+style+'*.otf')))
      local[f'v0.{rv}']={ch:[x['angle'] for x in segments(ch)] for ch in 'Здл'}
    optical[style]=local
data={'phi':phi,'phi_diagonal_angle_deg':target,'definition':'atan(phi) degrees to horizontal',
      'cutoff_long_segment_units':MIN_LENGTH,'strict_angle_deg':0.35,'optical_angle_deg':3.5,
      'baseline':'v0.64 CFF outlines, unchanged from v0.61',
      'styles':reports,'optional_candidate_comparison':optical,
      'method_limits':['Only font-drawn CFF lineTo and closePath straight edges; ignores curved Bezier tangent geometry',
                       'Counts line segments, not independent glyph families or human weight',
                       'A golden-angle target is a design reference; optical deviations may be intentional',
                       'Cannot prove all geometric dimensions use phi',
                       'v0.63 glyph variants are NOT automatically accepted',
                       'Windows left deferred by owner']}
(P/'geometry-audit.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
# Branded histogram; actual measured data controls all bars. Uniform 0-90 angles
w,h=1750,880
canvas=Image.new('RGB',(w,h),'white');d=ImageDraw.Draw(canvas)
title=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',34)
label=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',20)
small=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',17)
d.text((55,20),'GOLDEN STEP  /  v0.68  /  measured straight-edge angles',font=title,fill='#132E3F')
d.text((55,72),'Line segments >= 280 UPM • Phi target = '+str(round(target,3))+'° • Not an owner-accepted design certificate',font=label,fill='#526978')
for ridx,style in enumerate(('Display','Text')):
    y0=163+ridx*337
    left=75; right=1640; bottom=y0+238
    d.text((left,y0-28),style,font=title,fill='#132E3F')
    d.line((left,bottom,right,bottom),fill='#aebec7',width=2)
    bins={int(k):v for k,v in reports[style]['angle_round_1_histogram'].items()}
    maximum=max(bins.values())
    for degree in range(5,86):
        val=bins.get(degree,0)
        x=left+(degree-5)*18.5
        hh=185*val/max(1,maximum)
        color='#31A89B' if abs(degree-target)<=1 else '#6963A2'
        d.rectangle((x,bottom-hh,x+13,bottom),fill=color)
    for angle in (30,45,60,75):
        x=left+(angle-5)*18.5
        d.text((x-8,bottom+12),str(angle)+'°',font=small,fill='#647584')
    xx=left+(target-5)*18.5
    d.line((xx,y0+11,xx,bottom),fill='#df8839',width=3)
    d.text((1150,y0-25),'Near φ: '+str(reports[style]['strict_share_pct'])+'%',font=label,fill='#526978')
    d.text((1190,y0+6),'Orange: 58.2825°',font=small,fill='#df8839')
canvas.save(P/'proofs/golden-angle-histogram.png')
# Simple text-filled proof with exact target and selected medians, no arbitrary drawn glyph glyph source.
sheet=Image.new('RGB',(1800,970),'white')
d=ImageDraw.Draw(sheet)
d.text((55,30),'GOLDEN STEP   /   geometric design audit',font=title,fill='#132E3F')
d.text((55,93),'Target diagonal angle = arctan(phi) = '+str(round(target,4))+' degrees',font=label,fill='#526978')
for ix,st in enumerate(('Display','Text')):
    x=55+ix*880
    d.text((x,160),st+' / actual long straight strokes',font=title,fill='#132E3F')
    for n,ch in enumerate(('А','V','Л','Д','л','д','ж','К','М','У')):
      v=reports[st]['focus'].get(ch)
      if not v:continue
      d.text((x,235+n*57),ch,font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',28),fill='#132E3F')
      angle=v['median_angle'];diff=angle-target
      text=f'{angle:7.2f}°  Δ {diff:+5.2f}°'
      d.text((x+100,238+n*57),text,font=label,fill=('#218C83' if abs(diff)<.35 else '#835681'))
d.text((55,870),'v0.63 altered З/д/л shapes are separate proposals; golden angle differences are not approval criteria.',font=small,fill='#526978')
sheet.save(P/'proofs/golden-angle-focus.png')
print('PASS geometrical angle audit and 2 graphics')
