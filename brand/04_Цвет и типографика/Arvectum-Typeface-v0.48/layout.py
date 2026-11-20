from pathlib import Path
from fontTools.ttLib import TTFont
import json,subprocess
P=Path(__file__).resolve().parent
r={}
for st in ('Display','Text'):
    f=next((P.parent/'Arvectum-Typeface-v0.47/experimental').glob(f'Arvectum{st}*.otf'));cm=TTFont(f).getBestCmap()
    samples={}
    for s in ('Ё','Е\u0308','ё','е\u0308','Й','И\u0306','й','и\u0306','e\u0301','a\u0308','а\u0301'):
        q=json.loads(subprocess.check_output(['hb-shape','--output-format=json',str(f),s],text=True))
        samples[s]={'covered_raw':all(ord(c) in cm for c in s),'shaped':q,'missing':any(x['g']=='.notdef' for x in q)}
    r[st]={'missing_printable_ascii':[chr(c) for c in range(32,127) if c not in cm],'decomposed_and_accent_tests':samples}
(P/'layout-probe.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print('Layout probe complete; missing marks recorded.')
