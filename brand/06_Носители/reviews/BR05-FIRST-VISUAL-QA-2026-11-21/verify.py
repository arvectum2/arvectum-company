from pathlib import Path
from PIL import Image
import json,hashlib,re
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
a=json.loads((P/'evidence/facts.json').read_text())
assert a['status']=='FIRST_INTERNAL_ART_DIRECTOR_REVIEW_NOT_OWNER_APPROVAL'
r=a['cover_overlap_chrome_css_rectangles']['overlap']
assert 100<r['width']<130 and 20<r['height']<30 and r['area']>2500
sim=a['3_vs_cyrillic_Z_mask_IoU_at_selected_px']
assert abs(sim['Display']['14']-.9259)<1e-6 and abs(sim['Text']['12']-.9474)<1e-6
assert a['design_token_mismatch']['difference_px']==4
assert a['typography_guide_page_break']['physical_crop_or_text_loss_established']==False
assert not a['presentation_equivalence']['native_Keynote_PPTX_rendered']
assert a['release_flag']['v0.64_fsType_preview_print']==4
f=P/'evidence/cover-footer-collision.png';im=Image.open(f)
assert im.width>350 and im.height>150
review=(P/'REVIEW.md').read_text()
for issue in ('GS-REV-01','GS-REV-02','GS-REV-03','GS-REV-04','GS-REV-05','GS-REV-06','GS-REV-07','GS-REV-08'):
 assert issue in review
for source in ('brand/04_Цвет и типографика/Arvectum-Typeface-v0.62/audit.json',
 'brand/06_Носители/GoldenStep-Applications-v0.73/proofs/render-slides-1.png',
 'brand/04_Цвет и типографика/Arvectum-Typeface-v0.75/proofs/Brandbook-Typeface-v075-Pages.pdf'):
 assert (ROOT/source).is_file(),source
print('PASS first-art-direction-review: 8 blocking/high issues, source-specific quantitative checks; no approval')
