"""Three-page real OTF owner review of W and its accents."""
from pathlib import Path
import subprocess
P=Path(__file__).resolve().parent
css=''
for f,w in [('Display','Medium'),('Text','Regular')]:
 for label,path in [('Old',f'../Arvectum-Typeface-v0.111/otf/ArvectumGoldenStep{f}WKernsWorking0111-{w}.otf'),
                    ('New',f'otf/ArvectumGoldenStep{f}WHarmonizedWorking0112-{w}.otf')]:
  css+=f'@font-face{{font-family:{f}{label};src:url("{path}") format("opentype")}}'
css+="""
@page{size:A4 landscape;margin:0}
*{box-sizing:border-box}body{margin:0;font-family:Arial,sans-serif;color:#12334a;-webkit-print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:12mm;break-after:page;position:relative}
.page:last-child{break-after:auto}
header{border-bottom:2px solid #26b29d;display:flex;justify-content:space-between;padding-bottom:10px}
h1{font-size:23px;font-weight:500;margin:0}.meta{font-size:11px;color:#6d8188}
.columns{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:17px}
.panel{padding:15px;background:#f8fbfa;border:1px solid #bfd9d6;min-height:345px;overflow:hidden}
.panel.new{border:2px solid #28aa99}
h2{font:700 14px Arial;color:#0a8878}
.large{font-size:75px;line-height:1.4;white-space:nowrap}
.medium{font-size:34px;line-height:1.5;white-space:nowrap}
.note{background:#ecf8f3;border-left:4px solid #2db6a1;font-size:12px;line-height:1.5;padding:12px;margin-top:14px}
.footer{position:absolute;bottom:12mm;left:12mm;right:12mm;border-top:1px solid #d4e1df;padding-top:8px;font-size:10px;color:#678088;display:flex;justify-content:space-between}
"""
def header(t):
 return f'<header><h1>{t}</h1><div class="meta">ARVECTUM GOLDEN STEP · v0.112 · инженерный образец</div></header>'
def footer(n):
 return f'<div class="footer"><span>W: α=69.0948° / X и Х: β=58.2825° · production без изменений</span><span>{n}/3</span></div>'
def panel(face,label):
 ft=face+label
 return f'<div class="panel{" new" if label=="New" else ""}"><h2>{face} · {"v0.112 — согласовано" if label=="New" else "v0.111 — рассогласовано"}</h2><div class="large" style="font-family:{ft}">W Ẃ Ŵ</div><div class="large" style="font-family:{ft}">Ẅ Ẁ Ẇ Ẉ</div><div class="medium" style="font-family:{ft}">WAVE ẂAVE</div></div>'
pages=[]
for i,face in enumerate(('Display','Text'),1):
 pages.append('<section class="page">'+header(face+' — W и диакритические знаки')+
  '<div class="columns">'+panel(face,'Old')+panel(face,'New')+'</div>'+
  '<div class="note">В правом варианте девять акцентированных форм используют точно тот же W-контур, что простая W. Сами знаки не перерисованы: перенесены относительно нового оптического центра, сохранён контур и высота. Точки крепления комбинируемых знаков и кернинг также обновлены.</div>'+footer(i)+'</section>')
def small(face):
 f=face+'New'
 parts=['<div class="panel new"><h2>'+face+' · v0.112</h2>']
 for size in (12,14,16,24,32):
  parts.append(f'<p style="margin:7px 0"><span style="font:12px Arial;color:#758790">{size}px </span><span style="font:{size}px/1.35 {f}">{('W Ẃ Ŵ · X Х' if size>=32 else 'W Ẃ Ŵ Ẅ Ẁ Ẇ Ẉ · WA ẂA · X Х')}</span></p>')
 parts.append(f'<div class="medium" style="font-family:{f}">W̄ W̆ Ẃ</div></div>')
 return ''.join(parts)
pages.append('<section class="page">'+header('Мелкие кегли и двухугловая система')+
 '<div class="columns">'+small('Display')+small('Text')+'</div>'+
 '<div class="note">Профессиональная проверка: единый W-силуэт сохранён в обеих оптических версиях. X и кириллическая Х остались на β, без изменения геометрии. Остаётся проверить пропорции широкой W относительно A/M и интервал с акцентированными соседями (например WÁ), а также физические устройства. Геометрическая точность ещё не означает художественного утверждения.</div>'+footer(3)+'</section>')
assert len(pages)==3
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
pdf=P/'Golden-Step-v0112-ACCENTS-REVIEW.pdf'
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--no-sandbox','--disable-gpu',
 '--user-data-dir=/tmp/gsv0112proof','--no-pdf-header-footer','--print-to-pdf='+str(pdf),(P/'specimen.html').as_uri()],
 capture_output=True,text=True,timeout=35)
assert r.returncode==0,r.stderr[-900:]
print('RENDERED PDF',pdf.stat().st_size)
