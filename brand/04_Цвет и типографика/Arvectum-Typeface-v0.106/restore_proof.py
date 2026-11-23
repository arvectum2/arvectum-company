"""Short comparative owner proof, actual installed webfonts, no production change."""
from pathlib import Path
import subprocess
P=Path(__file__).resolve().parent
css=''
for face,weight in (('Display','Medium'),('Text','Regular')):
 sources={'Restored':f'experimental/ArvectumGoldenStep{face}UnifiedForkDraft0106-{weight}.otf',
          'Rejected':f'../Arvectum-Typeface-v0.107/experimental/ArvectumGoldenStep{face}ForkDraft0107-{weight}.otf'}
 for name,path in sources.items():
  css+=f'@font-face{{font-family:{face}{name};src:url("{path}") format("opentype")}}'
css+="""
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}
body{margin:0;font-family:Arial,sans-serif;color:#12364c;background:#fff;-webkit-print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:12mm 14mm;position:relative;break-after:page;overflow:hidden}
.page:last-child{break-after:auto}
.header{border-bottom:2px solid #27aa93;padding-bottom:9px;display:flex;justify-content:space-between;align-items:end}
.kicker{font:bold 10px Arial;color:#087f73;letter-spacing:1px}
h1{font:500 24px Arial;margin:6px 0}
.meta{font:10px/1.35 Arial;color:#657e87;text-align:right}
.compare{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:15px}
.panel{border:1px solid #c4dbd7;background:#f8fbfa;padding:13px;min-height:350px;overflow:hidden}
.panel.active{border:2px solid #2db49d;padding:12px}
h2{font:bold 14px Arial;color:#097b70;margin:0 0 8px}
.big{font-size:89px;line-height:1.2;white-space:nowrap}
.mid{font-size:45px;line-height:1.25;white-space:nowrap}
.small{font-size:22px;line-height:1.35;white-space:nowrap}
.note{background:#eaf7f2;border-left:4px solid #28b49e;padding:12px;margin-top:15px;font:12px/1.48 Arial}
.footer{position:absolute;bottom:9mm;left:14mm;right:14mm;border-top:1px solid #cbdedb;padding-top:8px;font:10px Arial;color:#687d87;display:flex;justify-content:space-between}
"""
def header(title):
 return f'<div class="header"><div><div class="kicker">ARVECTUM GOLDEN STEP · RESTORED v0.106</div><h1>{title}</h1></div><div class="meta">Решение собственника: отклонить v0.107<div>Исходные OTF · контроль 23.11.2026</div></div></div>'
def panel(title,fam,active=False,top='',middle='',bottom=''):
 return f'<div class="panel{" active" if active else ""}"><h2>{title}</h2><div class="big" style="font-family:{fam}">{top}</div><div class="mid" style="font-family:{fam}">{middle}</div><div class="small" style="font-family:{fam}">{bottom}</div></div>'
def foot(n):
 return f'<div class="footer"><span>v0.106 восстановлена точно по SHA256 · никаких изменений утверждённого Wordmark и production</span><span>{n:02d}/02</span></div>'
p1=('<section class="page">'+header('Новые разрывы отменены: восстановлены исходные буквы')+
 '<div class="compare">'+panel('ОТКЛОНЕНО · v0.107','DisplayRejected',top='Р P Ь Ъ Ы',middle='Я R',bottom='ПРОЕКТ · БЫЛЬ · ПОДЪЁМ')+
 panel('ВОССТАНОВЛЕНО · v0.106','DisplayRestored',True,top='Р P Ь Ъ Ы',middle='Я R',bottom='ПРОЕКТ · БЫЛЬ · ПОДЪЁМ')+'</div>'+
 '<div class="note">Все экспериментальные прорези в стойках и горизонтальных соединениях у P/Р, Ь/Ъ/Ы, R/Я отменены. Восстановлены исходные цельные контуры в Display и Text, без правок размеров или Unicode.</div>'+foot(1)+'</section>')
p2=('<section class="page">'+header('Единственная разомкнутая перемычка — заглавные A/А')+
 '<div class="compare">'+panel('DISPLAY v0.106 · разрыв справа сохранён','DisplayRestored',True,top='A А',middle='K К Ж',bottom='АРВЕКТУМ · ARVECTUM')+
 panel('TEXT v0.106 · перемычка A/А замкнута, как раньше','TextRestored',False,top='A А',middle='K К Ж',bottom='АРВЕКТУМ · ARVECTUM')+'</div>'+
 '<div class="note">В Display A/А остаётся одобренная ранее диагональная правая отсечка с просветом в толщину правой ножки. В Text форма A/А всегда имела замкнутую перемычку; этот оптический мастер не изменяли. K/К и Ж возвращены к существовавшей до v0.107 геометрии с короткими горизонтальными соединениями.</div>'+foot(2)+'</section>')
html='<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+p1+p2+'</body></html>'
target=P/'RESTORE-v0106-A-ONLY-REVIEW.pdf'
(P/'restore_proof.html').write_text(html)
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--no-sandbox',
 '--disable-gpu','--user-data-dir=/tmp/gsv106-restore','--no-pdf-header-footer',
 '--print-to-pdf='+str(target),(P/'restore_proof.html').as_uri()],capture_output=True,text=True,timeout=38)
if r.returncode:raise RuntimeError(r.stderr[-950:])
print('PDF CREATED',target.name,target.stat().st_size)
