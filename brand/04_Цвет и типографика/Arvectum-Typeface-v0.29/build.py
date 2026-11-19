from pathlib import Path
import ast,math,hashlib,json,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent
S=P.parent.parent/'02_Концепции/Vector-Hybrid-v0.25/glyphs'
V=P.parent/'Arvectum-Typeface-v0.28'
Q=P.parent/'Arvectum-Typeface-v0.27'
names={'parse','tok','fmt','serialize','polygon','width_at','gap_report','check'}
ns={'re':__import__('re'),'ET':ET,'NS':'{http://www.w3.org/2000/svg}'}
src=ast.parse((Q/'build.py').read_text())
exec(compile(ast.Module(body=[n for n in src.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(Q/'build.py'),'exec'),ns)
parse,tok,fmt,serialize,polygon,check=[ns[n] for n in ('parse','tok','fmt','serialize','polygon','check')]
phi=(1+5**.5)/2
chars='nmhuпмиш'
results={};examples={}
def spans(p,y):
    x=sorted(a+(c-a)*(y-b)/(d-b) for (a,b),(c,d) in zip(p,p[1:]) if min(b,d)<=y<max(b,d))
    assert len(x)%2==0,(y,x)
    return [round(x[i+1]-x[i],4) for i in range(0,len(x),2)]
def gaps(p,y):
    x=sorted(a+(c-a)*(y-b)/(d-b) for (a,b),(c,d) in zip(p,p[1:]) if min(b,d)<=y<max(b,d))
    return [round(x[i+1]-x[i],4) for i in range(1,len(x)-1,2)]
def normal_thickness(dx,dy,offset):return offset*dx/math.hypot(dx,dy)
for style,t in [('Display',200.59127),('Text',185.435)]:
    group={};ex={}
    for ch in chars:
        f=(V/'candidates'/style/'C-compact'/'U+006D.svg') if ch=='m' else S/style/f'U+{ord(ch):04X}.svg'
        e,p=parse(f);w=float(e.get('viewBox').split()[2]);a=tok(p.get('d'))
        check(a,w); poly=polygon(a)
        # Normalize the actual SVG transform onto common x-height/baseline.
        if ch=='u':poly=[(w-x,1056-y) for x,y in poly]
        bounds=[round(min(x for x,y in poly),4),round(min(y for x,y in poly),4),round(max(x for x,y in poly),4),round(max(y for x,y in poly),4)]
        assert bounds[0]==0 and abs(bounds[2]-w)<.001
        group[ch]={'source':str(f.relative_to(P.parent.parent)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'width':w,'bbox':bounds,'ink_spans_y':{str(y):spans(poly,y) for y in (100,500,800,950)},'counter_gaps_y':{str(y):gaps(poly,y) for y in (100,500,800,950)}}
        ex[ch]=(w,a)
    # Stem baselines; lower-case n/h share contours, u is a 180-degree reflection.
    n=ex['n'][1];h=ex['h'][1];u=ex['u'][1]
    assert n==u and h[:1]+[n[1]]+h[2:]==n
    for ch,y,count in [('n',950,2),('h',950,2),('u',100,2),('m',950,3),('п',950,2),('ш',100,3)]:
        vals=group[ch]['ink_spans_y'][str(y)];assert len(vals)==count and all(abs(v-t)<.002 for v in vals),(ch,vals)
    for ch,y in [('m',950),('ш',100)]:
        vals=group[ch]['counter_gaps_y'][str(y)];assert len(vals)==2 and abs(vals[0]-vals[1])<.002
    # Cyrillic diagonal geometry measured from actual path vertices.
    ia=ex['и'][1];ma=ex['м'][1]
    i0=ia[1][1][0];iy=ia[2][1][0];i2=ia[3][1][0]
    dx=i2-i0;dy=iy;it=normal_thickness(dx,dy,1056-dy)
    # outer and inner left slope m; unequal slopes imply changing perpendicular stroke weight.
    m0=ma[2][1][0]; mc,my=ma[3][1];mlx,mly=ma[-2][1] if ma[-2][0]=='L' else (0,0)
    left_dx=mc-m0
    # explicit inner vertices from path token sequence
    lower=next(v for o,v in ma if o=='L' and abs(v[0]-(t))<.001 and v[1]>100)
    inner_tip=[ma[10][1][0],ma[9][1][1]]
    angle=lambda dx,dy:math.degrees(math.atan2(abs(dy),abs(dx)))
    results[style]={'glyphs':group,'stem_target':t,'n_h_share_geometry':True,'u_rotated_n':True,'golden_angle_deg':round(math.degrees(math.atan(phi)),4),'и':{'angle_deg':round(angle(dx,dy),4),'normal_thickness':round(it,4),'ratio_to_stem':round(it/t,5)},'м':{'outer_left_angle_deg':round(angle(left_dx,my),4),'inner_left_angle_deg':round(angle(inner_tip[0]-lower[0],inner_tip[1]-lower[1]),4)}}
    examples[style]=ex
W,H=1620,960
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="white"/>']
def text(x,y,s,size=18):parts.append(f'<text x="{x}" y="{y}" font-family="Arial" font-size="{size}" fill="#334155">{s}</text>')
def glyph(x,base,sc,ch,w,a):
    norm=f'translate({w} 1056) rotate(180)' if ch=='u' else ''
    parts.append(f'<g transform="translate({x} {base-1056*sc}) scale({sc})"><path d="{serialize(a)}" transform="{norm}" fill="#001432" fill-rule="evenodd"/></g>')
text(30,40,'Arvectum Typeface v0.29 | shoulder and joint family | working candidates',24)
for ri,(style,ex) in enumerate(examples.items()):
    top=80+ri*425; base=top+206
    text(30,top+12,style,22)
    for i,ch in enumerate(chars):
        x=30+198*i;w,a=ex[ch];sc=.12
        parts.append(f'<path d="M{x} {base}h188 M{x} {base-1056*sc}h188" stroke="#cbd5e1" stroke-width="1"/>')
        glyph(x+(188-w*sc)/2,base,sc,ch,w,a)
        text(x+65,base+26,f'{ch} U+{ord(ch):04X}',15)
    for sc,dy,run in ((.053,318,'nhmumnh пмишпмиш'),(.020,365,'nhmumnh пмишпмиш nhmumnh пмишпмиш')):
        x=35
        for ch in run:
            if ch==' ':x+=400*sc;continue
            w,a=ex[ch];glyph(x,top+dy,sc,ch,w,a);x+=(w+135)*sc
    q=results[style];text(35,top+405,f"и diagonal {q['и']['angle_deg']:.2f} deg | м outer / inner {q['м']['outer_left_angle_deg']:.2f} / {q['м']['inner_left_angle_deg']:.2f} deg | golden {q['golden_angle_deg']:.2f} deg",16)
parts.append('</svg>')
(P/'family-proof.svg').write_text(''.join(parts));ET.parse(P/'family-proof.svg')
(P/'geometry.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
for style,q in results.items():
    print(style,q['и'],q['м'])
    for ch in chars:
        print(ch,q['glyphs'][ch]['bbox'],q['glyphs'][ch]['ink_spans_y'])
