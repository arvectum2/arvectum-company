#!/usr/bin/env python3
"""Read-only Mac launchd + Docker inventory. Never persists argv or environment."""
import argparse
from datetime import datetime, timezone
import json
import pathlib
import plistlib
import re
import subprocess
import sys
from xml.parsers.expat import ExpatError

PREFIX=("com.arvectum.","ru.arvectum.")
EXT=(".py",".sh",".js",".mjs",".ts",".swift")
PLISTS=(pathlib.Path.home()/"Library/LaunchAgents",pathlib.Path("/Library/LaunchAgents"),pathlib.Path("/Library/LaunchDaemons"))
def call(args, timeout=8):
    try:
        r=subprocess.run(args,capture_output=True,text=True,timeout=timeout)
        return r.stdout if r.returncode==0 else ""
    except (OSError,subprocess.TimeoutExpired):return ""

def checked(args, timeout=8):
    """Distinguish unavailable commands from successful empty results."""
    try:
        r=subprocess.run(args,capture_output=True,text=True,timeout=timeout)
        return r.returncode == 0, r.stdout if r.returncode == 0 else ""
    except (OSError,subprocess.TimeoutExpired):
        return False, ""

def identity(root):
    u=call(["git","-C",str(root),"remote","get-url","origin"]).strip()
    if not u:u=call(["git","-C",str(root),"remote","get-url","gitverse"]).strip()
    m=re.search(r"(?:github\.com|gitverse\.ru)[:/]([^?]+)",u)
    return m.group(1).removesuffix(".git").strip("/") if m else None

def source(path,cache):
    if not path:return None
    t=pathlib.Path(path).expanduser()
    if not t.exists():return None
    t=(t.parent if t.is_file() else t).resolve()
    # Only exact-path cache hits: an ancestor without Git may contain worktrees.
    if t in cache:return cache[t]
    r=call(["git","-C",str(t),"rev-parse","--show-toplevel"]).strip()
    if not r:
        cache[t]=None
        return None
    root=pathlib.Path(r).resolve()
    d={"repository_identity":identity(root),
       "checkout_head":call(["git","-C",str(root),"rev-parse","--short=12","HEAD"]).strip() or None,
       "checkout_path":str(root)}
    cache[t]=d
    return d

def process_cwd(pid):
    """Observed process working directory; not proof of loaded code version."""
    if pid is None:
        return None
    raw=call(["lsof","-a","-p",str(pid),"-d","cwd","-Fn"],timeout=4)
    return next((x[1:] for x in raw.splitlines() if x.startswith("n") and len(x)>1), None)

def release_hint(*paths):
    """A version-like release folder is only a source hint, not a code proof."""
    for path in paths:
        if not path:
            continue
        found=re.search(r"/releases/([0-9a-f]{40})/",path)
        if found:
            return found.group(1)
    return None

def launchd(cache):
    observed={}
    query_ok, launchctl_text=checked(["launchctl","list"],timeout=12)
    for line in launchctl_text.splitlines():
        a=line.split("\t")
        if len(a)==3 and a[2].startswith(PREFIX):
            observed[a[2]]={"pid":int(a[0]) if a[0].isdigit() else None,
                            "last_exit_status":int(a[1]) if re.fullmatch(r"-?\d+",a[1]) else None}
    result={}
    for folder in PLISTS:
        if not folder.is_dir():continue
        for path in sorted(folder.glob("*.plist")):
            try:
                with path.open("rb") as f:d=plistlib.load(f)
            except (OSError,ValueError,TypeError,plistlib.InvalidFileException,ExpatError):continue
            label=d.get("Label")
            if not isinstance(label,str) or not label.startswith(PREFIX):continue
            args=d.get("ProgramArguments") or []
            if not isinstance(args,list):args=[]
            files=[x for x in args if isinstance(x,str) and x.startswith("/") and x.endswith(EXT) and pathlib.Path(x).is_file()]
            prog=d.get("Program") if isinstance(d.get("Program"),str) else None
            if prog and prog.endswith(EXT) and pathlib.Path(prog).is_file():files.insert(0,prog)
            wd=d.get("WorkingDirectory") if isinstance(d.get("WorkingDirectory"),str) else None
            mappings=[(x,source(x,cache)) for x in files+([wd] if wd else [])]
            direct=next(((p,v) for p,v in mappings if v and v["repository_identity"]),None)
            obs=observed.get(label)
            cwd=process_cwd(obs["pid"]) if obs else None
            cwd_repo=source(cwd,cache) if cwd else None
            if not direct and cwd_repo and cwd_repo.get("repository_identity"):
                direct=(cwd,cwd_repo)
            state=("running_pid" if obs and obs["pid"] is not None
                   else "loaded_no_pid" if obs
                   else "installed_not_loaded" if query_ok
                   else "unknown_launchctl")
            result[label]={"label":label,"plist":str(path),"state":state,
              "pid":obs["pid"] if obs else None,"last_exit_status":obs["last_exit_status"] if obs else None,
              "source_file_hint":direct[0] if direct else (files[0] if files else None),
              "working_dir_hint":wd,"repository":direct[1] if direct else None,
              "mapping_proof":("git_root_of_plist_source_or_workdir" if direct and direct[0] in (files+([wd] if wd else []))
                                else "process_cwd_git_root" if direct else "unresolved"),
              "process_cwd_hint":cwd,
              "release_id_hint":release_hint(*(files+([wd] if wd else []))),
              "run_at_load":bool(d.get("RunAtLoad",False)),
              "has_schedule":any(k in d for k in ("StartInterval","StartCalendarInterval")),
              "keep_alive":bool(d.get("KeepAlive",False))}
    for label,obs in observed.items():
        if label not in result:
            result[label]={"label":label,"plist":None,
             "state":"running_pid" if obs["pid"] is not None else "loaded_no_pid",
             "pid":obs["pid"],"last_exit_status":obs["last_exit_status"],
             "repository":None,"mapping_proof":"unresolved"}
    return sorted(result.values(),key=lambda d:d["label"])

def docker(cache):
    result=[]
    query_ok, docker_text=checked(["docker","ps","--format","{{json .}}"],timeout=15)
    if not query_ok:
        return None
    for line in docker_text.splitlines():
        try:d=json.loads(line)
        except (TypeError,json.JSONDecodeError):continue
        ident=d.get("ID")
        labels={}
        if ident:
            try:labels=json.loads(call(["docker","inspect","--format","{{json .Config.Labels}}",ident])) or {}
            except (TypeError,json.JSONDecodeError):pass
        wanted={k:labels.get(k) for k in ("com.docker.compose.project","com.docker.compose.service","com.docker.compose.project.working_dir") if labels.get(k)}
        src=source(wanted.get("com.docker.compose.project.working_dir"),cache)
        result.append({"container_name":d.get("Names"),"container_id_prefix":ident[:12] if ident else None,
            "image_reference":d.get("Image"),"reported_status":d.get("Status"),"compose":wanted,
            "repository":src,"mapping_proof":"git_root_of_compose_workdir" if src else "unresolved"})
    return result

def summarize(la,co):
    from collections import Counter
    c=Counter(x["state"] for x in la)
    return {"launchd_total":len(la),"launchd_running_pid":c["running_pid"],
       "launchd_loaded_no_pid":c["loaded_no_pid"],"launchd_installed_not_loaded":c["installed_not_loaded"],
       "launchd_direct_git_mapping":sum(bool(x.get("repository")) for x in la),
       "launchd_unresolved":sum(not x.get("repository") for x in la),
       "launchd_unknown_query_count":c["unknown_launchctl"],
       "docker_running_count":len(co) if co is not None else None,
       "docker_direct_git_mapping":sum(bool(x.get("repository")) for x in co) if co is not None else None}

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--output",type=pathlib.Path)
    a.add_argument("--hostname",default=call(["hostname"]).strip() or "unknown")
    opt=a.parse_args()
    cache={}
    la=launchd(cache);co=docker(cache)
    data={"schema":"aec001-runtime-inventory-v1","observed_utc":datetime.now(timezone.utc).isoformat(),
          "host":opt.hostname,"health_claim":False,"launchd":la,"docker":co or [],
          "docker_collection_state":"available" if co is not None else "unavailable",
          "summary":summarize(la,co)}
    payload=json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True)+"\n"
    if opt.output:
        opt.output.parent.mkdir(parents=True,exist_ok=True)
        opt.output.write_text(payload,encoding="utf-8")
    else:sys.stdout.write(payload)
    print(json.dumps(data["summary"],ensure_ascii=False),file=sys.stderr)
if __name__=="__main__":main()
