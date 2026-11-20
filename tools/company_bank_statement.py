"""AC-404 offline bank-export review, not a ledger or approved financial fact.

Restricted 1CClientBankExchange 1.02/1.03, one RUB account, one whole-period
balance section. No credentials, network, raw counterparties or booking writes.
Exact byte reconciliation does not authenticate the bank or company coverage.
"""
import re,json,hashlib,os,stat
from datetime import date,datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from .company_control_register import private_dir,require,canonical,locked
import tempfile

MAX_BYTES=10*1024*1024
MAX_DOCS=20000
SCOPE={"account","currency","period_start","period_end","owner_confirmed_export"}

def day(s):
    require(isinstance(s,str) and re.fullmatch(r"\d{2}\.\d{2}\.\d{4}",s) is not None,"invalid statement date")
    return datetime.strptime(s,"%d.%m.%Y").date()

def money(s,signed=False):
    require(isinstance(s,str) and re.fullmatch(r"-?(0|[1-9][0-9]{0,13})(\.[0-9]{1,2})?",s) is not None,"invalid monetary value")
    neg=s.startswith("-")
    require(signed or not neg,"negative turnover")
    whole,_,frac=s.lstrip("-").partition(".")
    return (-1 if neg else 1)*(int(whole)*100+int(frac.ljust(2,"0") or 0))

def fmt(n):
    return ("-" if n<0 else "")+f"{abs(n)//100}.{abs(n)%100:02d}"

def decode(raw):
    require(type(raw) is bytes and 0<len(raw)<=MAX_BYTES,"statement size")
    # First line and encoding declaration are inspected under their own codec.
    matches=[]
    for codec,declared in (("cp1251","Windows"),("cp866","DOS")):
        try:s=raw.decode(codec)
        except UnicodeDecodeError:continue
        lines=s.splitlines()
        if lines and lines[0]=="1CClientBankExchange" and "Кодировка="+declared in lines[:20]:
            matches.append(lines)
    require(len(matches)==1,"unsupported or ambiguous encoding")
    lines=matches[0]
    require(all(len(x)<=32768 and not any(ord(c)<32 for c in x) for x in lines),"invalid line")
    return lines

def parse(raw,scope,*,today):
    require(type(scope) is dict and set(scope)==SCOPE and scope["owner_confirmed_export"] is True,"explicit local export scope required")
    account=scope["account"]
    require(isinstance(account,str) and re.fullmatch(r"[0-9]{20}",account) is not None and scope["currency"]=="RUB","one reviewed RUB account required")
    lo,hi=date.fromisoformat(scope["period_start"]),date.fromisoformat(scope["period_end"])
    require(lo<=hi<today,"closed calendar period required")
    lines=decode(raw)
    header={};balance=[];docs=[];current=header;state="header";ended=False
    for line in lines[1:]:
        if not line:continue
        require(not ended,"trailing statement content")
        if line=="СекцияРасчСчет":
            require(state=="header" and not balance,"unsupported balance sections")
            current={};state="balance";continue
        if line=="КонецРасчСчет":
            require(state=="balance","unexpected balance end")
            balance.append(current);current=None;state="between";continue
        if line.startswith("СекцияДокумент="):
            require(state=="between" and len(docs)<MAX_DOCS,"unexpected document or count")
            kind=line.split("=",1)[1];require(bool(kind),"missing document type")
            current={};state="doc";continue
        if line=="КонецДокумента":
            require(state=="doc","unexpected document end")
            docs.append((kind,current));state="between";current=None;continue
        if line=="КонецФайла":
            require(state=="between" and len(balance)==1,"incomplete statement")
            ended=True;continue
        require(current is not None and "=" in line,"unsupported statement record")
        k,v=line.split("=",1)
        require(bool(k),"missing field")
        if state=="header" and k=="Документ":
            # Provider may enumerate export document types; totals still must reconcile.
            header.setdefault(k,[]).append(v);continue
        require(k not in current,"duplicate field")
        current[k]=v
    require(ended and len(balance)==1,"missing end marker")
    require(header.get("ВерсияФормата") in ("1.02","1.03"),"unsupported version")
    def same_period(section):
        require(section.get("РасчСчет")==account and day(section.get("ДатаНачала"))==lo and day(section.get("ДатаКонца"))==hi,"account or period mismatch")
    same_period(header);b=balance[0];same_period(b)
    require(all(k in b for k in ("НачальныйОстаток","ВсегоПоступило","ВсегоСписано","КонечныйОстаток")),"missing balance controls")
    opening=money(b["НачальныйОстаток"],True);credit=money(b["ВсегоПоступило"]);debit=money(b["ВсегоСписано"]);closing=money(b["КонечныйОстаток"],True)
    require(opening+credit-debit==closing,"balance equation mismatch")
    actual_in=actual_out=0;seen=set();counts=[0,0]
    for kind,d in docs:
        payer,receiver=d.get("ПлательщикСчет"),d.get("ПолучательСчет")
        require(all(isinstance(x,str) and re.fullmatch(r"[0-9]{20}",x) for x in (payer,receiver)),"missing account link")
        require((payer==account)!=(receiver==account),"ambiguous operation scope")
        out=payer==account
        posted=day(d.get("ДатаСписано" if out else "ДатаПоступило"))
        require(lo<=posted<=hi,"operation outside closed interval")
        num=d.get("Номер");require(isinstance(num,str) and bool(num.strip()),"missing document number")
        key=(payer,kind,day(d.get("Дата")),num)
        require(key not in seen,"duplicate document identity")
        seen.add(key)
        amount=money(d.get("Сумма"));require(amount>0,"nonpositive operation")
        if out:actual_out+=amount;counts[1]+=1
        else:actual_in+=amount;counts[0]+=1
    require((actual_in,actual_out)==(credit,debit),"document totals mismatch")
    return {"schema":"arvectum.company.bank-statement-review/1","source_sha256":hashlib.sha256(raw).hexdigest(),
      "period_start":lo.isoformat(),"period_end":hi.isoformat(),"currency":"RUB",
      "scope":"one_owner_selected_account","coverage":"partial","arithmetic":"reconciled",
      "opening_booked_rub":fmt(opening),"closing_booked_rub":fmt(closing),
      "gross_credits_rub":fmt(credit),"gross_debits_rub":fmt(debit),
      "credit_documents":counts[0],"debit_documents":counts[1],
      "available_cash":None,"actual_customer_receipts":None,"profit":None,
      "company_liquidity":"unknown","decision_readiness":"blocked_by_missing_financial_evidence",
      "source_authenticity":"requires_review","payment_authority":False,"canonical_authority":False}

def read_private(path,max_bytes):
    path=Path(path)
    private_dir(path.parent)
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    with os.fdopen(fd,"rb") as f:
        s=os.fstat(f.fileno())
        require(stat.S_ISREG(s.st_mode) and s.st_uid==os.getuid() and s.st_nlink==1 and not s.st_mode&0o077,"unsafe private file")
        raw=f.read(max_bytes+1)
    require(len(raw)<=max_bytes,"private input too large")
    return raw

def review_file(statement,scope_file,result):
    """Write only an immutable private review candidate; source stays untouched."""
    statement=Path(statement);scope_file=Path(scope_file);result=Path(result)
    raw=read_private(statement,MAX_BYTES)
    scope=json.loads(read_private(scope_file,4096))
    now=datetime.now(ZoneInfo("Europe/Moscow"))
    report=parse(raw,scope,today=now.date())
    report["reviewed_at"]=now.isoformat()
    folder=private_dir(result.parent)
    with locked(folder):
        require(not result.exists() and not result.is_symlink(),"refuse overwrite")
        fd,tmp=tempfile.mkstemp(prefix=".bank-review-",dir=folder)
        try:
            with os.fdopen(fd,"wb") as f:
                f.write(canonical(report));f.flush();os.fsync(f.fileno())
            os.link(tmp,result,follow_symlinks=False)
            os.unlink(tmp)
            dfd=os.open(folder,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
            try:os.fsync(dfd)
            finally:os.close(dfd)
        finally:
            if os.path.exists(tmp):os.unlink(tmp)
        require(read_private(result,MAX_BYTES)==canonical(report),"review write mismatch")
    return report

def main():
    import argparse
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("statement",type=Path)
    ap.add_argument("scope",type=Path)
    ap.add_argument("result",type=Path)
    args=ap.parse_args()
    try:
        review_file(args.statement,args.scope,args.result)
    except (ValueError,TypeError,KeyError,OSError,UnicodeError):
        raise SystemExit("AC-404 intake rejected: review format, scope, completeness, arithmetic and private paths locally.") from None
    print("AC-404 private arithmetic review saved; source authenticity and financial admission pending.")

if __name__=="__main__":main()
