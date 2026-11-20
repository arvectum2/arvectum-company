from pathlib import Path
import sys,json,subprocess,os
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parent/'Arvectum-Typeface-v0.49'))
from pipeline import Family,BASE,rect,polygon,ellipse,add,box,svg,sha,get,verify,write_json,digest_tree
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
scope='\u0300\u0301\u0302\u0303\u0304\u0306\u0308\u030a\u0327'
def glyphs(t,k):
    acute=polygon((-68,35),(60,35),(230,268),(102,268))
    breve=RecordingPen()
    breve.moveTo((-250,243));breve.curveTo((-230,65),(-120,18),(0,18))
    breve.curveTo((120,18),(230,65),(250,243))
    breve.lineTo((132,243));breve.curveTo((120,157),(55,135),(0,135))
    breve.curveTo((-55,135),(-120,157),(-132,243));breve.closePath()
    dots=add(rect(-194,35,130,155),rect(64,35,130,155))
    grave=polygon((68,35),(-60,35),(-230,268),(-102,268))
    circumflex=polygon((-245,45),(0,268),(245,45),(150,45),(0,165),(-150,45))
    tilde=RecordingPen()
    tilde.moveTo((-235,90));tilde.curveTo((-80,265),(30,265),(235,100))
    tilde.lineTo((235,215));tilde.curveTo((30,365),(-80,365),(-235,205));tilde.closePath()
    macron=rect(-220,90,440,100)
    ring=add(ellipse(0,145,152,145,k),ellipse(0,145,65,58,k))
    cedilla=polygon((-58,0),(62,0),(92,-170),(-30,-300),(-145,-300),(-145,-190),(-55,-190),(-10,-145))
    return {'\u0300':grave,'\u0301':acute,'\u0302':circumflex,'\u0303':tilde,
            '\u0304':macron,'\u0306':breve,'\u0308':dots,'\u030a':ring,'\u0327':cedilla}
def inject_mark(f,ch,pen):
    cp=ord(ch);name=f'uni{cp:04X}';assert cp not in f.f.getBestCmap()
    t=T2CharStringPen(0,None);pen.replay(t)
    cs=t.getCharString();cs.private=f.cff.Private;cs.globalSubrs=f.f['CFF '].cff.GlobalSubrs
    f.cff.CharStrings.charStrings[name]=len(f.cff.CharStrings.charStringsIndex)
    f.cff.CharStrings.charStringsIndex.items.append(cs);f.cff.charset.append(name);f.order.append(name)
    f.h.metrics[name]=(0,round(box(pen)[0]))
    for sub in f.cm.tables:
        if sub.isUnicode():sub.cmap[cp]=name
    f.scope[ch]={'type':'combining_mark','codepoint':f'U+{cp:04X}','advance':0}
    svg(f.output.parent.parent/'glyphs'/f.style/f'U+{cp:04X}.svg',pen)
r={}
for st in ('Display','Text'):
    src=next((P.parent/'Arvectum-Typeface-v0.53/experimental').glob(f'Arvectum{st}*.otf'))
    dest=P/'experimental'/('Arvectum'+st+'GoldenStepDraft054-'+('Medium' if st=='Display' else 'Regular')+'.otf')
    f=Family(st,54,src,dest)
    originals={c:get(f.f,c) for c in 'АаеEeiIЙ'}
    for c,pen in glyphs(f.t,f.k).items():inject_mark(f,c,pen)
    meta=f.finish();assert meta['codepoints']==212
    kernfea=(P.parent/'Arvectum-Typeface-v0.53'/('kerning-'+st.lower()+'.fea')).read_text()
    feat=[f'markClass uni{ord(c):04X} <anchor 0 0> @'+('BOTTOM' if c=='\u0327' else 'TOP')+';' for c in scope]+['feature mark {']
    current=TTFont(dest);cm=current.getBestCmap();gs=current.getGlyphSet()
    for cp,name in sorted(cm.items()):
        c=chr(cp)
        if not c.isalpha() or c in scope:continue
        b=box(get(current,c));assert b is not None
        x=round((b[0]+b[2])/2);y=round(min(b[3]+95,1700))
        feat.append(f'  pos base {name} <anchor {x} {y}> mark @TOP;')
        feat.append(f'  pos base {name} <anchor {x} {max(round(b[1])-15,-350)}> mark @BOTTOM;')
    feat.append('} mark;')
    fea=kernfea+'\n'+'\n'.join(feat)+'\n'
    (P/('features-'+st.lower()+'.fea')).write_text(fea)
    addOpenTypeFeaturesFromString(current,fea)
    tmp=dest.with_suffix('.tmp');current.recalcTimestamp=False;current.save(tmp);os.replace(tmp,dest)
    out=TTFont(dest)
    assert all(t in out for t in ('GPOS','GDEF'))
    assert out.getBestCmap().keys()>=set(map(ord,scope))
    assert verify(src,dest,set())==203
    mark_checks={}
    for word in ('е\u0301','а\u0301','a\u0308','e\u0301','a\u0300','e\u0302','n\u0303','o\u0304','u\u030a','c\u0327','Й','И\u0306','Е\u0308','е\u0308'):
        q=json.loads(subprocess.check_output(['hb-shape','--output-format=json',str(dest),word],text=True))
        assert all(g['g']!='.notdef' for g in q),(st,word,q)
        if word in ('е\u0301','а\u0301','a\u0308','e\u0301','a\u0300','e\u0302','n\u0303','o\u0304','u\u030a','c\u0327'):
            assert len(q)==2 and q[-1]['ax']==0,(st,word,q)
        mark_checks[word]=q
    # Existing numeric advances and kern remain unchanged.
    for c in '0123456789':assert out['hmtx'][cm[ord(c)]][0] in (1323,1266)
    a=json.loads(subprocess.check_output(['hb-shape','--output-format=json',str(dest),'AV'],text=True))
    b=json.loads(subprocess.check_output(['hb-shape','--output-format=json','--features=kern=0',str(dest),'AV'],text=True))
    assert sum(g['ax'] for g in a)<sum(g['ax'] for g in b)
    meta['marks']=mark_checks;meta['features']=['kern','mark'];meta['font_sha256']=sha(dest)
    r[st]=meta
write_json(P/'marks-qa.json',r)
from PIL import Image,ImageDraw,ImageFont
im=Image.new('RGB',(1840,990),'white');d=ImageDraw.Draw(im)
for i,st in enumerate(('Display','Text')):
    x=25+i*910;y=35;p=next((P/'experimental').glob(f'Arvectum{st}*.otf'))
    for s,sz in [('v0.54 '+st,27),('Ё ё Й Й А́ а́',58),('ä é à ê ñ ç   й ё',45),('AV VA — АУ ЛТ',48),('Арвектум: информация',37)]:
        ft=ImageFont.truetype(str(p),sz);d.text((x,y),s,font=ft,fill='#001432');y+=110
im.save(P/'mark-proof.png')
print('PASS v0.54',digest_tree(P))
