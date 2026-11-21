from pathlib import Path
import hashlib,zipfile
P=Path(__file__).resolve().parent;KIT=P/'qualification-kit'
files=sorted(f for f in KIT.rglob('*') if f.is_file() and f.name!='SHA256SUMS.txt' and '/results/' not in str(f))
(KIT/'SHA256SUMS.txt').write_text(''.join(f'{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.relative_to(KIT)}\n' for f in files))
files.append(KIT/'SHA256SUMS.txt')
dest=P/'golden-step-v060-windows-kit.zip'
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED) as z:
 for f in sorted(files):
  info=zipfile.ZipInfo('qualification-kit/'+f.relative_to(KIT).as_posix(),date_time=(2026,11,21,0,0,0))
  info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
  z.writestr(info,f.read_bytes())
with zipfile.ZipFile(dest) as z:
 assert z.testzip() is None and len(z.namelist())==len(files)
 print('Portable ZIP',dest.stat().st_size,'bytes',len(files),'files')
