"""Golden Step v0.86: one restrained, reproducible Inter-derived З/з design.
Flatten top/bottom extrema with tangent straight portions while preserving the
professional Inter bowl topology, terminals, counters, heights and metrics.
Only U+0417, U+0437 are modified; digit 3 and every other glyph stay exact.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import hashlib,json
P=Path(__file__).resolve().parent
BASE=P.parent/'Arvectum-Typeface-v0.85'
STYLES={'Display':'Medium','Text':'Regular'}
SRC={'Display':'ArvectumGoldenStepDisplayBaseDraft085-Medium.otf','Text':'ArvectumGoldenStepTextBaseDraft085-Regular.otf'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert (BASE/'OFL-LICENSE.txt').exists()
(P/'OFL-LICENSE.txt').write_bytes((BASE/'OFL-LICENSE.txt').read_bytes())

def edit(pen,advance):
    ops=list(pen.value)
    assert len(ops)==20 and [o for o,a in ops]==['moveTo','curveTo','curveTo','lineTo','curveTo','curveTo','curveTo','lineTo','curveTo','curveTo','curveTo','lineTo','lineTo','lineTo','curveTo','curveTo','curveTo','lineTo','curveTo','closePath']
    (_,_,(topx,topy))=ops[5][1]
    (bottomx,bottomy)=ops[0][1][0]
    assert bottomx==ops[18][1][-1][0] and bottomy==ops[18][1][-1][1]
    half=round(advance*0.07)
    assert ops[5][1][1][0]>topx+half and ops[6][1][0][0]<topx-half
    assert ops[1][1][0][0]>bottomx+half and ops[18][1][1][0]<bottomx-half
    new=[('moveTo',((bottomx+half,bottomy),))]
    new+=ops[1:5]
    t=list(ops[5][1]);t[-1]=(topx+half,topy)
    new.append(('curveTo',tuple(t)))
    new.append(('lineTo',((topx-half,topy),)))
    new+=ops[6:18]
    t=list(ops[18][1]);t[-1]=(bottomx-half,bottomy)
    new.append(('curveTo',tuple(t)))
    new.append(('lineTo',((bottomx+half,bottomy),)))
    new.append(ops[19])
    assert len(new)==22
    new_pen=RecordingPen();new_pen.value=new
    return new_pen,{'top_span':2*half,'bottom_span':2*half,'top_y':topy,'bottom_y':bottomy,'operation_count_original':20,'operation_count_proposed':22}

def svg_for(font,char,path):
    gs=font.getGlyphSet(); n=font.getBestCmap()[ord(char)]
    g=gs[n];pen=SVGPathPen(gs);g.draw(pen);bp=BoundsPen(gs);g.draw(bp)
    x0,y0,x1,y1=bp.bounds
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.3f} {-y1:.3f} {x1-x0:.3f} {y1-y0:.3f}"><path fill="#001432" fill-rule="nonzero" transform="scale(1 -1)" d="{pen.getCommands()}"/></svg>\n')

manifest={'version':'0.86','status':'experimental / not approved','concept':'one restrained optical correction of original Inter bowl: flat top and bottom tangents; no other form modifications','source_version':'0.85','changed_codepoints':['U+0417','U+0437'],'source_file_hashes':{},'styles':{}}
for sty,weight in STYLES.items():
    original=BASE/'experimental'/SRC[sty]
    a=TTFont(original)
    cm=a.getBestCmap()
    f=TTFont(original,recalcTimestamp=False)
    td=f['CFF '].cff.topDictIndex[0]
    rows={}
    for ch in 'Зз':
        gn=cm[ord(ch)]
        rec=RecordingPen();a.getGlyphSet()[gn].draw(rec)
        width,lsb=f['hmtx'][gn]
        modified,metadata=edit(rec,width)
        cs=T2CharStringPen(width,None);modified.replay(cs)
        td.CharStrings[gn]=cs.getCharString(private=td.Private,globalSubrs=f['CFF '].cff.GlobalSubrs)
        rows[ch]={'name':gn,'advance':width,'left_side_bearing':lsb,**metadata}
    family=f'Arvectum Golden Step {sty} Architectural Draft 086'
    ps=f'ArvectumGoldenStep{sty}ArchFlatsDraft086-{weight}'
    for plat,enc,lang in ((3,1,1033),(1,0,0)):
      for nid,val in ((1,family),(2,weight),(3,ps+';0.86;Inter-4.1-source'),(4,family+' '+weight),(5,'Version 0.086; experimental'),(6,ps),(16,family),(17,weight)):
        f['name'].setName(val,nid,plat,enc,lang)
    td.FamilyName=family;td.FullName=family+' '+weight;f['CFF '].cff.fontNames=[ps]
    f['head'].fontRevision=.086;f.recalcTimestamp=False
    out=P/'experimental'/f'{ps}.otf';out.parent.mkdir(parents=True,exist_ok=True);f.save(out)
    v=TTFont(out)
    for ch in 'Зз3':
        svg_for(a,ch,P/'glyphs'/'Inter'/sty/f'U+{ord(ch):04X}.svg')
        svg_for(v,ch,P/'glyphs'/'Arvectum'/sty/f'U+{ord(ch):04X}.svg')
    manifest['source_file_hashes'][sty]=sha(original)
    manifest['styles'][sty]={'otf':str(out.relative_to(P)),'source':str(original.relative_to(BASE)),'sha256':sha(out),'modified':rows}
    print('BUILT',sty,'top/bottom flat span',rows['З']['top_span'],rows['з']['top_span'],'sha256',sha(out)[:16])
(P/'evidence').mkdir(exist_ok=True)
(P/'evidence/build-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
