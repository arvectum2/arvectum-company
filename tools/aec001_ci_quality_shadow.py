#!/usr/bin/env python3
"""Offline, strict-subset CI YAML source characterization, not workflow execution."""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import re
import subprocess
import sys
from aec001_private_output import write_private_output

SCHEMA="aec001-ci-quality-shadow-report-v1"
CONTRACT="aec001-ci-quality-shadow-contract-v1"
CORE=["contents-read","checkout","setup-python","pip-install","ruff-check","pytest"]
COMMIT=re.compile(r"[0-9a-f]{40}")
REPO=re.compile(r"arvectum2/[a-z][a-z0-9-]{1,70}")
JOB=re.compile(r"[a-z][a-z0-9-]{1,70}")
WORKFLOW=re.compile(r"\.github/workflows/[a-z][a-z0-9-]{0,80}\.ya?ml")
ACTION=re.compile(r"actions/(checkout|setup-python)@([0-9A-Za-z._-]+)")
INSTALL=re.compile(r"^(?:python3?\s+-m\s+)?pip\s+install(?:\s|$)")
RUFF=re.compile(r"^(?:python3?\s+-m\s+)?ruff\s+check(?:\s|$)")
PYTEST=re.compile(r"^(?:python3?\s+-m\s+)?pytest(?:\s|$)")

def contract_read(path):
    data=json.loads(path.read_text(encoding="utf-8"))
    if (data.get("schema")!=CONTRACT or data.get("contract_version")!="0.1.0"
        or data.get("mode")!="offline-static-source-only" or data.get("core")!=CORE
        or len(data.get("consumers",[]))!=2):
        raise ValueError("unsupported contract")
    seen=set()
    for item in data["consumers"]:
        if set(item)!={"repository","commit","workflow","job"}:
            raise ValueError("unexpected consumer fields")
        if (not REPO.fullmatch(item["repository"]) or
            not COMMIT.fullmatch(item["commit"]) or
            not WORKFLOW.fullmatch(item["workflow"]) or
            not JOB.fullmatch(item["job"]) or item["repository"] in seen):
            raise ValueError("invalid contract pin")
        seen.add(item["repository"])
    return data

def workflow_extract(source,job):
    """Static subset only: never claim full YAML parsing or runner behavior."""
    if len(source)>70000 or "\t" in source or "\r" in source:
        raise ValueError("unsupported workflow whitespace/size")
    if re.search(r"(?m)^\s*(?:<<:|[-\w]+:\s*[&*][-\w]+)",source):
        raise ValueError("YAML alias/merge unsupported")
    lines=source.splitlines()
    if sum(line=="jobs:" for line in lines)!=1:
        raise ValueError("jobs root absent/duplicated")
    start=lines.index("jobs:")
    if re.search(r"(?m)^\s*pull_request_target\s*:",source):
        raise ValueError("privileged PR event unsupported")
    sections=[]
    for i,line in enumerate(lines[start+1:],start+1):
        match=re.fullmatch(r"  ([a-z][a-z0-9-]*):\s*",line)
        if match:sections.append((match.group(1),i))
        elif line and not line.startswith(" ") and not line.startswith("#"):
            break
    hits=[i for name,i in sections if name==job]
    if len(hits)!=1:raise ValueError("missing/duplicate required job")
    index=hits[0]
    stop=min((i for _,i in sections if i>index),default=len(lines))
    section=lines[index:stop]
    if section.count("    steps:")!=1:raise ValueError("missing job steps")
    if any(re.match(r"^    (?:if|continue-on-error):",line) for line in section):
        raise ValueError("skipped or tolerated quality job unsupported")
    entries=[];current=None
    for line in section[section.index("    steps:")+1:]:
        if re.match(r"^      - (uses|run|name):\s*",line):
            if current is not None:entries.append(current)
            current=[line[8:]]
        elif current is not None and line.startswith("        "):
            current.append(line[8:])
        elif line.strip():
            raise ValueError("unsupported step indentation")
    if current is not None:entries.append(current)
    if not entries:raise ValueError("no steps")
    actions=[];install=[];lint=[];test=[];hardening=False
    for i,step in enumerate(entries):
        body="\n".join(step)
        if re.search(r"(?m)^(?:if|continue-on-error):\s*",body):
            raise ValueError("conditional core step unsupported")
        matches=re.findall(r"(?m)^uses:\s*([^\s#]+)\s*$",body)
        if len(matches)>1:raise ValueError("multiple uses in one step")
        for a in matches:
            m=ACTION.fullmatch(a)
            if m:actions.append((m.group(1),m.group(2),i))
            elif a.startswith(("actions/checkout@","actions/setup-python@")):
                raise ValueError("unsupported action ref")
        if matches and matches[0].startswith("actions/checkout@"):
            hardening|=bool(re.search(r"(?m)^\s*persist-credentials:\s*(?:false|'false'|\"false\")\s*$",body))
        # Only run declaration fields, not step name or comments.
        found=re.search(r"(?m)^run:\s*(.*)$",body)
        if not found:continue
        raw=found.group(1).strip()
        if raw.startswith(("|",">")):
            command="\n".join(x.lstrip() for x in step[1:] if x.startswith("  "))
        elif raw and not raw.startswith("#"):
            command=raw
        else:raise ValueError("unrecognized run command")
        if INSTALL.search(command):install.append(i)
        if RUFF.search(command):lint.append(i)
        if PYTEST.search(command):test.append(i)
    checkout=[(ref,i) for kind,ref,i in actions if kind=="checkout"]
    python=[(ref,i) for kind,ref,i in actions if kind=="setup-python"]
    return _result(lines,section,checkout,python,install,lint,test,hardening)

def _result(lines,section,checkout,python,install,lint,test,hardening):
    # A strict top-level contents:read boundary, with no job override.
    permissions=[]
    for i,line in enumerate(lines):
        if line=="permissions:":
            vals=[]
            for v in lines[i+1:]:
                if v and not v.startswith(" ") and not v.startswith("#"):break
                if v.startswith("  ") and v.strip():vals.append(v.strip())
            permissions.append(vals)
    if (permissions!=[["contents: read"]] or "    permissions:" in section
        or len(checkout)!=1 or len(python)!=1
        or not install or not lint or not test
        or not checkout[0][1]<python[0][1]<install[0]<lint[0]<test[0]):
        raise ValueError("common quality order or privilege contract missing")
    return {"core_observed":CORE[:],"declared_checkout_ref":checkout[0][0],
            "declared_setup_python_ref":python[0][0],
            "checkout_persist_credentials_false_explicit":hardening,
            "quality_order_confirmed":True,"source_yaml_fully_parsed":False,
            "product_specific_steps_left_unchanged":True}

def git_head(path):
    if path.is_symlink() or not path.is_dir():raise ValueError("unsafe checkout")
    p=subprocess.run(["git","-C",str(path),"rev-parse","HEAD"],
                     capture_output=True,text=True,timeout=8,check=False)
    if p.returncode or not COMMIT.fullmatch(p.stdout.strip()):
        raise ValueError("checkout commit unavailable")
    return p.stdout.strip()

def audit(contract,roots,git_check=git_head):
    if set(roots)!={c["repository"] for c in contract["consumers"]}:
        raise ValueError("consumer checkout mapping incomplete")
    records=[]
    for c in contract["consumers"]:
        base=roots[c["repository"]]
        if git_check(base)!=c["commit"]:
            raise ValueError("source snapshot pin mismatch")
        workflow=base/c["workflow"]
        if workflow.is_symlink() or not workflow.is_file() or workflow.stat().st_size>70000:
            raise ValueError("workflow source unsafe")
        evidence=workflow_extract(workflow.read_text(encoding="utf-8"),c["job"])
        records.append({"repository":c["repository"],"source_commit":c["commit"],
                        "workflow":c["workflow"],"job":c["job"],**evidence})
    refs={(r["declared_checkout_ref"],r["declared_setup_python_ref"]) for r in records}
    return {"schema":SCHEMA,"status":"TWO_CONSUMERS_MATCH_SHARED_STATIC_QUALITY_CHAIN",
            "observed_utc":datetime.now(timezone.utc).isoformat(),
            "contract_version":contract["contract_version"],"consumers":records,
            "declared_action_refs_same":len(refs)==1,
            "shared_quality_stages_per_consumer":len(CORE),
            "product_ci_executed":False,"product_workflow_modified":False,
            "runtime_quality_verified":False,"product_authority_granted":False,
            "organization_standard_approved":False}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--contract",required=True,type=Path)
    p.add_argument("--data-platform",required=True,type=Path)
    p.add_argument("--compliance",required=True,type=Path)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    try:
        result=audit(contract_read(a.contract),{
            "arvectum2/data-platform":a.data_platform,
            "arvectum2/compliance":a.compliance})
        if a.output:
            write_private_output(a.output,json.dumps(result,indent=2,sort_keys=True)+"\n")
    except (ValueError,OSError,KeyError,TypeError,UnicodeDecodeError,subprocess.TimeoutExpired) as exc:
        print("CI_QUALITY_SHADOW_INCOMPLETE",type(exc).__name__,file=sys.stderr)
        return 2
    print(result["status"],"consumers",len(result["consumers"]),
          "quality_stages_each",result["shared_quality_stages_per_consumer"],
          "action_refs_equal",result["declared_action_refs_same"])
    return 0

if __name__=="__main__":raise SystemExit(main())
