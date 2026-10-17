import { mkdirSync,cpSync,writeFileSync,readFileSync } from 'node:fs';
import { resolve,join } from 'node:path';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import assert from 'node:assert/strict';
import { ReviewStore } from '../../src/evaluation/review_store.ts';
import { RevisionCycle } from '../../src/evaluation/revision_cycle.ts';
import { TechnicalReview } from '../../src/evaluation/technical_review.ts';
import { skillDigest } from '../../src/harness/controller.ts';

/** 两项真实原生返工；评分为显式测试注入，不证明真实创作验收或完整6.6。 */
const [original,outputRoot,skillPath,runtimePath,python]=process.argv.slice(2);
if(!original||!outputRoot||!skillPath||!runtimePath||!python)throw new Error('usage: revision_cycle.ts ORIGINAL NEW_ROOT SKILL WARM_RUNTIME PYTHON');
const root=resolve(outputRoot),skill=resolve(skillPath),runtimeHome=resolve(runtimePath);mkdirSync(root);
const digest=(value:Buffer|string)=>createHash('sha256').update(value).digest('hex');
const dependencies=['src/planning/geometry.ts','skills.lock.json','src/cli.ts','src/evaluation/revision_cycle.ts','src/evaluation/review_store.ts','src/evaluation/technical_review.ts','src/evaluation/delivery_quality.py','src/harness/controller.ts','src/harness/ledger.ts','src/harness/process_registry.ts','src/harness/process_runner.py','tests/revision_cycle.test.ts','tests/controller.test.ts','scripts/acceptance/revision_cycle.ts'];
const fingerprints=Object.fromEntries(dependencies.map(p=>[p,digest(readFileSync(p))]));
const startingSkillSha256=skillDigest(skill);
assert.equal(startingSkillSha256,JSON.parse(readFileSync('skills.lock.json','utf8')).sources[0].sha256['vectorcraft-use'],'acceptance requires exact pinned skill bytes');
const targetColor={model:'rgb',r:Math.fround(34/255),g:Math.fround(85/255),b:Math.fround(136/255)};
const changes=[{objectId:4,field:'appearance.items.0.paint.color',value:targetColor},{objectId:5,field:'kind.runs.0.style.fill.color',value:targetColor},{objectId:7,field:'appearance.items.0.paint.color',value:targetColor}];
const cases:any[]=[];
for(const reason of ['stagnation','round_limit']){
  const work=join(root,reason),source=join(work,'source'),output=join(work,'revised');mkdirSync(work);cpSync(resolve(original),source,{recursive:true});
  const target=join(work,'brief.txt'),rubric=join(work,'rubric.json');writeFileSync(target,'Native bounded revision technical fixture');writeFileSync(rubric,'{}');
  const database=join(work,'reviews.sqlite'),auth={objects:[4,5,7],fields:[...new Set(changes.map(c=>c.field))],deadline:Date.now()+60000,maxAttempts:20,maxBytes:512*1024*1024,budgetId:reason,readRoots:[work],writeRoots:[work,runtimeHome]};
  let store=new ReviewStore(database,[work]),cycle=new RevisionCycle(store);
  const check=async(directory:string,score:number)=>{
    const manifest=JSON.parse(readFileSync(join(directory,'manifest.json'),'utf8'));
    const request=await new TechnicalReview(store).request({native:join(directory,'project.vectorcraft'),projectRevision:manifest.files['project.vectorcraft'],runtimeIdentity:manifest.runtimeSha256,candidates:manifest.outputs.map((o:any)=>join(directory,o.path)),targets:[{path:target,role:'target'}],rubric,exchangeLoss:join(directory,'exchange-loss.json'),technicalStatus:'PASS',authorization:auth},{python});
    store.importReceipt({schema:'vectorcraft-review-receipt/v1',requestId:request.id,bindingHash:request.bindingHash,reviewer:{kind:'human',identity:'automated fixture, not human creative acceptance',contextOrigin:'test-injected scores',independenceEvidence:null},verdict:'revise',issues:changes.map(c=>({objectId:c.objectId,field:c.field,message:'fixture color target',evidence:['native.json']})),scores:{structure:score,text:score,brand:score,layout:score,legibility:score}});
    return request;
  };
  try{
    const before=digest(readFileSync(join(source,'project.vectorcraft'))),initial=await check(source,2);
    cycle.open({id:reason,requestId:initial.id,policy:{maxRounds:reason==='round_limit'?1:3,stagnationLimit:1,minImprovement:0.1}});
    const proposal=cycle.propose(reason,initial.id,changes,'one');
    const originalPlan=JSON.parse(readFileSync(join(source,'plan.json'),'utf8')),plan=join(work,'revision-plan.json');
    writeFileSync(plan,JSON.stringify({expectedProjectSha256:before,operations:[{command:'swatch.edit',params:{name:'Brand Primary',color:'#225588'}}],exports:originalPlan.exports}));
    const execution=await cycle.execute(reason,proposal.id,{skill,expectedSkillSha256:skillDigest(skill),plan,output,runtimeHome,python,estimatedBytes:64*1024*1024});
    assert.equal(execution.state,'awaiting_review');assert.equal(digest(readFileSync(join(source,'project.vectorcraft'))),before);
    const next=await check(output,reason==='stagnation'?1.9:3),stopped=cycle.observe(reason,next.id,proposal.id);assert.equal(stopped.reason,reason);
    const best=cycle.best(reason);assert.equal(best.requestId,reason==='stagnation'?initial.id:next.id);
    assert.equal(best.unresolvedIssues.length,3);assert.equal(best.rounds,1);assert.equal(best.latestRequestId,next.id);
    const used=(store.db.prepare('SELECT attempts FROM budgets WHERE id=?').get(reason) as any).attempts;
    cycle.close();store.close();store=new ReviewStore(database,[work]);cycle=new RevisionCycle(store);
    assert.equal(cycle.get(reason).reason,reason);assert.equal(cycle.best(reason).projectRevision,best.projectRevision);
    assert.equal((store.db.prepare('SELECT attempts FROM budgets WHERE id=?').get(reason) as any).attempts,used);
    assert.throws(()=>cycle.propose(reason,next.id,changes,'two'),/revision_cycle_stopped/);
    assert.throws(()=>store.revision(next.id,changes),/revision_cycle_required/);
    const bestRequest=join(work,'best-request.json');writeFileSync(bestRequest,JSON.stringify({cycleId:reason,readRoots:[work]}));
    const cliBest=JSON.parse(execFileSync(process.execPath,['src/cli.ts','revision-cycle-best',database,bestRequest],{encoding:'utf8'}));
    assert.equal(cliBest.projectRevision,best.projectRevision);assert.equal(cliBest.reason,reason);
    cases.push({reason,sourceProjectRevision:before,outputProjectRevision:next.input.projectRevision,bestProjectRevision:best.projectRevision,bestScore:best.score,
      nativeExecution:execution.state,sourcePreserved:true,technicalStatus:next.input.technicalStatus,decodedExports:next.input.technicalEvidence.outputs.length,
      sharedAttempts:used,restartVerified:true,legacyBypassRefused:true,cliBestVerified:true,engineeringStatus:'NOT_RUN',creativeAssessment:'fixture only; NOT_RUN',acceptanceStatus:'pending'});
  }finally{cycle.close();store.close();}
}
assert.deepEqual(Object.fromEntries(dependencies.map(p=>[p,digest(readFileSync(p))])),fingerprints,'candidate source changed during execution');
assert.equal(skillDigest(skill),startingSkillSha256,'skill snapshot changed during execution');
const proof={schema:'vectorcraft-revision-cycle-candidate/v1',result:'PASS',level:'native-candidate',platform:process.platform+'-'+process.arch,skillSha256:skillDigest(skill),runtimeIdentity:JSON.parse(readFileSync(join(skill,'scripts/runtime.lock.json'),'utf8')).artifacts['darwin-arm64'].binarySha256,cases,
  fingerprints,scope:'two actual managed native color revisions and current decoder checks; source preserved; fixture scoring; full6.6, real creative acceptance, other revision families and model routing remain open'};
writeFileSync(join(root,'proof.json'),JSON.stringify(proof,null,2)+'\n');console.log(JSON.stringify({result:'PASS',cases:cases.length,scope:proof.scope}));
