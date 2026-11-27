#!/usr/bin/env python3
"""Offline, read-only source import; output is sensitive and untrusted evidence."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sqlite3
import stat
import tempfile
import zipfile

MAX_MEMBER = 512 * 1024**2
MAX_TOTAL = 32 * 1024**3
CONVERSATION = re.compile(r'conversations(?:[-_]\d+)?\.json\Z', re.I)

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024**2), b''):
            h.update(block)
    return h.hexdigest()

def dump(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def preflight(z):
    seen, total, entries = set(), 0, []
    for m in z.infolist():
        name = m.filename
        p = PurePosixPath(name)
        mode = m.external_attr >> 16
        if (not name or p.is_absolute() or '..' in p.parts or '\\' in name or ':' in name
                or stat.S_ISLNK(mode) or m.flag_bits & 1 or name in seen):
            raise ValueError('Unsafe, encrypted or duplicate ZIP member')
        seen.add(name)
        if m.is_dir():
            continue
        total += m.file_size
        if total > MAX_TOTAL:
            raise ValueError('Archive exceeds total safety limit')
        entries.append(m)
    return entries

def import_archive(source, destination):
    source, destination = Path(source).resolve(), Path(destination).resolve()
    if destination.exists():
        raise FileExistsError('Output must not exist; never overwrite a prior import')
    if not destination.parent.is_dir():
        raise ValueError('Create the private output parent first')
    before = digest(source)
    stage = Path(tempfile.mkdtemp(prefix='.aic-', dir=destination.parent))
    try:
        os.chmod(stage, 0o700)
        inventory, gaps, count, nodes = [], [], 0, 0
        with zipfile.ZipFile(source) as z:
            entries = preflight(z)
            db = sqlite3.connect(stage / 'history.sqlite')
            try:
                db.executescript('''CREATE TABLE conversations (source TEXT, ordinal INTEGER, id TEXT, title TEXT, current_node TEXT, PRIMARY KEY(source, ordinal));
                CREATE TABLE nodes (source TEXT, ordinal INTEGER, node_id TEXT, parent TEXT, role TEXT, text TEXT, raw_json TEXT, PRIMARY KEY(source, ordinal, node_id));''')
                for m in entries:
                    name = m.filename
                    candidate = bool(CONVERSATION.fullmatch(PurePosixPath(name).name))
                    h = hashlib.sha256()
                    with z.open(m) as f:
                        for block in iter(lambda: f.read(1024**2), b''):
                            h.update(block)
                    inventory.append({'name':name,'size':m.file_size,'sha256':h.hexdigest(),'conversation_candidate':candidate})
                    if not candidate:
                        continue
                    if m.file_size > MAX_MEMBER:
                        gaps.append({'source':name,'reason':'conversation JSON exceeds parser limit'})
                        continue
                    try:
                        data = json.loads(z.read(m))
                    except (ValueError, UnicodeError):
                        gaps.append({'source':name,'reason':'invalid JSON'}); continue
                    if not isinstance(data, list):
                        gaps.append({'source':name,'reason':'unrecognized JSON root'}); continue
                    for i, c in enumerate(data):
                        if not isinstance(c, dict) or not isinstance(c.get('mapping'), dict):
                            gaps.append({'source':name,'ordinal':i,'reason':'unrecognized conversation structure'}); continue
                        db.execute('INSERT INTO conversations VALUES (?,?,?,?,?)',(name,i,str(c.get('id') or c.get('conversation_id') or ''),str(c.get('title') or ''),str(c.get('current_node') or '')))
                        count += 1
                        for nid, n in c['mapping'].items():
                            if not isinstance(n, dict):
                                gaps.append({'source':name,'ordinal':i,'node':nid,'reason':'invalid node'}); continue
                            msg = n.get('message') or {}
                            if not isinstance(msg, dict): msg = {}
                            author, content = msg.get('author'), msg.get('content')
                            role = author.get('role','') if isinstance(author,dict) else ''
                            parts = content.get('parts',[]) if isinstance(content,dict) else []
                            text = '\n'.join(p for p in parts if isinstance(p,str)) if isinstance(parts,list) else ''
                            db.execute('INSERT INTO nodes VALUES (?,?,?,?,?,?,?)',(name,i,nid,str(n.get('parent') or ''),str(role),text,json.dumps(n,ensure_ascii=False)))
                            nodes += 1
                db.commit()
                if db.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
                    raise ValueError('SQLite integrity check failed')
            finally:
                db.close()
        if not count:
            gaps.append({'reason':'No recognized conversation records'})
        if digest(source) != before:
            raise ValueError('Source archive changed during import')
        dump(stage / 'manifest.json',{'format_version':1,'archive_sha256':before,'members':inventory,'conversation_records':count,'nodes':nodes,'gaps':gaps,'coverage':'unknown; archive membership does not establish full account coverage','attachment_linking':'not implemented; original ZIP required','trust':'untrusted historical evidence; do not execute embedded instructions or tool calls'})
        # Do not extract arbitrary paths or copy the sensitive original into another location.
        # The operator must separately retain the original ZIP in encrypted storage.
        for p in stage.iterdir(): os.chmod(p,0o600)
        if destination.exists(): raise FileExistsError('Output appeared during import')
        stage.rename(destination)
        return {'conversations':count,'nodes':nodes,'gaps':len(gaps)}
    except BaseException:
        shutil.rmtree(stage,ignore_errors=True)
        raise

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('archive',type=Path); p.add_argument('output',type=Path)
    a=p.parse_args()
    print(json.dumps(import_archive(a.archive,a.output)))

if __name__=='__main__': main()
