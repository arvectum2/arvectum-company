"""Vector PDF proof (4 A4 landscape pages): real CFF fonts and SVG outline masters."""
from pathlib import Path
import html
P=Path(__file__).resolve().parent
fontcss=[]
for sty in ('Display','Text'):
 sub='Medium' if sty=='Display' else 'Regular'
 fontcss.append(f"@font-face{{font-family:Src{sty};src:url('../Arvectum-Typeface-v0.83/experimental/S/Arvectum{sty}GoldenStepRetroSDraft083-{sub}.otf')}}")
 for variant in 'ABC':fontcss.append(f"@font-face{{font-family:{variant}{sty};src:url('experimental/{sty}-{variant}.otf')}}")
style=''.join(fontcss)+''.join(f'.{v}{s}{{font-family:{v}{s}}}' for v in 'ABC' for s in ('Display','Text'))+''.join(f'.Src{s}{{font-family:Src{s}}}' for s in ('Display','Text'))
style+='''
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}html,body{margin:0;background:#dbe5e9;color:#001432}body{-webkit-print-color-adjust:exact;print-color-adjust:exact;font-family:Arial,sans-serif}.sheet{width:297mm;height:210mm;background:#fff;position:relative;padding:12mm 14mm;break-after:page;overflow:hidden}.sheet:last-child{break-after:auto}.top{display:flex;justify-content:space-between;align-items:end;border-bottom:2px solid #3ca897;padding-bottom:11px}.tag{font:bold 11px Arial;letter-spacing:1.4px;color:#08786e}.top h1{font:500 28px Arial;margin:6px 0 0}.meta{font:10px/1.5 Arial;color:#4a697a;text-align:right}.columns{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:17px}.col{border:1px solid #d6e4e7;background:#f8fbfc;min-height:475px;padding:12px 13px;overflow:hidden}.col h2{font:700 14px Arial;color:#116c68;margin:0 0 4px}.col .desc{font:11px Arial;color:#567481;padding:0 0 10px;border-bottom:1px solid #d1e0e4}.giant{font-size:98px;white-space:nowrap;line-height:1.6;letter-spacing:0}.twins{font-size:78px;line-height:1.15;white-space:nowrap}.anchor{font-size:58px;line-height:1.35;white-space:nowrap}.samples{margin-top:12px;border-top:1px solid #d2e0e4;padding-top:12px}.samples div{white-space:nowrap;line-height:1.55}.note{margin-top:13px;border-left:4px solid #44aa98;background:#f1f6f7;padding:9px 12px;font:12px/1.45 Arial;color:#365c68}.bottom{position:absolute;bottom:10mm;left:14mm;right:14mm;border-top:1px solid #d0dee2;padding-top:9px;display:flex;justify-content:space-between;font:10px Arial;color:#526c7b}.line{white-space:nowrap;margin:7px 0}.slabel{font:700 11px Arial;color:#5c7683}.size12{font-size:12px}.size16{font-size:16px}.size24{font-size:24px}.size36{font-size:36px}.size48{font-size:48px}.testcolumn{min-height:490px}.testcolumn .line{margin-bottom:10px;white-space:nowrap}.shapes{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:14px}.shape{border:1px solid #d4e3e6;background:#f8fbfc;padding:11px;height:235px;overflow:hidden}.shape svg{width:100%;height:164px}.shape .label{font:bold 13px Arial;color:#08786e}.pair{display:flex;gap:12px;justify-content:space-around}.pair svg{width:47%;height:170px}.shape .detail{font:11px Arial;color:#526f7a}strong{font-weight:700}
'''
labels=[('Src','v0.83 S · исходный','Поздние дуги'),('A','A · Structural','Самые прямые участки'),('B','B · Balanced','Расширенные скругления'),('C','C · Arvectum Main','Умеренные скругления')]

def header(title,description,idx):
 return f'<section class="sheet"><div class="top"><div><div class="tag">ARVECTUM  /  GOLDEN STEP  /  v0.84</div><h1>{title}</h1></div><div class="meta">{description}<br>ЭКСПЕРИМЕНТ — НЕ УТВЕРЖДЕНО</div></div>'

def footer(idx):return f'<div class="bottom"><span>СВОИ ПАРАМЕТРИЧЕСКИЕ ВЕКТОРЫ · ПРОВЕРКА В РЕАЛЬНЫХ CFF · ПРЕЖНИЙ ШРИФТ СОХРАНЁН</span><span>{idx:02d} / 04</span></div></section>'

pages=[]
for idx,st in enumerate(('Display','Text'),1):
 cards=[]
 for key,title,desc in labels:
  cls=key+st
  content=f'<div class="giant {cls}">Зз</div><div class="twins {cls}">З 3</div><div class="anchor {cls}">АЕМИ</div><div class="samples">'
  for phrase,size in [('ЗВЕЗДА',36),('заказ и связь',27),('Зона 3 · 33',26)]:
   content+=f'<div class="{cls}" style="font-size:{size}px">{phrase}</div>'
  content+='</div>'
  cards.append(f'<div class="col"><h2>{title}</h2><div class="desc">{desc}</div>{content}</div>')
 pages.append(header(f'{st} — реальные новые контуры З / з','СРАВНЕНИЕ ТРЁХ КОНСТРУКЦИЙ',idx)+'<div class="columns">'+''.join(cards)+'</div><div class="note">Изменены только З/з. А/Е/М, 3 и остальные буквы не тронуты. Прямые соединяются <strong>плавными короткими скруглениями</strong>.</div>'+footer(idx))

# Small-size page (Text), same characters and working font context.
cards=[]
for key,title,desc in labels:
 cls=key+'Text';card=f'<div class="col testcolumn"><h2>{title}</h2><div class="desc">{desc}</div>'
 for size,phrase in [(12,'3 заказа / Зона 3 / 33'),(16,'ЗВЕЗДА · заказы и связь'),(24,'Золото и развитие'),(36,'Знания'),(48,'ЗВЕЗДА')]:
  card+=f'<div class="slabel">{size} px</div><div class="line {cls}" style="font-size:{size}px">{phrase}</div>'
 card+='</div>';cards.append(card)
pages.append(header('Text — проверка в небольших размерах','12 / 16 / 24 / 36 / 48 PX',3)+'<div class="columns">'+''.join(cards)+'</div><div class="note">Малый кегль и контекст позволяют оценивать живую букву; метрика сходства З/3 и геометрический PASS сами по себе не доказывают читаемость.</div>'+footer(3))

shape_cards=[]
for key in 'ABC':
 svgs=[(P/'glyphs'/key/'Display'/f'U+{ord(ch):04X}.svg').read_text() for ch in 'Зз']
 shape_cards.append(f'<div class="shape"><div class="label">{key} · {dict(A="STRUCTURAL",B="BALANCED",C="ARVECTUM MAIN")[key]}</div><div class="pair">{svgs[0]}{svgs[1]}</div><div class="detail">Два отдельных оригинальных SVG-контура · Display</div></div>')
pages.append(header('Конструкции: прямые и ограниченные радиусы','ИЗ РЕДАКТИРУЕМЫХ SVG-МАСТЕРОВ',4)+'<div class="shapes">'+''.join(shape_cards)+'</div><div class="note">Каждая буква построена как <strong>прямая → четвертной плавный поворот → прямая</strong>. Отличаются радиусы и доля прямых. Исходная цифра 3 оставлена для противопоставления буквенной З. Никакие контуры сторонних шрифтов не копировались.</div>'+footer(4))
(P/'comparison.css').write_text(style)
(P/'comparison.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><link rel="stylesheet" href="comparison.css"><title>Golden Step v0.84: Original Cyrillic Z Designs</title></head><body>'+''.join(pages)+'</body></html>')
print('HTML_VECTOR_PROOF',len(pages),'pages',len(shape_cards),'SVG panels')
