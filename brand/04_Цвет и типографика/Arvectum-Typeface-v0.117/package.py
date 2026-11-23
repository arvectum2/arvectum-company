"""Deterministic local SOURCE-AND-DESIGN-KIT packager; verifies all files and hashes."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib
P=Path(__file__).resolve().parent
z=P/'Golden-Step-v0117-FULL-EDITABLE-SOURCE-KIT.zip'
files=sorted(x for x in P.rglob('*') if x.is_file() and '__pycache__' not in x.parts
 and x.suffix!='.pyc' and x.name not in (z.name,'SHA256SUMS.txt'))
(P/'SHA256SUMS.txt').write_text('\n'.join(
 hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(P)) for f in files)+'\n')
with ZipFile(z,'w',ZIP_DEFLATED,compresslevel=7) as a:
 for f in files+[P/'SHA256SUMS.txt']:
  a.write(f,P.name+'/'+str(f.relative_to(P)))
with ZipFile(z) as a:assert a.testzip() is None
print('COMPLETE',len(files),'files',z.stat().st_size,'bytes')
print('SHA256',hashlib.sha256(z.read_bytes()).hexdigest())
