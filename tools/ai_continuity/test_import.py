import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
import zipfile
from import_export import import_archive, digest
from search_history import search

class ImportTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name); self.z=self.root/'sample.zip'; self.out=self.root/'out'
    def archive(self, entries):
        with zipfile.ZipFile(self.z,'w') as z:
            for name,content in entries: z.writestr(name,content)
    def conversation(self):
        return {'id':'c1','title':'Пример','current_node':'b','mapping':{'a':{'parent':None,'message':None},'b':{'parent':'a','message':{'author':{'role':'user'},'content':{'parts':['Текст',{'asset_pointer':'x'}]}}},'c':{'parent':'a','message':{'author':{'role':'assistant'},'content':{'parts':['Альтернативная ветка']}}}}}
    def test_branches_and_parts(self):
        self.archive([('conversations-001.json',json.dumps([self.conversation()])),('files/x.bin',b'abc')]); old=digest(self.z)
        self.assertEqual(import_archive(self.z,self.out),{'conversations':1,'nodes':3,'gaps':0})
        self.assertEqual(digest(self.z),old)
        with sqlite3.connect(self.out/'history.sqlite') as db:
            self.assertEqual(db.execute('select count(*) from nodes').fetchone()[0],3)
            self.assertIn('asset_pointer',db.execute("select raw_json from nodes where node_id='b'").fetchone()[0])
        self.assertFalse((self.out/'files').exists())
    def test_unicode_search(self):
        self.archive([("conversations.json",json.dumps([self.conversation()]))]); import_archive(self.z,self.out)
        r=search(self.out/"history.sqlite","ТЕКСТ"); self.assertEqual(len(r),1); self.assertEqual(r[0]["node_id"],"b")
        self.assertEqual(search(self.out/"history.sqlite","' OR 1=1 --"),[])
    def test_multiple_files(self):
        c=json.dumps([self.conversation()]); self.archive([('conversations.json',c),('conversations_2.json',c)])
        self.assertEqual(import_archive(self.z,self.out)['conversations'],2)
    def test_traversal_rejected(self):
        self.archive([('../escape',b'x')]); self.assertRaises(ValueError,import_archive,self.z,self.out); self.assertFalse(self.out.exists())
    def test_duplicate_rejected(self):
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter('ignore'); self.archive([('x',b'a'),('x',b'b')])
        self.assertRaises(ValueError,import_archive,self.z,self.out)
    def test_symlink_rejected(self):
        with zipfile.ZipFile(self.z,'w') as z:
            info=zipfile.ZipInfo('link'); info.create_system=3; info.external_attr=0o120777<<16; z.writestr(info,'/tmp')
        self.assertRaises(ValueError,import_archive,self.z,self.out)
    def test_unknown_and_invalid(self):
        self.archive([('conversations.json','bad'),('conversations_1.json','{}')]); self.assertEqual(import_archive(self.z,self.out)['gaps'],3)
    def test_no_overwrite(self):
        self.archive([('conversations.json','[]')]); self.out.mkdir(); self.assertRaises(FileExistsError,import_archive,self.z,self.out)
    def test_manifest_hash(self):
        self.archive([('other.json','{}')]); import_archive(self.z,self.out); m=json.loads((self.out/'manifest.json').read_text()); self.assertEqual(m['archive_sha256'],digest(self.z)); self.assertEqual(len(m['members']),1); self.assertEqual(m['attachment_linking'],'not implemented; original ZIP required')

if __name__=='__main__': unittest.main()
