from pathlib import Path
import subprocess,json,html,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent
m=json.loads((P/'evidence/build-manifest.json').read_text())
css=''
for st,w in (('Display','Medium'),('Text','Regular')):
 for i,path in enumerate((f'../Arvectum-Typeface-v0.94/experimental/ArvectumGoldenStep{st}StrictStructuralDraft094-{w}.otf',
                        f'experimental/ArvectumGoldenStep{st}RoofGeometryDraft095-{w}.otf')):
  css+=f'@font-face{{font-family:F{st}{i};src:url("{path}") format("opentype")}}'
css+='''
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}body,html{margin:0;background:white;color:#001432;font-family:Arial}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:10mm 13mm;break-after:page;position:relative;overflow:hidden}
.page:last-child{break-after:auto}
.head{border-bottom:2px solid #3aaa99;display:flex;justify-content:space-between;align-items:end;padding-bottom:9px}
.kicker{font:bold 10px Arial;color:#08766c;letter-spacing:1px}
h1{font:500 24px Arial;margin:5px 0 0}.meta{font:10px Arial;color:#59777d;text-align:right}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:13px;margin-top:14px}
.panel{border:1px solid #c8dcde;background:#f8fbfb;padding:13px;overflow:hidden;min-height:400px}
.panel.new{border:2px solid #3aaa99;padding:12px}
h2{font:bold 14px Arial;color:#08766e;margin:0 0 7px}
.big{font-size:107px;line-height:1.25;white-space:nowrap}
.headline{font-size:47px;line-height:1.25;white-space:nowrap}
.medium{font-size:27px;line-height:1.4;white-space:nowrap}
.body{font-size:16px;line-height:1.45}
.rule{border-top:1px solid #c8dcde;margin:10px 0}
.note{background:#eaf5f3;border-left:4px solid #3aaa99;margin-top:13px;padding:11px;font:11.5px/1.45 Arial}
.footer{position:absolute;left:13mm;right:13mm;bottom:8mm;border-top:1px solid #c6d8da;padding-top:8px;display:flex;justify-content:space-between;font:10px Arial;color:#5a757d}
.ovgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:16px}
.ov{border:1px solid #c8dede;background:#f8fbfb;padding:9px}.ov svg{width:100%;height:191px}
.sub{font:bold 10px Arial;color:#667a82;margin:9px 0 3px}
.alph{font-size:27px;line-height:1.27;white-space:nowrap}
'''
def hd(t,n):return f'<div class="head"><div><div class="kicker">ARVECTUM · GOLDEN STEP · v0.95</div><h1>{t}</h1></div><div class="meta">{n}<div>ЭКСПЕРИМЕНТ / НЕ УТВЕРЖДЕНО</div></div></div>'
def ft(i):return f'<div class="footer"><span>Д/Л: конструктивная φ-система «кровли» · П: сохранена для совместимости</span><span>{i}/04</span></div>'
def panel(st,i):
 font=f'F{st}{i}'
 h='<div class="panel'+(' new' if i else '')+'"><h2>'+('v0.95 · новая совместная геометрия' if i else 'v0.94 · прежние контуры')+'</h2>'
 for cl,t in [('big','ДЛ П'),('headline','ДЕЛО · ПЛАН'),('medium','ЛИДЕРСТВО · ПРОЕКТ'),('medium','ПРИКЛАДНАЯ АРХИТЕКТУРА')]:
  h+=f'<div class="{cl}" style="font-family:{font}">{t}</div>'
 h+=f'<div class="rule"></div><div class="body" style="font-family:{font}">Для предприятий: планирование, деловая аналитика и разработка решений. Обе формы должны сохранять читаемость.</div></div>'
 return h
pages=[]
for page,st in enumerate(('Display','Text'),1):
 pages.append('<section class="page">'+hd(st+': конструктивные Д/Л и П','Одна геометрическая система; две оптические ветви')+
 '<div class="cols">'+panel(st,0)+panel(st,1)+'</div>'+
 '<div class="note">Левая внешняя точка «кровли» смещена на h/φ⁶ = 83 ед.; внутренняя вычислена так, чтобы отношение клина к верхней внутренней горизонтали было φ⁻²≈0,382. Непрерывность кривых сохранена корректировкой контрольных точек. П остаётся неизменной: её верхняя перемычка уже согласуется с Д/Л.</div>'+ft(page)+'</section>')
def overlay(st,ch):
 def load(v):
  e=ET.parse(P/'glyphs'/v/st/f'U+{ord(ch):04X}.svg').getroot()
  return e.attrib['viewBox'],list(e)[0].attrib['d']
 v0,d0=load('v094');v1,d1=load('v095');assert v0==v1
 return f'<div class="ov"><h2>{st} · {ch}</h2><svg viewBox="{v0}"><path transform="scale(1 -1)" d="{html.escape(d0)}" fill="#2a79bf" fill-opacity=".05" stroke="#2a79bf" stroke-width="12"/><path transform="scale(1 -1)" d="{html.escape(d1)}" fill="#e28238" fill-opacity=".06" stroke="#e28238" stroke-width="11"/></svg></div>'
pages.append('<section class="page">'+hd('Д/Л/П — наложение реальных CFF-контуров','Синий v0.94, оранжевый v0.95')+
 '<div class="ovgrid">'+''.join(overlay(st,ch) for st in ('Display','Text') for ch in 'ДЛП')+'</div>'+
 '<div class="note">У П синий и оранжевый контуры совпадают намеренно. Другие глифы, включая ранее уточнённые К/K, И, А/А, Е/E, Н/H, М/M, остались идентичны v0.94.</div>'+ft(3)+'</section>')
def reading(st,i):
 fam=f'F{st}{i}'
 out='<div class="panel'+(' new' if i else '')+'"><h2>'+('v0.95' if i else 'v0.94')+'</h2>'
 for sz in (12,14,16,18,24,32):
  out+=f'<div class="sub">{sz} PX · ФРАЗА С Д / Л / П</div>'
  out+=f'<div style="font-family:{fam};font-size:{sz}px;line-height:1.38">Деловое планирование и подготовка предложений.</div>'
 return out+'</div>'
pages.append('<section class="page">'+hd('Arvectum Text — читаемость 12–32 px','Деловые слова и контекст, без автоматической художественной приёмки')+
 '<div class="cols">'+reading('Text',0)+reading('Text',1)+'</div>'+
 '<div class="note">Этот просмотр не заменяет независимый читательский тест. Внешние размеры, расстояния между глифами и Unicode-покрытие сохраняются; проверяем стабильность форм на прикладных размерах.</div>'+ft(4)+'</section>')
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
out=P/'Golden-Step-v095-DEL-PE-ROOF-REVIEW.pdf'
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--no-sandbox','--disable-gpu','--user-data-dir=/tmp/arvectum-golden-v095','--no-pdf-header-footer','--print-to-pdf='+str(out),(P/'specimen.html').as_uri()],capture_output=True,text=True,timeout=40)
if r.returncode:raise RuntimeError(r.stderr[-1100:])
print('RENDERED',out.name,out.stat().st_size)
