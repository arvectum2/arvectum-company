import unittest
from tools.legacy_source_anchors import digest, inspect, compare, observe

def entry(raw):
    return {"path":"roadmap.md","sha256":digest(raw),"lines":len(raw.splitlines()),
            "checkbox_occurrences":3,"list_rows":2,"table_rows":1}

class SourceAnchorTests(unittest.TestCase):
    raw=b"- [x] Parent; [ ] remaining\n  - [!] Child\n| A | B |\nProse requirement\n"
    def test_inline_open_and_exception(self):
        out=inspect(self.raw,entry(self.raw))
        self.assertEqual(out["marker_counts"],{"x":1," ":1,"!":1})
        self.assertEqual(len(out["anchors"]),4)
    def test_tamper(self):
        with self.assertRaises(ValueError):
            inspect(self.raw+b"New line\n",entry(self.raw))
    def test_removed_child(self):
        old=inspect(self.raw,entry(self.raw))
        new=inspect(self.raw.replace(b"  - [!] Child\n",b""),entry(self.raw),False)
        self.assertEqual(len(compare(old,new)["missing_or_changed"]),1)
    def test_reorder(self):
        old=inspect(self.raw,entry(self.raw))
        new=inspect(b"\n".join(reversed(self.raw.splitlines()))+b"\n",entry(self.raw),False)
        self.assertFalse(compare(old,new)["review_required"])
    def test_unmarked_requirement(self):
        old=inspect(self.raw,entry(self.raw))
        new=inspect(self.raw.replace(b"Prose requirement",b"Other text"),entry(self.raw),False)
        self.assertTrue(compare(old,new)["review_required"])
    def test_duplicate_removed(self):
        raw=self.raw+b"Prose requirement\n"
        old=inspect(raw,entry(self.raw),False)
        new=inspect(self.raw,entry(self.raw))
        self.assertEqual(len(compare(old,new)["missing_or_changed"]),1)
    def test_no_acceptance_or_authority(self):
        conf={"repo":"sample","commit":"test","sources":[entry(self.raw)]}
        report=observe(conf,lambda _:self.raw)
        self.assertIs(report["actual_acceptance_verified"],False)
        self.assertIs(report["execution_authorized"],False)
