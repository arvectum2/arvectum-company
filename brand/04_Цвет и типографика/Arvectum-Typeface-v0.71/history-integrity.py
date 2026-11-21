"""Non-mutating history snapshot and checksums for all existing typeface version directories."""
from pathlib import Path
import json,hashlib,re,subprocess
P=Path(__file__).resolve().parent;ROOT=P.parent
history=[]
for directory in sorted(ROOT.glob('Arvectum-Typeface-v0.*')):
    if not directory.is_dir() or directory==P:continue
    recorded=directory/'SHA256SUMS.txt'
    d={'version':directory.name,'manifest_available':recorded.is_file(),'files_checked':0,
       'checksum_errors':[],'tracked_file_count':0,'has_README':(directory/'README.md').is_file()}
    tracked=subprocess.check_output(['git','ls-files','--',str(directory)],text=True,cwd=ROOT.parent.parent)
    d['tracked_file_count']=len([s for s in tracked.splitlines() if s])
    if recorded.is_file():
        for line in recorded.read_text().splitlines():
            sha,rel=line.split('  ',1)
            f=directory/rel
            if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest()!=sha:
                d['checksum_errors'].append(rel)
            d['files_checked']+=1
    history.append(d)
assert len(history)>=58
errors=[(d['version'],d['checksum_errors']) for d in history if d['checksum_errors']]
latest=[d for d in history if any(d['version'].endswith(f'.{x}') for x in range(61,71))]
assert len(latest)==10 and all(d['manifest_available'] and not d['checksum_errors'] for d in latest)
report={'status':'VERSIONED_SOURCE_INVENTORY','version_folders_existing':len(history),
        'prior_history_directory_presence_not_original_archive_recovery':True,
        'manifests_present':sum(d['manifest_available'] for d in history),
        'manifests_missing':sum(not d['manifest_available'] for d in history),
        'total_tracked_files':sum(d['tracked_file_count'] for d in history),
        'files_checksum_verified':sum(d['files_checked'] for d in history),
        'checksum_errors':errors,'latest_v061_v070_manifests_all_pass':True,
        'original_zip_gap':['v0.13','v0.23','v0.24'],
        'versions':history,
        'limitations':['Older version folders may predate SHA256 manifests, do not add retroactive claims',
                       'Tracked files are not proof that original historical ZIP bytes were restored',
                       'This checks local working copy, not GitHub/GitVerse remote persistence',
                       'No previous version files modified']}
(P/'evidence/history-integrity.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('VERSIONS',len(history),'manifest',report['manifests_present'],'pre-manifest',report['manifests_missing'],
      'files checked',report['files_checksum_verified'],'errors',len(errors))
if errors:
 print('CHECKSUM EXCEPTIONS',errors[:12])
else:print('PASS all available historical SHA manifests')
