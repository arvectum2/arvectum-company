import copy,json,os,tempfile,unittest
from datetime import date
from pathlib import Path
from tools import company_bank_statement as s

ACCOUNT="40702810000000000001"
OTHER="40702810000000000002"
START="01.11.2026";END="19.11.2026"
TODAY=date(2026,11,20)
SCOPE={"account":ACCOUNT,"currency":"RUB","period_start":"2026-11-01","period_end":"2026-11-19","owner_confirmed_export":True}
def fixture():
    return f"""1CClientBankExchange
ВерсияФормата=1.03
Кодировка=Windows
Отправитель=TEST
ДатаНачала={START}
ДатаКонца={END}
РасчСчет={ACCOUNT}
Документ=Платежное поручение
СекцияРасчСчет
ДатаНачала={START}
ДатаКонца={END}
РасчСчет={ACCOUNT}
НачальныйОстаток=100.00
ВсегоПоступило=25.30
ВсегоСписано=10.20
КонечныйОстаток=115.10
КонецРасчСчет
СекцияДокумент=Платежное поручение
Номер=1
Дата=31.10.2026
Сумма=25.30
ПлательщикСчет={OTHER}
ПолучательСчет={ACCOUNT}
ДатаПоступило=02.11.2026
НазначениеПлатежа=synthetic source only
КонецДокумента
СекцияДокумент=Платежное поручение
Номер=2
Дата=03.11.2026
Сумма=10.20
ПлательщикСчет={ACCOUNT}
ПолучательСчет={OTHER}
ДатаСписано=04.11.2026
КонецДокумента
КонецФайла
"""
def parse(text=None,scope=None):
    return s.parse((fixture() if text is None else text).encode("cp1251"),SCOPE if scope is None else scope,today=TODAY)

class StatementTests(unittest.TestCase):
    def test_reconcile_exact_minor_units_and_privacy(self):
        r=parse()
        self.assertEqual(r["closing_booked_rub"],"115.10")
        self.assertEqual(r["gross_credits_rub"],"25.30")
        self.assertEqual(r["gross_debits_rub"],"10.20")
        self.assertEqual(r["credit_documents"],1)
        self.assertEqual(r["debit_documents"],1)
        self.assertIsNone(r["available_cash"])
        self.assertIsNone(r["actual_customer_receipts"])
        self.assertIsNone(r["profit"])
        self.assertFalse(r["payment_authority"])
        self.assertNotIn(ACCOUNT,json.dumps(r))
        self.assertNotIn(OTHER,json.dumps(r))
        self.assertNotIn("synthetic source only",json.dumps(r))
    def test_supported_second_encoding_and_version(self):
        raw=fixture().replace("Windows","DOS").replace("1.03","1.02").encode("cp866")
        self.assertEqual(s.parse(raw,SCOPE,today=TODAY)["closing_booked_rub"],"115.10")
    def test_bad_scope_and_open_day(self):
        for k,v in (("account",OTHER),("currency","USD"),("period_end","2026-11-20"),("owner_confirmed_export",False)):
            with self.subTest(k=k),self.assertRaises(ValueError):
                parse(scope={**SCOPE,k:v})
    def test_bad_balance_or_turnover(self):
        for a,b in (("115.10","115.11"),("25.30","25.31"),("Сумма=10.20","Сумма=10.21"),("Сумма=10.20","Сумма=10.201"),("ВсегоСписано=10.20","ВсегоСписано=-10.20")):
            with self.subTest(a=a,b=b),self.assertRaises(ValueError):parse(fixture().replace(a,b,1))
    def test_missing_posting_dates_and_wrong_scope(self):
        for t in (fixture().replace("ДатаПоступило=02.11.2026\n",""),fixture().replace("ДатаСписано=04.11.2026","ДатаСписано=20.11.2026"),fixture().replace("ПолучательСчет="+OTHER,"ПолучательСчет="+ACCOUNT)):
            with self.assertRaises(ValueError):parse(t)
    def test_duplicate_or_truncated_or_extra(self):
        t=fixture()
        start=t.index("СекцияДокумент=");end=t.index("КонецДокумента")+len("КонецДокумента")
        for x in (t[:end]+"\n"+t[start:end]+t[end:],t.replace("КонецФайла",""),t+"extra=1\n",t.replace("Номер=1\n","Номер=1\nНомер=3\n")):
            with self.assertRaises(ValueError):parse(x)
    def test_no_operations_and_real_zero_distinct_from_unknown(self):
        t=fixture().split("СекцияДокумент=")[0]+"КонецФайла\n"
        for a,b in (("100.00","0.00"),("25.30","0.00"),("10.20","0.00"),("115.10","0.00")):t=t.replace(a,b)
        r=parse(t)
        self.assertEqual(r["closing_booked_rub"],"0.00")
        self.assertIsNone(r["available_cash"])
        self.assertEqual(r["credit_documents"],0)
    def test_private_review_immutable_no_source_mutation(self):
        with tempfile.TemporaryDirectory() as t:
            d=Path(t).resolve();os.chmod(d,0o700)
            src=d/"statement.txt";raw=fixture().encode("cp1251");src.write_bytes(raw);os.chmod(src,0o600)
            scope=d/"scope.json";scope.write_text(json.dumps(SCOPE));os.chmod(scope,0o600)
            out=d/"review.json"
            r=s.review_file(src,scope,out)
            self.assertEqual(r["arithmetic"],"reconciled")
            self.assertEqual(src.read_bytes(),raw)
            self.assertEqual(out.stat().st_mode&0o777,0o600)
            with self.assertRaises(ValueError):s.review_file(src,scope,out)
            link=d/"link.txt";link.symlink_to(src)
            with self.assertRaises(OSError):s.review_file(link,scope,d/"other.json")
            os.chmod(src,0o644)
            with self.assertRaises(ValueError):s.review_file(src,scope,d/"other.json")
    def test_extra_balance_section_and_encoding_rejected(self):
        t=fixture()
        i=t.index("СекцияРасчСчет");j=t.index("КонецРасчСчет")+len("КонецРасчСчет")
        with self.assertRaises(ValueError):parse(t[:j]+"\n"+t[i:j]+t[j:])
        with self.assertRaises(ValueError):s.parse(t.encode("utf-8"),SCOPE,today=TODAY)
