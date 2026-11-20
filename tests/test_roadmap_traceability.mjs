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
assert.ok(validate(ledger,ledger,spec,board.replace('[ ] MC-T001','[x] MC-T001')).length);const nested=clone(ledger);nested.tasks.push({id:'MC-T010',milestone:'inventory',parent_task:'MC-T001',requirements:['MC-R001'],depends_on:[],description:'Nested criterion',state:'open',evidence:[]});
const nestedBoard=board+'\n- [ ] MC-T010 nested\n';
assert.deepEqual(validate(nested,ledger,spec,nestedBoard),[],'valid nested task');
const missing=clone(nested);missing.tasks.pop();assert.ok(validate(missing,nested,spec,board).some(x=>x.includes('MC-T010 lost')),'deleted child');
const early=clone(nested);early.tasks[0].state='verified';early.tasks[0].evidence=[{ref:'fixture',criterion:'fixture',version:'v1',outcome:'pass'}];assert.ok(validate(early,nested,spec,nestedBoard.replace('[ ] MC-T001','[x] MC-T001')).some(x=>x.includes('open child')),'parent closure');
const cycle=clone(nested);cycle.tasks[0].parent_task='MC-T010';assert.ok(validate(cycle,nested,spec,nestedBoard).some(x=>x.includes('parent cycle')),'parent cycle');
const moved=clone(nested);moved.tasks[9].parent_task='MC-T002';assert.ok(validate(moved,nested,spec,nestedBoard).some(x=>x.includes('untracked scope/link change')),'silent reparent');
const unlink=clone(ledger);unlink.tasks[0].requirements=['MC-R001'];assert.ok(validate(unlink,ledger,spec,board).some(x=>x.includes('untracked scope/link change')),'silent unlink');
console.log('18 structural cases PASS');
