"""Independent paragraph, financial, URL and tabular-digit differential HarfBuzz audit."""
from pathlib import Path
from fontTools.ttLib import TTFont
import uharfbuzz as hb
import json,collections
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
samples={
'ru_headings':['Гибридная система управления','Гнездо тестов и графики','Главный инженер и генеральный директор','Гражданский договор, гарантия, город'],
'ru_document':['Гибридный процесс обеспечивает контроль исполнения.','Гнездо данных и главное управление формируют отчёты.','Предложение содержит стоимость работ, График поставки, номер счёта.','Акт оказанных услуг подписывается после завершения приёмки.'],
'en_document':['Arvectum provides governed work and transparent automation.','Trustworthy workflows, analytics, security and knowledge.','TURNKEY, TRADE, ALWAYS, PAYMENTS, ARVECTUM.'],
'finance':['Договор № 123/26 от 23.11.2026','125 000 ₽ · НДС 0% · 7%, 12 345,67 ₽.','КП: 1 234 567,89 ₽; 17:45; № 2026/31','Номер счёта: 1234567890 · дата 23.11.2026'],
'url':['arvectum.com/reports/2026/11','https://arvectum.com/company/2026?lang=ru','info@arvectum.com'],
'protected':['3/З · 33 · ЗЗ','WÁ · АW · «А» · ₽. · ₽,','А К Х Ж М W X Y N'],
}
def shape(file,text,features=None):
 f=hb.Font(hb.Face(file.read_bytes()));f.scale=(2048,2048)
 b=hb.Buffer();b.add_str(text);b.guess_segment_properties();hb.shape(f,b,features or {'kern':True})
 return [i.codepoint for i in b.glyph_infos],[(x.x_advance,x.x_offset,x.y_offset) for x in b.glyph_positions]
report={'current':'0.121','baseline':'0.120','scope':'synthetic A/B only, no customer data, not optical owner signoff','masters':{}}
for face,d in m['masters'].items():
 old=R/d['source'];new=P/d['output']
 fa,fb=TTFont(old),TTFont(new)
 digits='0123456789'
 digit_glyphs=[fa.getBestCmap()[ord(x)] for x in digits]
 assert [fa['hmtx'][x] for x in digit_glyphs]==[fb['hmtx'][x] for x in digit_glyphs]
 out={};changed=[];controls=0
 for section,lines in samples.items():
  res=[]
  for line in lines:
   a,pa=shape(old,line);b,pb=shape(new,line)
   assert a==b and len(pa)==len(pb),(face,section,line,'shaping altered')
   advance_before=sum(x[0] for x in pa)
   advance_after=sum(x[0] for x in pb)
   n=line.count('Ги')+line.count('Гн')
   delta=advance_after-advance_before
   assert delta==-235*n,(face,section,line,delta,n)
   if n==0:
    assert pa==pb,(face,section,line,'unexpected glyph placement drift')
    controls+=1
   else:changed.append(line)
   res.append({'text':line,'changed_target_occurrences':n,'advance_delta_UPM':delta})
  out[section]=res
 report['masters'][face]={'categories':out,'controlled_lines_unchanged':controls,'target_lines':len(changed),'tabular_digits':{x:fa['hmtx'][y][0] for x,y in zip(digits,digit_glyphs)}}
 print('PASS CORPUS',face,'lines',sum(map(len,samples.values())),'target lines',len(changed),'unchanged controls',controls)
(P/'evidence/phrase-differential.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
