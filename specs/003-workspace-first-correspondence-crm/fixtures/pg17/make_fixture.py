import sqlite3,pathlib,sqlite_to_pg as m
root=pathlib.Path(__file__).resolve().parent
db=root/'synthetic.sqlite3'
if db.exists():raise SystemExit("fixture already exists")
c=sqlite3.connect(db)
c.executescript("""CREATE TABLE source_messages(source_id,match_key,message_at,direction,state);CREATE TABLE registry(number,date,subject,direction,party,match_key,source_id,link_quality);""")
g='1'*64;k='2'*64;ts='2026-01-01T10:00:00+03:00';day='2026-01-01';party='synthetic@example.invalid'
with c:
 c.executemany('INSERT INTO source_messages VALUES(?,?,?,?,?)',[('a'*64,g,ts,'incoming','registered_group'),('b'*64,g,ts,'incoming','registered_group'),('c'*64,k,ts,'outgoing','registered_exact'),('d'*64,'3'*64,ts,'incoming','historical_not_admitted')])
 c.executemany('INSERT INTO registry VALUES(?,?,?,?,?,?,?,?)',[(1,day,"Part's", 'incoming',party,g,None,'group_reconciled'),(2,day,"Part's",'incoming',party,g,None,'group_reconciled'),(3,day,'Exact','outgoing',party,k,'c'*64,'exact')])
c.close()
sql=m.generate(db,'synthetic-a','box')
(root/'synthetic-import.sql').write_text(sql)
# Verify invalid group multiplicity rejected before any SQL generation.
c=sqlite3.connect(db)
with c:c.execute("DELETE FROM source_messages WHERE source_id=?",('a'*64,))
c.close()
try:m.generate(db,'synthetic-a','box')
except ValueError as e:assert str(e)=='multiplicity parity';print('PASS invalid multiplicity rejected')
else:raise AssertionError('bad group accepted')
try:m.generate(db,'synthetic$$a','box')
except ValueError as e:assert str(e)=='invalid scope';print('PASS invalid scope rejected')
else:raise AssertionError('bad scope accepted')
