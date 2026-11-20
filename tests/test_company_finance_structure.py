import copy,unittest
from tools import company_finance_structure as s
from tools.company_finance_report import build
NOW="2026-11-20T09:00:00Z"
BASE="2026-11-20";END="2026-12-20"
def row(kind="incurred_outflow",amount="40.00",due="2026-11-25",condition=None,refs=None):
    return {"kind":kind,"title":"Synthetic","amount_rub":amount,"due_date":due,"condition":condition,
       "source_kind":s.SOURCE_KIND[kind],"source_refs":["fixture source"],"as_of":NOW,
       "control_refs":refs if refs is not None else ["OBL-001"]}
def forecast(items,coverage="complete_for_reviewed_scope",cash=None,confirmed=True):
    return s.conservative_forecast(cash=s.fact("100.00",NOW,["fixture bank"]) if cash is None else cash,
          calendar_view=s.calendar(items,coverage=coverage,as_of=NOW),
          base_date=BASE,through=END,as_of=NOW,scope_confirmed=confirmed)
class StructureTests(unittest.TestCase):
    def test_empty_structure_has_no_invented_values(self):
        p=s.empty_packet(NOW)
        self.assertEqual(len(p["facts"]),14)
        self.assertTrue(all(v==s.unknown() for v in p["facts"].values()))
        self.assertIsNone(p["forecast"]["minimum_cash_after_confirmed_outflows_rub"])
        self.assertFalse(p["canonical_authority"]);self.assertFalse(p["payment_authority"])
    def test_existing_contract_is_conditional_and_not_cash(self):
        initial=build(as_of=NOW,contract_ref="fixture",xml_ref="fixture xml",amount="123.45",
            work_refs=["OBL-001"],risk_refs=["RSK-001"],condition="After acceptance")
        p=s.from_initial_report(initial)
        self.assertEqual(p["calendar"]["items"][0]["kind"],"conditional_inflow")
        self.assertEqual(p["calendar"]["items"][0]["amount_rub"],"123.45")
        self.assertIsNone(p["calendar"]["items"][0]["due_date"])
        self.assertEqual(p["facts"]["available_cash"],s.unknown())
        self.assertEqual(p["calendar"]["coverage"],"partial")
    def test_calendar_dated_then_conditions_and_approval_separation(self):
        a=row("conditional_inflow",due=None,condition="After acceptance")
        b=row("approved_not_incurred",due="2026-11-22",refs=["APR-001"])
        c=row()
        result=s.calendar([c,a,b],coverage="partial",as_of=NOW)
        self.assertEqual([v["kind"] for v in result["items"]],["approved_not_incurred","incurred_outflow","conditional_inflow"])
    def test_calendar_blocks_due_and_condition_and_wrong_source(self):
        a=row()
        for v in ({**a,"condition":"also"},{**a,"source_kind":"forecast"},{**a,"control_refs":[]},{**a,"amount_rub":"-1.00"}):
            with self.assertRaises(ValueError):s.calendar([v],coverage="partial",as_of=NOW)
        with self.assertRaises(ValueError):s.calendar([a,a],coverage="partial",as_of=NOW)
    def test_forecast_never_counts_conditional_receipt_or_plans(self):
        a=row()
        b=row("conditional_inflow","1000.00",due=None,condition="After acceptance")
        c=row("planned_outflow","200.00",refs=["WORK-001"])
        r=forecast([a,b,c]);self.assertEqual(r["minimum_cash_after_confirmed_outflows_rub"],"60.00")
        self.assertTrue(r["confirmed_outflows_only"])
        self.assertEqual(forecast([row(amount="150.00")])["minimum_cash_after_confirmed_outflows_rub"],"-50.00")
    def test_forecast_excludes_future_after_horizon_includes_overdue(self):
        a=row(due="2026-11-19")
        b=row(amount="500.00",due="2026-12-21",refs=["OBL-002"])
        self.assertEqual(forecast([a,b])["minimum_cash_after_confirmed_outflows_rub"],"60.00")
    def test_forecast_blocks_incomplete_stale_duplicate_and_unknown(self):
        for r in (forecast([row()],coverage="partial"),forecast([row()],cash=s.unknown()),
            forecast([row()],confirmed=False),forecast([row(amount=None)]),
            forecast([row(due=None,condition="Due after delivery")]),
            forecast([{**row(),"as_of":"2026-11-19T09:00:00Z"}]),
            forecast([row(),row("mandatory_outflow",refs=["OBL-001"])])):
            self.assertIsNone(r["minimum_cash_after_confirmed_outflows_rub"])
            self.assertEqual(r["state"],"unknown")
    def test_no_zero_from_unknown_or_unverified_fact(self):
        for f in ({**s.unknown(),"value":"0.00"},
            {"state":"stale","value":"10.00","as_of":NOW,"source_refs":["fixture"]}):
            with self.assertRaises(ValueError):s.validate_fact(f,NOW)
        self.assertEqual(forecast([],cash=s.fact("0.00",NOW,["fixture"]))["minimum_cash_after_confirmed_outflows_rub"],"0.00")
    def test_economics_direct_contribution_not_profit(self):
        kw={"project_ref":"fixture","period_start":"2026-11-01","period_end":"2026-11-19","as_of":NOW,"scope_confirmed":True}
        rev=s.fact("100.00",NOW,["fixture revenue"])
        cost=s.fact("70.25",NOW,["fixture cost"])
        r=s.project_economics(**kw,revenue=rev,direct_costs=cost)
        self.assertEqual(r["direct_contribution_rub"],"29.75");self.assertIsNone(r["net_profit_rub"])
        self.assertIsNone(s.project_economics(**kw,revenue=rev,direct_costs=s.unknown())["direct_contribution_rub"])
        self.assertIsNone(s.project_economics(**{**kw,"scope_confirmed":False},revenue=rev,direct_costs=cost)["direct_contribution_rub"])
    def test_review_candidate_typed_facts_period_and_source(self):
        f=s.category_fact("actual_credits","100.00",NOW,["reviewed bank export"],scope_ref="reviewed account scope",
          period_start="2026-11-01",period_end="2026-11-19")
        p=s.assemble_review(as_of=NOW,facts={"actual_credits":f},calendar_items=[],calendar_coverage="unknown")
        self.assertEqual(p["facts"]["actual_credits"]["value"]["amount_rub"],"100.00")
        self.assertEqual(p["facts"]["available_cash"],s.unknown())
        self.assertEqual(p["facts"]["project_economics"],s.unknown())
        self.assertEqual(p["decision_readiness"],"blocked_by_missing_financial_evidence")
        q=copy.deepcopy(f);q["value"]["source_kind"]="accounting"
        with self.assertRaises(ValueError):s.assemble_review(as_of=NOW,facts={"actual_credits":q},calendar_items=[],calendar_coverage="unknown")
        with self.assertRaises(ValueError):s.category_fact("actual_credits","100.00",NOW,["fixture"],scope_ref="fixture")
    def test_review_preserves_conditional_inflow_and_rejects_unknown_categories(self):
        initial=build(as_of=NOW,contract_ref="fixture",xml_ref="fixture xml",amount="123.45",
            work_refs=["OBL-001"],risk_refs=["RSK-001"],condition="After acceptance")
        p=s.assemble_review(as_of=NOW,facts={},calendar_items=[],calendar_coverage="partial",initial=initial)
        self.assertEqual(len(p["calendar"]["items"]),1)
        self.assertIsNone(p["forecast"]["minimum_cash_after_confirmed_outflows_rub"])
        with self.assertRaises(ValueError):s.assemble_review(as_of=NOW,facts={"profit":s.unknown()},calendar_items=[],calendar_coverage="unknown")
        with self.assertRaises(ValueError):s.assemble_review(as_of=NOW,facts={},calendar_items=[],calendar_coverage="complete_for_reviewed_scope",initial=initial)
