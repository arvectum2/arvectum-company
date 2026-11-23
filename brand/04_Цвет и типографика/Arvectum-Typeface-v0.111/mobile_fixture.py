"""Two exactly equivalent local HTML typography fixtures, differing ONLY font URLs."""
from pathlib import Path
P=Path(__file__).resolve().parent
(P/'cases').mkdir(exist_ok=True)
body='''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Golden Step W kerning - responsive case</title>
<style>
@font-face{font-family:GSD;src:url("DISPLAY_SRC") format("opentype")}
@font-face{font-family:GST;src:url("TEXT_SRC") format("opentype")}
*{box-sizing:border-box}
html,body{margin:0;padding:0;color:#18374f;background:#fbfdfd;width:100%;overflow-x:hidden}
body{font-family:GST,sans-serif}
header{background:#0c3448;color:white;padding:22px 18px 16px}
.brand{font-family:GSD;font-size:27px}
header p{font-size:13px;line-height:1.5;max-width:550px;margin:8px 0}
main{padding:16px;max-width:760px;margin:auto}
.kicker{font:600 12px sans-serif;letter-spacing:.04em;color:#007a73;margin:12px 0 8px}
.large{font-family:GSD;white-space:normal;overflow-wrap:normal;font-size:38px;line-height:1.25}
.example{font-family:GST;line-height:1.4}
.mini{font-family:GST;font-size:12px;line-height:1.4}
.k14{font-family:GST;font-size:14px;line-height:1.4}
.k16{font-family:GST;font-size:16px;line-height:1.4}
.k24{font-family:GST;font-size:24px;line-height:1.4}
.card{background:white;border:1px solid #c7dbd9;border-radius:8px;padding:12px;margin-bottom:14px}
.em{color:#0a7b6e;font-weight:600}
footer{padding:18px;font:12px/1.5 sans-serif;color:#52767e}
</style></head>
<body><header><div class="brand">ARVECTUM · WAVE</div><p>Два оптических мастера Golden Step: W под углом α; X/Х под углом β.</p></header>
<main>
<div class="kicker">Display / 38px</div>
<div class="card large">WAX · WAVE · WOW<br>WONDER WORLD</div>
<div class="kicker">Text / 12px</div><div class="card mini">WA AW WE WO OW WI WR WN WL W. W, · X Х<br>WAVE · WELCOME · WATER · ХАРАКТЕР</div>
<div class="kicker">Text / 14px</div><div class="card k14">WA AW WE WO OW WI WR WN WL W. W, · X Х<br>WAVE · WELCOME · WATER · ХАРАКТЕР</div>
<div class="kicker">Text / 16px</div><div class="card k16">WA AW WE WO OW WI WR WN WL W. W, · X Х<br>WAVE · WELCOME · WATER · ХАРАКТЕР</div>
<div class="kicker">Text / 24px</div><div class="card k24">WA · AW · WO · OW<br>X Х · WAVE</div>
<div class="kicker">Mixed word and recognition checks</div>
<div class="card example">Arvectum WAVE — ЯРКО · ХЛЕБ · WAX · WORLD · ХАРАКТЕР.<br><span class="em">До выпуска необходима художественная приёмка на устройствах.</span></div>
</main><footer>Исследовательская фикстура. Утверждённый Wordmark не изменён; дополнительные разрывы отсутствуют.</footer>
</body></html>'''
src={
 'before':('..%2F..%2FArvectum-Typeface-v0.110%2Fotf%2FArvectumGoldenStepDisplayAlphaWWorking0110-Medium.otf',
           '..%2F..%2FArvectum-Typeface-v0.110%2Fotf%2FArvectumGoldenStepTextAlphaWWorking0110-Regular.otf'),
 'after':('../otf/ArvectumGoldenStepDisplayWKernsWorking0111-Medium.otf',
          '../otf/ArvectumGoldenStepTextWKernsWorking0111-Regular.otf')}
# Browser file relative to cases/: actual directories are ../.. /v0.110
src['before']=('../../Arvectum-Typeface-v0.110/otf/ArvectumGoldenStepDisplayAlphaWWorking0110-Medium.otf',
               '../../Arvectum-Typeface-v0.110/otf/ArvectumGoldenStepTextAlphaWWorking0110-Regular.otf')
for label,(display,text) in src.items():
 # after relative to cases should go back one directory
 if label=='after':
  display='../otf/ArvectumGoldenStepDisplayWKernsWorking0111-Medium.otf'
  text='../otf/ArvectumGoldenStepTextWKernsWorking0111-Regular.otf'
 data=body.replace('DISPLAY_SRC',display).replace('TEXT_SRC',text)
 (P/'cases'/f'mobile-{label}.html').write_text(data)
assert (P/'cases/mobile-before.html').read_text().replace('Arvectum-Typeface-v0.110/otf/ArvectumGoldenStepDisplayAlphaWWorking0110-Medium.otf','PATH').replace('Arvectum-Typeface-v0.110/otf/ArvectumGoldenStepTextAlphaWWorking0110-Regular.otf','PATH').replace('../../PATH','PATH') == (P/'cases/mobile-after.html').read_text().replace('../otf/ArvectumGoldenStepDisplayWKernsWorking0111-Medium.otf','PATH').replace('../otf/ArvectumGoldenStepTextWKernsWorking0111-Regular.otf','PATH')
print('MOBILE HTML MATCH, only local font URLs differ')
