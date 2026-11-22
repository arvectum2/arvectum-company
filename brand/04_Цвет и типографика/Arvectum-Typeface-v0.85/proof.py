from pathlib import Path
import subprocess
P=Path(__file__).resolve().parent
style='''@font-face{font-family:GSDisplay;src:url("experimental/ArvectumGoldenStepDisplayBaseDraft085-Medium.otf") format("opentype")}
@font-face{font-family:GSText;src:url("experimental/ArvectumGoldenStepTextBaseDraft085-Regular.otf") format("opentype")}
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}
html,body{margin:0;background:#fff;color:#001432}body{-webkit-print-color-adjust:exact;print-color-adjust:exact;font-family:Arial,sans-serif}
.sheet{width:297mm;height:210mm;padding:11mm 14mm;break-after:page;position:relative;overflow:hidden}.sheet:last-child{break-after:auto}
.heading{display:flex;justify-content:space-between;align-items:end;border-bottom:2px solid #42ad9a;padding-bottom:10px}
.kicker{font:bold 11px Arial;color:#0a746b;letter-spacing:1px}h1{font:500 26px Arial;margin:6px 0 0}
.meta{font:10px/1.5 Arial;text-align:right;color:#456371}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:15px;margin-top:15px}
.panel{border:1px solid #cbdcdf;border-radius:4px;padding:14px 16px;background:#f8fbfc;overflow:hidden}
.panel h2{font:700 15px Arial;margin:0;color:#0a746b}
.note{font:11px/1.4 Arial;color:#617882;margin:5px 0 9px}
.gd{font-family:GSDisplay}.gt{font-family:GSText}
.hero{font-size:116px;line-height:1.14}.comparison{font-size:60px;line-height:1.25;white-space:nowrap}
.sentence{font-size:27px;line-height:1.5;white-space:nowrap}
.anchors{font-size:37px;line-height:1.46;white-space:nowrap}
.sr{font:10px Arial;color:#4e6a77;letter-spacing:.5px;margin-top:8px}
.line{white-space:nowrap;line-height:1.35}
.rule{border-top:1px solid #c8dddb;margin:10px 0}
.info{margin-top:13px;background:#edf6f4;border-left:4px solid #42ad9a;padding:10px 12px;font:12px/1.4 Arial}
.foot{position:absolute;left:14mm;right:14mm;bottom:9mm;border-top:1px solid #c8d5d9;padding-top:8px;display:flex;justify-content:space-between;font:10px Arial;color:#536f78}
'''
head=lambda title,meta:f'<div class="heading"><div><div class="kicker">ARVECTUM / GOLDEN STEP / v0.85</div><h1>{title}</h1></div><div class="meta">{meta}<br>Inter 4.1 CFF / ЭКСПЕРИМЕНТ</div></div>'
foot=lambda n:f'<div class="foot"><span>ИСХОДНЫЕ ВЕКТОРНЫЕ КОНТУРЫ INTER · НОЛЬ ПЕРЕРИСОВАННЫХ БУКВ</span><span>{n:02d}/02</span></div>'
panel=lambda sty,cl:f'<div class="panel"><h2>{sty}</h2><div class="note">Оригинальные буквы и метрики Inter (без дизайнерских поправок)</div><div class="{cl} hero">Зз</div><div class="{cl} comparison">З 3 · з 3</div><div class="rule"></div><div class="{cl} sentence">ЗВЕЗДА</div><div class="{cl} sentence">Зона 3. Заказ.</div><div class="{cl} anchors">АЕМИ Вв Бб</div></div>'
one='<section class="sheet">'+head('Возвращаемся к исходным буквам Inter','НУЛЕВАЯ БАЗА ДЛЯ НОВОГО ДИЗАЙНА')+'<div class="cols">'+panel('Display · Medium','gd')+panel('Text · Regular','gt')+'</div><div class="info">З/з здесь — <b>подлинные буквы Inter</b>. Три отвергнутых варианта v0.84 не используются. На следующем этапе меняем одну букву за раз, сравнивая с этой зафиксированной базой.</div>'+foot(1)+'</section>'
parts=[]
for sty,cl in [('Display','gd'),('Text','gt')]:
 rows=''.join(f'<div class="sr">{px} PX</div><div class="{cl} line" style="font-size:{px}px">{phrase}</div>' for px,phrase in [(12,'Зона 3. Заказ 33. Связь.'),(16,'Знания · технологии · Арвектум'),(24,'Золотое сечение и интеллект'),(38,'ЗВЕЗДА · Зз / 3')])
 parts.append(f'<div class="panel"><h2>{sty}: проверка читабельности</h2>{rows}<div class="rule"></div><div class="sr">ДРУГИЕ БУКВЫ — ЕЩЁ НЕ АДАПТИРОВАНЫ</div><div class="{cl} anchors">АЕМИ Зз Вв Бб</div></div>')
two='<section class="sheet">'+head('Буквы в словах и малых кеглях','12 / 16 / 24 / 38 PX')+'<div class="cols">'+''.join(parts)+'</div><div class="info">Концепция Arvectum: модульность, чёткая архитектура, управляемые плавные переходы. φ≈1,618 и диагональ 58,2825° используются только там, где это оправдано; контрформы, терминалы, читаемость и межбуквенные интервалы важнее формальной геометрии.</div>'+foot(2)+'</section>'
(P/'specimen.html').write_text('<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8"><style>'+style+'</style></head><body>'+one+two+'</body></html>')
pdf=P/'Golden-Step-v085-INTER-BASELINE-REVIEW.pdf'
exe='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
res=subprocess.run([exe,'--headless=new','--disable-gpu','--no-sandbox','--user-data-dir=/tmp/arvectum-gs-v085-print','--no-pdf-header-footer','--print-to-pdf='+str(pdf),(P/'specimen.html').as_uri()],capture_output=True,text=True,timeout=40)
if res.returncode!=0:raise RuntimeError(res.stderr[-1600:])
print('PDF:',pdf,'bytes:',pdf.stat().st_size)

