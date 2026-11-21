"""One review PDF from the exact v0.82 A CFF vector outlines, not generated imagery.
No mutation of font masters; all 212 encoded Unicode positions per style included.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen
import unicodedata,hashlib,html,json,math
P=Path(__file__).resolve().parent
SRC=P/'experimental/A'
FONTS={
 'Display':P/'experimental/A/ArvectumDisplayGoldenStepFacetADraft082-Medium.otf',
 'Text':P/'experimental/A/ArvectumTextGoldenStepFacetADraft082-Regular.otf',
}
S={}
for sty,path in FONTS.items():
 f=TTFont(path); cmap=f.getBestCmap(); glyphset=f.getGlyphSet()
 assert len(cmap)==212,(sty,len(cmap))
 assert hashlib.sha256(path.read_bytes()).digest()==hashlib.sha256((SRC/path.name).read_bytes()).digest()
 S[sty]={'font':f,'cmap':cmap,'glyphset':glyphset,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'contours':{}}
 for cp,name in cmap.items():
  rec=RecordingPen();glyphset[name].draw(rec)
  S[sty]['contours'][f'U+{cp:04X}']=len(rec.value)
 assert cmap==S['Display']['cmap'] if sty=='Text' else True
print('VERIFIED',[(s,len(v['cmap'])) for s,v in S.items()])

def cls(cp):
 if cp in (0x0401,) or 0x0410<=cp<=0x042F:return 'КИРИЛЛИЦА · ПРОПИСНЫЕ'
 if cp in (0x0451,) or 0x0430<=cp<=0x044F:return 'КИРИЛЛИЦА · СТРОЧНЫЕ'
 if 0x41<=cp<=0x5A:return 'ЛАТИНИЦА · ПРОПИСНЫЕ'
 if 0x61<=cp<=0x7A:return 'ЛАТИНИЦА · СТРОЧНЫЕ'
 if 0x30<=cp<=0x39:return 'ЦИФРЫ'
 if 0x300<=cp<=0x36F:return 'КОМБИНИРУЕМЫЕ ЗНАКИ'
 return 'ПУНКТУАЦИЯ · ДЕНЕЖНЫЕ · МАТЕМАТИЧЕСКИЕ ЗНАКИ'
ORDER=['КИРИЛЛИЦА · ПРОПИСНЫЕ','КИРИЛЛИЦА · СТРОЧНЫЕ','ЛАТИНИЦА · ПРОПИСНЫЕ','ЛАТИНИЦА · СТРОЧНЫЕ','ЦИФРЫ','ПУНКТУАЦИЯ · ДЕНЕЖНЫЕ · МАТЕМАТИЧЕСКИЕ ЗНАКИ','КОМБИНИРУЕМЫЕ ЗНАКИ']

def outline(style,cp,large=False):
 font=S[style]['font'];name=S[style]['cmap'][cp];g=S[style]['glyphset'][name]
 pen=SVGPathPen(S[style]['glyphset']);g.draw(pen)
 d=pen.getCommands()
 if not d:return None
 b=BoundsPen(S[style]['glyphset']);g.draw(b)
 x0,y0,x1,y1=b.bounds
 W,H=(194,142) if large else (116,79)
 scale=.062 if large else .0335
 scale=min(scale,(W-12)/max(1,x1-x0),(H-10)/max(1,y1-y0))
 cx=(x0+x1)/2; cy=(y0+y1)/2
 x=W/2-cx*scale;y=H/2+cy*scale
 return f'<svg class="outline" viewBox="0 0 {W} {H}" role="img" aria-label="{cp:04X}"><path d="{html.escape(d,quote=True)}" fill="#001432" transform="translate({x:.4f} {y:.4f}) scale({scale:.6f} {-scale:.6f})"/></svg>'

def card(style,cp):
 name=unicodedata.name(chr(cp),'SPACE')
 if cp in (0x20,0xA0,0x202F):
  # Visualise spacing through a real font-based side-by-side pair, no invented glyph.
  glyph=f'<span class="space-preview {style.lower()}">A{html.escape(chr(cp))}B</span>'
 elif 0x300<=cp<=0x36F:
  glyph=f'<span class="mark-preview {style.lower()}">а{chr(cp)}</span>'
 else:glyph=outline(style,cp)
 assert glyph
 descr=html.escape(name.title())
 label=html.escape('ПРОБЕЛ' if cp==0x20 else chr(cp)) if cp in (0x20,0xA0,0x202F) else ''
 return f'<div class="glyphcard"><div class="glyph-visual">{glyph}</div><div class="glyphid">U+{cp:04X} <span class="origchar">{label}</span></div><div class="glyphname">{descr}</div></div>'

def pnum(n):return f'<footer><span>ARVECTUM GOLDEN STEP · ВЕКТОРНЫЙ КАТАЛОГ v0.82 A</span><span>{n:02d} · ЧЕРНОВИК ДЛЯ ВЫЧИТКИ</span></footer>'

def page(title,eyebrow,body,number,extra=''):
 return f'<section class="page {extra}"><header><div><span class="brand">ARVECTUM / GOLDEN STEP</span><h1>{title}</h1></div><div class="eyebrow">{eyebrow}</div></header><main>{body}</main>{pnum(number)}</section>'

pages=[]
def add(title,eyebrow,body,extra=''):
 pages.append(page(title,eyebrow,body,len(pages)+1,extra))

b='''<div class="coverrow"><div><div class="kicker">ПОЛНЫЙ НАБОР СИМВОЛОВ</div><div class="hero display">Интеллект<br>в действии.</div><p class="caption">Display Medium · крупный кегль и заголовки</p></div><div><div class="kicker">РАБОЧЕЕ НАЧЕРТАНИЕ</div><div class="hero text">Цифровые решения<br>для бизнеса.</div><p class="caption">Text Regular · текст, таблицы и документы</p></div></div><div class="notebox"><strong>Для художественной вычитки, а не утверждения выпуска.</strong> 212 кодовых позиций на начертание — 424 отдельных образца. В таблицах показаны <b>реальные векторные контуры CFF</b> из Golden Step Facet A Draft 082, построенные из ранее сохранённых SVG-мастеров. Две версии: Display / Text. В конце — реальные фразы, размеры и проблемные сочетания.<br><br>Красные флаги: похожесть 3/З, формы р/е, высота и соединения д/л, цифры, знаки и межбуквенные интервалы. Экспериментальные оптические варианты v0.63 не подмешаны.</div><div class="smallnote">Контуры только кандидата v0.82 A, без растровой генерации. В документе встроены точные исходные OTF с CFF-контуром (SIL OFL 1.1, производный от Inter 4.1).</div>'''
add('Гарнитура для вычитки','DISPLAY MEDIUM · TEXT REGULAR / v0.82 A',b,'cover')

for style in ('Display','Text'):
 groups={k:[] for k in ORDER}
 for cp in S[style]['cmap']:
  groups[cls(cp)].append(cp)
 for category in ORDER:
  vals=groups[category]
  if not vals:continue
  for start in range(0,len(vals),35):
   chunk=vals[start:start+35]
   body='<div class="glyphgrid">'+''.join(card(style,cp) for cp in chunk)+'</div>'
   label=f'{style.upper()} / {category} · {min(start+35,len(vals))}/{len(vals)}'
   add(category.title(),label,body,'catalog')
add('Два начертания рядом','ОСНОВНАЯ ГЕОМЕТРИЯ · МАССА · ПРОПОРЦИИ','''
<div class="twocol"><div class="panel"><div class="tag">DISPLAY MEDIUM</div><div class="demo-d display">АБВГДЕЁЖЗ<br>ИЙКЛМНОПР</div><div class="demo-s display">Абвгдеёжзийклмнопрстуфхцчшщъыьэюя</div><div class="demo-d display">ARVECTUM</div><div class="demo-s display">0123456789 · З / 3 · О / 0</div></div>
<div class="panel"><div class="tag">TEXT REGULAR</div><div class="demo-d text">АБВГДЕЁЖЗ<br>ИЙКЛМНОПР</div><div class="demo-s text">Абвгдеёжзийклмнопрстуфхцчшщъыьэюя</div><div class="demo-d text">ARVECTUM</div><div class="demo-s text">0123456789 · З / 3 · О / 0</div></div></div>
<div class="prompt">Вопросы: баланс веса, открытость форм, различие латинских и кириллических букв, ширина цифр, высота строчных.</div>''','specimen')

add('Русский текст в работе','ДВА НАЧЕРТАНИЯ · РЕАЛЬНЫЕ СТРОКИ','''
<div class="wordblock"><div class="tag">DISPLAY MEDIUM · ЗАГОЛОВКИ</div><div class="headline display">Интеллект в действии.</div><div class="subhead display">Программное обеспечение и автоматизация</div><div class="thirdhead display">Цифровые решения для организаций</div></div>
<div class="twocol"><div class="panel"><div class="tag">TEXT REGULAR · 20 PX</div><p class="para-big text">Разрабатываем цифровые решения для бизнеса и организаций. Удобство интерфейса, ясность документации и проверяемость результатов важнее декоративности.</p><div class="tag">TEXT REGULAR · 16 PX</div><p class="para text">Заказчик получает согласованные исходные материалы, инструкции и результаты испытаний. Каждый этап предполагает критерии приёмки и понятный следующий шаг.</p></div>
<div class="panel"><div class="tag">DISPLAY MEDIUM · 20 PX</div><p class="para-big display">Разрабатываем цифровые решения для бизнеса и организаций. Удобство интерфейса, ясность документации и проверяемость результатов важнее декоративности.</p><div class="tag">DISPLAY MEDIUM · 16 PX</div><p class="para display">Заказчик получает согласованные исходные материалы, инструкции и результаты испытаний. Каждый этап предполагает критерии приёмки и понятный следующий шаг.</p></div></div>
<div class="prompt">Проверить р/е, З/3, д/л, ж/з, интервалы «сл», «ед», «оч» и общий ритм строк.</div>''','specimen')

add('English text','LATIN · TITLE · KERNING','''
<div class="wordblock"><div class="tag">DISPLAY MEDIUM</div><div class="headline display">Intelligence in action.</div><div class="subhead display">Arvectum · Software Engineering</div></div>
<div class="twocol"><div class="panel"><div class="tag">TEXT REGULAR</div><p class="para-big text">Clear systems. Reliable software. Thoughtful automation. We build tools that help teams work with information, documents and business processes.</p><div class="pairline text">AV  To  Wa  Yo  Te  Co  Pr</div><div class="pairline text">ct  ty  rv  AI  ov  ly</div></div>
<div class="panel"><div class="tag">DISPLAY MEDIUM</div><p class="para-big display">Clear systems. Reliable software. Thoughtful automation. We build tools that help teams work with information, documents and business processes.</p><div class="pairline display">AV  To  Wa  Yo  Te  Co  Pr</div><div class="pairline display">ct  ty  rv  AI  ov  ly</div></div></div>
<div class="prompt">Проверить интервалы, узнаваемость C/G/Q, I/l/1, O/0, f/t и читаемость небольших заголовков.</div>''','specimen')

add('Цифры и знаки','ТАБЛИЧНЫЕ СУММЫ · ПУНКТУАЦИЯ','''
<div class="twocol"><div class="panel"><div class="tag">TEXT REGULAR</div><div class="amount text">1 250 000,00 ₽</div><div class="amount text">25 670,42 €</div><div class="amount text">1234567890</div><div class="amount text">0000000000</div><div class="amount text">№ 17/2026</div></div>
<div class="panel"><div class="tag">DISPLAY MEDIUM</div><div class="amount display">1 250 000,00 ₽</div><div class="amount display">25 670,42 €</div><div class="amount display">1234567890</div><div class="amount display">0000000000</div><div class="amount display">№ 17/2026</div></div></div>
<div class="wordblock"><div class="tag">ЗНАКИ · TEXT REGULAR</div><div class="punct text">«Услуги» — от идеи до результата. “Design”: (A) [B] {C} / 1–2 …</div><div class="punct text">15 %, 1,5 ‰, +7 °C, ± 0,5, × ÷ ≤ ≥ ≠ ≈</div><div class="tag">КОМБИНИРУЕМЫЕ ДИАКРИТИКИ</div><div class="marks text">а̀  а́  а̂  а̃  а̄  ӑ  ӓ  а̊  а̧</div></div><div class="prompt">Проверить ширину и ритм цифр, знаки ₽/€/$, знак №, скобки, тире и положение ударений.</div>''','specimen')

focus=['3','З','р','е','д','л','0','О']
focusitems=[]
for ch in focus:
 a=outline('Display',ord(ch),True);b=outline('Text',ord(ch),True)
 focusitems.append(f'<div class="focuscard"><div class="focusname">{html.escape(ch)} <span>U+{ord(ch):04X}</span></div><div class="focuspair"><div>{a}<small>DISPLAY</small></div><div>{b}<small>TEXT</small></div></div></div>')
add('Контуры спорных букв','ПРЯМЫЕ ВЕКТОРНЫЕ ПУТИ CFF · 2 НАЧЕРТАНИЯ','<div class="focusgrid">'+''.join(focusitems)+'</div><div class="prompt">Проверить сходство 3 и З, скругление р, высоту перекладины е, рисунок д/л и пару О/0. Формы увеличены из оригинальных путей CFF, без растрирования и без подмены v0.63.</div>','specimen')

add('Пары и расстояния','ОПТИЧЕСКИЙ КОНТРОЛЬ КЕРНИНГА','''
<div class="twocol"><div class="panel"><div class="tag">DISPLAY</div><div class="pairbig display">З3З3 03ОO</div><div class="pairbig display">рее ед сл жд</div><div class="pairbig display">ту ут ку оч уч</div><div class="pairbig display">AV To Wa AI</div><div class="pairbig display">ct ty rv Co Pr</div></div>
<div class="panel"><div class="tag">TEXT</div><div class="pairbig text">З3З3 03ОO</div><div class="pairbig text">рее ед сл жд</div><div class="pairbig text">ту ут ку оч уч</div><div class="pairbig text">AV To Wa AI</div><div class="pairbig text">ct ty rv Co Pr</div></div></div>
<div class="notebox">Golden Step v0.82 A содержит 85 явно настроенных пар кернинга в каждом начертании. Эта проверка не меняет пары. Смотрите на «дырки» внутри слов, касания, оптическую равномерность и соотношение круглых и прямых штрихов.</div>''','specimen')

add('Лист замечаний','ДЛЯ ВЫЧИТКИ · НЕ АКТ ПРИЁМКИ','''
<div class="checks"><div><b>01</b> Различимость 3/З при малом размере <span>□ ОК  □ ПРАВИТЬ</span></div>
<div><b>02</b> Рисунок р и перекладина е <span>□ ОК  □ ПРАВИТЬ</span></div>
<div><b>03</b> Кириллица д/л/ж/з/ё <span>□ ОК  □ ПРАВИТЬ</span></div>
<div><b>04</b> Латиница, цифры, знаки, валюты <span>□ ОК  □ ПРАВИТЬ</span></div>
<div><b>05</b> Диакритика и интервалы <span>□ ОК  □ ПРАВИТЬ</span></div>
<div><b>06</b> Реальный текст в разных кеглях <span>□ ОК  □ ПРАВИТЬ</span></div></div>
<div class="noteheading">Замечание к знаку (например, U+0417), начертанию и кеглю:</div>
<div class="emptyline"></div><div class="emptyline"></div><div class="emptyline"></div>
<div class="noteheading">Общие замечания:</div><div class="emptyline"></div><div class="emptyline"></div>
<div class="notebox">Отдельное художественное решение собственника необходимо для выбора форм букв. Этот PDF — каталог рабочего кандидата. Он не меняет мастер-логотип, не является финальным лицензированием шрифта и не утверждает выпуск.</div>''','specimen')

(P/'full-specimen-A.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>Arvectum Golden Step — полный векторный каталог для вычитки</title><link rel="stylesheet" href="specimen-A.css"></head><body>'+''.join(pages)+'</body></html>')
result={'status':'SOURCE_CANDIDATE_V081_DRAFT','styles':{},'pages':len(pages),'font_technology':'CFF vector from preserved historical SVG masters; no synthetic glyphs',
 'catalog_codepoints_per_style':212,'catalog_display_total':424,'review_categories':ORDER}
for style,d in S.items():
 result['styles'][style]={'source_otf':FONTS[style].name,'sha256':d['source_sha256'],'codepoints':[f'U+{cp:04X}' for cp in d['cmap']],
 'nonempty_vector_outlines':sum(bool(x) for x in d['contours'].values()),'empty_outlines':[key for key,n in d['contours'].items() if not n]}
(P/'evidence/full-specimen-A-coverage.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('SPECIMEN HTML PAGES',len(pages),'GLYPHS',sum(len(v['cmap']) for v in S.values()),'from original vector CFF')
