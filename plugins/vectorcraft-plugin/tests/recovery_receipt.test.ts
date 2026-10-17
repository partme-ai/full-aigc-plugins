import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,mkdirSync,writeFileSync,readFileSync,rmSync,lstatSync,unlinkSync,realpathSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {createHash} from 'node:crypto';
import {Ledger} from '../scripts/harness/ledger.ts';
import {Recovery} from '../scripts/harness/recovery.ts';
import {skillDigest} from '../scripts/harness/skill_digest.ts';
import {canonical} from '../src/strict_json.ts';
const sha=(value:string|Buffer)=>createHash('sha256').update(value).digest('hex');
// 合成账本只验证原生启动前的回执门禁；不声明原生工程验收。
function fixture(change:string){
 const root=realpathSync(mkdtempSync(join(tmpdir(),'vector-receipt-'))),skill=join(root,'skill');mkdirSync(join(skill,'scripts'),{recursive:true});
 writeFileSync(join(skill,'scripts/mcp_session.py'),'# receipt fixture\n');
 const ledger=new Ledger(join(root,'state.sqlite')),plan={operations:[]},planSnapshot=join(root,'plan.json');writeFileSync(planSnapshot,canonical(plan));
 const binding={skillSha256:skillDigest(skill),planHash:sha(canonical(plan)),runtimeIdentity:'b'.repeat(64),projectRevision:null,inputHashes:{},authorization:{objects:[],fields:[],maxAttempts:1,maxBytes:10000,deadline:Date.now()+60000}};
 const output=join(root,'output'),task=ledger.claim('one',join(root,'source.vectorcraft'),output,binding);mkdirSync(output);
 const project=join(output,'project.vectorcraft');writeFileSync(project,'synthetic native placeholder');
 const manifestFile=join(output,'manifest.json'),manifest={schema:'vectorcraft-delivery/v1',sourceProjectSha256:null,runtimeSha256:binding.runtimeIdentity,files:{'project.vectorcraft':sha(readFileSync(project))}};
 writeFileSync(manifestFile,canonical(manifest));
 const eventFile=join(root,'events.jsonl'),stage=lstatSync(output);
 const initial=join(root,'initial-stage');if(change.startsWith('prepared-'))mkdirSync(initial);
 const initialStat=change.startsWith('prepared-')?lstatSync(initial):stage;
 const initialPath=change.startsWith('prepared-')?initial:output;
 const eventRecords=[{event:'stage_created',task:task.id,epoch:task.epoch,path:initialPath,inode:initialStat.ino,device:initialStat.dev}];
 if(change.startsWith('prepared-'))eventRecords.push({event:'delivery_prepared',task:task.id,epoch:task.epoch,path:join(initial,'delivery'),output:change==='prepared-wrong-output'?join(root,'wrong-output'):output,inode:stage.ino,device:stage.dev,manifestSha256:change==='prepared-bad-digest'?'f'.repeat(64):sha(readFileSync(manifestFile))} as any);
 writeFileSync(eventFile,eventRecords.map(canonical).join('\n')+'\n');
 const eventStat=lstatSync(eventFile),controlFile=join(root,'control.json');writeFileSync(controlFile,canonical({task:task.id,epoch:task.epoch,planHash:binding.planHash,eventFile,eventInode:eventStat.ino,eventDevice:eventStat.dev}));
 ledger.intent(task.id,task.epoch,0,{skillSha256:binding.skillSha256,skillSnapshot:skill,planHash:binding.planHash,plan,planSnapshot,controlFile,controlSha256:sha(readFileSync(controlFile)),runtimeHome:join(root,'missing-runtime'),python:'python3'},1000);
 if(change!=='no-receipt')ledger.receipt(task.id,task.epoch,0,{manifestSha256:sha(readFileSync(manifestFile)),runtimeIdentity:binding.runtimeIdentity});
 ledger.unknown(task.id,task.epoch,'synthetic crash after receipt');
 if(change==='manifest-missing')unlinkSync(manifestFile);
 if(change==='manifest-changed')writeFileSync(manifestFile,canonical({...manifest,tampered:true}));
 if(change==='artifact-changed')writeFileSync(project,'replaced project');
 if(change==='runtime')ledger.db.prepare('UPDATE steps SET result=? WHERE task=?').run(canonical({manifestSha256:sha(readFileSync(manifestFile)),runtimeIdentity:'c'.repeat(64)}),task.id);
 if(change==='malformed')ledger.db.prepare('UPDATE steps SET result=? WHERE task=?').run('{broken',task.id);
 if(change==='invalid-state')ledger.db.prepare("UPDATE steps SET state='submitted' WHERE task=?").run(task.id);
 if(change==='missing-result')ledger.db.prepare('UPDATE steps SET result=NULL WHERE task=?').run(task.id);
 return {root,ledger,task,recovery:new Recovery(ledger,{observe:()=>({stopped:true})} as any),close(){ledger.close();rmSync(root,{recursive:true,force:true});}};
}
for(const change of ['manifest-missing','manifest-changed','artifact-changed','runtime','malformed','invalid-state','missing-result']){
 test('recovery refuses persisted receipt '+change+' before native inspection',async()=>{
  const f=fixture(change);try{
   await assert.rejects(()=>f.recovery.inspect(f.task.id,f.task.epoch),/recovery_receipt_mismatch/);
   assert.equal(f.ledger.get(f.task.id).state,'reconciling');assert.equal(f.ledger.get(f.task.id).attempts,1);
   assert.equal((f.ledger.db.prepare('SELECT COUNT(*) AS n FROM recovery_checks').get() as any).n,0);
  }finally{f.close();}
 });
}
for(const change of ['valid','no-receipt','prepared-valid']){
 test('recovery '+change+' reaches the subsequent runtime identity gate',async()=>{
  const f=fixture(change);try{
   await assert.rejects(()=>f.recovery.inspect(f.task.id,f.task.epoch),/ENOENT/);
   assert.equal((f.ledger.db.prepare('SELECT COUNT(*) AS n FROM recovery_checks').get() as any).n,0);
  }finally{f.close();}
 });
}

for(const change of ['prepared-wrong-output','prepared-bad-digest']){
 test('recovery refuses '+change+' without launching native inspection',async()=>{
  const f=fixture(change);try{
   await assert.rejects(()=>f.recovery.inspect(f.task.id,f.task.epoch),/recovery_delivery_mismatch/);
   assert.equal(f.ledger.get(f.task.id).state,'reconciling');
   assert.equal((f.ledger.db.prepare('SELECT COUNT(*) AS n FROM recovery_checks').get() as any).n,0);
  }finally{f.close();}
 });
}
