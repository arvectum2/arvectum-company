"""6-page vector owner specimen, beta K/К/X/Х and W constraints, real embedded OTF."""
from pathlib import Path
import subprocess,json,html,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent
data=json.loads((P/'evidence/build-manifest.json').read_text())
css=''
for face,w in [('Display','Medium'),('Text','Regular')]:
 for ver,src in [('104',f'../Arvectum-Typeface-v0.104/experimental/ArvectumGoldenStep{face}AlphaHarmonizedDraft0104-{w}.otf'),('105',f'experimental/ArvectumGoldenStep{face}BetaCrossDraft0105-{w}.otf')]:
  css+=f'@font-face{{font-family:F{face}{ver};src:url("{src}") format("opentype");font-weight:400}}'
css+='''
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}
html,body{margin:0;color:#092941;background:#fff;font-family:Arial,sans-serif}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:10mm 13mm;break-after:page;position:relative;overflow:hidden}
.page:last-child{break-after:auto}
.head{border-bottom:2px solid #33b6a0;padding-bottom:9px;display:flex;justify-content:space-between;align-items:end}
.kicker{font:bold 10px Arial;color:#087c73;letter-spacing:1px}
h1{font:500 24px Arial;margin:4px 0}
.meta{font:10px Arial;color:#677c85;text-align:right}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:13px;margin-top:14px}
.panel{background:#f8fbfb;border:1px solid #ccdddd;padding:12px;overflow:hidden;min-height:360px}
.panel.new{border:2px solid #31b6a0;padding:11px}
h2{font:bold 13px Arial;color:#08796d;margin:0 0 7px}
.huge{font-size:84px;line-height:1.2;white-space:nowrap}
.large{font-size:38px;line-height:1.29;white-space:nowrap}
.medium{font-size:26px;line-height:1.31;white-space:nowrap}
.small{font-size:18px;line-height:1.34}
.note{background:#eaf7f3;border-left:4px solid #35bba2;font:11.5px/1.4 Arial;padding:9px 11px;margin-top:14px}
.foot{position:absolute;bottom:8mm;left:13mm;right:13mm;border-top:1px solid #ccdddf;padding-top:8px;font:10px Arial;color:#697e86;display:flex;justify-content:space-between}
.sub{font:bold 10px Arial;color:#617e85;margin:8px 0 4px}
.tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;margin-top:15px}
.tile{background:#f7fafb;border:1px solid #ccdddd;padding:8px}
.tile svg{width:100%;height:210px}
.summary{font:12px/1.6 Arial;color:#24485b}
.mini{font-size:14px;line-height:1.45}
'''
def head(title,sub):
 return f'<div class="head"><div><div class="kicker">ARVECTUM GOLDEN STEP / v0.105</div><h1>{title}</h1></div><div class="meta">{sub}<div>Эксперимент, художественная приёмка OPEN</div></div></div>'
def foot(i):
 return f'<div class="foot"><span>α = 69,0948° · β = 58,2825° · W не изменена · approved Wordmark untouched</span><span>{i:02d}/06</span></div>'
def panel(face,ver):
 fam=f'F{face}{ver}'
 s=f'<div class="panel{" new" if ver=="105" else ""}"><h2>{face} v0.{ver}</h2>'
 for kind,line in [('huge','K К X Х'),('large','КОНТЕКСТ K-X'),('medium','КЛЮЧ · ХАКИ'),('medium','KERNEL · X-RAY'),('small','WAVE · A/А · N/И/Y')]:
  s+=f'<div class="{kind}" style="font-family:{fam}">{line}</div>'
 return s+'</div>'
pages=[]
for page,face in enumerate(('Display','Text'),1):
 pages.append('<section class="page">'+head(f'{face}: эксперимент K/К X/Х', 'β на ветвях и диагональных пересечениях')+
 '<div class="cols">'+panel(face,'104')+panel(face,'105')+'</div>'+
 '<div class="note">Новые формы справа. K и К остаются разными знаками по строению ветвей, а X и Х получают связанную идентичную геометрию. Метрики и внешние границы сохраняются. W показана для контекста, но её контур не менялся.</div>'+foot(page)+'</section>')
def overlay(face,ch):
 def src(ver):
  file=P/'glyphs'/ver/face/f'U+{ord(ch):04X}.svg'
  root=ET.parse(file).getroot()
  return root.attrib['viewBox'],next(x.attrib['d'] for x in root if x.tag.endswith('path'))
 box,old=src('v0104');_,new=src('v0105')
 return (f'<div class="tile"><h2>{face} · {ch}</h2><svg viewBox="{box}">'
 f'<path d="{html.escape(old,quote=True)}" transform="scale(1 -1)" stroke="#3972b6" stroke-width="8" fill="#3972b6" fill-opacity=".06"/>'
 f'<path d="{html.escape(new,quote=True)}" transform="scale(1 -1)" stroke="#e39245" stroke-width="8" fill="#e39245" fill-opacity=".09"/></svg></div>')
for page,face in enumerate(('Display','Text'),3):
 tiles=''.join(overlay(face,ch) for ch in ('K','К','X','Х'))
 pages.append('<section class="page">'+head(f'{face}: наложение реальных контуров', 'синий v0.104 / оранжевый v0.105')+
 '<div class="tiles">'+tiles+'</div>'+
 '<div class="note">Это экспорт настоящих Type2 CFF-геометрий. Видно изменение плеча латинской K и сохранение горизонтального узла кириллической К. У X/Х центральное пересечение утолщается — проверять оптически на мелком кегле, а не только по математике.</div>'+foot(page)+'</section>')
def reader(ver):
 fam=f'FText{ver}';r=f'<div class="panel{" new" if ver=="105" else ""}"><h2>Text v0.{ver}</h2>'
 for size in (12,14,16,18,24,32):
  r+=f'<div class="sub">{size} px</div><div style="font:{size}px/1.30 {fam}">Ключ, характер и структура. Kinetic X-factor.</div>'
 return r+'</div>'
pages.append('<section class="page">'+head('Проверка Text 12–32 px', 'Реальные кириллические и латинские слова')+
 '<div class="cols">'+reader('104')+reader('105')+'</div>'+
 '<div class="note">Кандидаты K/К и X/Х строятся по β=atan(φ). Оценка читаемости для новых соединений и утолщённого центра X/Х должна предшествовать принятию этих форм. Все прочие глифы остаются от v0.104.</div>'+foot(5)+'</section>')
pages.append('<section class="page">'+head('W: геометрическое ограничение ширины', 'Два угла не должны разрушать форму')+
 '<div class="cols"><div class="panel"><h2>W v0.104 = v0.105 · без изменения</h2>'+
 '<div style="font:140px FDisplay104">W</div><div class="summary">Текущие длинные наружные штрихи: ~75°; требуемый базовый α=69,0948°. Для полной высоты 1490 UPM горизонтальный ход одной диагонали меняется примерно с 404 до 569 UPM (+165).</div></div>'+
 '<div class="panel new"><h2>Решение для следующего эскиза</h2>'+
 '<div class="summary">Сохраняя прежнюю ширину W, нельзя одновременно просто сдвинуть обе наружные длинные ножки на α и оставить прежние внутренние просветы. Нужна новая композиция четырех штрихов: либо шире глиф, либо изменённые внутренние соединения/высоты. В v0.105 W оставлена без изменения как осознанный HOLD.</div>'+
 '<div class="sub">Открытые вопросы для оптической оценки</div>'+
 '<div class="summary">Ширина → высота → толщина штриха → просветы между двойными V → кернинг WA/WE → Text 12–24 px.</div></div></div>'+
 '<div class="note">W пока не прошла проверку α. Принадлежность к двум базовым углам — проектное правило, а не основание механически исправлять сложный знак без оценки его пропорций.</div>'+foot(6)+'</section>')
assert len(pages)==6
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
pdf=P/'Golden-Step-v0105-K-X-BETA-W-HOLD-REVIEW.pdf'
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--no-sandbox',
 '--disable-gpu','--user-data-dir=/tmp/gs-v0105','--no-pdf-header-footer','--print-to-pdf='+str(pdf),(P/'specimen.html').as_uri()],
 capture_output=True,text=True,timeout=40)
if r.returncode:raise RuntimeError(r.stderr[-1000:])
print('PDF READY',pdf.name,pdf.stat().st_size)
