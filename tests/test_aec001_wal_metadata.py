"""Pure filesystem metadata fixtures: sparse WAL-shaped files, no database reads."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

P=Path(__file__).resolve().parents[1]/"tools/aec001_wal_metadata.py"
sys.path.insert(0,str(P.parent))
s=importlib.util.spec_from_file_location("aec_wal",P)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

def wal(log,seg,timeline=1,partial=False):
    return f"{timeline:08X}{log:08X}{seg:08X}"+(".partial" if partial else "")

class WALMetadataTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.folder=Path(t.name)/"wal";self.folder.mkdir(mode=0o700)

    def create(self,name,size=None):
        f=self.folder/name
        with f.open("wb") as out:out.truncate(size if size is not None else m.SEG_BYTES)
        f.chmod(0o600)
        return f

    def scan(self):return m.inspect(self.folder)

    def test_contiguous_sequence_and_immediate_partial(self):
        self.create(wal(1,254))
        self.create(wal(1,255))
        self.create(wal(2,0))
        self.create(wal(2,1,partial=True))
        result=self.scan()
        self.assertEqual(result["status"],"CONTIGUOUS_OBSERVED_FILENAMES")
        self.assertEqual(result["complete_segments"],3)
        self.assertTrue(result["partial_is_next_expected"])
        self.assertFalse(result["recovery_or_pitr_verified"])
        self.assertFalse(result["file_payload_bytes_read"])

    def test_missing_segment_detected(self):
        self.create(wal(1,1));self.create(wal(1,3))
        r=self.scan()
        self.assertEqual(r["status"],"REVIEW_SEQUENCE_GAPS")
        self.assertEqual(r["gap_segment_count"],1)

    def test_partial_is_not_finished(self):
        self.create(wal(1,1));self.create(wal(1,3,partial=True))
        self.assertEqual(self.scan()["status"],"REVIEW_PARTIAL_POSITION")

    def test_two_partials_cannot_be_contiguous_pass(self):
        self.create(wal(1,1))
        self.create(wal(1,2,partial=True))
        self.create(wal(1,3,partial=True))
        self.assertNotEqual(self.scan()["status"],"CONTIGUOUS_OBSERVED_FILENAMES")

    def test_wrong_segment_length_denied(self):
        self.create(wal(1,1),500)
        self.assertEqual(self.scan()["status"],"REVIEW_BAD_SEGMENT_SIZE")

    def test_bad_index_beyond_page_boundary(self):
        self.create(wal(1,256))
        self.assertEqual(self.scan()["status"],"REVIEW_BAD_SEGMENT_INDEX")

    def test_multiple_timelines_not_automatically_accepted(self):
        self.create(wal(1,1,timeline=1))
        self.create(wal(1,2,timeline=2))
        self.assertEqual(self.scan()["status"],"REVIEW_MULTIPLE_TIMELINES")

    def test_unexpected_file_requires_review(self):
        self.create(wal(1,1))
        (self.folder/"password.txt").write_text("do not read")
        self.assertEqual(self.scan()["status"],"REVIEW_UNRECOGNIZED_FILES")

    def test_symlink_in_root_fails_closed(self):
        self.create(wal(1,1))
        (self.folder/"other").symlink_to("/etc/passwd")
        self.assertEqual(self.scan()["status"],"REVIEW_UNSAFE_FILES")

    def test_permission_exposure_denied(self):
        self.folder.chmod(0o755)
        self.create(wal(1,1))
        self.assertEqual(self.scan()["status"],"UNKNOWN_UNSAFE_OR_MISSING_DIRECTORY")

    def test_symlinked_wal_directory_denied(self):
        symlink=self.folder.parent/"symlink"
        symlink.symlink_to(self.folder,target_is_directory=True)
        self.assertEqual(m.inspect(symlink)["status"],"UNKNOWN_UNSAFE_OR_MISSING_DIRECTORY")

    def test_empty_directory_not_continuous(self):
        self.assertEqual(self.scan()["status"],"UNKNOWN_NO_WAL_FILES")

    def test_partial_only_not_complete_chain(self):
        self.create(wal(1,1,partial=True))
        self.assertEqual(self.scan()["status"],"REVIEW_NO_COMPLETE_SEGMENTS")

    def test_oversized_partial_is_invalid(self):
        self.create(wal(1,1))
        self.create(wal(1,2,partial=True),size=m.SEG_BYTES+1)
        self.assertEqual(self.scan()["status"],"REVIEW_BAD_SEGMENT_SIZE")

if __name__=="__main__":unittest.main()
