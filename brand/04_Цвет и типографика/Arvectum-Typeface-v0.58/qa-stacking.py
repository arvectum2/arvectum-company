"""Regression QA for GPOS mkmk, all 57 explicit kern pairs, and glyph overlap diagnostics."""
from pathlib import Path
import json,subprocess,sys,itertools,unicodedata,ast
import numpy as np
from PIL import Image,ImageDraw,ImageFont,features
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
P=Path(__file__).resolve().parent;BASE=P.parent
assert features.check('raqm')
node=ast.parse((BASE/'Arvectum-Typeface-v0.53/kerning.py').read_text())
pairs=ast.literal_eval(next(n.value for n in node.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='pairs' for t in n.targets)))
assert len(pairs)==57
top='\u0300\u0301\u0302\u0303\u0304\u0306\u0308\u030a'
def shape(font,text,feat=None):
    args=['hb-shape','--output-format=json']
    if feat:args+=['--features='+feat]
    return json.loads(subprocess.check_output(args+[str(font),text],text=True))
def bounds(font,glyph):
    p=BoundsPen(font.getGlyphSet());font.getGlyphSet()[glyph].draw(p)
    return p.bounds
def ink_overlap(fontpath,pair,at_px=128):
    f=ImageFont.truetype(str(fontpath),at_px)
    shaped=shape(fontpath,pair,'kern=1')
    assert len(shaped)==2
    a,off_a=f.getmask2(pair[0],anchor='ls',mode='L');b,off_b=f.getmask2(pair[1],anchor='ls',mode='L')
    ar=np.frombuffer(bytes(a),dtype=np.uint8).reshape(a.size[1],a.size[0])
    br=np.frombuffer(bytes(b),dtype=np.uint8).reshape(b.size[1],b.size[0])
    # Convert from baseline origin to a common canvas; font units -> px.
    x1,y1=off_a
    x2,y2=round(shaped[0]['ax']*at_px/2048)+off_b[0],off_b[1]
    lo_x=max(x1,x2);hi_x=min(x1+ar.shape[1],x2+br.shape[1])
    lo_y=max(y1,y2);hi_y=min(y1+ar.shape[0],y2+br.shape[0])
    if hi_x<=lo_x or hi_y<=lo_y:return 0
    aa=ar[lo_y-y1:hi_y-y1,lo_x-x1:hi_x-x1]
    bb=br[lo_y-y2:hi_y-y2,lo_x-x2:hi_x-x2]
    return int(np.count_nonzero((aa>128)&(bb>128)))
reports={}
files={}
for st in ('Display','Text'):
    older=next((BASE/'Arvectum-Typeface-v0.57/experimental').glob(f'Arvectum{st}*.otf'))
    newer=next((P/'experimental').glob(f'Arvectum{st}*.otf'))
    f=TTFont(newer);files[st]=(older,newer)
    cm=f.getBestCmap();assert len(cm)==212 and all(ord(c) in cm for c in top)
    b={c:bounds(f,cm[ord(c)]) for c in top}
    before=shape(older,'c\u0327\u0327')
    assert before[1]['dy']==before[2]['dy'] and before[1]['dx']==before[2]['dx']
    tests=[];composed=[];min_gap=1e9;max_top=-1e9
    for base,first,second in itertools.product(('a','е'),top,top):
        sample=base+first+second;data=shape(newer,sample)
        assert all(v['g']!='.notdef' for v in data),(st,sample,data)
        if len(data)==2:
            nfc=unicodedata.normalize('NFC',base+first)
            assert len(nfc)==1 and ord(nfc) in cm and data[0]['g']==cm[ord(nfc)] and data[1]['ax']==0,(st,sample,data)
            composed.append({'sample':sample,'composed_base':nfc,'last_mark_y_offset':data[1]['dy']})
            continue
        assert len(data)==3 and data[1]['ax']==data[2]['ax']==0
        assert data[2]['dy']>data[1]['dy'],(st,sample,data)
        # Vertical ink gap: min bottom of next vs max top of previous.
        gap=data[2]['dy']+b[second][1]-(data[1]['dy']+b[first][3])
        min_gap=min(min_gap,gap)
        max_top=max(max_top,data[2]['dy']+b[second][3])
        assert gap>=80,(st,sample,gap)
        tests.append({'sample':sample,'base':base,'first':f'U+{ord(first):04X}','second':f'U+{ord(second):04X}','vertical_gap':round(gap,1),'top':round(data[2]['dy']+b[second][3],1)})
    # Baseline c + cedilla + cedilla overlaps, new v0.58 separates them.
    bottom_tests=[]
    cedilla='\u0327';cb=bounds(f,cm[ord(cedilla)])
    for base in ('c','e','с','е'):
        seq=base+cedilla+cedilla
        oldq=shape(older,seq);newq=shape(newer,seq)
        assert len(oldq)==len(newq)==3 and oldq[1]['dy']==oldq[2]['dy']
        assert newq[2]['dy']<newq[1]['dy'] and all(x['g']!='.notdef' for x in newq)
        gap=(newq[1]['dy']+cb[1])-(newq[2]['dy']+cb[3])
        lower=newq[2]['dy']+cb[1]
        assert gap>=90 and lower>=-f['OS/2'].usWinDescent,(st,seq,gap,lower)
        bottom_tests.append({'sample':seq,'gap':round(gap,1),'lowest_ink':round(lower,1),'old_overlap':True})
    for sample in ('e\u0327\u0301','e\u0301\u0327','а\u0327\u0303'):
        combo=shape(newer,sample)
        assert len(combo)==3 and all(x['g']!='.notdef' for x in combo) and combo[1]['dy']!=combo[2]['dy']
    assert all(shape(newer,samp)==shape(older,samp) for samp in ('a\u0308\u0301','e\u0302\u0301','u\u030a\u0301'))
    # Triple combinations can exceed Windows ascent or descent. Record risk.

    triples=[]
    for sample in ('a\u0303\u0303\u0303','e\u0302\u0308\u0301','е\u0308\u0301\u0308'):
        data=shape(newer,sample);top_y=data[-1]['dy']+b[sample[-1]][3]
        triples.append({'sample':sample,'top':top_y,'win_ascent':f['OS/2'].usWinAscent,'exceeds_win_ascent':top_y>f['OS/2'].usWinAscent})
    low_seq='c\u0327\u0327\u0327'
    low=shape(newer,low_seq)
    deepest=low[-1]['dy']+cb[1]
    assert -deepest>f['OS/2'].usWinDescent
    pairs_checked={}
    overlaps=[]
    for pair,expected in pairs.items():
        initial=shape(older,pair,'kern=1');final=shape(newer,pair,'kern=1')
        plain=shape(newer,pair,'kern=0')
        assert len(initial)==len(final)==len(plain)==2
        assert initial==final,(st,pair,'kern regression')
        delta=sum(v['ax'] for v in final)-sum(v['ax'] for v in plain)
        assert delta==expected,(st,pair,delta,expected)
        collision=ink_overlap(newer,pair,128)
        if collision:overlaps.append({'pair':pair,'ink_overlap_pixels_128px':collision})
        pairs_checked[pair]={'kern_delta':delta,'raster_overlap_pixels_128px':collision}
    for sample in ('0123456789','1\u202f250\u202f000 ₽','Арвектум — Arvectum'):
        assert shape(newer,sample)==shape(older,sample),(st,sample)
    reports[st]={'top_mark_stacks_tested':len(tests),'precomposed_cases':composed,'bottom_mark_tests':bottom_tests,'triple_bottom_ink_low':round(deepest,1),'triple_bottom_exceeds_win_descent':True,'minimum_vertical_ink_gap':min_gap,'maximum_double_mark_top':max_top,
                 'double_stacks_within_win_ascent':max_top<=f['OS/2'].usWinAscent,
                 'triple_stack_probes':triples,'kern_pairs_tested':len(pairs_checked),'kerning_raster_overlaps':overlaps,
                 'pair_details':pairs_checked,'mark_pair_details':tests,
                 'codepoints':212,'control_no_change':True,'prior_overlapping_sample':before}
    print(st,'top stacks / bottom marks',len(tests),'min gap',min_gap,'max top',max_top,'kern pairs',len(pairs_checked),'ink overlaps',overlaps[:15],'triple',triples)
(P/'stack-and-kern-qa.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n')
# Side by side proof of the *actual* versioned OTF at consistent pixel sizes.
im=Image.new('RGB',(1940,1380),'white');d=ImageDraw.Draw(im)
label='/System/Library/Fonts/Supplemental/Arial.ttf';caption=lambda sz:ImageFont.truetype(label,sz)
d.text((28,16),'ARVECTUM GOLDEN STEP  /  v0.58  /  top+bottom mkmk QA',font=caption(34),fill='#001432')
d.text((28,65),'Baseline v0.57 vs candidate v0.58.  Preserved outlines; changed OpenType positioning.',font=caption(21),fill='#475569')
samples=[('c\u0327\u0327  e\u0327\u0327  а\u0327\u0327',63),('c\u0327\u0327\u0327   e\u0327\u0301   a\u0308\u0301',60),('c\u0327\u0327   e\u0327\u0301   A\u030a\u0301',46),('AV  VA  To  Te  АУ  ЛТ  ДА',50),('Арвектум — 1\u202f250\u202f000,00 ₽',39),('c\u0327\u0327  a\u0308\u0301  е\u0308\u0301 — 14 px readability',23)]
for i,st in enumerate(('Display','Text')):
    x=i*970+25
    d.line((x,117,x+900,117),fill='#cbd5e1',width=2)
    d.text((x,130),st+' / stacked accents',font=caption(26),fill='#001432')
    y=175
    for fontpath,label_text in zip(files[st],('v0.57 / bottom overlap', 'v0.58 / bottom mkmk')):
        d.text((x,y),label_text,font=caption(20),fill='#475569');y+=34
        for line,size in samples:
            # The font deliberately does not map precomposed Å; use a decomposed A.
            line=line.replace('Å\u0301','A\u030a\u0301')
            ft=ImageFont.truetype(str(fontpath),size)
            assert d.textlength(line,font=ft)<925,(st,label_text,line,size,d.textlength(line,font=ft))
            d.text((x,y),line,font=ft,fill='#001432')
            y+=max(46,size+24)
        y+=20
im.save(P/'stack-and-kern-proof.png')
print('PASS mark-stack, kerning and proof',P/'stack-and-kern-proof.png')
