from pathlib import Path,PurePosixPath
from zipfile import ZipFile
from io import BytesIO
import hashlib,csv,json,re,string,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent
B=P.parent.parent
T=P.parent
Z=P/'recovered/Arvectum_Golden_Step_v0.21.zip'
sha=lambda b:hashlib.sha256(b).hexdigest()
checks=[]
def verify_archive(z,label):
    names=z.namelist();assert len(names)==len(set(names))
    assert z.testzip() is None
    for n in names:
        assert not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts
        assert not n.lower().endswith(('.ttf','.otf','.woff','.woff2'))
    if 'SHA256SUMS.txt' in names:
        lines=z.read('SHA256SUMS.txt').decode().splitlines()
        for line in lines:
            h,n=line.split(maxsplit=1);assert sha(z.read(n.lstrip('*').removeprefix('./')))==h,n
        count=len(lines)
    else:count=0
    checks.append({'archive':label,'members':len(names),'verified_internal_hashes':count})
    for n in names:
        if n.endswith('.zip'):verify_archive(ZipFile(BytesIO(z.read(n))),n)
with ZipFile(Z) as z:
    verify_archive(z,Z.name)
    for f in (B/'03_Логотип/Golden-Wordmark-v0.21').glob('C_*.svg'):
        assert sha(f.read_bytes())==sha(z.read(f.name)),f.name
    assert sha((B/'03_Логотип/Golden-Vector-v0.18/AV_Golden_v018_mint.svg').read_bytes())==sha(z.read('sources/AV_Golden_v018_mint.svg'))
    ctx={}
    for n in z.namelist():
        if re.fullmatch(r'glyphs/C/U\+[0-9A-F]+\.svg',n):
            data=z.read(n);ET.fromstring(data)
            ctx[chr(int(PurePosixPath(n).stem[2:],16))]=n
            f=P/'recovered/wordmark-v0.21-C'/PurePosixPath(n).name;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(data)
    assert len(ctx)==16
alphabet=string.ascii_uppercase+string.ascii_lowercase+'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
assert len(alphabet)==118 and len(set(alphabet))==118
rows=[];summary={}
for style in ('Display','Text'):
    versions=[('legacy-v0.4',T/'Arvectum-Typeface-v0.4/glyphs'/style),
              ('current-candidate-v0.22',T/'Arvectum-Typeface-v0.22/glyphs'/style),
              ('current-candidate-v0.25',B/'02_Концепции/Vector-Hybrid-v0.25/glyphs'/style),
              ('current-candidate-v0.28',T/'Arvectum-Typeface-v0.28/candidates'/style/'C-compact'),
              ('current-candidate-v0.30',T/'Arvectum-Typeface-v0.30/candidates'/style/'F-width')]
    index={}
    for state,d in versions:
        for f in d.glob('U+*.svg'):
            ET.parse(f);ch=chr(int(f.stem[2:],16));index[ch]=(state,str(f.relative_to(B)),sha(f.read_bytes()))
    assert set(index)<=set(alphabet)
    counts={'current_candidate':0,'legacy_only':0,'wordmark_reference_only':0,'missing':0}
    for ch in alphabet:
        a=index.get(ch)
        category='current_candidate' if a and a[0].startswith('current') else 'legacy_only' if a else 'wordmark_reference_only' if ch in ctx else 'missing'
        counts[category]+=1
        rows.append({'style':style,'unicode':f'U+{ord(ch):04X}','char':ch,'coverage':category,'version':a[0] if a else '', 'path':a[1] if a else '', 'sha256':a[2] if a else '', 'wordmark_C_reference':str((P/'recovered/wordmark-v0.21-C'/PurePosixPath(ctx[ch]).name).relative_to(B)) if ch in ctx else '', 'note':'C is wordmark-only, not Text or finalized Display' if ch in ctx else ''})
    summary[style]=counts
with (P/'coverage.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0],lineterminator="\n");w.writeheader();w.writerows(rows)
report={'alphabet_scope':'52 Latin + 66 Russian letters per style; no digits/punctuation; not full font coverage','archive_sha256':sha(Z.read_bytes()),'archive_checks':checks,'matched_wordmark_master_files':4,'matched_monogram':True,'wordmark_context_count':len(ctx),'wordmark_context_chars':''.join(sorted(ctx)),'coverage':summary,'missing_original_archives':{'v0.13':'745acc1e6f1a702721298d427f1ae23ea6a7c8aa9aa4c03339905885927408aa','v0.22':'73545648eefd0f9681e85cd4032cade81f2be4136551cf9ad64d71bf63b96306','v0.23':'1bf1ac8110f7cd45ce1c5069e7e3146415572897e2c83f80da78c84dec9b481b','v0.24':'a3206640071c5e1522a90a3f1078cfc8ebe7bad0c72d7a02053fc3aa2cc4653a'}}
(P/'inventory.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
for state in summary['Display']:
 print(state, ''.join(r['char'] for r in rows if r['style']=='Display' and r['coverage']==state))
