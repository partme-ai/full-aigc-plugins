import { mkdirSync,readFileSync,writeFileSync,cpSync } from 'node:fs';
import { resolve,join } from 'node:path';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { ReviewStore } from '../../src/evaluation/review_store.ts';
import { TechnicalReview } from '../../src/evaluation/technical_review.ts';

/** 使用已有原生产物验证协调器；不冒充本轮原生生成、工程重开或真实视觉评审。 */
const [sourceRoot,outputRoot,python]=process.argv.slice(2);
if(!sourceRoot||!outputRoot||!python)throw new Error('usage: checked_review.ts NATIVE_GATEWAY_ROOT NEW_OUTPUT_ROOT PYTHON');
const root=resolve(outputRoot);mkdirSync(root);const cases:any[]=[];
const hash=(v:Buffer|string)=>createHash('sha256').update(v).digest('hex');
const dependencies=['src/evaluation/technical_review.ts','src/evaluation/review_store.ts','src/evaluation/delivery_quality.py','src/harness/ledger.ts','src/harness/process_registry.ts','src/harness/process_runner.py','src/strict_json.ts','src/cli.ts','tests/technical_review.test.ts','scripts/acceptance/checked_review.ts'];
const fingerprints=Object.fromEntries(dependencies.map(p=>[p,hash(readFileSync(p))]));
for(const mode of ['direct','native-gateway'])for(const corrupt of [false,true]){
  const name=mode+(corrupt?'-corrupt':'-healthy'),work=join(root,name),delivery=join(work,'delivery');mkdirSync(work);
  cpSync(join(resolve(sourceRoot),mode),delivery,{recursive:true});
  const manifestPath=join(delivery,'manifest.json'),manifest=JSON.parse(readFileSync(manifestPath,'utf8'));
  if(corrupt){const png=manifest.outputs.find((o:any)=>o.path.endsWith('.png')).path;writeFileSync(join(delivery,png),'invalid png');manifest.files[png]=hash(readFileSync(join(delivery,png)));writeFileSync(manifestPath,JSON.stringify(manifest));}
  const target=join(work,'brief.txt'),rubric=join(work,'rubric.json');writeFileSync(target,'Technical integration fixture; no creative assessment');writeFileSync(rubric,'{}');
  const database=join(work,'review.sqlite'),input={native:join(delivery,'project.vectorcraft'),projectRevision:manifest.files['project.vectorcraft'],runtimeIdentity:manifest.runtimeSha256,
    candidates:manifest.outputs.map((o:any)=>join(delivery,o.path)),targets:[{path:target,role:'target'}],rubric,exchangeLoss:join(delivery,'exchange-loss.json'),technicalStatus:'PASS',
    authorization:{objects:[2],fields:['paint.color'],deadline:Date.now()+30000,maxAttempts:3,maxBytes:64*1024*1024,budgetId:name,readRoots:[work],writeRoots:[work]}};
  let store=new ReviewStore(database,[work]);
  try{
    const request=await new TechnicalReview(store).request(input,{python});
    assert.equal(request.input.technicalStatus,corrupt?'FAIL':'PASS');assert.equal(request.input.technicalEvidence.outputs.length,9);
    const again=await new TechnicalReview(store).request(input,{python});assert.equal(again.id,request.id);
    store.close();store=new ReviewStore(database,[work]);
    const result=store.importReceipt({schema:'vectorcraft-review-receipt/v1',requestId:request.id,bindingHash:request.bindingHash,
      reviewer:{kind:'human',identity:'automated high-score fixture, not a human acceptance',contextOrigin:'acceptance test injection',independenceEvidence:null},verdict:'accept',issues:[],scores:{structure:4,text:4,brand:4,layout:4,legibility:4}});
    assert.equal(result.acceptanceStatus,corrupt?'blocked':'pending');assert.equal(result.engineeringStatus,'NOT_RUN');
    assert.equal((store.db.prepare('SELECT attempts FROM budgets WHERE id=?').get(name) as any).attempts,1);
    cases.push({name,sourceManifestSha256:hash(readFileSync(join(resolve(sourceRoot),mode,'manifest.json'))),
      report:request.input.technicalEvidence,state:result.state,acceptanceStatus:result.acceptanceStatus,creativeVerdict:'fixture only; not assessed',restartVerified:true,attempts:1});
  }finally{store.close();}
}
assert.deepEqual(Object.fromEntries(dependencies.map(p=>[p,hash(readFileSync(p))])),fingerprints,'candidate source changed during execution');
const proof={schema:'vectorcraft-checked-review-candidate/v1',result:'PASS',level:'native-candidate',platform:process.platform+'-'+process.arch,cases,
  fingerprints,
  scope:'Current coordinator checks copies of previously generated fixed38/source35 native exports; four persisted checks and fixture receipts; no new native generation, native reopening, real creative judgment, model routing, or full V1 acceptance'};
writeFileSync(join(root,'proof.json'),JSON.stringify(proof,null,2)+'\n');console.log(JSON.stringify({result:proof.result,cases:cases.length,exports:36,scope:proof.scope}));
