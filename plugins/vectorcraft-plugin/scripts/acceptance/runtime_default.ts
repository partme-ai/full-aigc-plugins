import {mkdirSync,readFileSync,writeFileSync,cpSync,existsSync} from 'node:fs';
import {join,resolve} from 'node:path';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import {Controller,skillDigest} from '../../src/harness/controller.ts';
const [output,skillArg,python]=process.argv.slice(2);if(!output||!skillArg||!python)throw new Error('usage: runtime_default.ts NEW_ROOT SKILL PYTHON');
const root=resolve(output),skill=resolve(skillArg);mkdirSync(root);const runtimeHome=join(root,'empty-runtime');assert.equal(existsSync(runtimeHome),false);
const sha=(p:string)=>createHash('sha256').update(readFileSync(p)).digest('hex');
const deps=['src/runtime/prepare_runtime.ts','src/runtime/runtime_probe.py','src/runtime/runtime_gate.ts','runtime/vectorcraft-headless-capabilities.json','src/harness/controller.ts','src/harness/ledger.ts','tests/runtime_default.test.ts','tests/runtime_fixture.ts','scripts/acceptance/runtime_default.ts'];
const fingerprints=Object.fromEntries(deps.map(p=>[p,sha(p)]));const expectedSkillSha256=skillDigest(skill);
const plan=join(root,'plan.json');writeFileSync(plan,JSON.stringify({document:{width:40,height:40,units:'Points'},operations:[{command:'shape.rectangle',params:{x:3,y:3,width:12,height:12},as:'box'}]}));
const request={key:'first',skill,expectedSkillSha256,plan,output:join(root,'first'),runtimeHome,python,estimatedBytes:16*1024*1024,authorization:{objects:[],fields:[],deadline:Date.now()+180000,maxAttempts:2,maxBytes:32*1024*1024,readRoots:[root],writeRoots:[root]}};
const database=join(root,'state.sqlite'),controller=new Controller(database),cases:any[]=[],deliveries:any={};
function recordDelivery(name:string){const directory=join(root,name),manifestPath=join(directory,'manifest.json'),manifest=JSON.parse(readFileSync(manifestPath,'utf8'));for(const [file,digest] of Object.entries(manifest.files))assert.equal(sha(join(directory,file)),digest);deliveries[name]={manifestSha256:sha(manifestPath),files:manifest.files};}
try{
 const first=await controller.run(request);assert.equal(first.state,'review_ready');assert.ok(first.binding.inputHashes['runtime:capabilities']);
 const installation=JSON.parse(readFileSync(join(runtimeHome,'vectorcraft/0.2.0-craft.2/installation.json'),'utf8'));
 assert.equal(installation.binarySha256,first.binding.runtimeIdentity);
 assert.equal(sha(join(runtimeHome,'vectorcraft/0.2.0-craft.2/vectorcraft-cli')),installation.binarySha256);
 cases.push({case:'empty-runtime-default-first-use',state:first.state,binarySha256:installation.binarySha256,capabilityFingerprint:first.binding.inputHashes['runtime:capabilities']});
 recordDelivery('first');
 assert.equal((await controller.run(request)).id,first.id);cases.push({case:'same-key-readonly',state:'PASS'});
 const other=new Controller(database);try{
  const [second,third]=await Promise.all([controller.run({...request,key:'second',output:join(root,'second')}),other.run({...request,key:'third',output:join(root,'third')})]);
  assert.equal(second.state,'review_ready');assert.equal(third.state,'review_ready');recordDelivery('second');recordDelivery('third');cases.push({case:'same-ledger-parallel-distinct-targets',state:'PASS'});
 }finally{other.close();}
 const wrongSkill=join(root,'wrong-schema-skill');cpSync(skill,wrongSkill,{recursive:true});
 const catalogPath=join(wrongSkill,'references/command-coverage.json');const catalog=JSON.parse(readFileSync(catalogPath,'utf8'));catalog.commands[0].params='{} adversarial schema';writeFileSync(catalogPath,JSON.stringify(catalog));
 const taskCount=()=>Number((controller.ledger.db.prepare('SELECT COUNT(*) AS n FROM tasks').get() as any).n);const before=taskCount();
 await assert.rejects(()=>controller.run({...request,key:'bad-schema',skill:wrongSkill,expectedSkillSha256:skillDigest(wrongSkill),output:join(root,'refused')}),/capability_schema_mismatch/);
 assert.equal(taskCount(),before);assert.equal(existsSync(join(root,'refused')),false);cases.push({case:'live-schema-drift-before-task-or-edit',state:'PASS'});
 const invalidPlan=join(root,'invalid-plan.json'),invalidHome=join(root,'invalid-runtime');writeFileSync(invalidPlan,JSON.stringify({operations:[{command:'__invalid__'}]}));
 await assert.rejects(()=>controller.run({...request,key:'bad-plan',plan:invalidPlan,runtimeHome:invalidHome,output:join(root,'bad-plan-output')}),/runtime_probe_failed/);
 assert.equal(existsSync(invalidHome),false);assert.equal(taskCount(),before);cases.push({case:'invalid-plan-before-install',state:'PASS'});
 const selected=JSON.parse((controller.ledger.db.prepare('SELECT active FROM runtime_selection WHERE id=1').get() as any).active);
 assert.equal(selected.commands.length,585);assert.equal(selected.tools.length,25);
 assert.equal(skillDigest(skill),expectedSkillSha256);assert.deepEqual(fingerprints,Object.fromEntries(deps.map(p=>[p,sha(p)])));
 const proof={schema:'vectorcraft-runtime-default-evidence/v1',result:'PASS',level:'native-candidate',platform:process.platform+'-'+process.arch,cases,deliveries,commandCount:585,toolCount:25,skillSha256:expectedSkillSha256,runtimeIdentity:installation.binarySha256,fingerprints,
  scope:'actual cold public fixed install, default headless probe and managed create, readonly resume, parallel tasks and live signature drift refusal; no desktop, different-version upgrade, rollback or complete2.6 acceptance'};
 writeFileSync(join(root,'proof.json'),JSON.stringify(proof,null,2)+'\n');console.log(JSON.stringify({result:'PASS',cases:cases.length}));
}finally{controller.close();}
