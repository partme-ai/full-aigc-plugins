import { mkdirSync,readFileSync,writeFileSync } from 'node:fs';
import { join,resolve } from 'node:path';
import { createHash } from 'node:crypto';
import assert from 'node:assert/strict';
import { Controller,skillDigest } from '../../src/harness/controller.ts';
import type { GeometryContract } from '../../src/planning/geometry.ts';

/** 真实原生控制点与坐标验收候选；不据此关闭完整4.3或视觉验收。 */
const [newRoot,skillPath,runtimePath,python]=process.argv.slice(2);
if(!newRoot||!skillPath||!runtimePath||!python)throw new Error('usage: geometry.ts NEW_ROOT PINNED_SKILL WARM_RUNTIME PYTHON');
const root=resolve(newRoot),skill=resolve(skillPath),runtimeHome=resolve(runtimePath);mkdirSync(root);
const sha=(v:string|Buffer)=>createHash('sha256').update(v).digest('hex');
const dependencies=['skills.lock.json','src/planning/geometry.ts','src/harness/controller.ts','src/harness/ledger.ts','src/harness/process_registry.ts','src/harness/process_runner.py','src/strict_json.ts','tests/geometry.test.ts','scripts/acceptance/geometry.ts'];
const fingerprints=Object.fromEntries(dependencies.map(p=>[p,sha(readFileSync(p))]));
const source=jsonParse('skills.lock.json').sources[0],expectedSkillSha256=source.sha256['vectorcraft-use'];assert.equal(skillDigest(skill),expectedSkillSha256);
function jsonParse(path:string){return JSON.parse(readFileSync(path,'utf8'));}
const cases:any[]=[];
for(const name of ['Pixels','Points','closed-mismatch']){
  const work=join(root,name);mkdirSync(work);const units=name==='Points'?'Points':'Pixels';
  const plan={document:{name:'Native geometry proof',width:200,height:120,units},operations:[
    {command:'artboard.new',params:{x:300,y:40,width:200,height:120,name:'Offset'}},
    {command:'path.create',params:{anchors:[{x:320,y:60,out:[340,60]},{x:450,y:60,in:[430,60]},{x:450,y:130}],closed:true},as:'curve'},
    {command:'paint.setStroke',params:{ids:[{$ref:'curve.id'}],none:true}}
  ],exports:[{format:'svg',artboard:1},{format:'png',artboard:1},{format:'pdf',artboard:1}]};
  const path=join(work,'plan.json');writeFileSync(path,JSON.stringify(plan));
  const geometryContract:GeometryContract={schema:'vectorcraft-geometry-contract/v1',units,coordinateSpace:'artboard-local',tolerance:0.000001,
    artboards:[{id:2,rect:[300,40,500,160]}],paths:[{binding:'curve.id',artboardId:2,subpaths:[{closed:name!=='closed-mismatch',anchors:[{p:[20,20],out:[40,20]},{p:[150,20],in:[130,20]},{p:[150,90]}]}],strokes:[{width:1,paint:{type:'none'}}]}]};
  const controller=new Controller(join(work,'state.sqlite')),output=join(work,'delivery');
  const request={key:name,skill,expectedSkillSha256,plan:path,output,runtimeHome,python,estimatedBytes:8*1024*1024,geometryContract,
    authorization:{objects:[],fields:[],deadline:Date.now()+30000,maxAttempts:2,maxBytes:32*1024*1024,readRoots:[work],writeRoots:[work,runtimeHome]}};
  try{
    if(name==='closed-mismatch'){
      await assert.rejects(()=>controller.run(request),/geometry_acceptance_failed/);
      const row=controller.ledger.db.prepare('SELECT id,reason FROM tasks WHERE key=?').get(name) as any,task=controller.ledger.get(row.id);
      assert.equal(task.state,'reconciling');assert.match(row.reason,/path_closed_mismatch/);assert.equal(controller.processes.observe(row.id,1).stopped,true);
      const originalSha=sha(readFileSync(join(output,'project.vectorcraft')));const repeated=await controller.run(request);
      assert.equal(repeated.id,row.id);assert.equal(repeated.state,'reconciling');assert.equal(sha(readFileSync(join(output,'project.vectorcraft'))),originalSha);
      const manifest=jsonParse(join(output,'manifest.json'));assert.ok(Number.isSafeInteger(manifest.bindings.curve.id));
      cases.push({name,expectedFailure:'path_closed_mismatch',objectId:manifest.bindings.curve.id,projectRevision:originalSha,originalStageRetained:true,replayRefused:true,ownedProcessStopped:true});
    }else{
      const task=await controller.run(request);assert.equal(task.state,'review_ready');assert.equal(task.geometryVerification.status,'PASS');
      const repeated=await controller.run(request);assert.equal(repeated.id,task.id);assert.deepEqual(repeated.geometryVerification,task.geometryVerification);
      await assert.rejects(()=>controller.run({...request,geometryContract:{...geometryContract,tolerance:0}}),/idempotency_conflict/);
      const receipt=controller.ledger.db.prepare('SELECT result FROM steps WHERE task=? AND n=0').get(task.id) as any;
      assert.deepEqual(JSON.parse(receipt.result).geometryVerification,task.geometryVerification);
      for(const wrong of [{...geometryContract,units:units==='Pixels'?'Points':'Pixels'},
        {...geometryContract,paths:[{...geometryContract.paths[0],subpaths:[{...geometryContract.paths[0].subpaths[0],closed:false}]}]}] as GeometryContract[]){
        assert.throws(()=>controller.verifyDelivery(output,task.binding.runtimeIdentity,wrong),/geometry_acceptance_failed/);
      }
      cases.push({name,report:task.geometryVerification,geometryReceiptPersisted:true,sameKeyStable:true,changedContractRejected:true,wrongUnitAndClosureRejected:true});
    }
  }finally{controller.close();}
}
assert.deepEqual(Object.fromEntries(dependencies.map(p=>[p,sha(readFileSync(p))])),fingerprints,'source changed during native acceptance');assert.equal(skillDigest(skill),expectedSkillSha256);
const proof={schema:'vectorcraft-geometry-candidate/v1',result:'PASS',level:'native-candidate',platform:process.platform+'-'+process.arch,sourceRef:source.ref,sourceCommit:source.sha,skillSha256:expectedSkillSha256,cases,fingerprints,
  scope:'two real native document units, offset artboard, explicit controls/stroke and a retained real closure failure; full4.3, arbitrary transforms and visual acceptance remain open'};
writeFileSync(join(root,'proof.json'),JSON.stringify(proof,null,2)+'\n');console.log(JSON.stringify({result:'PASS',cases:cases.length,scope:proof.scope}));
