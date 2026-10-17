/** 原生 opt-in：在真实检查点已保存后撤销，不注入引擎或模拟写盘。 */
import assert from 'node:assert/strict';
import { executionIdentity } from './execution_identity.ts';
const executionFingerprints=executionIdentity();
import { readFileSync, writeFileSync, existsSync, statSync, mkdirSync,chmodSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { Controller, skillDigest } from '../../src/harness/controller.ts';
import { strictJson } from '../../src/strict_json.ts';
const input=strictJson(readFileSync(process.argv[2],'utf8'));
const root=resolve(input.output),source=resolve(input.source),skill=resolve(input.skill),runtime=resolve(input.runtimeHome);
mkdirSync(root,{recursive:true});
const hash=(path:string)=>createHash('sha256').update(readFileSync(path)).digest('hex');
const original=hash(join(source,'project.vectorcraft'));
const plan=join(root,'cancel-plan.json');
writeFileSync(plan,JSON.stringify({expectedProjectSha256:original,operations:Array.from({length:100},()=>({command:'swatch.edit',params:{name:'Brand Primary',color:input.targetColor}}))}));
const controller=new Controller(join(root,'tasks.sqlite'));
let interval:ReturnType<typeof setInterval>|undefined,id:string|undefined,checkpoint:any;
try{
  interval=setInterval(()=>{
    if(id)return;
    const task=controller.ledger.db.prepare("SELECT id,epoch FROM tasks WHERE state='running'").get() as any;
    if(!task)return;
    const events=join(controller.snapshotRoot,task.id+'-events.jsonl');if(!existsSync(events))return;
    const lines=readFileSync(events,'utf8').split('\n').filter(Boolean);
    const record=lines.map(line=>strictJson(line)).find(r=>r.event==='revision_checkpoint');
    if(record){checkpoint=record;id=task.id;controller.requestCancel(task.id,task.epoch);}
  },10);
  const request={key:'cancel-after-native-save',skill,expectedSkillSha256:skillDigest(skill),plan,
    source,output:join(root,'cancelled'),runtimeHome:runtime,python:input.python,estimatedBytes:10000000,
    authorization:{...input.authorization,deadline:Date.now()+120000,maxAttempts:1,maxBytes:10000000,readRoots:[source,root],writeRoots:[root,runtime]}};
  await assert.rejects(()=>controller.run(request),/outcome_unknown/);
  clearInterval(interval);
  assert.ok(id&&checkpoint,'real saved checkpoint must precede cancellation');
  const task=controller.ledger.get(id!);
  assert.equal(task.state,'cancel_requested');
  assert.equal(controller.processes.observe(id!,task.epoch).stopped,true);
  assert.throws(()=>controller.ledger.claim('dependent',join(source,'project.vectorcraft'),join(root,'dependent'),task.binding),/resource_busy/);
  assert.equal(hash(checkpoint.path),checkpoint.sha256);
  const inode=statSync(checkpoint.path).ino;
  const binary=join(runtime,'vectorcraft/0.2.0-craft.2/vectorcraft-cli');
  assert.equal(hash(binary),task.binding.runtimeIdentity);
  const python=`import importlib.util,json,sys\ns=importlib.util.spec_from_file_location('session',sys.argv[1]);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)\nwith m.Session([sys.argv[2],'mcp','--headless']) as session:\n session.command('document.open',{'path':sys.argv[3]})\n d=session.command('document.json',{})\n print(json.dumps({'layers':len(d['layers']),'artboards':len(d['artboards'])}))`;
  const reopened=strictJson(execFileSync(input.python,['-I','-B','-c',python,join(skill,'scripts/mcp_session.py'),binary,checkpoint.path],{encoding:'utf8'}));
  assert.equal(hash(checkpoint.path),checkpoint.sha256);assert.equal(statSync(checkpoint.path).ino,inode);
  assert.equal(hash(join(source,'project.vectorcraft')),original);
  const eventFile=join(controller.snapshotRoot,id!+'-events.jsonl');
  const events=readFileSync(eventFile,'utf8').split('\n').filter(Boolean).map(line=>strictJson(line));
  const stateRecord=events.filter(event=>event.event==='submitted');
  assert.ok(stateRecord.some(event=>event.params?.arguments?.params?.path===checkpoint.path));
  const proof={result:'PASS',level:'native-candidate',fingerprints:executionFingerprints,scope:'real saved checkpoint cancellation, owned group stop, original inode/hash readonly reopen and writer retained; no recovery completion or fixed-install claim',
    skillSha256:skillDigest(skill),runtimeSha256:hash(binary),sourceProjectSha256:original,taskId:id,epoch:task.epoch,state:task.state,
    checkpoint:{path:checkpoint.path,sha256:checkpoint.sha256,inode,readonlyReopened:reopened},eventSha256:hash(eventFile),eventCount:events.length,
    sourceUnchanged:true,nativeGroupStopped:true,dependentWriterRejected:true};
  controller.close();
  const restarted=new Controller(join(root,'tasks.sqlite'));
  try{
    const snapshotRefusals:any[]=[];
    if(input.verifyRecoverySnapshots){
      const eventBefore=hash(eventFile),attemptsBefore=restarted.ledger.get(id!).attempts;
      const resumed=await restarted.run(request);
      assert.equal(resumed.state,'cancel_requested');assert.match(resumed.resumePolicy,/no automatic replay/);
      assert.equal(restarted.ledger.get(id!).attempts,attemptsBefore);assert.equal(hash(eventFile),eventBefore);
      await assert.rejects(()=>restarted.run({...request,output:join(root,'changed-output')}),/idempotency_conflict/);
      await assert.rejects(()=>restarted.run({...request,key:'competing-after-restart',output:join(root,'competing-output')}),/resource_busy/);
      const intent=strictJson((restarted.ledger.db.prepare('SELECT intent FROM steps WHERE task=? AND n=0').get(id!) as any).intent);
      for(const [file,error,content] of [
        [join(intent.skillSnapshot,'scripts/mcp_session.py'),'skill_snapshot_mismatch',readFileSync(join(intent.skillSnapshot,'scripts/mcp_session.py'),'utf8')+'\n# replaced retained session\n'],
        [intent.planSnapshot,'recovery_plan_mismatch',JSON.stringify({...intent.plan,recoveryTamper:true})],
        [intent.controlFile,'recovery_control_mismatch',JSON.stringify({...strictJson(readFileSync(intent.controlFile,'utf8')),recoveryTamper:true})],
        [join(intent.sourceSnapshot,'manifest.json'),'recovery_source_snapshot_mismatch',readFileSync(join(intent.sourceSnapshot,'manifest.json'),'utf8')+'\n']
      ]){
        const originalBytes=readFileSync(file),mode=statSync(file).mode&0o777;
        const processes=(restarted.ledger.db.prepare('SELECT COUNT(*) AS n FROM native_processes').get() as any).n;
        try{
          chmodSync(file,0o600);writeFileSync(file,content);
          await assert.rejects(()=>restarted.reconcileOriginal(id!,task.epoch),new RegExp(error));
          assert.equal(restarted.ledger.get(id!).state,'cancel_requested');
          assert.equal((restarted.ledger.db.prepare('SELECT COUNT(*) AS n FROM native_processes').get() as any).n,processes);
          assert.equal(hash(checkpoint.path),checkpoint.sha256);assert.equal(hash(eventFile),eventBefore);
          snapshotRefusals.push({snapshot: file===intent.controlFile?'control':file===intent.planSnapshot?'plan':file===join(intent.sourceSnapshot,'manifest.json')?'source':'skill',error,inspectionProcessStarted:false,checkpointUnchanged:true});
        }finally{writeFileSync(file,originalBytes);chmodSync(file,mode);}
      }
    }
    const recovered=await restarted.reconcileOriginal(id!,task.epoch);
    assert.equal(recovered.task.state,'cancelled');assert.equal(recovered.task.epoch,task.epoch+1);
    assert.throws(()=>restarted.ledger.receipt(id!,task.epoch,0,{late:true}),/stale_epoch/);
    assert.equal(restarted.ledger.get(id!).state,'cancelled');
    const late=restarted.ledger.db.prepare('SELECT COUNT(*) AS n FROM late_receipts WHERE task=?').get(id!) as any;
    assert.equal(late.n,1);
    const completeProof={...proof,scope:'real checkpoint cancellation, native group stopped, restart readonly recovery of original files/dependencies, cancelled epoch fence and durable late receipt quarantine; no successful delivery or fixed-install claim',
      snapshotRefusals,...(input.verifyRecoverySnapshots?{readonlyRestartNoReplay:true,changedOutputRejected:true,competingSourceRejected:true}:{}),recovery:recovered.proof,settledState:recovered.task.state,settledEpoch:recovered.task.epoch,lateReceiptQuarantined:true};
    writeFileSync(join(root,'proof.json'),JSON.stringify(completeProof,null,2));console.log(JSON.stringify(completeProof,null,2));
  }finally{restarted.close();}
}finally{clearInterval(interval);controller.close();}
