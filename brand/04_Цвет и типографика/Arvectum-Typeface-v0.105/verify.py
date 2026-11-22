"""Independent CFF check: exact provisional beta K/К/X/Х, W HOLD."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.areaPen import AreaPen
import math,hashlib,json,subprocess
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
phi=(1+math.sqrt(5))/2;alpha=math.degrees(math.atan(phi**2));beta=math.degrees(math.atan(phi))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ops(f,n):
 pen=RecordingPen();f.getGlyphSet()[n].draw(pen);return pen.value
def bounds(f,n):
 p=BoundsPen(f.getGlyphSet());f.getGlyphSet()[n].draw(p);return p.bounds
def area(f,n):
 p=AreaPen(f.getGlyphSet());f.getGlyphSet()[n].draw(p);return p.value
report={'version':'0.105','status':'experimental mechanics PASS; owner optical approval OPEN',
 'angle_alpha':alpha,'angle_beta':beta,'W_status':'UNCHANGED/HOLD due metric conflict',
 'limitations':['X/Х center ink area increase 7-9%, needs optical assessment',
 'K vs К differing anatomy; separate artistic approval',
 'W α would compromise widths/counters, unbuilt',
 'K/X family angle mapping proposed, not adopted owner decision',
 'other inherited scripts/kerning/legal/open'], 'styles':{}}
for face,spec in m['styles'].items():
 src=R/spec['source'];dst=P/spec['output']
 assert sha(src)==spec['source_sha256'] and sha(dst)==spec['output_sha256']
 a,b=TTFont(src),TTFont(dst);cm=b.getBestCmap()
 assert a.getGlyphOrder()==b.getGlyphOrder() and len(b.getGlyphOrder())==2937
 assert a.getBestCmap()==cm and len(cm)==2852
 assert a['hmtx'].metrics==b['hmtx'].metrics
 for tag in ('cmap','hhea','OS/2','GPOS','GSUB','GDEF'):
  assert a[tag].compile(a)==b[tag].compile(b),(face,tag)
 changed={name for name in a.getGlyphOrder() if ops(a,name)!=ops(b,name)}
 assert changed=={'K','Kacyr','X','uni0425'},(face,changed)
 assert ops(b,cm[ord('X')])==ops(b,cm[ord('Х')]),(face,'linked X/Х')
 assert ops(b,cm[ord('K')])!=ops(b,cm[ord('К')]),(face,'K distinct')
 assert ops(a,cm[ord('W')])==ops(b,cm[ord('W')])
 for ch in 'AАVMМNИYДЛдл':
  name=cm[ord(ch)];assert ops(a,name)==ops(b,name),(face,'previous approved family regression',ch)
 results={}
 for ch in ('K','К','X','Х'):
  name=cm[ord(ch)];old=ops(a,name);cur=ops(b,name)
  assert len(old)==len(cur) and [z[0] for z in old]==[z[0] for z in cur]
  errors=[]
  for i,j in spec['glyphs'][ch]['edges']:
   x,y=cur[i][1][-1];X,Y=cur[j][1][-1]
   ang=math.degrees(math.atan2(abs(Y-y),abs(X-x)))
   errors.append(abs(ang-beta))
  assert max(errors)<.0001,(face,ch,'beta',errors)
  one,two=bounds(a,name),bounds(b,name)
  assert all(abs(u-v)<.001 for u,v in zip(one,two)),(face,ch,'bbox changed',one,two)
  area_change=(abs(area(b,name))/abs(area(a,name))-1)*100
  limit=4 if ch in ('K','К') else 10
  assert abs(area_change)<limit,(face,ch,'ink',area_change)
  assert b['hmtx'][name]==a['hmtx'][name]
  contours=sum(op=='moveTo' for op,pts in cur)
  assert contours==1,(face,ch,'unexpected contour count')
  results[ch]={'glyph_name':name,'max_beta_angle_error_deg':max(errors),
    'target_segments':len(errors),'area_change_pct':round(area_change,5),
    'bounds_preserved':True,'advance':b['hmtx'][name][0]}
 for sentence in ('КЛЮЧИ И ХАРАКТЕР', 'KERNEL X-RAY WAVE',
  'КОД ХОРОШИЙ, КЛЮЧ КРАСИВЫЙ','AА VММ NИY W КK XХ'):
  shaped=subprocess.check_output(['hb-shape',str(dst),sentence],text=True)
  assert '.notdef' not in shaped and 'gid0' not in shaped,(face,sentence)
 report['styles'][face]={'changed_glyphs':sorted(changed),'unchanged_2937':2933,
    'metrics_and_layout_unchanged':True,'provisional_beta_glyphs':results}
 print('PASS',face,'K/К/X/Х',[(x,round(v['max_beta_angle_error_deg'],8),v['area_change_pct'])
  for x,v in results.items()])
(P/'evidence/qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
