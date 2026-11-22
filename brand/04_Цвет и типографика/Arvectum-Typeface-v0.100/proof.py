"""Five-page real-font PDF specimen with canonical logo reference and diagonal audit."""
from pathlib import Path
import html,subprocess,xml.etree.ElementTree as ET,json
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
audit=json.loads((P/'evidence/diagonal-audit.json').read_text())
ref=ET.parse(R/m['source_logo']).getroot()
mark=next(x.attrib['d'] for x in ref.iter() if x.tag.endswith('path'))
(P/'evidence/approved-A-reference.svg').write_text(
 '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1925 1490"><g transform="translate(0 1490) scale(1 -1)"><path fill="#001432" d="'+html.escape(mark,quote=True)+'"/></g></svg>\n')
css=''
for face,weight in [('Display','Medium'),('Text','Regular')]:
 for v,file in [('old',f'../Arvectum-Typeface-v0.99/experimental/ArvectumGoldenStep{face}LowercaseRhythmDraft099-{weight}.otf'),
 ('new',f'experimental/ArvectumGoldenStep{face}CanonicalAngleDraft0100-{weight}.otf')]:
  css+=f'@font-face{{font-family:"{face}{v}";src:url("{file}") format("opentype")}}'
css+='''
@page{size:A4 landscape;margin:0}
*{box-sizing:border-box}html,body{margin:0;background:white;color:#001432;font-family:Arial,sans-serif}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:10mm 13mm;position:relative;break-after:page;overflow:hidden}
.page:last-child{break-after:auto}
.head{display:flex;justify-content:space-between;align-items:end;border-bottom:2px solid #41b599;padding-bottom:9px}
.kicker{font:bold 11px Arial;color:#087c70;letter-spacing:1.2px}h1{font:500 24px Arial;margin:5px 0 0}
.meta{font:10px/1.4 Arial;color:#5a7680;text-align:right}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:15px}
.panel{border:1px solid #c5dcdc;background:#f8fbfb;padding:12px;min-height:335px;overflow:hidden}
.panel.new{border:2px solid #41b599;padding:11px}
h2{font:bold 14px Arial;color:#08776a;margin:0 0 6px}
.big{font-size:103px;line-height:1.19;white-space:nowrap}
.med{font-size:49px;line-height:1.2;white-space:nowrap}
.words{font-size:32px;line-height:1.3;white-space:nowrap}
.small{font-size:16px;line-height:1.38}
.rule{height:1px;background:#c9dede;margin:8px 0}
.note{margin-top:12px;padding:9px 12px;border-left:4px solid #41b599;background:#ecf7f4;font:11.5px/1.45 Arial}
.foot{position:absolute;bottom:8mm;left:13mm;right:13mm;border-top:1px solid #cedfdf;padding-top:8px;display:flex;justify-content:space-between;font:10px Arial;color:#607880}
.glyphs{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:14px}
.glyph{background:#f8fbfb;border:1px solid #c7dddd;padding:9px;overflow:hidden}
.glyph img{width:100%;height:170px;object-fit:contain}
.measure{font:12px/1.5 Arial;color:#365963}
.demo{font:11px Arial;color:#668089;margin:10px 0 4px}
.alpha{font-size:26px;line-height:1.30;white-space:nowrap}
'''
def header(t,sub):
 return f'<div class="head"><div><div class="kicker">ARVECTUM GOLDEN STEP / v0.100</div><h1>{t}</h1></div><div class="meta">{sub}<div>ЭКСПЕРИМЕНТ — художественная приёмка открыта</div></div></div>'
def foot(n):
 return f'<div class="foot"><span>Источник наклона — утверждённый Golden Wordmark C v0.21 · θ=58,2825°</span><span>{n:02d}/05</span></div>'
def panel(face,ver,letters,phrase,prose):
 font=face+ver
 label='v0.100 — корректировка' if ver=='new' else 'v0.99 — до исправления'
 return f'<div class="panel{" new" if ver=="new" else ""}"><h2>{face}: {label}</h2><div class="big" style="font-family:{font}">{letters}</div><div class="rule"></div><div class="med" style="font-family:{font}">{phrase}</div><div class="small" style="font-family:{font};margin-top:13px">{prose}</div></div>'
pages=[]

pages.append('<section class="page">'+header('A/А Display: оригинальный угол и правый разрыв','Исправлена также ширина и слант ноги')+
 '<div class="cols">'+panel('Display','old','A А','АРВЕКТУМ','Старая конструкция Inter с наклоном около 70°.')+
 panel('Display','new','A А','АРВЕКТУМ','Новый контур первой A утверждённого логотипа, сохранён без масштабирования.')+'</div>'+
 '<div class="note"><img src="evidence/approved-A-reference.svg" style="display:inline-block;width:100px;height:72px;vertical-align:middle;margin-right:18px">Эталон: исходный утверждённый вектор A из Wordmark C. Перекладина опирается СЛЕВА и разрывается СПРАВА. Основные диагонали — 58,2825°, а не ≈70°.</div>'+foot(1)+'</section>')
pages.append('<section class="page">'+header('A/А Text: закрытая перекладина, тот же наклон','Оба начертания продолжают разрабатываться')+
 '<div class="cols">'+panel('Text','old','A А','АНАЛИТИКА','Ранее закрытая А из Inter-конструкции с наклонами около 70°.')+
 panel('Text','new','A А','АНАЛИТИКА','Закрытая Arvectum Text с геометрией ног логотипа, θ=58,2825°.')+'</div>'+
 '<div class="note">Ширина A/А теперь 2050 UPM вместо 1379/1338. Это намеренное изменение метрик, которое может изменить переносы: старые правила кернинга сохраняются как история, но ещё не приняты оптически.</div>'+foot(2)+'</section>')
def glyph(face,ch,version):
 path=f'glyphs/{version}/{face}/U+{ord(ch):04X}.svg'
 label={'v099':'v0.99','v0100':'v0.100'}[version]
 return f'<div class="glyph"><h2>{face} · {ch} · {label}</h2><img src="{path}"/></div>'
pages.append('<section class="page">'+header('Д/Л: прямые наклонные, трапециевидные формы','Л открыта снизу; Д замкнута нижней планкой')+
 '<div class="cols"><div class="panel"><h2>Display v0.100</h2><div class="big" style="font-family:Displaynew">Д Л</div><div class="words" style="font-family:Displaynew">ДЕЛО · ЛИДЕР</div></div>'+
 '<div class="panel new"><h2>Text v0.100</h2><div class="big" style="font-family:Textnew">Д Л</div><div class="words" style="font-family:Textnew">ДЕЛО · ЛИДЕР</div></div></div>'+
 '<div class="glyphs">'+glyph('Display','Д','v099')+glyph('Display','Д','v0100')+
 glyph('Display','Л','v099')+glyph('Display','Л','v0100')+'</div>'+
 '<div class="note">Левые внешние и внутренние прямые параллельны и совпадают с эталонным углом логотипа; Bézier-дуги прошлой версии полностью устранены. Д сохраняет нижнюю замкнутую перемычку и два выступа.</div>'+foot(3)+'</section>')
def lower(face):
 font=face+'new'
 h=f'<div class="panel{" new" if face=="Text" else ""}"><h2>{face} v0.100 — д/л</h2>'
 h+=f'<div class="big" style="font-family:{font}">д л</div>'
 for size in (12,14,16,18,24):
  h+=f'<div class="demo">{size} px</div><div style="font-family:{font};font-size:{size}px;line-height:1.2">Деловое предложение и план для отдела.</div>'
 return h+'</div>'
pages.append('<section class="page">'+header('Строчные д/л: те же правила на уровне x-height','Text 12–24 px, Display отдельно')+
 '<div class="cols">'+lower('Display')+lower('Text')+'</div>'+
 '<div class="note">Высота строчных 1056 UPM; оба левых края каждой формы имеют прямой наклон θ. Нижние элементы различаются: л разомкнута, д имеет замкнутую нижнюю планку и выступы. Нужна отдельная проверка читателями.</div>'+foot(4)+'</section>')
def summary(face):
 v=audit['masters'][face]
 items=v['key_glyphs']
 checked=' '.join(c+':'+items[c]['status'].replace('NEEDS_DESIGN','OPEN').replace('PASS','✓') for c in 'AАДЛдлKКИиМMХX')
 return f'<div class="panel{" new" if face=="Text" else ""}"><h2>{face} / полный CFF-аудит</h2><div class="measure"><b>{v["major_within_half_degree"]} / {v["major_diagonal_segments"]}</b> крупных прямых диагоналей в допуске ±0,5°</div><div class="rule"></div><div class="measure">{checked}</div><div class="demo">Сканированы все 2937 глифов, включая ещё не доработанные исходные формы Inter.</div></div>'
pages.append('<section class="page">'+header('Результат проверки ВСЕХ диагоналей','Полный аудит: не путать локальный PASS и глобальный')+
 '<div class="cols">'+summary('Display')+summary('Text')+'</div>'+
 '<div class="note">A/А, Д/Л и д/л проходят строгий локальный допуск ±0,08°. Однако K/К, M/М, X/Х и многие унаследованные знаки всё ещё используют другие углы. Глобальное соответствие не утверждено; следующая работа должна последовательно исправлять семейства с сохранением различимости.</div>'+foot(5)+'</section>')
assert len(pages)==5
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
out=P/'Golden-Step-v0100-STRUCTURAL-CORRECTION-REVIEW.pdf'
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--disable-gpu','--no-sandbox','--user-data-dir=/tmp/arvectum-golden-v0100-correction','--no-pdf-header-footer','--print-to-pdf='+str(out),(P/'specimen.html').as_uri()],capture_output=True,text=True,timeout=40)
if r.returncode:raise RuntimeError(r.stderr[-1100:])
print('RENDERED',out.name,out.stat().st_size)
