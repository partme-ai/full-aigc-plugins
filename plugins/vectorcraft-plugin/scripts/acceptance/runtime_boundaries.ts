import {readFileSync,writeFileSync,mkdirSync,existsSync} from 'node:fs';
import {join,resolve} from 'node:path';
import {spawn} from 'node:child_process';
import {DatabaseSync} from 'node:sqlite';
import {pathToFileURL,fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const [newRoot,probeDirectory,python,implementation=process.cwd()]=process.argv.slice(2);
const implementationRoot=resolve(implementation);
const {Controller,skillDigest}=await import(pathToFileURL(join(implementationRoot,'src/harness/controller.ts')).href);
const {RuntimeGate}=await import(pathToFileURL(join(implementationRoot,'src/runtime/runtime_gate.ts')).href);
const {Ledger}=await import(pathToFileURL(join(implementationRoot,'src/harness/ledger.ts')).href);if(!newRoot||!probeDirectory||!python)throw new Error('usage: runtime_boundaries.ts NEW_ROOT PROBE_DIRECTORY PYTHON');
const root=resolve(newRoot),probes=resolve(probeDirectory);mkdirSync(root);const read=(p:string)=>JSON.parse(readFileSync(p,'utf8')),sha=(p:string)=>createHash('sha256').update(readFileSync(p)).digest('hex');
const old=read(join(probes,'old-probe.json')),current=read(join(probes,'new-probe.json')),bridge=read(join(probes,'bridge-probe.json')),desktop=read(join(probes,'desktop-lifecycle.json'));
const dependencies=['src/harness/controller.ts','src/harness/ledger.ts','src/harness/process_registry.ts','src/runtime/runtime_gate.ts','src/runtime/runtime_probe.py','src/runtime/prepare_runtime.ts','scripts/acceptance/runtime_boundaries.ts','scripts/acceptance/runtime_native_child.py','tests/state_migration.test.ts','runtime/vectorcraft-headless-capabilities.json','skills.lock.json'];
const fingerprints=Object.fromEntries(dependencies.map(p=>[p,sha(join(implementationRoot,p))]));
assert.equal(sha(fileURLToPath(import.meta.url)),sha(join(implementationRoot,'scripts/acceptance/runtime_boundaries.ts')));const registry=Object.fromEntries(current.commands.map((r:any)=>[r.id,r.params]));
const requiredNames=['file.new','shape.rectangle','document.save','document.open','document.inspect'];
const requirements={mode:'headless',commands:Object.fromEntries(requiredNames.map(id=>[id,registry[id]])),tools:{run_command:current.tools.find((r:any)=>r.name==='run_command').inputSchema}};
const database=join(root,'state.sqlite'),controller=new Controller(database),ledger=controller.ledger,gate=new RuntimeGate(ledger),cases:any[]=[];
const binaries={old:join(probes,'runtime/vectorcraft/0.2.0/vectorcraft-cli'),current:join(probes,'runtime/vectorcraft/0.2.0-craft.2/vectorcraft-cli')};
const hashes={old:sha(binaries.old),current:sha(binaries.current)};assert.equal(hashes.old,old.binarySha256);assert.equal(hashes.current,current.binarySha256);
async function native(name:string,report:any,skill:string,binary:string,source?:string,onReady?:()=>void,onExit?:()=>void){
 const output=join(root,name),auth={objects:[],fields:[],deadline:Date.now()+60000,maxAttempts:1,maxBytes:1024*1024};
 const plan={name,sourceSha256:source?sha(source):null,skillSha256:skillDigest(skill)};
 const binding={planHash:createHash('sha256').update(JSON.stringify(plan)).digest('hex'),inputHashes:{helper:fingerprints['scripts/acceptance/runtime_native_child.py']},projectRevision:plan.sourceSha256,runtimeIdentity:report.binarySha256,authorization:auth};
 const task=ledger.claim(name,source??join(output,'project.vectorcraft'),output,binding);ledger.intent(task.id,1,0,plan,65536);
 const args=['-I','-B',join(implementationRoot,'scripts/acceptance/runtime_native_child.py'),task.id,skill,binary,output,...(source?['--source',source]:[]),...(onReady?['--hold']:[])];
 const child=spawn(python,args,{detached:true,stdio:['pipe','pipe','pipe']});let stdout='',stderr='';child.stdout.on('data',b=>stdout+=b);child.stderr.on('data',b=>stderr+=b);
 const done=new Promise<number|null>((ok,no)=>{child.on('error',no);child.on('close',ok);});
 controller.processes.register(task.id,1,child.pid!,task.id);child.stdin.end(JSON.stringify({task:task.id,go:true})+'\n');
 try{
  const deadline=Date.now()+20000;while(!existsSync(join(output,'ready.json'))&&Date.now()<deadline&&child.exitCode===null)await new Promise(r=>setTimeout(r,25));
  assert.ok(existsSync(join(output,'ready.json')),stderr);const ready=read(join(output,'ready.json'));assert.equal(ready.projectSha256,sha(join(output,'project.vectorcraft')));
  if(onReady){onReady();writeFileSync(join(output,'release.json'),'{}',{flag:'wx'});}
  assert.equal(await done,0,stderr);const proof=JSON.parse(stdout);assert.equal(proof.runtimeIdentity,report.binarySha256);assert.equal(proof.reopened,true);assert.equal(proof.projectSha256,sha(join(output,'project.vectorcraft')));
  ledger.receipt(task.id,1,0,proof);ledger.verified(task.id,1,{path:join(output,'project.vectorcraft'),sha256:proof.projectSha256});if(onExit)onExit();assert.equal(controller.processes.observe(task.id,1).stopped,true);
  if(source)assert.equal(sha(source),plan.sourceSha256);
  return {output,proof};
 }catch(error){await controller.processes.stop(task.id,1);ledger.unknown(task.id,1,String(error));throw error;}
}
function equivalent(a:string,b:string){const first=read(a).document,next=read(b).document;delete first.metadata.modified;delete next.metadata.modified;assert.deepEqual(next,first);}
try{
 gate.activate(old,requirements,[3]);
 assert.throws(()=>gate.activate(current,{...requirements,commands:{'__missing_required_capability__':'{}'}},[3]),/capability_missing/);assert.equal(gate.current().active.binarySha256,old.binarySha256);
 cases.push({case:'missing-new-capability-retains-old',result:'PASS'});
 assert.throws(()=>gate.activate(old,{...requirements,commands:{'document.serialize':registry['document.serialize']}},[3]),/capability_schema_mismatch/);cases.push({case:'actual-old-new-schema-drift-refused',result:'PASS'});
 const legacy=await native('old-created',old,join(probes,'old-probe-skill'),binaries.old,undefined,()=>{
  assert.throws(()=>gate.activate(current,requirements,[3]),/runtime_tasks_not_drained/);assert.equal(gate.current().active.binarySha256,old.binarySha256);
 },()=>{assert.throws(()=>gate.activate(current,requirements,[3]),/runtime_process_stop_unconfirmed/);});cases.push({case:'actual-old-session-blocks-upgrade',...legacy.proof});cases.push({case:'exited-but-unconfirmed-group-blocks-upgrade',result:'PASS'});
 const stateFixture=join(root,'legacy-state-fixture.sqlite');ledger.db.prepare('VACUUM INTO ?').run(stateFixture);const fixture=new DatabaseSync(stateFixture);fixture.exec('DROP TABLE budgets; DROP TABLE late_receipts; PRAGMA user_version=1');fixture.close();
 const upgradedState=new Ledger(stateFixture);try{assert.ok(upgradedState.schemaBackup);const backup=new DatabaseSync(upgradedState.schemaBackup.path,{readOnly:true});try{assert.equal((backup.prepare('PRAGMA user_version').get() as any).user_version,1);assert.equal((upgradedState.db.prepare('PRAGMA user_version').get() as any).user_version,3);assert.deepEqual(upgradedState.db.prepare('SELECT id,state,attempts,bytes,binding FROM tasks').all(),backup.prepare('SELECT id,state,attempts,bytes,binding FROM tasks').all());}finally{backup.close();}cases.push({case:'schema1-fixture-with-real-native-task-rows',backupSha256:upgradedState.schemaBackup.sha256,fromSchema:1,toSchema:3,rowsPreserved:true});}finally{upgradedState.close();}
 gate.activate(current,requirements,[3]);assert.equal(gate.current().previous.binarySha256,old.binarySha256);cases.push({case:'drained-upgrade-retains-old',result:'PASS'});
 const upgraded=await native('new-reopened-old',current,join(implementationRoot,'skills/vectorcraft-use'),binaries.current,join(legacy.output,'project.vectorcraft'));
 equivalent(join(legacy.output,'project.vectorcraft'),join(upgraded.output,'project.vectorcraft'));cases.push({case:'new-runtime-reopens-old-native',...upgraded.proof,documentPreservedExceptSaveTimestamp:true});
 const defaultPlan=join(root,'default-plan.json');writeFileSync(defaultPlan,JSON.stringify({document:{width:32,height:32,units:'Points'},operations:[{command:'shape.rectangle',params:{x:2,y:2,width:12,height:12}}]}));
 const defaultTask=await controller.run({key:'default-after-upgrade',skill:join(implementationRoot,'skills/vectorcraft-use'),expectedSkillSha256:skillDigest(join(implementationRoot,'skills/vectorcraft-use')),plan:defaultPlan,output:join(root,'default-created'),runtimeHome:join(probes,'runtime'),python,estimatedBytes:1024*1024,authorization:{objects:[],fields:[],deadline:Date.now()+60000,maxAttempts:1,maxBytes:1024*1024,readRoots:[root],writeRoots:[root,probes]}});assert.equal(defaultTask.state,'review_ready');cases.push({case:'default-harness-after-upgrade',runtimeIdentity:defaultTask.binding.runtimeIdentity,projectSha256:sha(join(root,'default-created/project.vectorcraft'))});
 assert.throws(()=>gate.activate(old,requirements,[2]),/incompatible_state_schema/);assert.equal(gate.current().active.binarySha256,current.binarySha256);cases.push({case:'incompatible-rollback-policy-refused',result:'PASS'});
 gate.activate(old,requirements,[3]);assert.equal(gate.current().previous.binarySha256,current.binarySha256);
 const rolled=await native('old-reopened-new',old,join(probes,'old-probe-skill'),binaries.old,join(upgraded.output,'project.vectorcraft'));equivalent(join(upgraded.output,'project.vectorcraft'),join(rolled.output,'project.vectorcraft'));
 cases.push({case:'compatible-rollback-reopens-native',...rolled.proof,documentPreservedExceptSaveTimestamp:true});
 assert.equal(desktop.listenerOwnedByPID,true);assert.equal(desktop.ownedProcessesStopped,true);assert.equal(desktop.cliBinarySha256,current.binarySha256);
 const bridgeRequirements={...requirements,mode:'bridge',commands:{'document.inspect':bridge.commands.find((r:any)=>r.id==='document.inspect').params}};
 gate.activate(bridge,bridgeRequirements,[3]);
 const plan=join(root,'headless-refused.json');writeFileSync(plan,JSON.stringify({document:{width:32,height:32},operations:[]}));
 await assert.rejects(()=>controller.run({key:'headless-refused',skill:join(implementationRoot,'skills/vectorcraft-use'),expectedSkillSha256:skillDigest(join(implementationRoot,'skills/vectorcraft-use')),plan,output:join(root,'headless-refused'),runtimeHome:join(probes,'runtime'),python,estimatedBytes:10000,authorization:{objects:[],fields:[],deadline:Date.now()+60000,maxAttempts:1,maxBytes:10000,readRoots:[root],writeRoots:[root,probes]}}),/runtime_mode_mismatch/);
 assert.equal(existsSync(join(root,'headless-refused')),false);cases.push({case:'actual-desktop-bridge-is-not-headless',...desktop});
 assert.deepEqual(hashes,{old:sha(binaries.old),current:sha(binaries.current)});assert.deepEqual(fingerprints,Object.fromEntries(dependencies.map(p=>[p,sha(join(implementationRoot,p))])));
 const proof={schema:'vectorcraft-runtime-boundaries/v1',result:'PASS',level:'native-candidate',platform:process.platform+'-'+process.arch,versions:[old.version,current.version],runtimeHashes:hashes,cases,fingerprints,
  scope:'two actual pinned native CLI versions, live-session drain, native reopen across upgrade/rollback, explicit state compatibility policy and owned signed desktop bridge; no fixed plugin install, full GUI creative assessment or other platforms'};
 writeFileSync(join(root,'proof.json'),JSON.stringify(proof,null,2)+'\n');console.log(JSON.stringify({result:'PASS',cases:cases.length}));
}finally{controller.close();}
