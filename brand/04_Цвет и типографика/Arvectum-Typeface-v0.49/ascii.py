from pathlib import Path
from pipeline import Family,PHI,BASE,rect,ellipse,polygon,add,move,rotate,get,box,verify,write_json,digest_tree,fontproof,sha
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform
import math,json,subprocess
P=Path(__file__).resolve().parent;OUT=P/'experimental';OUT.mkdir(exist_ok=True)
scope='#&*/<>@\\^_`~'
assert len(scope)==12
def slash(t,forward=True,height=1490,width=950):
    x=950;dx=height/PHI;th=t*math.sqrt(1+(1/PHI)**2)
    pp=polygon((100,0),(100+th,0),(100+th+dx,height),(100+dx,height))
    if not forward: pp=move(pp,width,0,-1,1)
    return pp
def star(t,cx=390,cy=840):
    p=RecordingPen();r=t*1.45;r2=t*.48
    pts=[(cx+(r if j%2==0 else r2)*math.cos(math.pi*j/6),
          cy+(r if j%2==0 else r2)*math.sin(math.pi*j/6)) for j in range(12)]
    return polygon(*pts)
def wedge(t,w=850,y=750,left=True):
    p=polygon((w,y+470),(0,y+100),(0,y-100),(w,y-470),(w,y-470+t*1.1),(t*1.9,y),(w,y+470-t*1.1))
    return p if left else move(p,w,0,-1,1)
def wave(t):
    p=RecordingPen();p.moveTo((70,660));p.curveTo((290,850),(500,850),(710,670))
    p.lineTo((710,670+t*.62));p.curveTo((500,850+t*.85),(290,850+t*.85),(70,660+t*.62));p.closePath();return p
def atsign(f,t,k):
    circ=get(f,'C');c0=box(circ)
    roundc=move(circ,75-c0[0]*.82,-20-c0[1]*.82,.82,.82)
    a=get(f,'a');ab=box(a);small=move(a,425-ab[0]*.70,345-ab[1]*.70,.70,.70)
    bar=rect(915,420,t*.70,670)
    return add(roundc,small,bar)
def ampersand(f,t):
    eight=get(f,'8');x=box(eight);s=move(eight,105-x[0]*.82,65-x[1]*.82,.82,.82)
    tail=polygon((735,65),(930,65),(1195,650),(1010,650))
    return add(s,tail)
def glyphs(f):
    t=f.t;w=1120;Y=720
    # Two parallel stems and two crossbars. Intersections explicitly recorded as
    # composite artwork: require separate overlap QA rather than topology claims.
    hashmark=add(rect(345,0,t*.75,1490),rect(695,0,t*.75,1490),rect(120,495,1000,t*.56),rect(120,935,1000,t*.56))
    caret=polygon((40,710),(490,1490),(935,710),(755,710),(490,1180),(220,710))
    return {'#':hashmark,'&':ampersand(f.f,t),'*':star(t),
            '/':slash(t),'<':wedge(t,left=True),'>':wedge(t,left=False),
            '@':atsign(f.f,t,f.k),'\\':slash(t,False),
            '^':caret,'_':rect(35,-130,1050,t*.72),
            '`':polygon((110,1600),(110+t*.85,1600),(110+t*1.65,1600-t*1.65),(110+t*.75,1600-t*1.65)),
            '~':wave(t)}
r={};fonts={}
for st in ('Display','Text'):
    source=next((BASE/'Arvectum-Typeface-v0.47/experimental').glob(f'Arvectum{st}*.otf'))
    dest=OUT/('Arvectum'+st+'GoldenStepDraft049-'+('Medium' if st=='Display' else 'Regular')+'.otf')
    family=Family(st,49,source,dest)
    forms=glyphs(family)
    assert set(forms)==set(scope)
    for ch,pen in forms.items():
        b=box(pen)
        family.put(ch,pen,max(math.ceil(b[2]+115),600),note='golden draft ASCII')
    result=family.finish()
    assert result['codepoints']==194
    assert verify(source,dest,set(scope))==182
    cm=TTFont(dest).getBestCmap()
    assert all(c in cm for c in range(32,127))
    shaped=json.loads(subprocess.check_output(['hb-shape','--output-format=json',str(dest),'info@arvectum.com & /api/v1/test?a=1#ok'],text=True))
    assert len(shaped)==len('info@arvectum.com & /api/v1/test?a=1#ok') and not any(x['g']=='.notdef' for x in shaped)
    r[st]=result;fonts[st]=dest
fontproof(P,fonts,[('info@arvectum.com',51),('https://arvectum.com/api/v1',39),('# & * / < > @ \\ ^ _ ` ~',51),('Arvectum — Арвектум',48)],'v0.49 ASCII')
write_json(P/'build-report.json',r)
print('PASS v0.49',r['Display']['codepoints'],r['Text']['codepoints'],digest_tree(P))
