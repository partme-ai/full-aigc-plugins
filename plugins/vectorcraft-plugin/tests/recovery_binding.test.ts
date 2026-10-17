import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,mkdirSync,writeFileSync,readFileSync,rmSync,lstatSync,unlinkSync,symlinkSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {createHash} from 'node:crypto';
import {Ledger} from '../scripts/harness/ledger.ts';
import {Recovery} from '../scripts/harness/recovery.ts';
import {skillDigest} from '../scripts/harness/controller.ts';
import {canonical} from '../src/strict_json.ts';
// 仅核验恢复启动前的快照门禁；不把合成事件当作原生重开证据。
const sha=(s:string|Buffer)=>createHash('sha256').update(s).digest('hex');
function fixture(change:string){
 const root=mkdtempSync(join(tmpdir(),'vector-recovery-binding-')),skill=join(root,'skill');mkdirSync(join(skill,'scripts'),{recursive:true});
 writeFileSync(join(skill,'scripts/mcp_session.py'),'# bound session fixture\n');
 const plan={operations:[]},planSnapshot=join(root,'plan.json');writeFileSync(planSnapshot,canonical(plan));
 const ledger=new Ledger(join(root,'state.sqlite')),authorization={objects:[3],fields:['paint.color'],deadline:Date.now()+60000,maxAttempts:1,maxBytes:10000};
 const binding={skillSha256:skillDigest(skill),planHash:sha(canonical(plan)),inputHashes:{},projectRevision:null,runtimeIdentity:'b'.repeat(64),authorization};
 const task=ledger.claim('interrupted',join(root,'source.vectorcraft'),join(root,'output'),binding);
 const eventFile=join(root,'events.jsonl');writeFileSync(eventFile,'');const stat=lstatSync(eventFile),controlFile=join(root,'control.json');
 const profile={task:task.id,epoch:task.epoch,planHash:binding.planHash,planFile:planSnapshot,eventFile,eventInode:stat.ino,eventDevice:stat.dev,runtimeIdentity:binding.runtimeIdentity,authorization};
 writeFileSync(controlFile,canonical(profile));const controlSha256=sha(readFileSync(controlFile));
 const sourceSnapshot=join(root,'source-snapshot');
 if(change.startsWith('source-')){mkdirSync(sourceSnapshot);writeFileSync(join(sourceSnapshot,'project.vectorcraft'),'bound source bytes');}
 const sourceIdentity=change.startsWith('source-')?{source:join(root,'original-source'),sourceSnapshot,...(change==='source-missing-hash'?{}:{sourceSnapshotSha256:skillDigest(sourceSnapshot)})}:{};
 ledger.intent(task.id,task.epoch,0,{...sourceIdentity,skillSha256:binding.skillSha256,skillSnapshot:skill,planHash:binding.planHash,plan,planSnapshot,controlFile,...(change==='missing-control-hash'?{}:{controlSha256}),runtimeHome:join(root,'runtime'),python:'python3'},1000);
 ledger.cancel(task.id,task.epoch,false);
 if(change==='skill')writeFileSync(join(skill,'scripts/mcp_session.py'),'# replaced executable\n');
 if(change==='plan')writeFileSync(planSnapshot,'{"operations":[{"command":"changed"}]}');
 if(change==='control')writeFileSync(controlFile,canonical({...profile,authorization:{...authorization,fields:['structure']}}));
 if(change==='symlink-plan'){const other=join(root,'other.json');writeFileSync(other,canonical(plan));unlinkSync(planSnapshot);symlinkSync(other,planSnapshot);}
 if(change==='source-edited')writeFileSync(join(sourceSnapshot,'project.vectorcraft'),'changed source bytes');
 if(change==='source-deleted')unlinkSync(join(sourceSnapshot,'project.vectorcraft'));
 if(change==='source-added')writeFileSync(join(sourceSnapshot,'unexpected.json'),'{}');
 if(change==='source-symlink'){unlinkSync(join(sourceSnapshot,'project.vectorcraft'));symlinkSync(planSnapshot,join(sourceSnapshot,'project.vectorcraft'));}
 if(change==='source-missing-directory')rmSync(sourceSnapshot,{recursive:true});
 return {root,ledger,task,recovery:new Recovery(ledger,{observe:()=>({stopped:true})} as any),close(){ledger.close();rmSync(root,{recursive:true,force:true});}};
}
for(const [change,error] of [['skill','skill_snapshot_mismatch'],['plan','recovery_plan_mismatch'],['control','recovery_control_mismatch'],['missing-control-hash','recovery_identity_missing'],['symlink-plan','recovery_snapshot_symlink'],['unchanged','original_stage_identity_missing'],['source-edited','recovery_source_snapshot_mismatch'],['source-deleted','recovery_source_snapshot_mismatch'],['source-added','recovery_source_snapshot_mismatch'],['source-symlink','recovery_source_snapshot_mismatch'],['source-missing-directory','recovery_source_snapshot_mismatch'],['source-missing-hash','recovery_identity_missing'],['source-unchanged','original_stage_identity_missing']]){
 test('recovery refuses '+change+' before any inspection process or proof',async()=>{
  const f=fixture(change);try{
   await assert.rejects(()=>f.recovery.inspect(f.task.id,f.task.epoch),new RegExp(error));
   assert.equal(f.ledger.get(f.task.id).state,'cancel_requested');assert.equal(f.ledger.get(f.task.id).attempts,1);
   assert.equal((f.ledger.db.prepare('SELECT COUNT(*) AS n FROM recovery_checks').get() as any).n,0);
  }finally{f.close();}
 });
}
