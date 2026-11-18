import tempfile,unittest,copy
from pathlib import Path
from tools import company_finance_report as r
def build():
    return r.build(as_of="2026-11-18T05:00:00Z",contract_ref="fixture",xml_ref="fixture xml",amount="123.45",work_refs=["OBL-001"],risk_refs=["RSK-001"],condition="After acceptance")
class Tests(unittest.TestCase):
    def test_conditional_forecast_is_not_cash(self):
        d=build();self.assertEqual(d["expected_inflows"][0]["contract_price_rub"],"123.45")
        self.assertIsNone(d["expected_inflows"][0]["expected_available_cash_rub"])
        self.assertEqual(d["liquidity_status"],"unknown")
        self.assertTrue(all(d[k]["value"] is None for k in r.UNKNOWN_FIELDS))
    def test_reject_unverified_facts(self):
        for key in r.UNKNOWN_FIELDS:
            d=build();d[key]={"status":"current","value":0}
            with self.assertRaises(ValueError):r.validate(d)
        for k,v in (("actual_receipt_confirmed",True),("receivable_confirmed",True),("expected_available_cash_rub","123.45")):
            d=build();d["expected_inflows"][0][k]=v
            with self.assertRaises(ValueError):r.validate(d)
    def test_no_authority_or_false_margin(self):
        d=build();d["payment_authority"]=True
        with self.assertRaises(ValueError):r.validate(d)
        d=build();d["portfolio_project_economic_signals"][0]["margin"]="0"
        with self.assertRaises(ValueError):r.validate(d)
    def test_decimal_not_float_or_missing(self):
        for v in (0,123.45,"0.00","-1.00","1e3","1.234",""):
            with self.assertRaises(ValueError):r.money(v)
    def test_private_exclusive_restore(self):
        d=build()
        with tempfile.TemporaryDirectory() as t:
            p=Path(t).resolve()/"report";b=p.with_name("backup")
            r.write_initial(p,d);r.write_initial(b,r.load(p))
            self.assertEqual(p.read_bytes(),b.read_bytes())
            with self.assertRaises(ValueError):r.write_initial(p,d)
            s=p.with_name("link");s.symlink_to(p)
            with self.assertRaises(OSError):r.load(s)
if __name__=="__main__":unittest.main()
