#!/usr/bin/env python3
"""Local substring search; output can contain sensitive data."""
import argparse
from pathlib import Path
import sqlite3
import json

def search(db_path, query, limit=20):
    if not query or not 1 <= limit <= 1000:
        raise ValueError('Nonempty query and limit 1..1000 required')
    uri = Path(db_path).resolve().as_uri() + '?mode=ro'
    with sqlite3.connect(uri, uri=True) as db:
        db.create_function('fold', 1, lambda s: (s or '').casefold(), deterministic=True)
        sql = '''SELECT c.title,n.role,n.text,n.source,n.ordinal,n.node_id FROM nodes n JOIN conversations c USING(source,ordinal) WHERE instr(fold(n.text),fold(?))>0 OR instr(fold(c.title),fold(?))>0 ORDER BY n.source,n.ordinal,n.node_id LIMIT ?'''
        return [dict(zip(('title','role','text','source','ordinal','node_id'), row)) for row in db.execute(sql,(query,query,limit))]

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('database'); p.add_argument('query'); p.add_argument('--limit',type=int,default=20); a=p.parse_args()
    print(json.dumps(search(a.database,a.query,a.limit),ensure_ascii=False,indent=2))
