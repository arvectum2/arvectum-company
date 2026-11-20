"""Additive/revision CFF pipeline for Golden Step; keep original inputs immutable."""
from pathlib import Path
import json,math,hashlib,subprocess
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.misc.transform import Transform
from fontTools.pens.transformPen import TransformPen
from PIL import Image,ImageDraw,ImageFont
PHI=(1+math.sqrt(5))/2
BASE=Path(__file__).resolve().parent.parent
ENV={'PYTHONPATH':'/Users/master/.cache/uv/archive-v0/uc0JJVE_R9CFd-Am'}
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(commands):
    p=RecordingPen()
    for op,pts in commands:
        getattr(p,op)(*pts) if op!='closePath' else p.closePath()
    return p
def polygon(*pts):
    p=RecordingPen();p.moveTo(pts[0])
    for x in pts[1:]:p.lineTo(x)
    p.closePath();return p
def rect(x,y,w,h):return polygon((x,y),(x+w,y),(x+w,y+h),(x,y+h))
def ellipse(cx,cy,rx,ry,k):
    p=RecordingPen();p.moveTo((cx+rx,cy))
    p.curveTo((cx+rx,cy+k*ry),(cx+k*rx,cy+ry),(cx,cy+ry))
    p.curveTo((cx-k*rx,cy+ry),(cx-rx,cy+k*ry),(cx-rx,cy))
    p.curveTo((cx-rx,cy-k*ry),(cx-k*rx,cy-ry),(cx,cy-ry))
    p.curveTo((cx+k*rx,cy-ry),(cx+rx,cy-k*ry),(cx+rx,cy));p.closePath();return p
def add(*pens):
    p=RecordingPen()
    for a in pens:a.replay(p)
    return p
def move(p,x=0,y=0,sx=1,sy=1):
    out=RecordingPen();p.replay(TransformPen(out,Transform(sx,0,0,sy,x,y)));return out
def rotate(p,angle,cx,cy):
    co=math.cos(angle);si=math.sin(angle)
    t=Transform(1,0,0,1,-cx,-cy).transform(Transform(co,si,-si,co,0,0)).transform(Transform(1,0,0,1,cx,cy))
    out=RecordingPen();p.replay(TransformPen(out,t));return out
def box(p):
    q=BoundsPen(None);p.replay(q);return q.bounds
def get(f,c):
    p=RecordingPen();f.getGlyphSet()[f.getBestCmap()[ord(c)]].draw(p);return p
def svg(dest,pen):
    b=box(pen);assert b is not None
    x0,y0,x1,y1=b;out=SVGPathPen(None);pen.replay(out)
    dest=Path(dest);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.7f} {-y1:.7f} {x1-x0:.7f} {y1-y0:.7f}"><path fill="#001432" fill-rule="evenodd" transform="scale(1 -1)" d="{out.getCommands()}"/></svg>\n')
class Family:
    def __init__(self,style,version,input_file,output):
        self.style=style;self.version=version;self.source=Path(input_file);self.output=Path(output)
        self.output.parent.mkdir(parents=True,exist_ok=True)
        self.f=TTFont(self.source);self.order=list(self.f.getGlyphOrder())
        self.h=self.f['hmtx'];self.hh=self.f['hhea'];self.maxp=self.f['maxp'];self.cm=self.f['cmap'];self.cff=self.f['CFF '].cff.topDictIndex[0]
        self.gset=self.f.getGlyphSet();self.scope={};self.step=self.f['OS/2'].usWeightClass
        self.t=200.59127 if style=='Display' else 185.435
        self.b=190.77974 if style=='Display' else 175
        self.k=1/PHI if style=='Display' else .5522847498
        self.name=f'Arvectum{style}GoldenStepDraft{version:03d}-'+('Medium' if style=='Display' else 'Regular')
    def put(self,ch,pen,width=None,lsb=None,note='draft'):
        assert len(ch)==1 and box(pen) is not None
        cp=ord(ch);name=self.f.getBestCmap().get(cp,f'uni{cp:04X}')
        isnew=name not in self.order
        if width is None:
            width=self.h.metrics[name][0] if not isnew else math.ceil(box(pen)[2]+110)
        if lsb is None:lsb=round(box(pen)[0])
        width=int(round(width));assert width>0
        tt=T2CharStringPen(width,None);pen.replay(tt);cs=tt.getCharString();cs.private=self.cff.Private;cs.globalSubrs=self.f['CFF '].cff.GlobalSubrs
        if isnew:
            self.cff.CharStrings.charStrings[name]=len(self.cff.CharStrings.charStringsIndex)
            self.cff.CharStrings.charStringsIndex.items.append(cs);self.cff.charset.append(name);self.order.append(name)
            for t in self.cm.tables:
                if t.isUnicode():t.cmap[cp]=name
        else:
            idx=self.cff.CharStrings.charStrings[name]
            self.cff.CharStrings.charStringsIndex.items[idx]=cs
        self.h.metrics[name]=(width,round(lsb))
        self.scope[ch]={'type':'added' if isnew else 'revised','codepoint':f'U+{cp:04X}','width':width,'lsb':round(lsb),'note':note}
        svg(self.output.parent.parent/'glyphs'/self.style/f'U+{cp:04X}.svg',pen)
    def metrics(self,ch,width,lsb=None):
        name=self.f.getBestCmap()[ord(ch)]
        a,b=self.h.metrics[name];self.h.metrics[name]=(round(width),b if lsb is None else round(lsb))
        self.scope[ch]={'type':'metrics','codepoint':f'U+{ord(ch):04X}','old_width':a,'new_width':round(width),'note':'optical spacing candidate'}
    def finish(self):
        self.f.setGlyphOrder(self.order);self.maxp.numGlyphs=len(self.order);self.hh.numberOfHMetrics=len(self.order)
        self.f['head'].fontRevision=round(self.version/1000,3)
        family=f'Arvectum {self.style} Golden Step Draft {self.version:03d}'
        sub='Medium' if self.style=='Display' else 'Regular'
        names=self.f['name']
        for i,s in [(1,family),(2,sub),(3,self.name+';'+str(self.version)),(4,family+' '+sub),(5,'Version 0.'+f'{self.version:03d}'),(6,self.name)]:
            names.setName(s,i,3,1,0x409);names.setName(s,i,1,0,0)
        self.cff.FamilyName=family;self.cff.FullName=family+' '+sub;self.cff.version='0.'+str(self.version).zfill(3)
        self.f.recalcTimestamp=False;self.f['head'].created=self.f['head'].modified=3877564800
        self.f.save(self.output)
        check=TTFont(self.output);assert check['maxp'].numGlyphs==len(check.getGlyphOrder())
        assert len(check.getBestCmap())==len(self.f.getBestCmap())
        assert check['OS/2'].usWeightClass==self.step
        return {'file':self.output.name,'sha256':sha(self.output),'input':str(self.source.name),'input_sha256':sha(self.source),'scope':self.scope,'codepoints':len(check.getBestCmap())}
def verify(old,new,changed):
    a=TTFont(old);b=TTFont(new);A=a.getBestCmap();B=b.getBestCmap()
    assert set(A)<=set(B)
    untouched=0
    for c,n in A.items():
        if chr(c) in changed:continue
        x=RecordingPen();y=RecordingPen();a.getGlyphSet()[n].draw(x);b.getGlyphSet()[B[c]].draw(y)
        assert x.value==y.value,(c,old,new)
        assert a['hmtx'][n]==b['hmtx'][B[c]],(c,'metrics')
        untouched+=1
    return untouched
def write_json(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def digest_tree(root):
    root=Path(root);files=sorted(x for x in root.rglob('*') if x.is_file() and x.name!='SHA256SUMS.txt')
    (root/'SHA256SUMS.txt').write_text(''.join(f'{sha(f)}  {f.relative_to(root)}\n' for f in files))
    return len(files)
def fontproof(dir,styles,lines,title):
    image=Image.new('RGB',(1950,1120),'white');d=ImageDraw.Draw(image)
    for i,st in enumerate(('Display','Text')):
        fontfile=styles[st];d.text((25+i*975,20),title+' — '+st,fill='#001432',font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',26))
        y=95
        for line,size in lines:
            ft=ImageFont.truetype(str(fontfile),size)
            assert d.textlength(line,font=ft)<940,(line,st)
            assert all(ord(c) in TTFont(fontfile).getBestCmap() for c in line)
            d.text((25+i*975,y),line,fill='#001432',font=ft);y+=max(size+25,62)
    image.save(Path(dir)/'proof.png')
    return str(Path(dir)/'proof.png')
