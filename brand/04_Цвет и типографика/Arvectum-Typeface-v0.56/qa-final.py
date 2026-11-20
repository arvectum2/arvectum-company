from pathlib import Path
import json,sys,subprocess,hashlib,re,unicodedata
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
P=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
styles={}
for st in ('Display','Text'):
    files={suffix:next((P/'experimental').glob(f'Arvectum{st}*.{suffix}')) for suffix in ('otf','woff','woff2')}
    fonts={suffix:TTFont(p) for suffix,p in files.items()}
    cm=fonts['otf'].getBestCmap()
    assert len(cm)==212 and all(i in cm for i in range(32,127))
    assert all(set(cm)==set(f.getBestCmap()) for f in fonts.values())
    assert all(f['hmtx'].metrics==fonts['otf']['hmtx'].metrics for f in fonts.values())
    for fmt in ('woff','woff2'):
        for cp,n in cm.items():
            x=RecordingPen();y=RecordingPen()
            fonts['otf'].getGlyphSet()[n].draw(x)
            fonts[fmt].getGlyphSet()[fonts[fmt].getBestCmap()[cp]].draw(y)
            assert x.value==y.value,(st,fmt,cp,'outline roundtrip')
    assert all({'GPOS','GDEF'}<=set(f.keys()) for f in fonts.values())
    assert all(ch in cm for ch in map(ord,'©®™§¶•←→↔'))
    m=fonts['otf']['hmtx']
    widths={m[cm[ord(c)]][0] for c in '0123456789'}
    assert widths==({1323} if st=='Display' else {1266})
    assert [m[cm[ord(c)]][0] for c in (' ','\u00a0','\u202f')]==[512,512,316]
    assert fonts['otf']['hhea'].ascent==2080 and fonts['otf']['hhea'].descent==-680
    def shape(s,features=None):
        args=['hb-shape','--output-format=json']
        if features:args.append('--features='+features)
        args.extend([str(files['otf']),s])
        return json.loads(subprocess.check_output(args,text=True))
    assert all(g['g']!='.notdef' for g in shape('info@arvectum.com/©®™')+shape('Арвектум а\u0301 e\u0301 ç'))
    assert len(shape('AV'))==2
    assert sum(x['ax'] for x in shape('AV','kern=1'))<sum(x['ax'] for x in shape('AV','kern=0'))
    for s in ('а\u0301','c\u0327','e\u0302','a\u0300'):
        g=shape(s)
        assert len(g)==2 and g[1]['ax']==0 and all(x['g']!='.notdef' for x in g)
    # Verify the QA repair actually changed composite glyphs vs previous version.
    prev=TTFont(next((P.parent/'Arvectum-Typeface-v0.55/experimental').glob(f'Arvectum{st}*.otf')))
    def recorded(f,c):
        p=RecordingPen();f.getGlyphSet()[f.getBestCmap()[ord(c)]].draw(p);return p.value
    changed=[c for c in map(chr,cm) if ord(c) in prev.getBestCmap() and recorded(fonts['otf'],c)!=recorded(prev,c)]
    assert set(changed)==set('©®¶\u030a'),changed
    out=subprocess.check_output(['fc-scan','--format','%{family}|%{style}\n',str(files['otf'])],text=True).strip()
    assert 'Arvectum' in out
    styles[st]={'codepoints':212,'ascii':95,'format_sha256':{k:sha(v) for k,v in files.items()},
                'corrected_glyphs':changed,'figure_advance':next(iter(widths)),'fontconfig':out,
                'tables':[k for k in ('GPOS','GDEF','GSUB') if k in fonts['otf']]}
pdf=P/'print-proof.pdf';assert pdf.is_file()
pdfinfo=subprocess.check_output(['pdfinfo',str(pdf)],text=True)
assert re.search(r'Pages:\s+2\b',pdfinfo) and '595 x 842 pts' in pdfinfo
pdf_fonts=subprocess.check_output(['pdffonts',str(pdf)],text=True)
for st in ('Display','Text'):
    lines=[s for s in pdf_fonts.splitlines() if 'Arvectum'+st in s]
    assert lines and all('yes yes' in s for s in lines),(st,lines)
text=subprocess.check_output(['pdftotext',str(pdf),'-'],text=True)
assert 'Арвектум' in text and '1 250 000,00 ₽' in text and 'info@arvectum.com' in text
html=(P/'chrome-dom.html').read_text()
match=re.search(r'<div id="qa">(FONT_QA[^<]+)',html)
assert match and 'display=true text=true' in match[1] and 'result=PASS' in match[1]
for page in (1,2):assert (P/f'print-renders/page-{page}.png').is_file()
report={'status':'TECHNICAL_DRAFT_PASS','styles':styles,'browser':match[1],
        'PDF':{'pages':2,'embedded_subset_fonts':True,'text_extraction':True,'sha256':sha(pdf)},
        'limitations':['Windows device unavailable (HTTP 530)','Office/Pages document rendering not validated','No physical paper print','No owner optical/release approval','Some overlapping composite glyphs require expanded QA','Font license remains derived SIL OFL']}
(P/'qualification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS stage 0.56',report['status'],report['browser'])
