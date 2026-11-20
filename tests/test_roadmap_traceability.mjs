import assert from 'node:assert/strict';
import fs from 'node:fs';
import {validate} from '../tools/roadmap_traceability.mjs';
const dir='specs/001-mission-control-roadmap-traceability';const ledger=JSON.parse(fs.readFileSync(dir+'/traceability.json','utf8'));const spec=fs.readFileSync(dir+'/spec.md','utf8');const board=fs.readFileSync(dir+'/tasks.md','utf8');const clone=x=>JSON.parse(JSON.stringify(x));
const cases=[["valid",x=>{},false],
["lost task",x=>x.tasks.pop(),true],
["lost req",x=>x.requirements.pop(),true],
["orphan",x=>x.tasks[0].requirements=[],true],
["duplicate",x=>x.tasks.push(clone(x.tasks[0])),true],
["bad dependency",x=>x.tasks[0].depends_on=["MISSING"],true],
["cycle",x=>x.tasks[0].depends_on=["MC-T009"],true],
["false complete",x=>x.tasks[0].state="verified",true],
["cancellation",x=>x.tasks[0].state="cancelled",true],
["rewrite",x=>x.tasks[0].description="changed",true],
["false req",x=>x.requirements[0].state="verified",true]];
for(const[n,f,b]of cases){const x=clone(ledger);f(x);assert.equal(Boolean(validate(x,ledger,spec,board).length),b,n);}
assert.ok(validate(ledger,ledger,spec,board.replace('[ ] MC-T001','[x] MC-T001')).length);console.log('12 structural cases PASS');
