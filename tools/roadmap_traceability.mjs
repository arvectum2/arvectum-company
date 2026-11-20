// Candidate structural gate; not evidence authentication.
import fs from 'node:fs';
import {pathToFileURL} from 'node:url';
export function validate(cur,prior,spec,board){
 const e=[],bad=s=>e.push(s),filled=x=>typeof x==="string"&&x.trim().length>0,arr=x=>Array.isArray(x)?x:[];
 const terminal=new Set(["verified","cancelled","superseded"]),states=new Set(["open","in_progress","implemented","blocked","waiting_external","deferred",...terminal]);
 const index=(xs,kind)=>{const m=new Map();for(const x of arr(xs)){if(!x||!filled(x.id)||m.has(x.id)){bad(kind+" missing/duplicate ID");continue;}m.set(x.id,x);}if(!m.size)bad(kind+" empty");return m;};
 if(cur?.schema!=="arvectum.company.roadmap-traceability-candidate/1"||prior?.schema!==cur?.schema)bad("schema/baseline");
 const r=index(cur?.requirements,"requirements"),t=index(cur?.tasks,"tasks"),milestones=new Set(arr(cur?.milestones)),coverage=new Set();
 const admissible=x=>!["cancelled","superseded"].includes(x.state);
 const proof=x=>Array.isArray(x.evidence)&&x.evidence.length>0&&x.evidence.every(z=>filled(z?.ref)&&filled(z?.criterion)&&filled(z?.version)&&z?.outcome==="pass");
 for(const [id,x] of r){if(!filled(x.source)||!filled(x.description)||!states.has(x.state))bad(id+" metadata");}
 for(const [id,x] of t){
  if(!filled(x.description)||!milestones.has(x.milestone)||!states.has(x.state))bad(id+" metadata");
  if(!Array.isArray(x.requirements)||!x.requirements.length)bad(id+" orphan");
  for(const q of arr(x.requirements)){if(!r.has(q))bad(id+" unknown requirement "+q);else if(admissible(x))coverage.add(q);}
  if(!Array.isArray(x.depends_on)||new Set(arr(x.depends_on)).size!==arr(x.depends_on).length)bad(id+" invalid dependencies");
  for(const d of arr(x.depends_on)){if(!t.has(d)||d===id)bad(id+" invalid dependency "+d);if(x.state==="verified"&&t.get(d)?.state!=="verified")bad(id+" dependency unverified");}
  if(x.parent_task!=null&&(!filled(x.parent_task)||x.parent_task===id||!t.has(x.parent_task)))bad(id+" invalid parent task");
  if(x.parent_task!=null&&t.has(x.parent_task)&&t.get(x.parent_task).milestone!==x.milestone)bad(id+" parent milestone mismatch");
  if(x.state==="verified"&&[...t.values()].some(child=>child.parent_task===id&&admissible(child)&&child.state!=="verified"))bad(id+" open child task");
  if(x.state==="verified"&&!proof(x))bad(id+" no pinned PASS evidence");
 }
 for(const [id,x] of r){if(admissible(x)&&!coverage.has(id))bad(id+" uncovered");if(x.state==="verified"&&(!proof(x)||[...t.values()].some(z=>admissible(z)&&arr(z.requirements).includes(id)&&z.state!=="verified")))bad(id+" unverified requirement");}
 for(const [m,old] of [[r,prior?.requirements],[t,prior?.tasks]]){
  for(const [id,x] of m){
   if(!admissible(x)&&(!filled(x.disposition_reason)||!filled(x.decision_ref)))bad(id+" disposition lacks decision");
   if(x.state==="superseded"){let z=x,seen=new Set([id]);while(z?.state==="superseded"){if(!filled(z.successor)||!m.has(z.successor)||seen.has(z.successor)){bad(id+" invalid successor");break;}seen.add(z.successor);z=m.get(z.successor);}}
  }
  for(const [id,x] of index(old,"baseline")){const n=m.get(id);if(!n){bad(id+" lost");continue;}const norm=v=>Array.isArray(v)?[...v].sort().join("\u0000"):String(v??"");if((x.description!==n.description||["source","milestone","parent_task","requirements","depends_on"].some(k=>norm(x[k])!==norm(n[k])))&&(!filled(n.change_ref)||!filled(n.change_reason)))bad(id+" untracked scope/link change");if(terminal.has(x.state)&&!terminal.has(n.state)&&(!filled(n.reopen_ref)||!filled(n.reopen_reason)))bad(id+" untracked reopen");}
 }
 for(const [id,x] of t){const seen=new Set([id]);let p=x.parent_task;while(p!=null&&t.has(p)){if(seen.has(p)){bad(id+" parent cycle");break;}seen.add(p);p=t.get(p).parent_task;}}
 const done=new Set(),active=new Set();function visit(id){if(active.has(id)){bad(id+" dependency cycle");return;}if(done.has(id)||!t.has(id))return;active.add(id);for(const d of arr(t.get(id).depends_on))visit(d);active.delete(id);done.add(id);}for(const id of t.keys())visit(id);
 const ids=[...spec.matchAll(/^- (MC-R\d+)\b/gm)].map(m=>m[1]);if(ids.length!==r.size||new Set(ids).size!==ids.length||ids.some(i=>!r.has(i)))bad("spec/ledger mismatch");
 const rows=[...board.matchAll(/^- \[([ xX])\] (MC-T\d+)\b/gm)];if(rows.length!==t.size||new Set(rows.map(m=>m[2])).size!==rows.length||rows.some(m=>!t.has(m[2])||(m[1].toLowerCase()==="x")!==(t.get(m[2]).state==="verified")))bad("task board mismatch");
 return e;
}
if(process.argv[1] && import.meta.url===pathToFileURL(process.argv[1]).href){const [current,baseline,spec,board]=process.argv.slice(2);if(!current||!baseline||!spec||!board){console.error('Usage: node tools/roadmap_traceability.mjs CURRENT BASELINE SPEC TASKS');process.exit(2);}const read=p=>fs.readFileSync(p,'utf8');const errors=validate(JSON.parse(read(current)),JSON.parse(read(baseline)),read(spec),read(board));if(errors.length){console.error(errors.join('\n'));process.exit(1);}console.log('Structural PASS only; source completeness and actual acceptance not established.');}
