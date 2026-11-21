"""Isolated v0.59 candidate: extend Windows clipping rectangle, preserve typo/hhea metrics.
Never promote to production without Windows/Office compatibility decision.
"""
from pathlib import Path
import sys,json
from fontTools.ttLib import TTFont
P=Path(__file__).resolve().parent;BASE=P.parent
sys.path.insert(0,str(BASE/'Arvectum-Typeface-v0.49'))
from pipeline import Family,verify,sha,write_json
SOURCE=BASE/'Arvectum-Typeface-v0.58/experimental'
res={}
for st in ('Display','Text'):
    src=next(SOURCE.glob('Arvectum'+st+'*.otf'))
    p=P/'experimental'/('Arvectum'+st+'GoldenStepDraft059-'+('Medium' if st=='Display' else 'Regular')+'.otf')
    f=Family(st,59,src,p)
    f.f['CFF '].cff.fontNames=[f.name]
    base=TTFont(src);o0=base['OS/2'];h0=base['hhea']
    o=f.f['OS/2']
    assert (o.version,o.usWinAscent,o.usWinDescent,o.sTypoAscender,o.sTypoDescender)==(3,2160,760,2080,-680)
    old_selection=o.fsSelection
    o.version=4
    o.usWinAscent=2400  # 2334 measured max triple-upper ink + ~66 safety
    o.usWinDescent=1200 # 1120 measured triple-cedilla ink + 80 safety
    o.fsSelection |= 1<<7 # USE_TYPO_METRICS; not universally honored
    assert o.fsSelection==(old_selection|128)
    meta=f.finish()
    assert verify(src,p,set())==212
    ff=TTFont(p);b=ff['OS/2'];h=ff['hhea']
    assert b.version==4 and b.usWinAscent==2400 and b.usWinDescent==1200 and bool(b.fsSelection&128)
    assert (b.sTypoAscender,b.sTypoDescender,b.sTypoLineGap)==(o0.sTypoAscender,o0.sTypoDescender,o0.sTypoLineGap)
    assert (h.ascent,h.descent,h.lineGap)==(h0.ascent,h0.descent,h0.lineGap)
    assert ff['GPOS'].compile(ff)==base['GPOS'].compile(base)
    assert ff['GDEF'].compile(ff)==base['GDEF'].compile(base)
    for flavor in ('woff','woff2'):
        w=p.with_suffix('.'+flavor)
        web=TTFont(p);web.flavor=flavor;web.recalcTimestamp=False;web.save(w)
        back=TTFont(w)
        assert back['OS/2'].usWinAscent==2400 and back['OS/2'].usWinDescent==1200 and back['OS/2'].fsSelection&128
        assert verify(p,w,set())==212
    res[st]=dict(input=src.name,input_sha=sha(src),otf=p.name,otf_sha=sha(p),os2_version=4,
                 use_typo_metrics=True,hhea_typo_unchanged=True,old_win=[2160,760],
                 new_win=[2400,1200],old_win_sum=2920,new_win_sum=3600,
                 potential_legacy_lineheight_increase_pct=round(100*(3600/2920-1),2),
                 html_typo_preference_not_guaranteed=True,
                 codepoints=212,changed_outlines=0,changed_hmtx=0,
                 risk='legacy Windows applications may use usWin metrics for line spacing')
write_json(P/'build-report.json',res)
print('PASS metrics-only experimental candidate; 212 glyphs/hmtx and GPOS/GDEF unchanged')
