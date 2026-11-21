"""Non-authoritative vector options based on approved Golden Wordmark C v0.21 RU.
Variant B edits rounded р shoulder, C/D shift e bar by H/phi^7; source remains exact.
"""
from pathlib import Path
from fontTools.svgLib.path import parse_path
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
import xml.etree.ElementTree as ET,hashlib,math,json
P=Path(__file__).resolve().parent;MASTER=P.parents[1]/'03_Логотип/Golden-Wordmark-v0.21/C_Wordmark_RU.svg'
assert MASTER.is_file(),MASTER
out=P/'wordmark';out.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
svg_ns='http://www.w3.org/2000/svg';phi=(1+math.sqrt(5))/2;shift=1056/(phi**7)
variants=[('A_original',None,None),('B_rounder_p',True,None),('C_lower_e',None,-shift),('D_higher_e',None,shift),('E_rounder_p_lower_e',True,-shift),('F_rounder_p_higher_e',True,shift)]
report={'source':str(MASTER),'source_sha256':sha(MASTER),'phi':phi,'crossbar_adjustment':shift,
        'baseline_e_bar_center_ratio':((500+690.77974)/2)/1056,'approved_reference_unchanged':True,'options':{}}
for label,make_p,e_delta in variants:
 tree=ET.parse(MASTER);root=tree.getroot();group=next(c for c in root if c.tag.endswith('g'))
 assert len(group)==8
 if make_p:
  node=group[1];rec=RecordingPen();parse_path(node.get('d'),rec);ops=list(rec.value)
  assert len(ops)==17 and ops[4][0]==ops[5][0]==ops[6][0]=='curveTo'
  ops[4]=('curveTo',((260.,1010.),(380.,1071.),(500.,1071.)))
  ops[5]=('curveTo',((806.,1071.),(940.,897.),(940.,528.)))
  ops[6]=('curveTo',((940.,159.),(795.,-15.),(500.,-15.)))
  ops[7]=('curveTo',((363.,-15.),(245.,80.),(200.59127,178.)))
  edit=RecordingPen();edit.value=ops;pen=SVGPathPen(None);edit.replay(pen);node.set('d',pen.getCommands())
 if e_delta is not None:
  node=group[3];rec=RecordingPen();parse_path(node.get('d'),rec);ops=list(rec.value)
  assert len(ops)==16 and ops[11][0]=='moveTo' and ops[12][0]=='lineTo'
  d=e_delta
  def adjust(op,vals):return (op,vals)
  ops[0]=('moveTo',((200.59127,500.+d),))
  ops[1]=('curveTo',((200.59127,271.+d*.42),(277.,175.77974),(475.,175.77974)))
  ops[7]=('curveTo',((786.,1071.),(950.,887.+d*.25),(950.,580.+d)))
  ops[8]=('lineTo',((950.,500.+d),));ops[9]=('lineTo',((200.59127,500.+d),))
  ops[11]=('moveTo',((207.59127,690.77974+d),))
  ops[12]=('lineTo',((741.40873,690.77974+d),))
  ops[13]=('curveTo',((735.,820.+d*.32),(654.,880.22026),(475.,880.22026)))
  ops[14]=('curveTo',((300.,880.22026),(219.,830.+d*.32),(207.59127,690.77974+d)))
  edit=RecordingPen();edit.value=ops;pen=SVGPathPen(None);edit.replay(pen);node.set('d',pen.getCommands())
 dest=out/f'{label}.svg';ET.register_namespace('',svg_ns);tree.write(dest,encoding='unicode',xml_declaration=False)
 report['options'][label]={'filename':dest.name,'svg_sha256':sha(dest),'p_rounded':bool(make_p),'e_shift_y':round(e_delta,5) if e_delta is not None else None,
  'e_bar_ratio':round(((500+690.77974)/2+(e_delta or 0))/1056,6)}
print('OPTICAL WORDMARK OPTIONS',len(variants),'bar shift',round(shift,3),'source',sha(MASTER)[:14])
(P/'evidence/wordmark-options.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
