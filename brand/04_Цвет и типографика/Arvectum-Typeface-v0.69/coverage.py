"""Frozen corporate prose and Mac Pages DOCX repertoire analysis; no glyph modifications."""
from pathlib import Path
from fontTools.ttLib import TTFont
from docx import Document
import json,csv,hashlib,unicodedata,collections
P=Path(__file__).resolve().parent;ROOT=P.parent
FONTS=[next((ROOT/'Arvectum-Typeface-v0.64/experimental').glob('Arvectum'+style+'*.otf')) for style in ('Display','Text')]
maps=[]
for f in FONTS:
  ff=TTFont(f);maps.append(set(ff.getBestCmap()))
assert len(maps[0])==len(maps[1])==212 and maps[0]==maps[1]
SOURCES=[]
corpus=ROOT/'Arvectum-Typeface-v0.48/corpus.json'
for r in json.loads(corpus.read_text()):
    if r.get('path')=='synthetic use cases':continue
    SOURCES.append({'name':r.get('path'),'kind':'frozen repo text','content':r['text'],
                    'sha256':hashlib.sha256(r['text'].encode()).hexdigest()})
for v in ('061','064'):
    docpath=ROOT/'Arvectum-Typeface-v0.65/documents'/f'golden-step-{v}-mac-office.docx'
    doc=Document(docpath)
    content='\n'.join([p.text for p in doc.paragraphs]+[
        cell.text for table in doc.tables for row in table.rows for cell in row.cells])
    SOURCES.append({'name':docpath.name,'kind':'synthetic office DOCX','content':content,
                    'sha256':hashlib.sha256(docpath.read_bytes()).hexdigest()})
counts=collections.Counter();unsupported=collections.Counter()
source_report=[]
rows=[]
for source in SOURCES:
  text=source['content']
  visible=[ch for ch in text if not unicodedata.category(ch).startswith('C')]
  known=[ch for ch in visible if ord(ch) in maps[0]]
  missing=collections.Counter(ch for ch in visible if ord(ch) not in maps[0])
  counts.update(known);unsupported.update(missing)
  source_report.append({
   'source':source['name'],'kind':source['kind'],'source_sha256':source['sha256'],
   'visible_unicode_scalar_count':len(visible),'codepoint_coverage_pct':round(len(known)/max(1,len(visible))*100,3),
   'missing_occurrences':sum(missing.values()),
   'missing_unique':len(missing),
   'missing_escaped':{f'U+{ord(ch):04X}':v for ch,v in sorted(missing.items())}
  })
  for c,n in missing.items():
    rows.append(dict(source=source['name'],codepoint=f'U+{ord(c):04X}',unicode_name=unicodedata.name(c,'?'),
                     occurrences=n,category=unicodedata.category(c),remedy='monospace diagram fallback'))
count=sum(i['visible_unicode_scalar_count'] for i in source_report)
covered=count-sum(unsupported.values())
missing_set={ord(ch) for ch in unsupported}
assert len(SOURCES)==6 and len(missing_set)==7 and all(cp in {0x2500,0x2502,0x253c,0x250c,0x2510,0x2514,0x2518} for cp in missing_set)
assert all(cp>=0x2500 and cp<=0x257f for cp in missing_set)
assert source_report[0]['missing_occurrences']==source_report[1]['missing_occurrences']==source_report[3]['missing_occurrences']==0
assert source_report[-1]['missing_occurrences']==source_report[-2]['missing_occurrences']==0
with (P/'missing-symbols.csv').open('w',newline='') as fh:
  w=csv.DictWriter(fh,fieldnames=list(rows[0]),lineterminator='\n')
  w.writeheader();w.writerows(sorted(rows,key=lambda x:(x['source'],x['codepoint'])))
report={
 'analysis':'v0.69 frozen corporate text and synthetic office coverage',
 'baseline':'v0.64 212 encoded positions/style',
 'source_original':'v0.48/corpus.json snapshot, not current live site',
 'source_snapshot_sha256':hashlib.sha256(corpus.read_bytes()).hexdigest(),
 'visible_scalars_total':count,'visible_scalars_covered':covered,
 'weighted_coverage_pct':round(100*covered/count,4),'unsupported_total_occurrences':sum(unsupported.values()),
 'unsupported_unique_codepoints':len(unsupported),
 'unsupported_set':[{'unicode':f'U+{cp:04X}','glyph':chr(cp),'name':unicodedata.name(chr(cp)),'occurrences':unsupported[chr(cp)]}
                    for cp in sorted(missing_set)],
 'prose_codepoint_coverage':'Full in frozen brand platform, constitution, site and both office samples',
 'box_diagrams':'Missing seven line drawing glyphs only in frozen business-model doc diagram; separate monospace fallback',
 'sources':source_report,
 'recommendation':'Keep Golden Step for corporate prose. Route U+2500..U+257F box diagrams/code to a monospace font, rather than padding company brand font without a commercial use case.',
 'limits':['Corpus sources from prior v0.48 frozen snapshot; not all real client documents or current website',
           'Unicode scalar counts are not grapheme clusters and do not certify shaping or text extraction',
           'Missing glyph fallback varies by engine; only local Chrome CSS specimen tested',
           'Do not claim complete multilingual Unicode coverage, email clients or Windows support',
           'No source glyph/kerning/metrics modified; Windows postponed by owner']}
(P/'coverage-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS',len(SOURCES),'sources; chars visible',count,'covered',covered,
     'coverage %',report['weighted_coverage_pct'],'missing occurrences',sum(unsupported.values()),
     'unique',len(missing_set))
print('UNSUPPORTED',[(r['unicode'],r['glyph'],r['occurrences']) for r in report['unsupported_set']])
