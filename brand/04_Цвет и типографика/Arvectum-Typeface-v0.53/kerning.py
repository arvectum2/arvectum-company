from pathlib import Path
import json,sys,subprocess,os
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parent/'Arvectum-Typeface-v0.49'))
from pipeline import Family,verify,write_json,digest_tree,sha
from fontTools.ttLib import TTFont
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
# Conservative pair adjustments in design units, signed. No digit kerning:
# tabular financial columns must remain stable by default.
pairs={
'AV':-75,'VA':-65,'AW':-80,'WA':-60,'AT':-55,'TA':-40,
'To':-55,'Te':-45,'Ty':-45,'Ta':-40,'Tr':-30,'LT':-35,'LY':-55,'La':-25,
'Vo':-60,'Ve':-50,'Va':-45,'Wo':-65,'We':-50,'Wa':-50,
'Yo':-45,'Ya':-45,'Fo':-45,'Fa':-40,'Pa':-30,'Po':-30,
'ry':-20,'ly':-15,'ff':-20,'rt':-20,
'АУ':-70,'УА':-60,'АЛ':-30,'ЛТ':-50,'ДА':-35,'АТ':-55,
'ТО':-55,'То':-50,'Те':-45,'Ту':-45,'Го':-35,'Га':-30,
'Ча':-25,'Ла':-35,'Лу':-30,'Уо':-45,'Уе':-45,
'Ар':-25,'Ур':-25,'БА':-20,'Ро':-35,'Ра':-35,'Фо':-45,
'AУ':-45,'АV':-55,'VА':-55,'Tо':-40,
}
assert len(pairs)==len(set(pairs))
reports={};files={}
for st in ('Display','Text'):
    src=next((P.parent/'Arvectum-Typeface-v0.52/experimental').glob(f'Arvectum{st}*.otf'))
    out=P/'experimental'/('Arvectum'+st+'GoldenStepDraft053-'+('Medium' if st=='Display' else 'Regular')+'.otf')
    f=Family(st,53,src,out);r=f.finish();verify(src,out,set())
    cm=TTFont(out).getBestCmap()
    lines=['languagesystem DFLT dflt;','languagesystem latn dflt;','languagesystem cyrl dflt;','feature kern {']
    for pair,val in pairs.items():
        assert len(pair)==2 and val<0 and all(ord(c) in cm for c in pair)
        a,b=(cm[ord(c)] for c in pair)
        lines.append(f'    pos {a} {b} {val};')
    lines.append('} kern;')
    fea='\n'.join(lines)+'\n'
    (P/f'kerning-{st.lower()}.fea').write_text(fea)
    g=TTFont(out);addOpenTypeFeaturesFromString(g,fea)
    tmp=out.with_suffix('.tmp');g.recalcTimestamp=False;g.save(tmp);os.replace(tmp,out)
    check=TTFont(out);assert 'GPOS' in check
    beforeafter={}
    for pair,v in pairs.items():
        def shape(feature):
            cmd=['hb-shape','--output-format=json','--features=kern='+str(feature),str(out),pair]
            result=json.loads(subprocess.check_output(cmd,text=True))
            assert len(result)==2 and all(g['g']!='.notdef' for g in result)
            return sum(int(g['ax']) for g in result)
        plain,kern=shape(0),shape(1)
        assert kern-plain==v,(st,pair,plain,kern,v)
        beforeafter[pair]={'no_kern':plain,'kern':kern,'delta':kern-plain}
    # Confirm tabular digits unchanged regardless of kerning toggle.
    for c in ('01','10','90','00','11','12'):
        def x(feat):
            q=json.loads(subprocess.check_output(['hb-shape','--output-format=json','--features=kern='+str(feat),str(out),c],text=True))
            return sum(x['ax'] for x in q)
        assert x(1)==x(0)
    assert verify(src,out,set())==203
    reports[st]={'input':src.name,'input_sha256':sha(src),'output_sha256':sha(out),'pairs':beforeafter,'kern_pairs':len(pairs),'unchanged_hmtx':203}
    files[st]=out
write_json(P/'kerning-qa.json',reports)
from PIL import Image,ImageDraw,ImageFont,features
im=Image.new('RGB',(1700,970),'white');d=ImageDraw.Draw(im)
regular=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',22)
lines=['AV VA AW WA To Te Ty', 'АУ УА ЛТ ДА ТО То Те','Arvectum — Арвектум','1 250 000,00 ₽  |  2 500 000,00 ₽']
for j,st in enumerate(('Display','Text')):
    x=30+j*840;d.text((x,25),st+' / GPOS kern',font=regular,fill='#001432')
    y=95
    for s in lines:
        ft=ImageFont.truetype(str(files[st]),44)
        d.text((x,y),s,font=ft,fill='#001432');y+=120
im.save(P/'kerning-proof.png')
print('PASS kerning',len(pairs),'pairs per style',digest_tree(P),'raqm',features.check('raqm'))
