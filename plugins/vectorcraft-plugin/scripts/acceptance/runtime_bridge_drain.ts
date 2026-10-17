import {readFileSync,writeFileSync,mkdirSync,existsSync} from 'node:fs';
import {join,resolve} from 'node:path';
import {spawn} from 'node:child_process';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
// 验收驱动与被测固定安装分离记录；不修改安装快照，也不把驱动声称为已发布实现。
const [output,probeDirectory,python,implementation=process.cwd()]=process.argv.slice(2);
if(!output||!probeDirectory||!python)throw new Error('usage: runtime_bridge_drain.ts NEW_ROOT PROBE_DIRECTORY PYTHON [INSTALLED_PLUGIN]');
const driverRoot=process.cwd(),implementationRoot=resolve(implementation),root=resolve(output),probes=resolve(probeDirectory);mkdirSync(root);
const read=(p:string)=>JSON.parse(readFileSync(p,'utf8')),sha=(p:string)=>createHash('sha256').update(readFileSync(p)).digest('hex');
const {Controller,skillDigest}=await import(pathToFileURL(join(implementationRoot,'src/harness/controller.ts')).href);
const {RuntimeGate}=await import(pathToFileURL(join(implementationRoot,'src/runtime/runtime_gate.ts')).href);
const controller=new Controller(join(root,'state.sqlite')),ledger=controller.ledger,gate=new RuntimeGate(ledger),cases:any[]=[];
const paths=['src/harness/controller.ts','src/harness/ledger.ts','src/harness/process_registry.ts','src/runtime/runtime_gate.ts','src/strict_json.ts','skills.lock.json','plugin.json'];
const fingerprints=Object.fromEntries(paths.map(p=>[p,sha(join(implementationRoot,p))]));
const driverPaths=['scripts/acceptance/runtime_bridge_drain.ts','scripts/acceptance/runtime_bridge_child.py'];
const driverFingerprints=Object.fromEntries(driverPaths.map(p=>[p,sha(join(driverRoot,p))]));
const old=read(join(probes,'old-probe.json')),bridge=read(join(probes,'bridge-probe.json')),skill=join(implementationRoot,'skills/vectorcraft-use');
const names=['file.new','shape.rectangle','document.save','document.open','document.inspect'];
const requirements=(report:any)=>({mode:report.mode,commands:Object.fromEntries(names.map(id=>[id,report.commands.find((r:any)=>r.id===id).params])),tools:{run_command:report.tools.find((r:any)=>r.name==='run_command').inputSchema}});
const bridgeRequirements=requirements(bridge),oldRequirements=requirements(old),policy=join(root,'requirements.json');writeFileSync(policy,JSON.stringify(bridgeRequirements));
const binary=join(probes,'runtime/vectorcraft/0.2.0-craft.2/vectorcraft-cli'),oldBinary=join(probes,'runtime/vectorcraft/0.2.0/vectorcraft-cli');
assert.equal(sha(binary),bridge.binarySha256);assert.equal(sha(oldBinary),old.binarySha256);
async function execute(name:string,mode:'bridge'|'headless',source?:string){
 const destination=join(root,name),runtime=mode==='bridge'?bridge:old,selectedSkill=mode==='bridge'?skill:join(probes,'old-probe-skill');
 const plan={name,mode,sourceSha256:source?sha(source):null};
 const task=ledger.claim(name,source??join(destination,'project.vectorcraft'),destination,{executionMode:mode,skillSha256:skillDigest(selectedSkill),planHash:createHash('sha256').update(JSON.stringify(plan)).digest('hex'),inputHashes:driverFingerprints,projectRevision:plan.sourceSha256,runtimeIdentity:runtime.binarySha256,authorization:{objects:[],fields:[],deadline:Date.now()+120000,maxAttempts:1,maxBytes:1024*1024}});
 ledger.intent(task.id,1,0,plan,65536);
 const args=mode==='bridge'?['-I','-B',join(driverRoot,driverPaths[1]),task.id,selectedSkill,binary,join(probes,'runtime/vectorcraft-desktop/0.2.0'),destination,policy]:['-I','-B',join(implementationRoot,'scripts/acceptance/runtime_native_child.py'),task.id,selectedSkill,oldBinary,destination];
 if(source)args.push('--source',source);
 const child=spawn(python,args,{detached:true,stdio:['pipe','pipe','pipe']});let stdout='',stderr='';child.stdout.on('data',b=>stdout+=b);child.stderr.on('data',b=>stderr+=b);
 const done=new Promise<number|null>((ok,no)=>{child.on('error',no);child.on('close',ok);});controller.processes.register(task.id,1,child.pid!,task.id);child.stdin.end(JSON.stringify({task:task.id,go:true})+'\n');
 try{
  if(mode==='bridge'){
   const deadline=Date.now()+60000;while(!existsSync(join(destination,'ready.json'))&&Date.now()<deadline&&child.exitCode===null)await new Promise(r=>setTimeout(r,25));
   assert.ok(existsSync(join(destination,'ready.json')),stderr);const ready=read(join(destination,'ready.json'));assert.equal(ready.listenerOwnedByPID,true);assert.equal(ready.projectSha256,sha(join(destination,'project.vectorcraft')));
   const observed=controller.processes.observe(task.id,1);assert.equal(observed.owned,true);assert.equal(observed.stopped,false);assert.ok(observed.members.some((m:any)=>m.pid===ready.desktopPID),'actual desktop belongs to registered group');assert.ok(observed.members.length>=3,'Python,desktop and MCP process are live');
   assert.throws(()=>gate.activate(old,oldRequirements,[3]),/runtime_tasks_not_drained/);assert.equal(gate.current().active.mode,'bridge');
   cases.push({case:name+'-live-bridge-blocks-version-switch',result:'PASS',liveRegisteredMembers:observed.members.length,listenerOwnedByPID:true});writeFileSync(join(destination,'release.json'),'{}',{flag:'wx'});
  }
  assert.equal(await done,0,stderr);const proof=JSON.parse(stdout);assert.equal(proof.runtimeIdentity,runtime.binarySha256);assert.equal(proof.reopened,true);assert.equal(proof.projectSha256,sha(join(destination,'project.vectorcraft')));
  if(mode==='bridge')assert.equal(proof.ownedProcessesStopped,true);
  ledger.receipt(task.id,1,0,proof);ledger.verified(task.id,1,{path:join(destination,'project.vectorcraft'),sha256:proof.projectSha256});
  assert.throws(()=>gate.activate(mode==='bridge'?old:bridge,mode==='bridge'?oldRequirements:bridgeRequirements,[3]),/runtime_process_stop_unconfirmed/);
  assert.equal(controller.processes.observe(task.id,1).stopped,true);if(source)assert.equal(sha(source),plan.sourceSha256);
  // PID只供本次实时归属断言，公开证明保留稳定身份摘要及进程数。
  delete proof.desktopPID;cases.push({case:name+'-stopped-confirmed-and-native-reopened',...proof});return join(destination,'project.vectorcraft');
 }catch(error){await controller.processes.stop(task.id,1);ledger.unknown(task.id,1,String(error));throw error;}
}
function equivalent(a:string,b:string){const left=read(a).document,right=read(b).document;delete left.metadata.modified;delete right.metadata.modified;assert.deepEqual(left,right);}
try{
 gate.activate(bridge,bridgeRequirements,[3]);const first=await execute('registered-bridge','bridge');
 gate.activate(old,oldRequirements,[3]);assert.equal(gate.current().previous.mode,'bridge');const rolled=await execute('old-reopens-bridge','headless',first);equivalent(first,rolled);
 gate.activate(bridge,bridgeRequirements,[3]);assert.equal(gate.current().previous.binarySha256,old.binarySha256);const restored=await execute('restored-bridge','bridge',rolled);equivalent(rolled,restored);
 assert.deepEqual(fingerprints,Object.fromEntries(paths.map(p=>[p,sha(join(implementationRoot,p))])));assert.deepEqual(driverFingerprints,Object.fromEntries(driverPaths.map(p=>[p,sha(join(driverRoot,p))])));
 const proof={schema:'vectorcraft-registered-bridge-drain/v1',result:'PASS',platform:process.platform+'-'+process.arch,pluginVersion:read(join(implementationRoot,'plugin.json')).version,cases,fingerprints,driverFingerprints,skillSha256:skillDigest(skill),runtimeSha256:sha(binary),oldRuntimeSha256:sha(oldBinary),scope:'Actual registered owned signed bridge and CLI processes; live and unconfirmed stop prevent switching, drained rollback and reactivation preserve full native document except save timestamp; no model or creative visual acceptance'};
 writeFileSync(join(root,'proof.json'),JSON.stringify(proof,null,2)+'\n');console.log(JSON.stringify({result:'PASS',cases:cases.length}));
}finally{controller.close();}
