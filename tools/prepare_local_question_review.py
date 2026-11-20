"""Local-only question evidence review. Dry run read-only; apply only with explicit authorization."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
ROOT=Path("/Users/master/ArvectumSafe/spec-kit-local-20261120/baltika")
PIN="6ea3955555d67843819514fe00fb5509a8384711"
HEAD="bd0a25aeabfb8e1bb671734ca39c76adc70c6dc8"
DIR="specs/001-baltika-question-traceability"
MEETING="docs/BALTIKA_MEETING.md"
PILOT="docs/BALTIKA_PILOT.md"
REHEARSAL="docs/BALTIKA_REHEARSAL.md"
OFFER="docs/BALTIKA_OFFER.md"
HASHES={MEETING:"f71d570d193634f9751ff503cefd61fb9bf084c17409f4538c17a27704caa180",
PILOT:"51fd919ae7a659da03df2bf091b2dca1dd1202b1fc2cb16ccd9b03483c4f0af3",
REHEARSAL:"029ed496cc3b3f8f59f9504c93dbd077acfb755e39d2b752906054b8c7def106",
OFFER:"043ec395b71bd5c478d4c3b8a0179d7fbdddd8004cb685ed5bfca81015f79343"}
# Question IDs and references only; no private question/offer text in Company.
REFERENCES={1:(PILOT,22,29),2:(PILOT,22,29),3:(PILOT,22,29),4:(PILOT,22,29),
5:(PILOT,30,38),6:(PILOT,30,47),7:(PILOT,30,38),8:(PILOT,30,38),
9:(PILOT,30,38),10:(PILOT,39,47),11:(PILOT,30,38),12:(PILOT,22,47),
13:(PILOT,30,38),14:(PILOT,46,46),15:(PILOT,39,47),16:(PILOT,8,19),
17:(REHEARSAL,45,52),18:(PILOT,39,47),19:(PILOT,11,19),20:(OFFER,1,32)}
def git(*a):
    return subprocess.check_output(["git","-C",str(ROOT),*a])
def sha(b):return hashlib.sha256(b).hexdigest()
def build():
    if git("rev-parse","HEAD").decode().strip()!=HEAD or git("status","--porcelain").strip():
        raise ValueError("local review head changed or dirty")
    src={p:git("show",PIN+":"+p) for p in HASHES}
    if any(sha(b)!=HASHES[p] for p,b in src.items()):raise ValueError("source hash mismatch")
    for p,b in src.items():
        actual=(ROOT/p).read_bytes()
        if p==MEETING:
            if not actual.startswith(b) or actual!=git("show",HEAD+":"+p):raise ValueError("meeting source drift")
        elif actual!=b:raise ValueError("source drift "+p)
    board=(ROOT/DIR/"tasks.md").read_text()
    ids=re.findall(r"^- \[ \] REVIEW-BAL-Q(\d{2})\b",board,re.M)
    if ids!=[f"{i:02d}" for i in range(1,21)]:raise ValueError("review task coverage")
    rows=[]
    for n,line in enumerate(src[MEETING].decode().splitlines(),1):
        m=re.match(r"^\|\s*(\d+)\s*\|",line)
        if not m:continue
        i=int(m.group(1));p,a,z=REFERENCES[i]
        if not 1<=a<=z<=len(src[p].decode().splitlines()):raise ValueError("invalid observation range")
        state="open_no_demonstrated_scenario" if i==14 else "customer_scope_pending" if i==20 else "bounded_demo_reported" if i==17 else "partial_reported"
        rows.append({"id":f"BAL-Q{i:02d}","review_task_id":f"REVIEW-BAL-Q{i:02d}",
        "source_line":n,"question_row_sha256":sha(line.encode()),"source_row":line,
        "state":state,"observation":{"path":p,"first_line":a,"last_line":z,"commit":PIN,
        "kind":"recorded_report_not_independent_acceptance"},"acceptance_evidence":[]})
    if [r["id"] for r in rows]!=[f"BAL-Q{i:02d}" for i in range(1,21)]:raise ValueError("question coverage")
    return {"schema":"arvectum.local.question-review/1","source_commit":PIN,"baseline_review_head":HEAD,
    "actual_customer_acceptance_verified":False,"execution_authorized":False,"rows":rows}
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--apply",action="store_true");a=ap.parse_args()
    data=build()
    counts={}
    for r in data["rows"]:counts[r["state"]]=counts.get(r["state"],0)+1
    print(json.dumps({"questions":len(data["rows"]),"states":counts,"actual_acceptance_verified":False},ensure_ascii=False))
    if not a.apply:return
    dest=ROOT/DIR/"question-review.json"
    with dest.open("x",encoding="utf-8") as f:json.dump(data,f,ensure_ascii=False,indent=2);f.write("\n")
    if json.loads(dest.read_text())!=data:raise ValueError("readback")
    git("add","--",str(dest.relative_to(ROOT)));git("diff","--cached","--check")
    git("commit","-m","docs(spec): record private per-question evidence review")
    if git("status","--porcelain").strip():raise ValueError("dirty final candidate")
    print("Local candidate commit",git("rev-parse","HEAD").decode().strip())
if __name__=="__main__":main()
