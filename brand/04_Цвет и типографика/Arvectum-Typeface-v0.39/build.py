from pathlib import Path
import csv,json,hashlib,collections,string,xml.etree.ElementTree as ET
from fontTools.ttLib import TTFont
from fontTools.fontBuilder import FontBuilder
from fontTools.svgLib.path import parse_path
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.reverseContourPen import ReverseContourPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.areaPen import AreaPen
from fontTools.pens.pointInsidePen import PointInsidePen
from fontTools.misc.transform import Transform
P=Path(__file__).resolve().parent;B=P.parent.parent
NS='{http://www.w3.org/2000/svg}'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
src=P.parent/'Arvectum-Typeface-v0.36/sources';provenance=json.loads((src/'provenance.json').read_text())
for n,v in provenance['files'].items():assert sha(src/n)==v['sha256']
rows=list(csv.DictReader((P.parent/'Arvectum-Typeface-v0.35/integration-manifest.csv').open()))
assert len(rows)==236
alphabet=''.join(r['char'] for r in rows if r['style']=='Display')
assert len(alphabet)==118 and len(set(alphabet))==118
punct='.,:;!?…–—-‐‑«»“”‘’„‚"\'()[]{}'
math='+=−×÷±≠≤≥≈%‰°№'
currency='₽$€£¥₴¢'
assert list(map(len,(punct,math,currency)))==[28,14,7]
target=alphabet+string.digits+punct+math+currency
assert len(target)==177 and len(set(target))==177
chars=target+' \u00a0\u202f'
raw_manifest=[];report={}
def record_svg(path,version,ch):
    r=ET.parse(path).getroot();p=r.find(NS+'path');assert p is not None
    rec=RecordingPen();parse_path(p.get('d'),rec)
    if version in ('current-candidate-v0.25','current-candidate-v0.28','current-candidate-v0.30'):
        tr=Transform(-1,0,0,1,945,0) if ch=='u' else Transform(1,0,0,-1,0,1056)
    else:tr=Transform()
    norm=RecordingPen();rec.replay(TransformPen(norm,tr))
    contours=[];cur=None
    for op,args in norm.value:
        if op=='moveTo':assert cur is None;cur=RecordingPen()
        assert cur is not None;cur.value.append((op,args))
        if op=='closePath':contours.append(cur);cur=None
    assert cur is None and contours,path
    fixed=RecordingPen()
    for i,c in enumerate(contours):
        a=AreaPen(None);c.replay(a);assert abs(a.value)>1e-6,path
        pt=c.value[0][1][0];depth=0
        for j,o in enumerate(contours):
            if i==j:continue
            test=PointInsidePen(None,pt,evenOdd=True);o.replay(test);depth+=int(test.getResult())
        c.replay(fixed if (a.value>0)==(depth%2==0) else ReverseContourPen(fixed))
    return fixed
def bounds(rec):
    pen=BoundsPen(None);rec.replay(pen);return pen.bounds
def translated(rec,x):
    rr=RecordingPen();rec.replay(TransformPen(rr,Transform(1,0,0,1,x,0)));return rr
def cs(rec,width):
    pen=T2CharStringPen(width,None);rec.replay(pen);return pen.getCharString()
def glyph_name(ch):return 'space' if ch==' ' else f'uni{ord(ch):04X}'
for style,weight,base_name,side,digit_width in [('Display',500,'InterDisplay-Medium.otf',100,1323),('Text',400,'InterDisplay-Regular.otf',105,1266)]:
    base=TTFont(src/base_name);assert base['head'].unitsPerEm==2048 and base['OS/2'].sxHeight==1056
    assert '4.001' in base['name'].getDebugName(5) and base['OS/2'].usWeightClass==weight
    cmap=base.getBestCmap();gs=base.getGlyphSet()
    own={r['char']:r for r in rows if r['style']==style}
    outc={};metrics={};cmapout={};counts=collections.Counter()
    rec=RecordingPen();gs['.notdef'].draw(rec);outc['.notdef']=cs(rec,base['hmtx']['.notdef'][0]);metrics['.notdef']=base['hmtx']['.notdef']
    for ch in chars:
        n=glyph_name(ch);orig=cmap[ord(ch)];r=own.get(ch);path=None
        override=P/'glyphs'/style/f'U+{ord(ch):04X}.svg'
        bowl=P.parent/'Arvectum-Typeface-v0.38/glyphs'/style/f'U+{ord(ch):04X}.svg'
        previous=P.parent/'Arvectum-Typeface-v0.37/glyphs'/style/f'U+{ord(ch):04X}.svg'
        if override.is_file():
            path=override;state='straight_candidate_v039';version='v0.39'
        elif bowl.is_file():
            path=bowl;state='bowl_candidate_v038';version='v0.38'
        elif previous.is_file():
            path=previous;state='rounded_candidate_v037';version='v0.37'
        elif r and r['path']:
            path=B/r['path'];assert sha(path)==r['sha256']
            state=r['coverage'];version=r['version']
        elif style=='Display' and r and r['wordmark_C_reference']:
            path=B/(r['wordmark_candidate'] or r['wordmark_C_reference']);state='wordmark_adaptation_draft';version='v0.34-L' if r['wordmark_candidate'] else 'v0.21-C'
        else:state='upstream_fallback';version='Inter 4.001'
        if path:
            rec=record_svg(path,version,ch);b=bounds(rec);assert b
            if state=='legacy_only' or (state=='straight_candidate_v039' and ch=='Н'):
                width=round(float(ET.parse(path).getroot().get('viewBox').split()[2]));lsb=round(b[0]);assert width>=b[2],(ch,width,b)
            else:
                rec=translated(rec,side-b[0]);b=bounds(rec);lsb=round(b[0]);width=round(b[2]+side)
        else:
            rec=RecordingPen();gs[orig].draw(rec);width,lsb=base['hmtx'][orig]
            if ch in string.digits:
                offset=round((digit_width-width)/2);rec=translated(rec,offset);lsb+=offset;width=digit_width
        assert width>0,(style,ch,width)
        b=bounds(rec);assert b is None or all(abs(v)<3500 for v in b),(style,ch,b)
        outc[n]=cs(rec,width);metrics[n]=(width,lsb);cmapout[ord(ch)]=n;counts[state]+=1
        raw_manifest.append({'style':style,'char':ch,'unicode':f'U+{ord(ch):04X}','origin':state,'source_version':version,'source':str(path.relative_to(B)) if path else base_name,'source_sha256':sha(path) if path else provenance['files'][base_name]['sha256'],'advance':width,'lsb':lsb,'bbox':b})
    assert len(cmapout)==180
    family='Arvectum '+style+' Golden Step Draft 039';sub='Medium' if weight==500 else 'Regular';ps='Arvectum'+style+'GoldenStepDraft039-'+sub
    fb=FontBuilder(2048,isTTF=False)
    fb.setupGlyphOrder(list(outc));fb.setupCharacterMap(cmapout)
    fb.setupCFF(ps,{'FamilyName':family,'FullName':family+' '+sub,'Weight':sub,'version':'0.39','Notice':'Derived from Inter, Copyright (c) 2016 The Inter Project Authors; SIL OFL 1.1'},outc,{})
    fb.setupHorizontalMetrics(metrics);fb.setupHorizontalHeader(ascent=1984,descent=-494,lineGap=0)
    fb.setupNameTable({'familyName':family,'styleName':sub,'uniqueFontIdentifier':ps+';0.39','fullName':family+' '+sub,'psName':ps,'version':'Version 0.039','copyright':'Derived from Inter, Copyright (c) 2016 The Inter Project Authors. SIL OFL 1.1. Arvectum reconstruction draft.','licenseDescription':'SIL Open Font License, Version 1.1','licenseInfoURL':'https://openfontlicense.org/'})
    fb.setupOS2(sTypoAscender=1984,sTypoDescender=-494,sTypoLineGap=0,usWinAscent=2048,usWinDescent=600,usWeightClass=weight,sCapHeight=1490,sxHeight=1056,fsSelection=64 if weight==400 else 0)
    fb.setupPost();fb.font['head'].fontRevision=.039
    fb.font.recalcTimestamp=False;fb.font['head'].created=fb.font['head'].modified=3877564800
    dest=P/'experimental'/(ps+'.otf');fb.save(dest)
    f=TTFont(dest);assert f.getBestCmap()==cmapout and f['OS/2'].usWeightClass==weight
    assert all(f['hmtx'][cmapout[ord(c)]][0]==digit_width for c in string.digits)
    assert not any(t in f for t in ('GPOS','GSUB'))
    for c,n in cmapout.items():
        check=BoundsPen(f.getGlyphSet());f.getGlyphSet()[n].draw(check)
        assert (check.bounds is None)==(chr(c) in ' \u00a0\u202f'),(style,c,check.bounds)
    report[style]={'counts':dict(counts),'codepoints':len(cmapout),'digit_advance':digit_width,'upstream':base['name'].getDebugName(5),'file':dest.name,'sha256':sha(dest)}
    print(style,report[style])
with (P/'glyph-provenance.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(raw_manifest[0]),lineterminator='\n');w.writeheader();w.writerows(raw_manifest)
(P/'build-report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
