import {execFileSync} from 'node:child_process';
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {join,resolve} from 'node:path';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import {Controller,skillDigest} from '../../src/harness/controller.ts';
import {RuntimeGate,validateCapabilities} from '../../src/runtime/runtime_gate.ts';
const [output,skillArg,executable,home,python]=process.argv.slice(2);
if(!output||!skillArg||!executable||!home||!python)throw new Error('usage: runtime_gate.ts NEW_ROOT SKILL EXECUTABLE RUNTIME_HOME PYTHON');
const root=resolve(output),skill=resolve(skillArg);mkdirSync(root);const sha=(p:string)=>createHash('sha256').update(readFileSync(p)).digest('hex');
const inputs=['src/runtime/runtime_gate.ts','src/runtime/runtime_probe.py','src/cli.ts','src/harness/ledger.ts','src/harness/controller.ts','scripts/acceptance/runtime_gate.ts','tests/runtime_gate.test.ts','tests/runtime_selection.test.ts'];
const fingerprints=Object.fromEntries(inputs.map(p=>[p,sha(p)])),expectedSkillSha256=skillDigest(skill);
const catalog=JSON.parse(readFileSync(join(skill,'references/command-coverage.json'),'utf8'));
const requirements={mode:'headless',commands:Object.fromEntries(catalog.commands.map((r:any)=>[r.id,r.params])),tools:{}};
const probe=JSON.parse(execFileSync(python,['-I','-B','src/runtime/runtime_probe.py'],{input:JSON.stringify({skill,executable:resolve(executable),platform:'darwin-arm64',requirements}),encoding:'utf8',timeout:40000,maxBuffer:8*1024*1024}));
const schemas=Object.fromEntries(probe.tools.map((t:any)=>[t.name,t.inputSchema]));requirements.tools=schemas;
assert.equal(validateCapabilities(probe,requirements).commandCount,585);
const controller=new Controller(join(root,'state.sqlite')),gate=new RuntimeGate(controller.ledger);
try{
 gate.activate(probe,requirements,[3]);
 assert.throws(()=>gate.activate(probe,{...requirements,commands:{'__missing__':'{}'}},[3]),/capability_missing/);
 assert.throws(()=>gate.activate(probe,{...requirements,commands:{'file.new':'{}'}},[3]),/capability_schema_mismatch/);
 assert.throws(()=>gate.activate(probe,{...requirements,mode:'bridge'},[3]),/runtime_mode_mismatch/);
 assert.throws(()=>gate.activate(probe,requirements,[1]),/incompatible_state_schema/);
 const plan=join(root,'plan.json');writeFileSync(plan,JSON.stringify({document:{width:32,height:32,units:'Points'},operations:[{command:'shape.rectangle',params:{x:2,y:2,width:12,height:12},as:'box'}]}));
 const request={key:'native',skill,expectedSkillSha256,plan,output:join(root,'delivery'),runtimeHome:resolve(home),python,estimatedBytes:16*1024*1024,authorization:{objects:[],fields:[],deadline:Date.now()+60000,maxAttempts:2,maxBytes:32*1024*1024,readRoots:[root],writeRoots:[root,resolve(home)]}};
 const running=controller.run(request);
 assert.throws(()=>gate.activate(probe,requirements,[3]),/runtime_tasks_not_drained/);
 const task=await running;assert.equal(task.state,'review_ready');
 assert.ok(task.binding.inputHashes['runtime:capabilities']);
 assert.equal((await controller.run(request)).id,task.id);
 gate.activate(probe,requirements,[3]);assert.equal(gate.current().previous,null);
 assert.equal(skillDigest(skill),expectedSkillSha256);
 assert.deepEqual(fingerprints,Object.fromEntries(inputs.map(p=>[p,sha(p)])));
 const manifest=JSON.parse(readFileSync(join(request.output,'manifest.json'),'utf8'));
 const report={schema:'vectorcraft-runtime-gate-evidence/v1',result:'PASS',level:'native-candidate',platform:process.platform+'-'+process.arch,runtimeIdentity:probe.binarySha256,version:probe.version,skillSha256:expectedSkillSha256,commandCount:probe.commands.length,toolCount:probe.tools.length,
  cases:['live-schema','missing-command-refused','changed-schema-refused','bridge-substitution-refused','incompatible-state-refused','active-native-task-blocks-switch','native-create-with-selected-runtime','same-key-no-replay','idempotent-activation-preserves-history'],projectSha256:manifest.files['project.vectorcraft'],fingerprints,
  scope:'same pinned headless runtime probing, activation, drain and managed native create; no different-version upgrade, desktop GUI, migration or rollback acceptance'};
 writeFileSync(join(root,'proof.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({result:'PASS',cases:report.cases.length,commands:report.commandCount,tools:report.toolCount}));
}finally{controller.close();}
