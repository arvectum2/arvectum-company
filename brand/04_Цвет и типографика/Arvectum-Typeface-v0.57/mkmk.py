"""GS-007 follow-up: add mark-to-mark attachment; keep 212 CFF glyphs/metrics unchanged."""
from pathlib import Path
import json,subprocess,sys,math
P=Path(__file__).resolve().parent
BASE=P.parent
sys.path.insert(0,str(BASE/'Arvectum-Typeface-v0.49'))
from pipeline import Family,verify,sha,write_json,digest_tree
from fontTools.ttLib import TTFont
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen

top='\u0300\u0301\u0302\u0303\u0304\u0306\u0308\u030a'
reports={}
for st in ('Display','Text'):
    src=next((BASE/'Arvectum-Typeface-v0.56/experimental').glob(f'Arvectum{st}*.otf'))
    name='Arvectum'+st+'GoldenStepDraft057-'+('Medium' if st=='Display' else 'Regular')
    out=P/'experimental'/(name+'.otf')
    f=Family(st,57,src,out)
    # Prior experimental stages kept the original 047 CFF PostScript name,
    # despite updated name-table ID 6. Repair in this additive version only.
    f.f['CFF '].cff.fontNames=[f.name]
    meta=f.finish()
    assert verify(src,out,set())==212
    before=TTFont(src);current=TTFont(out)
    sourcefea=(BASE/'Arvectum-Typeface-v0.54'/('features-'+st.lower()+'.fea')).read_text()
    assert 'feature mkmk' not in sourcefea and 'feature mark' in sourcefea and 'feature kern' in sourcefea
    lines=['feature mkmk {'];mark_anchors={}
    for ch in top:
        glyph=current.getBestCmap()[ord(ch)]
        b=BoundsPen(current.getGlyphSet());current.getGlyphSet()[glyph].draw(b)
        assert b.bounds is not None and current['hmtx'][glyph][0]==0
        y=round(b.bounds[3]+95)
        mark_anchors[f'U+{ord(ch):04X}']={'name':glyph,'ink_bounds':list(b.bounds),'mkmk_attach_y':y}
        lines.append(f'  pos mark {glyph} <anchor 0 {y}> mark @TOP;')
    lines.append('} mkmk;')
    featuretext=sourcefea+'\n'+'\n'.join(lines)+'\n'
    (P/('features-'+st.lower()+'.fea')).write_text(featuretext)
    addOpenTypeFeaturesFromString(current,featuretext)
    assert set(x.FeatureTag for x in current['GPOS'].table.FeatureList.FeatureRecord)=={'kern','mark','mkmk'}
    assert 'GDEF' in current
    current.recalcTimestamp=False;current.save(out)
    reloaded=TTFont(out)
    assert reloaded['CFF '].cff.fontNames==[name] and reloaded['name'].getDebugName(6)==name
    assert 'GPOS' in reloaded and 'GDEF' in reloaded
    assert reloaded.getBestCmap()==before.getBestCmap()
    assert verify(src,out,set())==212
    assert {c:reloaded['hmtx'][n] for c,n in reloaded.getBestCmap().items()}=={c:before['hmtx'][n] for c,n in before.getBestCmap().items()}
    reports[st]={'input':src.name,'input_sha256':sha(src),'output':out.name,'output_sha256':sha(out),'mark_anchors':mark_anchors,'codepoints':212,'scope':'GPOS only: kern+mark+mkmk; CFF outlines and hmtx unchanged','web':{}}
    for flavor in ('woff','woff2'):
        w=out.with_suffix('.'+flavor)
        web=TTFont(out);web.flavor=flavor;web.recalcTimestamp=False;web.save(w)
        back=TTFont(w)
        assert back.getBestCmap()==reloaded.getBestCmap() and back['hmtx'].metrics==reloaded['hmtx'].metrics
        assert 'GPOS' in back and 'GDEF' in back
        assert {x.FeatureTag for x in back['GPOS'].table.FeatureList.FeatureRecord}=={'kern','mark','mkmk'}
        reports[st]['web'][flavor]={'file':w.name,'sha256':sha(w),'status':'PASS'}
write_json(P/'build-report.json',reports)
print('PASS: v0.57 CFF OTF, WOFF, WOFF2; 212 glyph outlines and metrics unchanged; kern/mark/mkmk')
