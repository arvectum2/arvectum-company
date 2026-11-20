"""Queue source conservation and fail-closed regression tests."""
import copy
import json
import unittest
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "docs" / "operations"
spec = importlib.util.spec_from_file_location("projection", ROOT / "tools" / "management_queue_projection.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class QueueTests(unittest.TestCase):
    def setUp(self):
        self.source = json.loads((P / "LIVE-WORK-RECONCILIATION-CANDIDATE-2026-11-20.json").read_text())
        self.queue = json.loads((P / "OWNER-WORK-QUEUE-PROJECTION-2026-11-20.json").read_text())

    def invalid(self, mutate):
        q = copy.deepcopy(self.queue)
        mutate(q)
        with self.assertRaises(ValueError):
            module.validate(self.source, q)

    def test_full_snapshot(self):
        self.assertEqual(module.validate(self.source, self.queue)["actions"], 51)
    def test_lost_action(self):
        self.invalid(lambda q: q["items"].pop())
    def test_duplicate_action(self):
        self.invalid(lambda q: q["items"].append(copy.deepcopy(q["items"][0])))
    def test_source_action_changed(self):
        self.invalid(lambda q: q["items"][0].update(action="done"))
    def test_pause_not_reopened(self):
        self.invalid(lambda q: next(x for x in q["items"] if x["queue"] == "hold").update(queue="prepare_within_existing_envelope"))
    def test_no_implicit_authority(self):
        self.invalid(lambda q: q["items"][0].update(execution_authorized=True))
    def test_no_implicit_acceptance(self):
        self.invalid(lambda q: q["items"][0].update(actual_acceptance_verified=True))
    def test_no_fake_control_ref(self):
        self.invalid(lambda q: q["items"][0]["related_control_refs"].append("WORK-999"))
    def test_no_lost_subview(self):
        self.invalid(lambda q: q["project_details"]["Arvectum Tools"]["subviews"].pop())
    def test_no_fake_owner_approval(self):
        self.invalid(lambda q: q["sections"][1]["entries"].append({"title":"Approve"}))
    def test_no_fake_cash(self):
        self.invalid(lambda q: q["sections"][3]["financial_visibility"].update(available_cash=0))
    def test_wrong_counts(self):
        self.invalid(lambda q: q["counts"].update(actions=52))

if __name__ == "__main__":
    unittest.main()
