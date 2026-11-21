"""Three narrowly-scoped optical candidate glyphs, no owner acceptance."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
import math,sys,json
P=Path(__file__).resolve().parent;ROOT=P.parent
sys.path.insert(0,str(ROOT/'Arvectum-Typeface-v0.49'))
from pipeline import Family,verify,box,sha
REPORT={}
def adjust(pen,fun):
    out=RecordingPen()
    for op,positions in pen.value:
        if op=='moveTo':out.moveTo(fun(*positions[0]))
        elif op=='lineTo':out.lineTo(fun(*positions[0]))
        elif op=='curveTo':out.curveTo(*(fun(*pt) for pt in positions))
        elif op=='qCurveTo':out.qCurveTo(*(fun(*pt) for pt in positions))
        elif op=='closePath':out.closePath()
        else:raise ValueError(op)
    return out
def rec(f,ch):
    n=f.getBestCmap()[ord(ch)];p=RecordingPen();f.getGlyphSet()[n].draw(p);return p
for st in ('Display','Text'):
    src=next((ROOT/'Arvectum-Typeface-v0.61/experimental').glob('Arvectum'+st+'*.otf'))
    output=P/'experimental'/('Arvectum'+st+'GoldenStepDraft063-'+('Medium' if st=='Display' else 'Regular')+'.otf')
    f=Family(st,63,src,output)
    f.f['CFF '].cff.fontNames=[f.name]
    bounds={}
    for ch in 'Здл':
        p=rec(f.f,ch)
        if ch=='З':
            # Shrink upper bowl's horizontal extension. Lower bowl and baseline stay fixed.
            # A local optical study, not a general affine transform of phi glyph geometry.
            def fun(x,y):
                q=max(0,min(1,(y-800)/165))
                return (round(100+(x-100)*(1-0.12*q),4),y)
        elif ch=='д':
            def fun(x,y):
                if y>=0:return (x,y)
                q=min(1,max(0,-y/174))
                out=-14*q if x<350 else (14*q if x>1240 else 0)
                return (round(x+out,4),round(y-(54*q),4))
        else: # л
            top=1118 if st=='Text' else 1056
            left=552 if st=='Text' else 610
            right=641 if st=='Text' else 695
            def fun(x,y):
                if abs(y-top)<1 and abs(x-left)<1:return (x-27,y)
                if abs(y-top)<1 and abs(x-right)<1:return (x+27,y)
                return (x,y)
        revised=adjust(p,fun)
        name=f.f.getBestCmap()[ord(ch)]
        oldwidth,oldlsb=f.h.metrics[name]
        f.put(ch,revised,width=oldwidth,lsb=round(box(revised)[0]),note='provisional small-text optical study; default not accepted')
        bounds[ch]={'prior':box(p),'candidate':box(revised),'width':oldwidth,'prior_lsb':oldlsb,
            'candidate_lsb':f.h.metrics[name][1]}
    f.finish()
    assert verify(src,output,set('Здл'))==209
    t=TTFont(src);new=TTFont(output)
    assert new.getBestCmap()==t.getBestCmap() and len(t.getBestCmap())==212
    assert {c:new['hmtx'][name][0] for c,name in new.getBestCmap().items()}=={
        c:t['hmtx'][name][0] for c,name in t.getBestCmap().items()}
    assert t['OS/2'].compile(t)==new['OS/2'].compile(new)
    assert t['hhea'].compile(t)==new['hhea'].compile(new)
    assert t['GPOS'].compile(t)==new['GPOS'].compile(new)
    assert t['GDEF'].compile(t)==new['GDEF'].compile(new)
    REPORT[st]={'source':src.name,'sha_source':sha(src),'candidate':output.name,'sha_candidate':sha(output),
      'modified':bounds,'unchanged_glyphs':209,'widths_unchanged':212,'GPOS_unchanged':True,'OS2_hhea_unchanged':True,
      'production_approved':False,'web':{}}
    for flavor in ('woff','woff2'):
        font=TTFont(output);font.flavor=flavor;font.recalcTimestamp=False;target=output.with_suffix('.'+flavor);font.save(target)
        assert TTFont(target).getBestCmap()==new.getBestCmap()
        REPORT[st]['web'][flavor]={'file':target.name,'sha256':sha(target)}
(P/'build-report.json').write_text(json.dumps(REPORT,ensure_ascii=False,indent=2)+'\n')
print('PASS v0.63 three experimental glyphs/style; unchanged 209 contours and 212 advances, metrics/GPOS intact')
