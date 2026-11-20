import unittest
from datetime import date
from tools.company_operating_cadence import classify_event,prepare_checkpoint,period_key
DAY=date(2026,11,20)
class CadenceTests(unittest.TestCase):
    def event(self,**kw):
        return classify_event(**{**dict(domain="work_obligation",material=True,source_refs=["fixture"],authority_need="none"),**kw})
    def test_material_event_needs_review_not_owner_by_default(self):
        r=self.event()
        self.assertTrue(r["review_needed"]);self.assertFalse(r["owner_attention_candidate"])
        self.assertFalse(r["execution_authorized"])
    def test_owner_requires_actionable_exact_basis(self):
        r=self.event(authority_need="owner",authority_basis="reserved",owner_actionable=True)
        self.assertTrue(r["owner_attention_candidate"]);self.assertFalse(r["owner_decision_ready"])
        for kw in (dict(authority_need="owner"),dict(authority_need="owner",authority_basis="reserved"),dict(authority_need="owner",authority_basis="made_up",owner_actionable=True)):
            with self.assertRaises(ValueError):self.event(**kw)
    def test_unknown_authority_requires_verification_not_inferred_approval(self):
        r=self.event(authority_need="unknown")
        self.assertTrue(r["authority_verification_needed"]);self.assertFalse(r["approval_provided"])
    def test_routine_and_waiting_not_material(self):
        for domain in ("routine_execution","technical_warning","informational","waiting_external"):
            r=self.event(domain=domain,material=False,source_refs=[])
            self.assertFalse(r["review_needed"])
            with self.assertRaises(ValueError):self.event(domain=domain)
    def test_no_material_review_without_evidence(self):
        with self.assertRaises(ValueError):self.event(source_refs=[])
    def test_period_boundaries(self):
        self.assertEqual(period_key("weekly",date(2027,1,1)),"2026-W53")
        self.assertEqual(period_key("monthly",DAY),"2026-11")
        self.assertEqual(period_key("quarterly",DAY),"2026-Q4")
    def test_weekly_only_when_active_and_material(self):
        for active,material,state in [(False,True,"not_needed"),(True,False,"not_needed"),(None,True,"eligibility_unknown"),(True,True,"history_unknown_prepare_only")]:
            r=prepare_checkpoint(mode="weekly",day=DAY,prior_review=None,active_week=active,material_aggregate=material)
            self.assertEqual(r["state"],state);self.assertFalse(r["task_created"])
    def test_duplicate_calendar_review_suppressed(self):
        for mode in ("weekly","monthly","quarterly"):
            flags=dict(active_week=True,material_aggregate=True) if mode=="weekly" else {}
            r=prepare_checkpoint(mode=mode,day=DAY,prior_review={"date":"2026-11-20","source_refs":["review proof"]},**flags)
            self.assertEqual(r["state"],"already_reviewed_for_period")
            self.assertFalse(r["review_completed"])
    def test_monthly_integrates_finance_portfolio_controls_and_burden(self):
        r=prepare_checkpoint(mode="monthly",day=DAY,prior_review=None,sections={"finance_summary":{"state":"partial","source_refs":["fixture"]}})
        self.assertEqual(set(r["sections"]),{"finance_summary","portfolio_exception_scan","open_material_controls","control_burden"})
        self.assertEqual(r["sections"]["portfolio_exception_scan"]["state"],"unknown")
        self.assertFalse(r["owner_meeting_required"]);self.assertFalse(r["owner_approval_required_by_checkpoint"])
    def test_quarterly_no_fake_review_or_daily_ceremony(self):
        r=prepare_checkpoint(mode="quarterly",day=DAY,prior_review=None)
        self.assertEqual(set(r["sections"]),{"portfolio_revalidation","continuity_dependency","control_fit","owner_burden"})
        self.assertFalse(r["review_completed"])
        with self.assertRaises(ValueError):prepare_checkpoint(mode="daily",day=DAY,prior_review=None)
        with self.assertRaises(ValueError):prepare_checkpoint(mode="monthly",day=DAY,prior_review=None,sections={"finance_summary":{"state":"reviewed_scope","source_refs":[]}})
        with self.assertRaises(ValueError):prepare_checkpoint(mode="monthly",day=DAY,prior_review={"date":"2026-11-21","source_refs":["future"]})
