"""Scope-gated metric and shaping regression. A PASS here is NOT Windows readiness."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
import subprocess,itertools,json,ast
P=Path(__file__).resolve().parent;BASE=P.parent
TOP='\u0300\u0301\u0302\u0303\u0304\u0306\u0308\u030a';BOTTOM='\u0327'
p53=(BASE/'Arvectum-Typeface-v0.53/kerning.py').read_text()
tree=ast.parse(p53);PAIR=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='pairs' for t in n.targets)))
assert len(PAIR)==57
def shape(p,s,feat=None):
    args=['hb-shape','--output-format=json']
    if feat:args+=['--features='+feat]
    return json.loads(subprocess.check_output(args+[str(p),s],text=True))
out={}
for style in ('Display','Text'):
    pre=next((BASE/'Arvectum-Typeface-v0.58/experimental').glob('Arvectum'+style+'*.otf'))
    new=next((P/'experimental').glob('Arvectum'+style+'*.otf'))
    f=TTFont(new);a=TTFont(pre);cm=f.getBestCmap();assert cm==a.getBestCmap() and len(cm)==212
    bb={}
    for c in TOP+BOTTOM:
        pen=BoundsPen(f.getGlyphSet());f.getGlyphSet()[cm[ord(c)]].draw(pen);bb[c]=pen.bounds
    upper=[]
    for m in itertools.product(TOP,repeat=3):
        s='a'+''.join(m)
        o=shape(pre,s);q=shape(new,s)
        assert len(q)==4 and o==q and all(item['g']!='.notdef' for item in q)
        top_y=max(q[i]['dy']+bb[c][3] for i,c in enumerate(m,1))
        low_y=min(q[i]['dy']+bb[c][1] for i,c in enumerate(m,1))
        assert top_y<=f['OS/2'].usWinAscent and low_y>=-f['OS/2'].usWinDescent
        upper.append((top_y,s))
    bottom=[]
    for n in (2,3,4):
        s='c'+BOTTOM*n
        q=shape(new,s)
        assert q==shape(pre,s) and len(q)==n+1
        lowest=min(q[i]['dy']+bb[BOTTOM][1] for i in range(1,len(q)))
        bottom.append({'count':n,'lowest_ink':round(lowest,2),'within_new_win_descent':-lowest<=f['OS/2'].usWinDescent})
    assert [x['within_new_win_descent'] for x in bottom]==[True,True,False]
    # Four upper marks unsupported by selected limited clipping envelope.
    four='a'+TOP[3]*4
    data=shape(new,four)
    ymax=max(data[i]['dy']+bb[TOP[3]][3] for i in range(1,len(data)))
    assert ymax>f['OS/2'].usWinAscent
    for pair,kern in PAIR.items():
        v=shape(new,pair,'kern=1')
        assert v==shape(pre,pair,'kern=1')
        no=shape(new,pair,'kern=0')
        assert sum(x['ax'] for x in v)-sum(x['ax'] for x in no)==kern
    for s in ('Arvectum — Арвектум', '1\u202f250\u202f000,00 ₽', 'AV To Te АУ ЛТ ДА','a\u0308\u0301','c\u0327\u0327','c\u0327\u0327\u0327'):
        assert shape(pre,s)==shape(new,s)
    out[style]={
     'triples_tested':len(upper),'max_triple_top':round(max(x[0] for x in upper),2),
     'max_triple_sample':max(upper)[1],
     'old_win_ascent':a['OS/2'].usWinAscent,'new_win_ascent':f['OS/2'].usWinAscent,
     'bottom_stacks':bottom,'four_tilde_upper_ink':round(ymax,2),
     'four_mark_support':False,'kerning_pairs_unchanged':len(PAIR),'GPOS_shaping_unchanged':True,
     'typo_metrics':[f['OS/2'].sTypoAscender,f['OS/2'].sTypoDescender,f['OS/2'].sTypoLineGap],
     'hhea_metrics':[f['hhea'].ascent,f['hhea'].descent,f['hhea'].lineGap],
     'win_metrics':[f['OS/2'].usWinAscent,f['OS/2'].usWinDescent],
     'use_typo_metrics_flag':bool(f['OS/2'].fsSelection & 128)}
(P/'qualification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
for st,q in out.items():
 print(st,'triples',q['triples_tested'],'upper',q['max_triple_top'],'bottom',q['bottom_stacks'],'4 mark',q['four_tilde_upper_ink'],'kern',q['kerning_pairs_unchanged'])
