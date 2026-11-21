from pathlib import Path
import json,hashlib
from PIL import Image,ImageStat
P=Path(__file__).resolve().parent
j=json.loads((P/'proofs/webkit-report.json').read_text())
assert j['actual_iPhone_run'] is False and j['user_safari_windows_modified'] is False
assert j['runner'].startswith('macOS WKWebView') and len(j['results'])==3
for r,w in zip(j['results'],(390,768,1440)):
 assert r['viewport']==w and r['scrollWidth']<=w
 assert r['fontDisplay'] is True and r['fontText'] is True
 assert r['titleFits'] is True and r['textSize']>=16
 z=r['zoom200'];assert z['scrollWidth']<=z['innerWidth']
 assert z['outliers']==[],(r['label'],z['outliers'])
 if w==390:assert z['innerWidth']==195 and z['rowsStacked'] is True and z['tableOverflow'] is False
 im=Image.open(P/'proofs'/f'webkit-{r["label"]}.png').convert('RGB')
 assert im.width==w and im.height>1500,(r['label'],im.size)
 assert min(ImageStat.Stat(im).stddev)>12
 print('WEBKIT_PASS',r['label'],w,'zoom200',z['innerWidth'],'screenshot',im.size)
def luminosity(h):
 nums=[int(h[i:i+2],16)/255 for i in (1,3,5)]
 lin=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in nums]
 return sum(a*b for a,b in zip(lin,(.2126,.7152,.0722)))
def contrast(a,b):
 x,y=sorted((luminosity(a),luminosity(b)),reverse=True)
 return (x+.05)/(y+.05)
ratios={name:round(contrast(fg,bg),3) for name,(fg,bg) in {
 'body_ink_on_white':('#153043','#FFFFFF'),
 'secondary_on_white':('#556875','#FFFFFF'),
 'old_teal_text_on_white_Fails':('#279C8D','#FFFFFF'),
 'candidate_dark_teal_text_on_white':('#0B7468','#FFFFFF'),
 'unchanged_mint_mark_on_white_decorative':('#41B599','#FFFFFF')}.items()}
assert ratios['old_teal_text_on_white_Fails']<4.5
assert ratios['candidate_dark_teal_text_on_white']>=4.5
assert ratios['secondary_on_white']>=4.5 and ratios['body_ink_on_white']>=4.5
css=(P/'proofs/webkit-type-specimen.html').read_text()
assert '--teal:#0B7468;' in css and '--accent:#41B599;' in css and '@media (max-width:260px)' in css
(P/'evidence/contrast-report.json').write_text(json.dumps({'ratios':ratios,'WCAG_ordinary_text_target':4.5,
 'safari_UI_automation':False,'mac_WebKit_verified':True,'real_iPhone':False,
 'source_CSS_changed_in_v070':False,'temporary_dark_teal_is_unapproved_design_candidate':True},ensure_ascii=False,indent=2)+'\n')
print('CONTRAST PASS dark teal',ratios['candidate_dark_teal_text_on_white'],'original sample',ratios['old_teal_text_on_white_Fails'])
