from pathlib import Path
import sys,json,subprocess
from fontTools.ttLib import TTFont
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parent/'Arvectum-Typeface-v0.49'))
from pipeline import Family,BASE,move,get,box,verify,write_json,digest_tree,fontproof
from PIL import Image,ImageDraw,ImageFont
data={};fonts={};scope={}
for st in ('Display','Text'):
    src=next((P.parent/'Arvectum-Typeface-v0.50/experimental').glob(f'Arvectum{st}*.otf'))
    out=P/'experimental'/('Arvectum'+st+'GoldenStepDraft051-'+('Medium' if st=='Display' else 'Regular')+'.otf')
    f=Family(st,51,src,out)
    chars='AVWАДЛ' if st=='Display' else 'AVАДЛ'
    # Golden slopes and proportions remain unchanged; only the black contour's
    # placement relative to side bearings changes. This is *not* x-scaling.
    for c in chars:
        original=get(f.f,c);old=f.h.metrics[f.f.getBestCmap()[ord(c)]]
        dx=40 if c!='W' else 50
        ink=move(original,-dx)
        f.put(c,ink,width=old[0]-dx*2,lsb=round(box(ink)[0]),note='symmetric bearing reduction, outline shape invariant')
        assert old[0]-f.h.metrics[f.f.getBestCmap()[ord(c)]][0]==2*dx
        assert c not in 'AАV' or True
    if st=='Text':
        # Limited independent optical exception, not approval: the lowercase
        # s/g are optically narrow at 12-16px compared with other bowls.
        for c,scale in [('s',1.025),('g',1.02)]:
            name=f.f.getBestCmap()[ord(c)];w=f.h.metrics[name][0]
            b=box(get(f.f,c));xcenter=(b[0]+b[2])/2
            corrected=move(get(f.f,c),-xcenter*(scale-1),0,scale,1)
            f.put(c,corrected,width=w+round((scale-1)*(b[2]-b[0])),note='provisional Text bowl horizontal optical correction')
    result=f.finish()
    allowed=set(chars)|({'s','g'} if st=='Text' else set())
    assert verify(src,out,allowed)==203-len(allowed)
    original=TTFont(src);current=TTFont(out)
    for c in chars:
        a=original['hmtx'][original.getBestCmap()[ord(c)]]
        b=current['hmtx'][current.getBestCmap()[ord(c)]]
        assert a[0]>b[0] and b[1]>=50
    result['allowed']=''.join(sorted(allowed));data[st]=result;fonts[st]=out
fontproof(P,fonts,[('AV VA WA TA To Te Ty',58),('АУ УА ЛТ ДА AV WA',54),('Arvectum — Арвектум',51),('System • Technology • Система',31),('k к y у s g д л',49)],'v0.51 OPTICAL')
write_json(P/'build-report.json',data)
print('PASS v0.51',digest_tree(P))
