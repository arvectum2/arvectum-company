from pathlib import Path
import ast,csv,json,hashlib,collections,subprocess,unicodedata as ud,re,math
from html.parser import HTMLParser
import numpy as np
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.areaPen import AreaPen
P=Path(__file__).resolve().parent;B=P.parent.parent;R=B.parent
V=P.parent/'Arvectum-Typeface-v0.47'
sha=lambda b:hashlib.sha256(b).hexdigest()
def run(*a):return subprocess.check_output(a,text=True).strip()
class Visible(HTMLParser):
    def __init__(self):super().__init__();self.skip=0;self.parts=[]
    def handle_starttag(self,t,a):
        if t in ('script','style','svg','template'):self.skip+=1
    def handle_endtag(self,t):
        if t in ('script','style','svg','template'):self.skip=max(0,self.skip-1)
    def handle_data(self,d):
        if not self.skip and d.strip():self.parts.append(' '.join(d.split()))
def collect():
    sources=[]
    for repo,name,kind in [(R,'brand/00_Управление/BRAND-PLATFORM-v0.3.md','markdown'),(R,'docs/constitution/COMPANY-CONSTITUTION.md','markdown'),(R,'docs/business/CURRENT-BUSINESS-MODEL-AND-VALUE-PROPOSITION.md','markdown'),(R.parent/'arvectum-site','public/index.html','html')]:
        raw=(repo/name).read_bytes();s=raw.decode()
        if kind=='html':
            p=Visible();p.feed(s);s='\n'.join(p.parts)
        else:
            s=re.sub(r'^\s*[-*#]+\s*','',s,flags=re.M);s=re.sub(r'`|\*\*','',s)
        sources.append({'repository':repo.name,'path':name,'commit':run('git','-C',str(repo),'rev-parse','HEAD'),'source_sha256':sha(raw),'extraction':kind,'text':s})
    # Explicitly synthetic use cases, not actual company documents.
    sources.append({'repository':None,'path':'synthetic use cases','text':'info@arvectum.com https://arvectum.com/a?x=1&y=2 #123 _test / \\ < > ~ ^ ` * © ® ™ § ¶ • € ₽ 1\u202f250\u202f000,00 ₽\nИНН/КПП, № 17, 44-ФЗ, 223-ФЗ, 2026 г.\n'+'Е\u0308 е\u0308 И\u0306 и\u0306 é naïve résumé','extraction':'synthetic'})
    return sources
if not (P/'corpus.json').exists():(P/'corpus.json').write_text(json.dumps(collect(),ensure_ascii=False,indent=2)+'\n')
sources=json.loads((P/'corpus.json').read_text())
def dump(name,data):(P/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
tree=ast.parse((P.parent/'Arvectum-Typeface-v0.32/build.py').read_text())
env={'np':np,'re':re}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'parse','poly','area','cross','intersects','inside','fmt','path'}],type_ignores=[]),'helpers','exec'),env)
poly,area,intersects,inside,path=[env[n] for n in ('poly','area','intersects','inside','path')]
def rec(f,n):
    p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
def normalize(a):
    out=[]
    for op,pts in a:
        if op=='moveTo':start=pts
        if op=='closePath' and out[-1]==('lineTo',start):out.pop()
        out.append((op,pts))
    return out
def commands(a):
    ops={'moveTo':'M','lineTo':'L','curveTo':'C','closePath':'Z'}
    return [(ops[o],[x for p in pts for x in p]) for o,pts in a]
rows=[];report={};coverage=[];pairs=[]
manifest={(r['style'],r['char']):r for r in csv.DictReader((V/'glyph-provenance.csv').open())}
pairset=[('A','А'),('B','В'),('C','С'),('E','Е'),('H','Н'),('K','К'),('M','М'),('O','О'),('P','Р'),('T','Т'),('X','Х'),('a','а'),('c','с'),('e','е'),('o','о'),('p','р'),('x','х'),('y','у'),('k','к')]
for st in ('Display','Text'):
    f=TTFont(next((V/'experimental').glob(f'Arvectum{st}*.otf')));gs=f.getGlyphSet();cm=f.getBestCmap()
    assert len(cm)==182
    win=f['OS/2'];head=f['hhea']
    issues=collections.defaultdict(list)
    for cp,n in sorted(cm.items()):
        c=chr(cp);m=manifest[st,c];source=B/m['source'];assert sha(source.read_bytes())==m['source_sha256'],(st,c)
        a=rec(f,n);b=BoundsPen(gs);gs[n].draw(b);adv,lsb=f['hmtx'][n]
        row={'style':st,'char':c,'unicode':f'U+{cp:04X}','origin':m['origin'],'advance':adv,'lsb':lsb,'xmin':'','ymin':'','xmax':'','ymax':'','rsb':'','ink_area':'','ink_density':'','flags':''};flags=[]
        if b.bounds:
            x0,y0,x1,y1=b.bounds;ap=AreaPen(gs);gs[n].draw(ap);ink=abs(ap.value);rsb=adv-x1
            row.update(xmin=x0,ymin=y0,xmax=x1,ymax=y1,rsb=round(rsb,2),ink_area=round(ink),ink_density=round(ink/((x1-x0)*(y1-y0)),4))
            if min(x0,rsb)<-2:flags.append('negative_bearing')
            if abs(lsb-x0)>1.01:flags.append('lsb_mismatch')
            if y1>win.usWinAscent or -y0>win.usWinDescent:flags.append('win_clip_risk')
            if y1>head.ascent or y0<head.descent:flags.append('hhea_exceeds')
            ps=poly(path(commands(a)))
            if any(area(p)<1 or intersects(p,p,True) for p in ps):flags.append('sampled_self_cross_or_zero')
            if any(intersects(p,q) for i,p in enumerate(ps) for q in ps[i+1:]):flags.append('sampled_contour_cross')
            if c.isalpha() and (adv>2048 or adv<300):flags.append('letter_advance_outlier')
        else:assert c in ' \u00a0\u202f'
        row['flags']=';'.join(flags);rows.append(row)
        for flag in flags:issues[flag].append(c)
    for a,b in pairset:
        na,nb=cm[ord(a)],cm[ord(b)];same=normalize(rec(f,na))==normalize(rec(f,nb));metric=f['hmtx'][na]==f['hmtx'][nb]
        pairs.append({'style':st,'pair':a+'/'+b,'outline_equal':same,'metrics_equal':metric,'review':'intentional or discrepancy requires review' if not (same and metric) else 'match'})
    for s in sources:
        text=s['text'];missing=collections.Counter(c for c in text if not c.isspace() and ord(c) not in cm)
        coverage.append({'style':st,'source':s['path'],'visible_nonspace_count':sum(not c.isspace() for c in text),'missing_occurrences':sum(missing.values()),'missing':[{'char':c,'codepoint':f'U+{ord(c):04X}','name':ud.name(c,'UNKNOWN'),'count':n} for c,n in missing.most_common()]})
    report[st]={'encoded':len(cm),'ink':179,'source_hashes_verified':182,'flags':dict(issues),'hhea':[head.ascent,head.descent],'win':[win.usWinAscent,win.usWinDescent],'font_sha256':sha(Path(f.reader.file.name).read_bytes()),'layout_tables':[n for n in ('GPOS','GSUB','GDEF','kern') if n in f]}
with (P/'glyph-audit.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
dump('audit.json',report);dump('coverage.json',coverage);dump('cross-script.json',pairs)
print(json.dumps(report,ensure_ascii=False,indent=2))
print('Missing (Display):',[(r['source'],r['missing_occurrences'],''.join(x['char'] for x in r['missing'])) for r in coverage if r['style']=='Display'])
print('Pair discrepancies:',[(r['style'],r['pair']) for r in pairs if not(r['outline_equal'] and r['metrics_equal'])])
