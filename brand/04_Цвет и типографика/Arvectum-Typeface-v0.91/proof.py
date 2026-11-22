"""Print A/B visual review for one Display-only, Inter-first open A/А candidate."""
from pathlib import Path
import html,json,subprocess,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent
m=json.loads((P/'evidence/build-manifest.json').read_text())
css='''
@font-face{font-family:InterDisplay;src:url("../Arvectum-Typeface-v0.85/experimental/ArvectumGoldenStepDisplayBaseDraft085-Medium.otf")}
@font-face{font-family:GoldenDisplay;src:url("experimental/ArvectumGoldenStepDisplayOpenADraft091-Medium.otf")}
@font-face{font-family:InterText;src:url("experimental/InterDisplay-Regular-exact-baseline-v085.otf")}
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}html,body{margin:0;color:#001432;background:white}body{font-family:Arial,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{position:relative;width:297mm;height:210mm;padding:11mm 14mm;overflow:hidden;break-after:page}.page:last-child{break-after:auto}
.head{display:flex;justify-content:space-between;align-items:end;border-bottom:2px solid #42aa96;padding-bottom:9px}
.brand{font:bold 10px Arial;color:#08796c;letter-spacing:1px}h1{font:500 24px Arial;margin:6px 0 0}
.meta{font:10px/1.5 Arial;color:#537580;text-align:right}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:15px;margin-top:15px}
.card{border:1px solid #cbdcde;background:#f7fbfb;padding:16px;overflow:hidden;min-height:385px}
.card.new{border:2px solid #41aa96;padding:15px}
.card h2{font:bold 15px Arial;color:#087b70;margin:0 0 6px}
.sub{font:11px Arial;color:#5d7881}
.giant{font-size:133px;line-height:1.15;white-space:nowrap}
.headline{font-size:49px;line-height:1.14;letter-spacing:-.018em;white-space:nowrap}
.sentence{font:15px/1.53 InterText;max-width:490px}
.rule{border-top:1px solid #ccdedd;margin:12px 0}
.note{font:11.5px/1.45 Arial;padding:9px 12px;border-left:4px solid #42aa96;background:#eef7f4;margin-top:11px}
.foot{border-top:1px solid #d1dede;display:flex;justify-content:space-between;position:absolute;bottom:9mm;left:14mm;right:14mm;padding-top:7px;font:10px Arial;color:#5b757e}
.block{font-size:37px;line-height:1.25;letter-spacing:-.02em;white-space:nowrap}
.small{font-size:26px;line-height:1.35;white-space:nowrap}
.h3{font:bold 10px Arial;color:#087b70;letter-spacing:1px;margin:12px 0 4px}
.overlaygrid{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:17px}
.overlay{border:1px solid #cbdede;background:#f7fbfb;padding:14px;text-align:center}.overlay svg{width:100%;height:230px}.overlay h2{font:700 15px Arial;color:#08776c;margin:0 0 8px}
'''
def head(title,meta):return f'<div class="head"><div><div class="brand">ARVECTUM · GOLDEN STEP DISPLAY · v0.91</div><h1>{title}</h1></div><div class="meta">{meta}<br>ЭКСПЕРИМЕНТ / НЕ УТВЕРЖДЕНО</div></div>'
def foot(n):return f'<div class="foot"><span>TEXT = исходный Inter · DISPLAY = эксперимент с открытой A/А · SIL OFL 1.1</span><span>{n}/03</span></div>'
def card(type):
 cand=type=='GoldenDisplay'
 name='Golden Step Display v0.91' if cand else 'Inter Display 4.1'
 txt='<div class="card'+(' new' if cand else '')+'"><h2>'+name+'</h2>'
 txt+='<div class="sub">'+('Перекладина открыта слева, пропорция 1/φ' if cand else 'Исходная классическая закрытая перекладина')+'</div>'
 txt+=f'<div class="giant" style="font-family:{type}">A А</div><div class="rule"></div>'
 txt+=f'<div class="headline" style="font-family:{type}">АРВЕКТУМ</div>'
 txt+=f'<div class="headline" style="font-family:{type};font-size:37px">АВТОМАТИЗАЦИЯ</div>'
 txt+='<div class="rule"></div><div class="sentence">Архитектура решений для организаций. Технические детали и полезные сценарии представлены в основном тексте неизменённым Inter.</div></div>'
 return txt
p1='<section class="page">'+head('От привычного Inter к узнаваемой A/А','Один новый знак; остальные детали сохранены')+'<div class="cols">'+card('InterDisplay')+card('GoldenDisplay')+'</div><div class="note">Отличие построено на утверждённом направлении Wordmark A/А, но не копирует его контуры. Оставлено 371 из 601 единицы нижней перекладины: 371/601 ≈ 0,6173 ≈ 1/φ. Открытая форма предназначена только для заголовочного Display.</div>'+foot(1)+'</section>'
def hierarchy(f):
 h='<div class="card'+(' new' if f=='GoldenDisplay' else '')+'"><h2>'+('Arvectum Display + Inter Text' if f=='GoldenDisplay' else 'Inter Display + Inter Text')+'</h2>'
 for size,line in ((52,'АРХИТЕКТУРА'),(40,'АВТОМАТИЗАЦИЯ'),(32,'Аналитика процессов'),(25,'Задачи бизнеса')):
  h+=f'<div class="h3">DISPLAY · {size} PX</div><div style="font-family:{f};font-size:{size}px;line-height:1.16;letter-spacing:-.015em;white-space:nowrap">{line}</div>'
 h+='<div class="rule"></div><div class="h3">TEXT · 16 PX / ОДИНАКОВЫЙ В ОБОИХ ВАРИАНТАХ</div><div class="sentence">ООО «Арвектум» создаёт прикладные цифровые решения. Читаемость обычных документов и интерфейсов сохраняем на базе Inter. Цифры: 2026 · 1 250 000 ₽.</div></div>'
 return h
p2='<section class="page">'+head('Иерархия заголовков и обычного текста','52 / 40 / 32 / 25 / 16 PX')+'<div class="cols">'+hierarchy('InterDisplay')+hierarchy('GoldenDisplay')+'</div><div class="note">Здесь между левой и правой колонками изменён только шрифт DISPLAY. Межбуквенные интервалы и основной Text идентичны; все шрифты реально встроены в PDF. Следующий этап — проверить ту же пару в мобильном/деловом макете.</div>'+foot(2)+'</section>'
def overlay(ch):
 def load(v):
  r=ET.parse(P/'glyphs'/v/f'U+{ord(ch):04X}.svg').getroot()
  return r.attrib['viewBox'],list(r)[0].attrib['d']
 view,baseline=load('base');view2,candidate=load('candidate')
 assert view==view2
 return f'<div class="overlay"><h2>{ch}: исходный контур (синий) и открытый (оранжевый)</h2><svg viewBox="{view}"><path transform="scale(1 -1)" d="{html.escape(baseline)}" fill="#357aba" fill-opacity=".13" stroke="#357aba" stroke-width="15"/><path transform="scale(1 -1)" d="{html.escape(candidate)}" fill="#ea8735" fill-opacity=".13" stroke="#ea8735" stroke-width="12"/></svg><div class="sub">Оригинальные крайние точки и высота не изменены</div></div>'
p3='<section class="page">'+head('Векторный контроль открытой перекладины','Латинская A и кириллическая А идентичны')+'<div class="overlaygrid">'+overlay('A')+overlay('А')+'</div><div class="note">Синий контур — исходная Display-буква Inter; оранжевый — эксперимент v0.91. Коррекция локальна, без декоративных диагоналей и угловатости. В Text форма А/А остаётся закрытой. Визуальная оценка владельца требуется до любых производственных изменений.</div>'+foot(3)+'</section>'
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+p1+p2+p3+'</body></html>')
pdf=P/'Golden-Step-Display-v091-OPEN-A-COMPARISON.pdf'
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--disable-gpu','--no-sandbox','--user-data-dir=/tmp/golden-open-a-091','--no-pdf-header-footer','--print-to-pdf='+str(pdf),(P/'specimen.html').as_uri()],capture_output=True,text=True,timeout=40)
if r.returncode:raise RuntimeError(r.stderr[-1300:])
print('RENDER PDF',pdf.name,pdf.stat().st_size)
