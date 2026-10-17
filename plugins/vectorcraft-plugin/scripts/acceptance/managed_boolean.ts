import { mkdirSync,readFileSync,writeFileSync,cpSync } from 'node:fs';
import { join,resolve } from 'node:path';
import { createHash } from 'node:crypto';
import assert from 'node:assert/strict';
import { Controller,skillDigest } from '../../src/harness/controller.ts';

/** 真实受控结构修改；精确绑定 supplied skill，候选与固定快照身份分别登记。 */
const [newRoot,skillPath,runtimePath,python]=process.argv.slice(2);
if(!newRoot||!skillPath||!runtimePath||!python)throw new Error('usage: managed_boolean.ts NEW_ROOT SKILL RUNTIME PYTHON');
const root=resolve(newRoot),skill=resolve(skillPath),runtimeHome=resolve(runtimePath);mkdirSync(root);
const sha=(v:string|Buffer)=>createHash('sha256').update(v).digest('hex');
const dependencies=['skills.lock.json','scripts/acceptance/managed_boolean.ts','src/harness/controller.ts','src/harness/ledger.ts','src/harness/process_registry.ts','src/harness/process_runner.py','src/planning/geometry.ts','src/strict_json.ts'];
const fingerprints=Object.fromEntries(dependencies.map(p=>[p,sha(readFileSync(p))]));
const expectedSkillSha256=skillDigest(skill),read=(p:string)=>JSON.parse(readFileSync(p,'utf8'));
const lock=read('skills.lock.json').sources[0],pinnedSkill=expectedSkillSha256===lock.sha256[skill.split('/').at(-1)!];
const cases:any[]=[];
async function execute(work:string,name:string,plan:any,source?:string,objects:number[]=[],fields:string[]=[]){
  const path=join(work,name+'.json');writeFileSync(path,JSON.stringify(plan));
  const controller=new Controller(join(work,name+'.sqlite'));
  const request={key:name,skill,expectedSkillSha256,plan:path,source,output:join(work,name),runtimeHome,python,estimatedBytes:16*1024*1024,
    authorization:{objects,fields,deadline:Date.now()+60000,maxAttempts:2,maxBytes:64*1024*1024,readRoots:[root],writeRoots:[root,runtimeHome]}};
  return {controller,request};
}
const work=join(root,'positive');mkdirSync(work);
const initial=await execute(work,'source',{document:{width:128,height:128,units:'Points'},operations:[
  {command:'shape.rectangle',params:{x:10,y:10,width:70,height:70},as:'outer'},
  {command:'shape.rectangle',params:{x:30,y:30,width:30,height:30},as:'inner'},
  {command:'shape.ellipse',params:{x:100,y:10,width:10,height:10},as:'sentinel'}]});
try{assert.equal((await initial.controller.run(initial.request)).state,'review_ready');}finally{initial.controller.close();}
const source=initial.request.output,sourceManifest=read(join(source,'manifest.json'));
const sourceHashes=Object.fromEntries(Object.keys(sourceManifest.files).map(p=>[p,sha(readFileSync(join(source,p)))]));
const ids=['outer','inner'].map(name=>sourceManifest.bindings[name].id);
for(const route of ['direct','gateway']){
  for(const command of ['object.pathfinder.unite','object.group']){
    const name=route+'-'+command.split('.').at(-1);
    const operation=route==='direct'?{command,as:'result'}:{command:'native.command',params:{command,params:{}},as:'result'};
    const run=await execute(work,name,{expectedProjectSha256:sourceManifest.files['project.vectorcraft'],operations:[{command:'select.set',params:{ids}},operation]},source,ids,['structure']);
    try{
      const task=await run.controller.run(run.request);assert.equal(task.state,'review_ready');
      assert.equal((await run.controller.run(run.request)).id,task.id);
      const report=read(join(run.request.output,'boolean-transactions.json')),record=report.operations[0];assert.equal(record.status,'verified');assert.deepEqual(record.participantIds,ids);
      const manifest=read(join(run.request.output,'manifest.json'));assert.equal(manifest.files[record.checkpoint],sha(readFileSync(join(run.request.output,record.checkpoint))));
      const events=readFileSync(join(run.controller.snapshotRoot,task.id+'-events.jsonl'),'utf8').trim().split('\n').map(JSON.parse);
      assert.ok(events.some(e=>e.event==='revision_verified'&&e.command===command&&JSON.stringify(e.fields)==='["structure"]'));
      cases.push({name,participantIds:ids,resultIds:record.resultIds,state:task.state,sameKeyStable:true,checkpointSha256:record.checkpointSha256,projectRevision:manifest.files['project.vectorcraft']});
      if(command==='object.group'){
        const groupId=manifest.bindings.result.id;
        const ungroup=await execute(work,route+'-ungroup',{expectedProjectSha256:manifest.files['project.vectorcraft'],operations:[
          {command:'select.set',params:{ids:[groupId]}},{command:'native.command',params:{command:'object.ungroup',params:{}}}]},run.request.output,[groupId,...ids],['structure']);
        try{assert.equal((await ungroup.controller.run(ungroup.request)).state,'review_ready');
          const r=read(join(ungroup.request.output,'boolean-transactions.json')).operations[0];assert.equal(r.status,'verified');assert.deepEqual(new Set(r.resultIds),new Set(ids));
          cases.push({name:route+'-ungroup',participantIds:[groupId],resultIds:r.resultIds,state:'review_ready'});
        }finally{ungroup.controller.close();}
      }
    }finally{run.controller.close();}
  }
}
for(const name of ['kind-is-not-structure','missing-operand-authorization']){
  const isolated=join(root,name);mkdirSync(isolated);const localSource=join(isolated,'original');cpSync(source,localSource,{recursive:true});
  const run=await execute(isolated,'refused',{expectedProjectSha256:sourceManifest.files['project.vectorcraft'],operations:[
    {command:'select.set',params:{ids}},{command:'object.pathfinder.unite'}]},localSource,name==='kind-is-not-structure'?ids:[ids[0]],name==='kind-is-not-structure'?['kind']:['structure']);
  try{
    await assert.rejects(()=>run.controller.run(run.request),/revision_outside_authorization/);
    const row=run.controller.ledger.db.prepare('SELECT id FROM tasks WHERE key=?').get('refused') as any;
    const task=run.controller.ledger.get(row.id);assert.equal(task.state,'reconciling');assert.equal(run.controller.processes.observe(task.id,task.epoch).stopped,true);
    const events=readFileSync(join(run.controller.snapshotRoot,task.id+'-events.jsonl'),'utf8').trim().split('\n').map(JSON.parse);
    assert.ok(!events.some(e=>e.event==='submitted'&&['select.set','object.pathfinder.unite'].includes(e.params?.arguments?.command)));
    assert.equal(sha(readFileSync(join(localSource,'project.vectorcraft'))),sourceManifest.files['project.vectorcraft']);
    assert.equal((await run.controller.run(run.request)).state,'reconciling');
    cases.push({name,state:'reconciling',mutationNotSubmitted:true,sourcePreserved:true,automaticReplayRefused:true,ownedProcessStopped:true});
  }finally{run.controller.close();}
}
assert.deepEqual(sourceHashes,Object.fromEntries(Object.keys(sourceHashes).map(p=>[p,sha(readFileSync(join(source,p)))])));
assert.equal(skillDigest(skill),expectedSkillSha256);assert.deepEqual(fingerprints,Object.fromEntries(dependencies.map(p=>[p,sha(readFileSync(p))])));
const proof={schema:'vectorcraft-managed-boolean/v1',result:'PASS',level:'native-candidate',platform:process.platform+'-'+process.arch,pinnedSkill,
  skillSha256:expectedSkillSha256,runtimeIdentity:read(join(skill,'scripts/runtime.lock.json')).artifacts['darwin-arm64'].binarySha256,cases,fingerprints,
  scope:'real managed group/ungroup/unite via direct and gateway routes; structural scope rejection before mutation, durable receipts and replay refusal; full4.6, GUI and creative acceptance remain open'};
writeFileSync(join(root,'proof.json'),JSON.stringify(proof,null,2)+'\n');console.log(JSON.stringify({result:'PASS',cases:cases.length,pinnedSkill}));
