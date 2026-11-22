"""Arvectum v0.103 dual-angle owner proof; real source OTF and SVG CFF contours."""
from pathlib import Path
import json,subprocess,html,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent;meta=json.loads((P/'evidence/build-manifest.json').read_text())
qa=json.loads((P/'evidence/qa-report.json').read_text())
css=''
for face,weight in [('Display','Medium'),('Text','Regular')]:
 for ver,suffix,prefix in [('0102','SlantedTerminalDraft0102','../Arvectum-Typeface-v0.102'),
                            ('0103','DualAngleDraft0103','.')]:
  name=f'ArvectumGoldenStep{face}{suffix}-{weight}.otf'
  css+=f'@font-face{{font-family:F{face}{ver};src:url("{prefix}/experimental/{name}") format("opentype")}}'
css+='''
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}
html,body{margin:0;background:#fff;color:#001432;font-family:Arial,sans-serif}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:10mm 13mm;break-after:page;position:relative;overflow:hidden}
.page:last-child{break-after:auto}
.hd{display:flex;align-items:end;justify-content:space-between;padding-bottom:9px;border-bottom:2px solid #35b29c}
.kicker{font:bold 10px Arial;color:#087d72;letter-spacing:1px}
h1{font:500 24px Arial;margin:5px 0 0}.meta{font:10px Arial;color:#637987;text-align:right}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:15px}
.panel{background:#f7fafb;border:1px solid #c9dfe1;padding:12px;min-height:370px;overflow:hidden}
.panel.new{border:2px solid #35b29c;padding:11px}
h2{font:bold 14px Arial;color:#08796d;margin:0 0 7px}
.huge{font-size:108px;line-height:1.18;white-space:nowrap}
.large{font-size:53px;line-height:1.22;white-space:nowrap}
.medium{font-size:30px;line-height:1.30;white-space:nowrap}
.sample{font-size:19px;line-height:1.3}
.note{background:#eaf7f3;border-left:4px solid #35b29c;font:11.5px/1.45 Arial;color:#234e55;padding:10px 12px;margin-top:13px}
.footer{position:absolute;bottom:8mm;left:13mm;right:13mm;border-top:1px solid #ccdfe2;padding-top:8px;font:10px Arial;color:#667c83;display:flex;justify-content:space-between}
.badge{font:bold 11px Arial;color:#2f7c71;letter-spacing:.4px}
.sub{font:bold 10px Arial;color:#587481;margin:6px 0 3px}
.alpha{font-size:26px;line-height:1.28;white-space:nowrap}
.outline{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:13px}
.tile{background:#f7fafb;border:1px solid #cbdddf;padding:9px}
.tile svg{width:100%;height:170px}
.metric{font:11.5px/1.5 Arial;color:#305461}
'''
def head(title,sub):
 return f'<div class="hd"><div><div class="kicker">ARVECTUM / GOLDEN STEP / v0.103</div><h1>{title}</h1></div><div class="meta">{sub}<div>Эксперимент · художественная приёмка OPEN</div></div></div>'
def foot(i,total=6):
 return f'<div class="footer"><span>α=arctan(φ²)=69,0948° · β=arctan(φ)=58,2825° · approved logo unchanged</span><span>{i:02d}/{total:02d}</span></div>'
def panel(face,version,title,words):
 family=f'F{face}{version}'
 h=f'<div class="panel{" new" if version=="0103" else ""}"><h2>{face} v{"0.103" if version=="0103" else "0.102"}</h2>'
 h+=f'<div class="huge" style="font-family:{family}">N И Y</div>'
 h+=f'<div class="large" style="font-family:{family}">{title}</div>'
 h+=f'<div class="medium" style="font-family:{family}">{words}</div>'
 h+=f'<div class="sub">Контроль α без изменения контуров</div>'
 h+=f'<div style="font-family:{family};font-size:43px;line-height:1.30">A А V M М</div>'
 return h+'</div>'
pages=[]
pages.append('<section class="page">'+head('Два угла в одной гарнитуре','Display / Text · N, И, Y → β')+
 '<div class="cols">'+panel('Display','0102','НИ','ИННОВАЦИИ')+
 panel('Display','0103','НИ','ИННОВАЦИИ')+'</div>'+
 '<div class="note">У N и И два основных протяжённых диагональных ребра, у Y — четыре прямые ветви. После согласования с β прежние α-конструкции A/А, V, M/М, Д/Л и согласованный срез перемычки Display A/А сохранены точно.</div>'+foot(1)+'</section>')
pages.append('<section class="page">'+head('Display: строгие опорные диагонали','Точные кандидаты v0.102 / v0.103')+
 '<div class="cols">'+panel('Display','0102','NY','NATIONAL')+
 panel('Display','0103','NY','NATIONAL')+'</div>'+
 '<div class="note">Скорректированы только необходимые координаты основных прямых: N — 2 участка, И — 2, Y — 4. У Y верхние экстремумы, середина разветвления и очертание внешних границ сохранены.</div>'+foot(2)+'</section>')
pages.append('<section class="page">'+head('Text: N / И / Y в абзацном контексте','Оптическая ветка Text Regular')+
 '<div class="cols">'+panel('Text','0102','NИY','ИНЖЕНЕРИЯ')+
 panel('Text','0103','NИY','ИНЖЕНЕРИЯ')+'</div>'+
 '<div class="note">Text использует те же два базовых угла, но собственную толщину штрихов и интервалов. Отдельный человеческий тест чтения ещё не проводился; техническая проверка не считается художественной приёмкой.</div>'+foot(3)+'</section>')

def overlay(face,char):
 def load(ver):
  f=P/'glyphs'/ver/face/f'U+{ord(char):04X}.svg'
  root=ET.parse(f).getroot()
  return root.attrib['viewBox'],next(x.attrib['d'] for x in root if x.tag.endswith('path'))
 vb,a=load('v0102');v2,b=load('v0103')
 return (f'<div class="tile"><h2>{face} · {char}</h2><svg viewBox="{vb}">'
  f'<path d="{html.escape(a,quote=True)}" transform="scale(1 -1)" stroke="#3376b7" stroke-width="8" fill="#3376b7" fill-opacity=".09"/>'
  f'<path d="{html.escape(b,quote=True)}" transform="scale(1 -1)" stroke="#da854a" stroke-width="8" fill="#da854a" fill-opacity=".08"/>'
  '</svg></div>')
for i,face in enumerate(('Display','Text'),start=4):
 tiles=''.join(overlay(face,ch) for ch in 'NИY')
 sample='ИННОВАЦИИ  NATIONAL  ИНЖЕНЕРИЯ  YOUR'
 pages.append('<section class="page">'+head(f'{face}: настоящие векторные контуры','Синий — v0.102 · оранжевый — v0.103')+
  '<div class="outline">'+tiles+'</div>'+
  f'<div class="panel new" style="min-height:0;margin-top:13px"><h2>Реальный строковый набор v0.103</h2>'
  f'<div class="medium" style="font-family:F{face}0103">{sample}</div></div>'+
  '<div class="note">Наложение из настоящих CFF-путей. Обе версии имеют одинаковые внешние границы и advance widths. У Y сохранены верхние края и плавный переход внутренних ветвей, изменено положение вертикальной ножки внутри той же внешней формы.</div>'+foot(i)+'</section>')
def reader(ver):
 fam=f'FText{ver}'
 h=f'<div class="panel{" new" if ver=="0103" else ""}"><h2>Arvectum Text v{"0.103" if ver=="0103" else "0.102"}</h2>'
 sentence='Инновации и инженерия. New vision for your future.'
 for size in (12,14,16,18,24,32):
  h+=f'<div class="sub">{size} px</div><div style="font:{size}px/1.34 {fam}">{sentence}</div>'
 return h+'</div>'
pages.append('<section class="page">'+head('Text: реальные слова 12–32px','Доказательства корректного рендеринга')+
 '<div class="cols">'+reader('0102')+reader('0103')+'</div>'+
 '<div class="note">Корректная отрисовка — не независимая оценка удобочитаемости. Изменений в GPOS/GSUB, кернинге, числах и прочих буквах этой итерацией не производится.</div>'+foot(6)+'</section>')
assert len(pages)==6,len(pages)
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
pdf=P/'Golden-Step-v0103-DUAL-ANGLE-N-I-Y-REVIEW.pdf'
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '--headless=new','--no-sandbox','--disable-gpu','--user-data-dir=/tmp/gs-v0103-angles',
  '--no-pdf-header-footer','--print-to-pdf='+str(pdf),(P/'specimen.html').as_uri()],
 capture_output=True,text=True,timeout=40)
if r.returncode:raise RuntimeError(r.stderr[-900:])
print('PDF',pdf.name,'size',pdf.stat().st_size)
