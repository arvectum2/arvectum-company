#!/usr/bin/env python3
"""Read-only Python/JavaScript SDK public-method surface drift checker.

Static method presence is not a runtime contract test or semver approval.
No repository code is executed and no Git remotes are contacted.
"""
import argparse
import ast
import json
from pathlib import Path
import re
import subprocess
import sys
from aec001_private_output import write_private_output
import tarfile

PY_PATH="sdk/python/src/arvectum_data_client/client.py"
JS_PATH="sdk/javascript/client.mjs"
REF=re.compile(r"[A-Za-z0-9_.\-/]{1,120}")
METHOD=re.compile(r"(?m)^  (?:async )?([A-Za-z_][A-Za-z0-9_]*)\(")
BRIDGE={
    "health":"health", "contract":"contract", "require_contract":"requireContract",
    "ensure_collection":"ensureCollection", "collection_exists":"collectionExists",
    "collection_stats":"collectionStats", "process_document":"processDocument",
    "ingest_document":"ingestDocument", "ingest_url":"ingestUrl",
    "write_memory":"writeMemory", "delete_memory":"deleteMemory",
    "search":"search", "search_with_profile":"searchWithProfile",
    "create_connector_credential":"createConnectorCredential",
    "list_connector_credentials":"listConnectorCredentials",
    "rotate_connector_credential":"rotateConnectorCredential",
    "revoke_connector_credential":"revokeConnectorCredential",
    "discover":"discover", "research":"research",
    "resolve_entity":"resolveEntity", "create_entity":"createEntity",
    "create_entity_relation":"createEntityRelation",
}

def git(repo, *args):
    try:
        x=subprocess.run(["git","-C",str(repo),"-c","core.hooksPath=/dev/null",*args],
                         capture_output=True,timeout=12)
        return x.stdout if x.returncode==0 else None
    except (OSError,subprocess.TimeoutExpired):
        return None

def blob(repo, ref, path):
    if not REF.fullmatch(ref) or ref.startswith("-") or ".." in ref:
        return None
    sha=git(repo,"rev-parse","--verify",ref+"^{commit}")
    if not sha:return None
    digest=sha.decode("ascii","replace").strip()
    if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})",digest):return None
    return git(repo,"show",digest+":"+path)

def python_methods(code):
    root=ast.parse(code)
    cls=next((n for n in root.body if isinstance(n,ast.ClassDef) and
              n.name=="DataPlatformClient"),None)
    if cls is None:raise ValueError("DataPlatformClient class absent")
    return {n.name for n in cls.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))
            and not n.name.startswith("_")}

def javascript_methods(code):
    text=code.decode("utf-8")
    if "export class DataPlatformClient" not in text:
        raise ValueError("DataPlatformClient class absent")
    return set(METHOD.findall(text[text.index("export class DataPlatformClient"):]))

def surface(repo,ref):
    py=blob(repo,ref,PY_PATH)
    js=blob(repo,ref,JS_PATH)
    if not py or not js:return None
    a,b=python_methods(py),javascript_methods(js)
    bridge=[name for name,jname in BRIDGE.items() if name in a and jname in b]
    gaps_py=[name for name,jname in BRIDGE.items() if name in a and jname not in b]
    gaps_js=[name for name,jname in BRIDGE.items() if name not in a and jname in b]
    return {"python":a,"javascript":b,"bridged":bridge,"unpaired_python":gaps_py,
            "unpaired_javascript":gaps_js,"js_source":js}

def packaged_archive(path):
    try:
        with tarfile.open(path,"r:gz") as t:
            member=t.getmember("package/sdk/javascript/client.mjs")
            metadata=t.getmember("package/package.json")
            if member.size>1_000_000 or metadata.size>100_000:return None
            code=t.extractfile(member).read()
            meta=json.loads(t.extractfile(metadata).read())
            return code, {"name":meta.get("name"),"version":meta.get("version")}
    except (OSError,ValueError,KeyError,tarfile.TarError,json.JSONDecodeError):
        return None

def audit(repo, baseline, candidate, archive=None):
    prev=surface(repo,baseline)
    cur=surface(repo,candidate)
    if prev is None or cur is None:
        return {"status":"UNKNOWN_SOURCE_UNAVAILABLE"}
    summary={
      "status":"STATIC_SURFACE_REVIEW",
      "baseline_ref":baseline, "candidate_ref":candidate,
      "baseline_python_methods":len(prev["python"]),
      "candidate_python_methods":len(cur["python"]),
      "baseline_javascript_methods":len(prev["javascript"]),
      "candidate_javascript_methods":len(cur["javascript"]),
      "python_added":sorted(cur["python"]-prev["python"]),
      "python_removed":sorted(prev["python"]-cur["python"]),
      "javascript_added":sorted(cur["javascript"]-prev["javascript"]),
      "javascript_removed":sorted(prev["javascript"]-cur["javascript"]),
      "candidate_declared_bridge_covered":len(cur["bridged"]),
      "candidate_python_only_bridge":cur["unpaired_python"],
      "candidate_javascript_only_bridge":cur["unpaired_javascript"],
      "semantics_and_runtime_contract_verified":False,
    }
    if archive:
        packed=packaged_archive(archive)
        summary["packaged_js"] = (
            {"status":"UNKNOWN_ARCHIVE"} if packed is None else
            {"status":"MATCHES_BASELINE_TAG" if packed[0]==prev["js_source"] else
             "DIFFERS_FROM_BASELINE_TAG",
             **packed[1]}
        )
    return summary

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repository",type=Path,required=True)
    p.add_argument("--baseline-ref",required=True)
    p.add_argument("--candidate-ref",required=True)
    p.add_argument("--package-archive",type=Path)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    result=audit(a.repository,a.baseline_ref,a.candidate_ref,a.package_archive)
    data={"schema":"aec001-sdk-static-surface-v1","result":result}
    payload=json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True)+"\n"
    if a.output:
        try:
            write_private_output(a.output,payload)
        except (OSError,ValueError,TypeError) as exc:
            print("SDK_SURFACE_OUTPUT_REJECTED",type(exc).__name__,file=sys.stderr)
            return 2
    else:sys.stdout.write(payload)
    print(result["status"],file=sys.stderr)
    return 0
if __name__=="__main__":sys.exit(main())
