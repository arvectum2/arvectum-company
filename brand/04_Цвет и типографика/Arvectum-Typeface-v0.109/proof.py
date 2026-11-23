"""v0.109 real-font 4-page A4 owner review; active parent 0.106 retained."""
from pathlib import Path
import json,subprocess
P=Path(__file__).resolve().parent;T=P.parent
m=json.loads((P/'evidence/build-manifest.json').read_text())
x=json.loads((P/'evidence/X-SMALL-SIZE-PIXEL-AUDIT.json').read_text())
css=''
for face,w in (('Display','Medium'),('Text','Regular')):
 for label,path in (('Base',f'../Arvectum-Typeface-v0.106/experimental/ArvectumGoldenStep{face}UnifiedForkDraft0106-{w}.otf'),
                    ('Wide',f'../Arvectum-Typeface-v0.108/experimental/ArvectumGoldenStep{face}WAlphaWideExperimental0108-{w}.otf'),
                    ('Balanced',f'experimental/ArvectumGoldenStep{face}AlphaBalancedExperimental0109-{w}.otf'),
                    ('XSoft',f'../Arvectum-Typeface-v0.108/experimental/ArvectumGoldenStep{face}XSoftExperimental0108-{w}.otf')):
  css+=f'@font-face{{font-family:"{face}{label}";src:url("{path}") format("opentype")}}'
css+="""
@page{size:A4 landscape;margin:0}
*{box-sizing:border-box}body,html{margin:0;background:#fff;color:#112e45;font-family:Arial,sans-serif}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:9mm 12mm;position:relative;break-after:page;overflow:hidden}
.page:last-child{break-after:auto}
.hd{display:flex;align-items:end;justify-content:space-between;border-bottom:2px solid #2fb39d;padding-bottom:8px}
h1{font:500 23px Arial;margin:4px 0}
.kicker{font:bold 10px Arial;letter-spacing:1px;color:#08816e}
.meta{font:10px/1.4 Arial;color:#65808a;text-align:right}
.three{display:grid;grid-template-columns:repeat(3,1fr);gap:11px;margin-top:14px}
.two{display:grid;grid-template-columns:repeat(2,1fr);gap:13px;margin-top:12px}
.panel{border:1px solid #c6dedd;background:#f8fbfb;padding:11px;min-height:341px;overflow:hidden}
.panel.new{border:2px solid #34b7a2;padding:10px}
h2{font:bold 13px Arial;color:#097d70;margin:0 0 8px}
.big{font-size:120px;line-height:1.13;white-space:nowrap}
.mid{font-size:46px;line-height:1.28;white-space:nowrap}
.small{font-size:24px;line-height:1.29;white-space:nowrap}
.note{border-left:4px solid #36b9a3;background:#edf8f4;font:11px/1.46 Arial;padding:9px 12px;margin-top:12px}
.ft{position:absolute;bottom:8mm;left:12mm;right:12mm;border-top:1px solid #cadedd;padding-top:7px;font:10px Arial;color:#66808a;display:flex;justify-content:space-between}
.sz{font:bold 10px Arial;color:#607f87;margin:8px 0 4px}
table{width:100%;border-collapse:collapse;margin-top:18px;font:13px Arial}
td,th{padding:9px;text-align:left;border-bottom:1px solid #cadedd}
"""
def header(title,note):
 return f'<div class="hd"><div><div class="kicker">ARVECTUM GOLDEN STEP / v0.109 · RESEARCH ONLY</div><h1>{title}</h1></div><div class="meta">{note}<div>Активная версия остаётся v0.106</div></div></div>'
def footer(i):
 return f'<div class="ft"><span>α=69,0948° / β=58,2825° · никаких дополнительных разрывов · production не менялся</span><span>{i:02d}/04</span></div>'
def wpanel(face,label):
 fm=face+label
 title={'Base':'v0.106 · исходная','Wide':'v0.108 · широкая +27%','Balanced':'v0.109 · баланс ширины +12–13%'}[label]
 return (f'<div class="panel{" new" if label=="Balanced" else ""}"><h2>{title}</h2>'
 f'<div class="big" style="font-family:{fm}">W</div>'
 f'<div class="mid" style="font-family:{fm}">WOW</div>'
 f'<div class="small" style="font-family:{fm}">WAVE · W</div>'
 f'<div style="font:15px/1.45 {fm}">WIDE WORLD</div></div>')
pages=[]
for i,face in enumerate(('Display','Text'),1):
 g=m['masters'][face]['geometry'];width=100*(g['new_advance']/g['original_advance']-1)
 pages.append('<section class="page">'+header(f'{face}: W с α — три компоновки','Сравнение реальных CFF контуров')+
 '<div class="three">'+''.join(wpanel(face,k) for k in ('Base','Wide','Balanced'))+'</div>'+
 f'<div class="note"><b>WAlphaBalanced:</b> 8/8 конструктивных диагоналей на α, новая ширина {g["new_advance"]:.0f} UPM (+{width:.2f}%). Для сравнения широкая v0.108 требовала около +27%. Уплотнение двух нижних просветов и изменение площади заливки означают, что без художественной оценки считать такую W готовой нельзя.</div>'+footer(i)+'</section>')

def xsizes(which):
 fm='Text'+which
 top='v0.106 · активная форма X/Х' if which=='Base' else 'v0.108 · XSoft (оптический кандидат)'
 z=f'<div class="panel{" new" if which=="XSoft" else ""}"><h2>{top}</h2>'
 z+=f'<div style="font:90px/1.08 {fm}">X Х</div>'
 for sz in (12,14,16,18,24,32):
  label=f'{sz} px'
  phrase='X Х X-RAY · ХАРАКТЕР' if sz<=18 else 'X Х X-RAY'
  z+=f'<div class="sz">{label}</div><div style="font:{sz}px/1.26 {fm};white-space:nowrap">{phrase}</div>'
 return z+'</div>'
pages.append('<section class="page">'+header('X/Х: Text на 12–32px','Геометрия XSoft против активной v0.106')+
 '<div class="two">'+xsizes('Base')+xsizes('XSoft')+'</div>'+
 '<div class="note">Независимый FreeType-растровый контроль в словах 12/14/16px обнаружил лишь небольшие изменения антиалиасинга/маски в отдельных пикселях. Обе формы читаются типографски сходно на пробе, но это не означает доказанного превосходства XSoft. Полные увеличенные пиксельные пробы приложены отдельным PNG.</div>'+footer(3)+'</section>')
rows=''
for face in ('Display','Text'):
 g=m['masters'][face]['geometry'];a=x['styles'][face]
 rows+=f'<tr><td>{face}</td><td>{g["original_advance"]} → {g["new_advance"]} (+{100*(g["new_advance"]/g["original_advance"]-1):.2f}%)</td><td>8/8 · α</td><td>{a["12"]["visible12"]}</td><td>{a["14"]["visible12"]}</td><td>{a["16"]["visible12"]}</td></tr>'
pages.append('<section class="page">'+header('Численные результаты и критерии решения','Проверены сохранённые OTF и реальная растеризация')+
 '<table><thead><tr><th>Мастер</th><th>W: advance (UPM)</th><th>Прямые α</th><th>XSoft 12px</th><th>XSoft 14px</th><th>XSoft 16px</th></tr></thead><tbody>'+rows+'</tbody></table>'+
 '<div class="panel" style="min-height:0;margin-top:16px"><h2>Что означают результаты</h2>'+
 '<p>1. WAlphaBalanced уменьшает рост ширины по сравнению с WAlphaWide, но требует дополнительного оптического согласования: центральные переходы/нижние просветы более плотные, площадь контура изменилась.</p>'+
 '<p>2. В трёх последних столбцах указано количество различающихся пикселей с порогом 12/255 в одной и той же строке «X Х X-RAY ХАРАКТЕР» размером 340×60 px. Эти значения показывают измеримый эффект рендера, а не улучшение читабельности.</p>'+
 '<p>3. Латинская/кириллическая X/Х в XSoft по-прежнему общий контур, все β-прямые и метрики без изменений. Новая W изменена в отдельном экспериментальном шрифте; изменения никогда не объединялись и не применялись к работе заказчиков.</p>'+
 '<p>4. По решению собственника активный baseline остаётся v0.106; эксперимент v0.107 с дополнительными прорезями не возобновляется. Только Display A/А имеет разомкнутую планку.</p></div>'+
 '<div class="note">Открытые критерии: художественное сравнение при 12–16px на физических экранах, межбуквенные интервалы для W, подтверждение оптического веса, лицензирование и подготовка шрифта к выпуску.</div>'+footer(4)+'</section>')
assert len(pages)==4
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
pdf=P/'Golden-Step-v0109-W-BALANCED-X-SMALL-REVIEW.pdf'
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new',
 '--no-sandbox','--disable-gpu','--user-data-dir=/tmp/gsv0109-proof',
 '--no-pdf-header-footer','--print-to-pdf='+str(pdf),(P/'specimen.html').as_uri()],
 capture_output=True,text=True,timeout=40)
if r.returncode:raise RuntimeError(r.stderr[-900:])
print('RENDERED',pdf.name,pdf.stat().st_size)
