"""Additive v0.61: conservative real-corpus Cyrillic kerning, immutable v0.58 base."""
from pathlib import Path
import json,sys,subprocess
from fontTools.ttLib import TTFont
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.pens.recordingPen import RecordingPen
P=Path(__file__).resolve().parent;ROOT=P.parent
sys.path.insert(0,str(ROOT/'Arvectum-Typeface-v0.49'))
from pipeline import Family,verify,sha
# Only pairs seen repeatedly in specimens; small adjustments; no numbers or punctuation.
ADDITIONS={'ст':-35,'кт':-40,'дл':-25,'от':-25,'те':-25,
           'ты':-25,'го':-30,'га':-30,'гр':-30,'ич':-25,
           'еч':-25,'ка':-20,'ЛА':-45,'ТА':-40}
REPORT={}
for style in ('Display','Text'):
    source=next((ROOT/'Arvectum-Typeface-v0.58/experimental').glob('Arvectum'+style+'*.otf'))
    output=P/'experimental'/('Arvectum'+style+'GoldenStepDraft061-'+('Medium' if style=='Display' else 'Regular')+'.otf')
    f=Family(style,61,source,output)
    f.f['CFF '].cff.fontNames=[f.name]
    f.finish()
    assert verify(source,output,set())==212
    font=TTFont(output);cmap=font.getBestCmap()
    fea=(ROOT/'Arvectum-Typeface-v0.58'/('features-'+style.lower()+'.fea')).read_text()
    assert fea.count('} kern;')==1
    insertion=[]
    for pair,value in ADDITIONS.items():
        assert len(pair)==2 and -60<=value<0 and all(ord(c) in cmap for c in pair)
        left,right=(cmap[ord(c)] for c in pair)
        assert f'pos {left} {right} ' not in fea
        insertion.append('    pos '+left+' '+right+' '+str(value)+';')
    newfea=fea.replace('} kern;', '\n'.join(insertion)+'\n} kern;')
    (P/('features-'+style.lower()+'.fea')).write_text(newfea)
    addOpenTypeFeaturesFromString(font,newfea)
    assert set(x.FeatureTag for x in font['GPOS'].table.FeatureList.FeatureRecord)=={'kern','mark','mkmk'}
    assert 'GDEF' in font
    font.recalcTimestamp=False;font.save(output)
    assert verify(source,output,set())==212
    after=TTFont(output);before=TTFont(source)
    assert after['hmtx'].metrics==before['hmtx'].metrics
    assert after['OS/2'].compile(after)==before['OS/2'].compile(before)
    assert after['hhea'].compile(after)==before['hhea'].compile(before)
    assert after.getBestCmap()==before.getBestCmap()
    assert after['CFF '].cff.fontNames==[after['name'].getDebugName(6)]
    REPORT[style]={'source':source.name,'source_sha256':sha(source),'output':output.name,
                  'output_sha256':sha(output),'new_pairs':ADDITIONS,'new_pair_count':len(ADDITIONS),'glyph_contours_and_hmtx_unchanged':212,
                  'windows_metrics':'identical to v0.58; never inherit v0.59 risk','web':{}}
    for flavor in ('woff','woff2'):
        w=output.with_suffix('.'+flavor)
        web=TTFont(output);web.flavor=flavor;web.recalcTimestamp=False;web.save(w)
        back=TTFont(w)
        assert back.getBestCmap()==after.getBestCmap()
        assert back['hmtx'].metrics==after['hmtx'].metrics
        assert set(x.FeatureTag for x in back['GPOS'].table.FeatureList.FeatureRecord)=={'kern','mark','mkmk'}
        REPORT[style]['web'][flavor]=dict(file=w.name,sha256=sha(w))
(P/'build-report.json').write_text(json.dumps(REPORT,ensure_ascii=False,indent=2)+'\n')
print('PASS v0.61 14 additional pairs/style; CFF/advances/OS2/marks preserved, OTF/WOFF/WOFF2')
