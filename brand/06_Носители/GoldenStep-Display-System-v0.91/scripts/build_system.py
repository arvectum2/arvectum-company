"""One applied composition candidate, separate from the pure font-only A/B."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent.parent
T=(P/'tokens-golden.css').read_text()
(P/'tokens-system.css').write_text(T)
styles={
 'letter':"""h1{font-size:29pt!important;line-height:1.10!important;letter-spacing:-.032em!important}
h1::after{content:'';display:block;width:28mm;height:.9mm;background:#41B599;margin-top:5mm}
""",
 'proposal':"""h1{font-size:34pt!important;line-height:1.05!important;letter-spacing:-.035em!important}
h1::after{content:'';display:block;width:22mm;height:1mm;background:#41B599;margin-top:5mm}
h2{letter-spacing:-.02em}
""",
 'mobile':""".hero h1{font-size:clamp(39px,9.5vw,69px)!important;line-height:1.06!important;letter-spacing:-.032em!important}
.hero h1::after{content:'';display:block;width:76px;height:4px;background:#41B599;margin-top:23px}
.content h2{letter-spacing:-.025em;line-height:1.12}
"""
}
for carrier,css in styles.items():
 src=(P/'cases'/carrier/'golden.html').read_text()
 assert src.count('</head>')==1
 dest=src.replace('tokens-golden.css','tokens-system.css')
 dest=dest.replace('</head>',f'<style id="golden-display-composition">{css}</style></head>')
 (P/'cases'/carrier/'system.html').write_text(dest)
# Renderer is identical in all other respects; avoid contamination of font-only evidence.
r=(P/'scripts/render.py').read_text()
r=r.replace("for variant in ('inter','golden'):", "for variant in ('inter','system'):")
r=r.replace("evidence/browser-report.json","evidence/browser-system-report.json")
assert "'system'" in r and 'browser-system-report' in r
(P/'scripts/render_system.py').write_text(r)
c=(P/'scripts/compare.py').read_text()
c=c.replace('golden','system').replace('Golden Step Display v0.91','Golden Display + hierarchy v0.91')
c=c.replace('SIDE-BY-SIDE-REVIEW.pdf','SYSTEM-SIDE-BY-SIDE-REVIEW.pdf')
c=c.replace("f'review-","f'system-review-")
c=c.replace("pixel-difference-report.json","system-pixel-difference-report.json")
(P/'scripts/compare_system.py').write_text(c)
(P/'evidence/system-composition.json').write_text(json.dumps({'intent':'presentation-only alternative to font-only A/B','styles':styles,'body_font_exact_inter':True,'font_display_open_A':True,
 'comparison_is_not_font_only':True,'site_and_office_sources_unchanged':True},ensure_ascii=False,indent=2)+'\n')
print('SYSTEM CANDIDATE CREATED',len(styles),'carriers')
