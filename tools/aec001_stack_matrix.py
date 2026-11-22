#!/usr/bin/env python3
"""Read-only inventory of DECLARED repository technology; no code execution.

Manifest presence != deployed stack. Output contains only named technologies,
relative paths, safe version labels, and source revisions. No env or secrets.
"""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys
import tomllib

TECH = {
 "fastapi":"FastAPI", "flask":"Flask", "django":"Django",
 "uvicorn":"Uvicorn", "sqlalchemy":"SQLAlchemy", "alembic":"Alembic",
 "psycopg":"Psycopg", "asyncpg":"Asyncpg", "redis":"Redis client",
 "celery":"Celery", "httpx":"HTTPX", "pydantic-settings":"Pydantic Settings",
 "openai":"OpenAI SDK", "langchain":"LangChain",
 "sentence-transformers":"Sentence Transformers", "llama-cpp-python":"llama.cpp",
 "arvectum-data-client":"Data Platform HTTP SDK",
 "arvectum-data":"Data Platform in-process library",
 "@arvectum/data-platform-client":"Data Platform JS HTTP SDK",
 "pytest":"pytest", "ruff":"Ruff", "playwright":"Playwright",
 "next":"Next.js", "react":"React", "vite":"Vite",
 "typescript":"TypeScript", "tailwindcss":"Tailwind CSS",
 "laravel/framework":"Laravel", "moonshine/moonshine":"MoonShine CMS",
 "phpunit/phpunit":"PHPUnit", "prisma":"Prisma", "express":"Express",
}
LANG = {".py":"Python",".swift":"Swift",".kt":"Kotlin",".ts":"TypeScript",
 ".tsx":"TSX",".js":"JavaScript",".jsx":"JSX",".php":"PHP",
 ".go":"Go",".rs":"Rust",".sh":"Shell",".ps1":"PowerShell"}
MANIFESTS=("pyproject.toml","requirements.txt","package.json","composer.json")
LOCKS=("uv.lock","poetry.lock","pdm.lock","requirements.lock",
       "package-lock.json","pnpm-lock.yaml","yarn.lock","composer.lock",
       "Cargo.lock","Package.resolved","Gemfile.lock")
BUILDS=("Package.swift","build.gradle.kts","build.gradle","Cargo.toml","go.mod",
        "Dockerfile","docker-compose.yml","compose.yml","compose.yaml","Makefile")
SKIP={"node_modules",".venv","venv","vendor",".git","dist","build",
      "DerivedData",".next","target","Pods","__pycache__",".local_archive"}
EXCLUDED_PREFIXES=("data/release/","archive/","archives/","tests/fixtures/")
def git(root,*args):
 try:
  p=subprocess.run(["git","-C",str(root),*args],capture_output=True,timeout=12)
  return p.stdout if p.returncode==0 else None
 except (OSError,subprocess.TimeoutExpired):return None

def identity(root):
 for remote in ("origin","gitverse"):
  url=git(root,"remote","get-url",remote)
  if not url:continue
  m=re.search(rb"(?:github\.com|gitverse\.ru)[:/]([^?#\s]+)",url)
  if m:
   return m.group(1).decode("utf-8","replace").removesuffix(".git").strip("/")
 return "local:"+root.name

def choose(roots):
 selected={}
 for root in roots:
  if not root.is_dir():continue
  for p in sorted(root.iterdir()):
   if not p.is_dir() or not (p/".git").exists():continue
   name=identity(p)
   if name not in selected:selected[name]=p
 return dict(sorted(selected.items()))

def normalize_req(item):
 if not isinstance(item,str):return None
 match=re.match(r"\s*([A-Za-z0-9_.-]+)",item)
 return match.group(1).lower().replace("_","-") if match else None

def manifest_deps(path):
 try:
  if path.name=="pyproject.toml":
   doc=tomllib.loads(path.read_text(encoding="utf-8"))
   pr=doc.get("project",{})
   direct=list(pr.get("dependencies",[]))
   optional=[v for group in pr.get("optional-dependencies",{}).values() for v in group]
   direct.extend(str(name) for name in doc.get("tool",{}).get("poetry",{}).get("dependencies",{}))
   all_deps=direct+optional
   opt=sorted(set(filter(None,(normalize_req(v) for v in optional))))
   return sorted(set(filter(None,(normalize_req(v) for v in all_deps)))),str(pr.get("requires-python") or ""),opt,None
  if path.name=="requirements.txt":
   lines=path.read_text(encoding="utf-8").splitlines()
   deps=[normalize_req(v) for v in lines if v.strip() and not v.lstrip().startswith(("#","-",".","git+"))]
   return sorted(set(filter(None,deps))),"",[],None
  doc=json.loads(path.read_text(encoding="utf-8"))
  groups=("dependencies","devDependencies","optionalDependencies","require","require-dev")
  deps={name.lower() for group in groups for name in doc.get(group,{})}
  opt={name.lower() for group in ("optionalDependencies","devDependencies","require-dev")
       for name in doc.get(group,{})}
  return sorted(deps),"",sorted(opt),None
 except (OSError,ValueError,TypeError,KeyError,UnicodeDecodeError) as exc:
  return [],"",[],type(exc).__name__

def safe_version(value):
    """Only keep non-secret version constraints. Never record URLs or tokens."""
    if not isinstance(value,str):
        return "unknown"
    if "git+" in value or "github.com" in value or "gitverse.ru" in value:
        return "direct Git reference (URL redacted)"
    if "://" in value or value.startswith(("file:","git@")):
        return "direct artifact/path (redacted)"
    match=re.search(r"(?:(?:>=|<=|==|!=|~=|>|<|\^|~)[0-9][A-Za-z0-9.,_*+<>=~^ -]*)",value)
    if match:
        return match.group(0).strip()[:80]
    if re.fullmatch(r"[A-Za-z0-9.*+\-^~<>=, ]{1,80}",value.strip()):
        return value.strip()
    return "unspecified/complex"

def version_specs(path):
    """Version constraints for allowlisted tech only; never raw source URLs."""
    try:
        if path.name=="pyproject.toml":
            d=tomllib.loads(path.read_text(encoding="utf-8"))
            direct=list(d.get("project",{}).get("dependencies",[]))
            direct.extend(v for group in d.get("project",{}).get("optional-dependencies",{}).values() for v in group)
            ans={}
            for item in direct:
                key=normalize_req(item)
                if key in TECH:
                    marker=re.sub(r"^\s*[A-Za-z0-9_.-]+(?:\[[^]]+\])?", "",item).strip()
                    ans[key]=safe_version(marker)
            return ans
        if path.name=="requirements.txt":
            lines=path.read_text(encoding="utf-8").splitlines()
            return {key:safe_version(re.sub(r"^\s*[A-Za-z0-9_.-]+(?:\[[^]]+\])?", "",line).strip())
                    for line in lines if (key:=normalize_req(line)) in TECH}
        d=json.loads(path.read_text(encoding="utf-8"))
        out={}
        for group in ("dependencies","devDependencies","optionalDependencies","require","require-dev"):
            for name,version in d.get(group,{}).items():
                if name.lower() in TECH:out[name.lower()]=safe_version(version)
        return out
    except (OSError,ValueError,TypeError,UnicodeDecodeError):
        return {}

def inspect(root,repo_id):
 raw=git(root,"ls-files","-z") or b""
 files=[s.decode("utf-8","replace") for s in raw.split(b"\0") if s]
 filtered=[s for s in files if not any(part in SKIP for part in Path(s).parts)
           and not s.startswith(EXCLUDED_PREFIXES)]
 langs=Counter(LANG[Path(s).suffix.lower()] for s in filtered if Path(s).suffix.lower() in LANG)
 manifests=[];deps=defaultdict(set);py_versions=set();optional=set();parse_errors=[]
 versions=defaultdict(set);workflow_actions=defaultdict(set)
 builds=[];locks=[];workflow_count=0
 for rel in filtered:
  p=Path(rel)
  if rel.startswith(".github/workflows/") and p.suffix.lower() in (".yml",".yaml"):
   workflow_count+=1
   try:
    workflow=(root/rel).read_text(encoding="utf-8")
    for action,version in re.findall(r"(?m)^\s*(?:-\s*)?uses:\s*(actions/[A-Za-z0-9_.-]+)@([A-Za-z0-9_.-]+)",workflow):
     workflow_actions[action].add(version)
   except (OSError,UnicodeDecodeError):pass
  if p.name in LOCKS and len(p.parts)<=6:locks.append(rel)
  if (p.name in BUILDS or p.suffix.lower() in (".xcodeproj",".xcworkspace")) and len(p.parts)<=6:builds.append(rel)
  for part in p.parts:
   if part.endswith((".xcodeproj",".xcworkspace")):
    builds.append("/".join(p.parts[:p.parts.index(part)+1]))
  if p.name in MANIFESTS and len(p.parts)<=6:
   manifests.append(rel)
   entries,py,opt,error=manifest_deps(root/p)
   if py:py_versions.add(py)
   if error:parse_errors.append({"relative_path":rel,"failure_type":error})
   optional.update(opt)
   for dep in entries:deps[dep].add(rel)
   for dep,version in version_specs(root/p).items():versions[dep].add(version)
 technologies=[{"name":TECH[k],"package":k,"manifest_paths":sorted(paths)[:8],
                "declared_versions":sorted(versions.get(k,()))}
               for k,paths in sorted(deps.items()) if k in TECH]
 return {"repository":repo_id,"checkout":root.name,
         "source_head":(git(root,"rev-parse","--short=12","HEAD") or b"").decode().strip(),
         "source_branch":(git(root,"branch","--show-current") or b"").decode().strip(),
         "tracked_files":len(files),"language_files":dict(sorted(langs.items())),
         "python_requires":sorted(py_versions),"manifest_paths":sorted(manifests),
         "build_paths":sorted(set(builds))[:40],"lock_paths":sorted(locks)[:40],
         "ci_workflow_count":workflow_count,
         "common_github_action_refs":{k:sorted(v) for k,v in sorted(workflow_actions.items())},
         "technologies":technologies,
         "optional_or_dev_dependency_names":sorted(optional),
         "manifest_parse_failures":parse_errors,
         "dependency_names":sorted(deps)}

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--root",type=Path,action="append",required=True)
 p.add_argument("--output",type=Path)
 args=p.parse_args()
 repos=[inspect(path,name) for name,path in choose(args.root).items()]
 shared=defaultdict(list)
 for record in repos:
  for dep in record["dependency_names"]:shared[dep].append(record["repository"])
 action_refs=defaultdict(lambda:defaultdict(set))
 for record in repos:
  for action,versions in record["common_github_action_refs"].items():
   for ref in versions:action_refs[action][ref].add(record["repository"])
 action_drift=[{"action":name,
                "reference_versions":sorted(refs),
                "consumer_repo_count":len({r for rs in refs.values() for r in rs})}
               for name,refs in sorted(action_refs.items())
               if len(refs)>1 and len({r for rs in refs.values() for r in rs})>=2]
 result={"schema":"aec001-stack-matrix-v1",
  "observed_utc":datetime.now(timezone.utc).isoformat(),
  "scope":"declared_manifests_and_tracked_files_only",
  "repo_count":len(repos),
  "ci_action_version_drift":action_drift,
  "shared_dependency_names":[{"package":k,"display":TECH.get(k,k),"consumers":v}
      for k,v in sorted(shared.items()) if len(v)>=2 and k in TECH],
  "repositories":repos,
  "no_runtime_claim":True,"no_semantic_duplication_claim":True}
 body=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
 if args.output:
  args.output.parent.mkdir(parents=True,exist_ok=True)
  args.output.write_text(body,encoding="utf-8")
 else:sys.stdout.write(body)
 print("repositories="+str(len(repos))+" shared_technology_names="+str(len(result["shared_dependency_names"])),file=sys.stderr)
if __name__=="__main__":main()
