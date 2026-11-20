from pathlib import Path
import sys,json,subprocess,unicodedata as ud
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parent/'Arvectum-Typeface-v0.49'))
from pipeline import Family,sha,verify,write_json,digest_tree
from fontTools.ttLib import TTFont
TARGET={'hhea_ascent':2080,'hhea_descent':-680,'win_ascent':2160,'win_descent':760}
reports={}
for st in ('Display','Text'):
    src=next((P.parent/'Arvectum-Typeface-v0.54/experimental').glob(f'Arvectum{st}*.otf'))
    dest=P/'experimental'/('Arvectum'+st+'GoldenStepDraft055-'+('Medium' if st=='Display' else 'Regular')+'.otf')
    f=Family(st,55,src,dest)
    old={'hhea_ascent':f.hh.ascent,'hhea_descent':f.hh.descent,
         'win_ascent':f.f['OS/2'].usWinAscent,'win_descent':f.f['OS/2'].usWinDescent}
    f.hh.ascent=TARGET['hhea_ascent'];f.hh.descent=TARGET['hhea_descent']
    os2=f.f['OS/2'];os2.sTypoAscender=f.hh.ascent;os2.sTypoDescender=f.hh.descent
    os2.usWinAscent=TARGET['win_ascent'];os2.usWinDescent=TARGET['win_descent']
    meta=f.finish();check=TTFont(dest)
    assert all([check['hhea'].ascent==TARGET['hhea_ascent'],check['hhea'].descent==TARGET['hhea_descent'],
                check['OS/2'].sTypoAscender==TARGET['hhea_ascent'],check['OS/2'].sTypoDescender==TARGET['hhea_descent'],
                check['OS/2'].usWinAscent==TARGET['win_ascent'],check['OS/2'].usWinDescent==TARGET['win_descent']])
    assert verify(src,dest,set())==212
    c=check.getBestCmap();widths={f'U+{ord(ch):04X}':check['hmtx'][c[ord(ch)]][0] for ch in ' \u00a0\u202f'}
    assert widths=={'U+0020':512,'U+00A0':512,'U+202F':316}
    assert {check['hmtx'][c[ord(ch)]][0] for ch in '0123456789'}==({1323} if st=='Display' else {1266})
    for s in ('1 250 000','1\u00a0250\u00a0000','1\u202f250\u202f000'):
        q=json.loads(subprocess.check_output(['hb-shape','--output-format=json',str(dest),s],text=True))
        assert len(q)==len(s) and all(x['g']!='.notdef' for x in q)
    max_combining_top=1700+365;min_combining_bottom=-350-300
    assert TARGET['hhea_ascent']>max_combining_top and TARGET['hhea_descent']<min_combining_bottom
    reports[st]={'input':src.name,'previous_metrics':old,'revised_metrics':TARGET,
        'source_sha256':sha(src),'sha256':sha(dest),'spacing':widths,'unchanged_outlines_and_hmtx':212,
        'test_synth_extents':[max_combining_top,min_combining_bottom],
        'at_12pt_lineheight_before':round((old['hhea_ascent']-old['hhea_descent'])/2048*12,2),
        'at_12pt_lineheight_after':round((f.hh.ascent-f.hh.descent)/2048*12,2)}
write_json(P/'metrics-qa.json',reports)
print('PASS v0.55 metrics',digest_tree(P),reports['Display']['at_12pt_lineheight_after'])
