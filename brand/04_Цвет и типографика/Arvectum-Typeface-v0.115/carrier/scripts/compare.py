"""Build same-size side-by-side proof images and an indexed comparison PDF."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
import subprocess,json
P=Path(__file__).resolve().parent.parent
proof=P/'proofs';evidence=P/'evidence'
def render(pdf,tag):
 subprocess.run(['pdftoppm','-r','105','-jpeg','-jpegopt','quality=86',str(pdf),str(proof/tag)],check=True,capture_output=True,timeout=25)
for typ in ('letter','proposal'):
 for variant in ('old0114','new0115'):
  render(proof/f'{typ}-{variant}.pdf',f'{typ}-{variant}')
expected={'letter':1,'proposal':2}
try:
 heading_font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',29)
 label_font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',22)
except OSError:
 heading_font=ImageFont.load_default();label_font=heading_font
reviews=[]
summary={}
for typ,pagecount in expected.items():
 for page in range(1,pagecount+1):
  a=Image.open(proof/f'{typ}-old0114-{page}.jpg').convert('RGB')
  b=Image.open(proof/f'{typ}-new0115-{page}.jpg').convert('RGB')
  assert a.size==b.size,(typ,page,a.size,b.size)
  w,h=a.size;gap=18;top=100
  canvas=Image.new('RGB',(2*w+3*gap,h+top+gap),'white')
  d=ImageDraw.Draw(canvas)
  label={'letter':'ПИСЬМО / ДЕМО','proposal':'КОММЕРЧЕСКОЕ ПРЕДЛОЖЕНИЕ / ДЕМО'}[typ]
  d.text((gap,16),f'{label} · стр. {page} / сравнение типографики',font=heading_font,fill='#001432')
  d.text((gap,58),'v0.114 · до коррекции',font=label_font,fill='#0B7468')
  d.text((2*gap+w,58),'v0.115 · N/Y, Й/Ё',font=label_font,fill='#0B7468')
  canvas.paste(a,(gap,top));canvas.paste(b,(2*gap+w,top))
  out=proof/f'review-{typ}-page-{page}.jpg';canvas.save(out,quality=87)
  change=ImageChops.difference(a,b).convert('L')
  changed=sum(v>12 for v in change.get_flattened_data())
  pct=100*changed/(w*h)
  summary[f'{typ}-page-{page}']={'size':list(a.size),'pixel_change_pct_threshold12':round(pct,5),'changed_pixels':changed}
  reviews.append(canvas)
# mobile full screenshot comparison
a=Image.open(proof/'mobile-old0114.png').convert('RGB')
b=Image.open(proof/'mobile-new0115.png').convert('RGB')
assert a.size==b.size
w,h=a.size;gap=22;top=100
mobile=Image.new('RGB',(2*w+3*gap,h+top+gap),'white')
md=ImageDraw.Draw(mobile)
md.text((gap,16),'МОБИЛЬНЫЙ МАКЕТ / 390 px / ДЕМО',font=heading_font,fill='#001432')
md.text((gap,58),'Arvectum v0.114',font=label_font,fill='#0B7468')
md.text((2*gap+w,58),'Arvectum v0.115',font=label_font,fill='#0B7468')
mobile.paste(a,(gap,top));mobile.paste(b,(2*gap+w,top))
mobile.save(proof/'review-mobile.jpg',quality=90)
d=ImageChops.difference(a,b).convert('L')
changed=sum(v>12 for v in d.get_flattened_data())
summary['mobile']={'size':[w,h],'pixel_change_pct_threshold12':round(100*changed/(w*h),5),'changed_pixels':changed}
# Build a multipage image-based quick-review PDF; source letter/proposal PDFs remain vector
reviews.append(mobile)
reviews=[im.convert('RGB') for im in reviews]
report=proof/'SIDE-BY-SIDE-REVIEW.pdf'
reviews[0].save(report,'PDF',save_all=True,append_images=reviews[1:],resolution=118)
(evidence/'pixel-difference-report.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print('PDF',report.name,report.stat().st_size)
for x,y in summary.items():print('DIFF',x,y['pixel_change_pct_threshold12'],'% /',y['changed_pixels'],'px')
