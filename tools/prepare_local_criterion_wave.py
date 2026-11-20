"""Local private review package. Dry run defaults to no writes; --apply requires concrete approval."""
import argparse,hashlib,importlib.util,json,re,subprocess
from pathlib import Path

ROOT=Path("/Users/master/ArvectumSafe/spec-kit-local-20261120")
PROFILES=json.loads("[{\"project\":\"1c-lab\",\"feature\":\"001-lab-acceptance-traceability\",\"head\":\"fc3d83040bf0f543cbf8c187577dc85ba50ee8e2\",\"source\":\"70297db68d3ffaaa20938b58b343ee78485e7fd8\",\"primary\":\"docs/acceptance.md\",\"original\":\"/Volumes/ArvectumSSD/Arvectum/repos/arvectum-1c-lab\",\"expected\":8,\"source_hashes\":{\"README.md\":\"ba5a2da1a88d0e1bdc67dca42034594c7513c0cda821b6595c73258a1e0652de\",\"docs/acceptance.md\":\"874bb7f4d61a6f4d430f85ad5fd47e031caddde970d15e8351ff227d30ef7fa4\"}},{\"project\":\"arc\",\"feature\":\"001-arc-roadmap-traceability\",\"head\":\"04cf26a3a9f8abf021f59a1f64b5f9cdf8274b2d\",\"source\":\"284a48497283dcbf2b9e6a12be2c68452b698466\",\"primary\":\"sites/PERSONAL_ECOSYSTEM_ROADMAP.md\",\"original\":\"/Volumes/ArvectumSSD/Arvectum/repos/desktop-commander\",\"expected\":40,\"source_hashes\":{\"sites/PERSONAL_ECOSYSTEM_ROADMAP.md\":\"07ba0018ead8b16f299162530912e3f27cde9330d1a7359af255826514ccba0d\",\"sites/PROJECT_EDITING_PLAN.md\":\"30b1fb04319c97b131a6d5c29985d8e624a97b54170a88b780de22a40d41eef9\"}},{\"project\":\"tender-app\",\"feature\":\"001-held-calculator-reference\",\"head\":\"d8c8c1fbaa4805772af2c34877544bee553c5b83\",\"source\":\"03f5fec5f2ddc722bf6e82d7332e9b469bfa0fd8\",\"primary\":\"archive-handover-reference\",\"expected\":110,\"source_hashes\":{\"archive-handover-reference\":\"07b61d454caa38a77cc8efd8f57233bb75321b03ec6f25b48f2cfd45cdc57e3f\"}}]")
ARCHIVE=Path("/Volumes/ArvectumSSD/Arvectum/archive/legacy/tender-app/docs/HANDOVER_2026-05-24.md")
BUNDLE=Path("/Volumes/ArvectumSSD/Arvectum/archive/recovery/tender-app/tender-app-legacy-history.bundle")
BUNDLE_HASH="4a7d9d8264633757b937f6aedd540b37fdadc24abc9b80b69b3a4616ba54735c"
QUESTION_SCRIPT_HASH="90b8b0aec866d349d518196432302ef12ecfea70734ab77caf4d83c587f08130"

def sha(b):return hashlib.sha256(b).hexdigest()
def git(p,*args):return subprocess.check_output(["git","-C",str(p),*args])
def require(ok,message):
    if not ok:raise ValueError(message)
def clean_at(p,head):
    require(git(p,"rev-parse","HEAD").decode().strip()==head and not git(p,"status","--porcelain").strip(),"changed or dirty checkout "+str(p))
def build(p):
    name=p["project"];root=ROOT/name;feature=root/"specs"/p["feature"]
    clean_at(root,p["head"])
    if p.get("original"):clean_at(Path(p["original"]),p["source"])
    else:require(sha(BUNDLE.read_bytes())==BUNDLE_HASH,"archive bundle changed")
    manifest=json.loads((feature/"source-anchors.json").read_text())
    require(manifest["source_commit"]==p["source"] and manifest["actual_acceptance_verified"] is False,"source manifest")
    require(set(manifest["anchors"])==set(p["source_hashes"]),"source coverage")
    sources={}
    for path,h in p["source_hashes"].items():
        raw=ARCHIVE.read_bytes() if path=="archive-handover-reference" else git(root,"show",p["source"]+":"+path)
        require(sha(raw)==h,"source hash "+path)
        lines=raw.decode().splitlines()
        require(manifest["anchors"][path]==[{"line":i,"sha256":sha(l.encode())} for i,l in enumerate(lines,1) if l.strip()],"source anchor "+path)
        if path!="archive-handover-reference":
            actual=(root/path).read_bytes()
            require(actual.startswith(raw) and actual==git(root,"show",p["head"]+":"+path),"current source drift "+path)
        sources[path]=lines
    board=(feature/"tasks.md").read_text()
    refs=re.findall(r"^- \[ \] (REVIEW-[A-Z0-9-]+) — reconcile existing source at line (\d+),",board,re.M)
    require(len(refs)==p["expected"] and len(set(refs))==len({x[0] for x in refs})==len(refs),"review task coverage")
    require(board.count("- [ ] REVIEW-SOURCE-COVERAGE —")==1,"source coverage task")
    lines=sources[p["primary"]];rows=[]
    for task,number in refs:
        n=int(number);require(1<=n<=len(lines) and lines[n-1].strip(),"invalid source line")
        line=lines[n-1];heading=max((j for j in range(1,n+1) if re.match(r"^#{1,6}\s",lines[j-1])),default=0)
        if name=="1c-lab":
            m=re.match(r"^\|\s*(LAB-\d{2})\s*\|.*\|\s*(.*?)\s*\|\s*$",line)
            require(m is not None and task=="REVIEW-"+m.group(1),"native LAB link")
            source_status=m.group(2)
            state="reported_done_unverified" if n==7 else "blocked_authorization" if n==8 else "not_run_dependency"
        elif name=="arc":
            m=re.match(r"^\s*-\s*\[([xX ])\]",line)
            require(m is not None and task==f"REVIEW-ARC-REF-{n:04d}","ARC source link")
            source_status=m.group(1);state="reported_checked_unverified" if source_status.lower()=="x" else "open_review"
        else:
            require(task==f"REVIEW-CALC-REF-{n:04d}","archive source link")
            source_status="historical_reference"
            state="contained_historical_acceptance" if 219<=n<=242 else "contained_historical_backlog" if 200<=n<=218 else "contained_context"
        rows.append({"id":task.removeprefix("REVIEW-"),"review_task_id":task,"source":p["primary"],"line":n,
                     "heading_line":heading,"line_sha256":sha(line.encode()),"source_status":source_status,
                     "review_state":state,"evidence":[]})
    data={"schema":"arvectum.local.native-review/1","project":name,"source_commit":p["source"],"review_baseline":p["head"],
          "source_hashes":p["source_hashes"],"source_coverage_task":"REVIEW-SOURCE-COVERAGE","actual_acceptance_verified":False,
          "execution_authorized":False,"archive_disposition":"KEEP_IN_PLACE" if name=="tender-app" else None,"rows":rows}
    return root,feature/"criterion-review.json",data

def main():
    parser=argparse.ArgumentParser();parser.add_argument("--apply",action="store_true");parser.add_argument("--question-script",type=Path,required=True);a=parser.parse_args()
    require(sha(a.question_script.read_bytes())==QUESTION_SCRIPT_HASH,"question script hash")
    qspec=importlib.util.spec_from_file_location("question",a.question_script);q=importlib.util.module_from_spec(qspec);qspec.loader.exec_module(q)
    bd=q.build();broot=q.ROOT;require(bd["actual_customer_acceptance_verified"] is False,"question acceptance")
    clean_at(Path("/Volumes/ArvectumSSD/Arvectum/repos/deal"),q.PIN)
    planned=[(broot,broot/q.DIR/"question-review.json",bd)]+[build(p) for p in PROFILES]
    for root,dest,data in planned:
        require(not dest.exists(),"destination exists "+str(dest))
        counts={}
        for r in data["rows"]:
            s=r.get("review_state",r.get("state"));counts[s]=counts.get(s,0)+1
        print(json.dumps({"project":root.name,"rows":len(data["rows"]),"states":counts,"apply":a.apply},ensure_ascii=False))
    if not a.apply:return
    # All sources and destinations checked before any writes. Local commits only.
    for root,dest,data in planned:
        with dest.open("x",encoding="utf8") as f:json.dump(data,f,ensure_ascii=False,indent=2);f.write("\n")
        require(json.loads(dest.read_text())==data,"readback")
        git(root,"add","--",str(dest.relative_to(root)));git(root,"diff","--cached","--check")
        git(root,"commit","-m","docs(spec): record local source criterion review")
        require(not git(root,"status","--porcelain").strip(),"dirty final candidate")
        print(json.dumps({"project":root.name,"local_head":git(root,"rev-parse","HEAD").decode().strip(),"readback":"PASS"},ensure_ascii=False))
    for p in PROFILES:
        if p.get("original"):clean_at(Path(p["original"]),p["source"])
    clean_at(Path("/Volumes/ArvectumSSD/Arvectum/repos/deal"),q.PIN)
    require(sha(BUNDLE.read_bytes())==BUNDLE_HASH and sha(ARCHIVE.read_bytes())==PROFILES[-1]["source_hashes"]["archive-handover-reference"],"archive altered")
if __name__=="__main__":main()
