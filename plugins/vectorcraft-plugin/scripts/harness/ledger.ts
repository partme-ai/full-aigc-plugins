import { DatabaseSync } from 'node:sqlite';
import { createHash, randomUUID } from 'node:crypto';
import { existsSync, realpathSync, rmSync } from 'node:fs';
import { resolve, dirname, basename } from 'node:path';
import {tmpdir} from 'node:os';
import {authorizedDirectory} from './authorized_tree.ts';
import {authorizedCopy,authorizedDigest} from './authorized_file.ts';
import { canonical, strictJson } from '../../src/strict_json.ts';

export type Authorization={objects:number[],fields:string[],deadline:number,maxAttempts:number,maxBytes:number,budgetId?:string};
export type Binding={launchProtocol?:'registered-go/v1',launchContext?:{skill:string,plan:string,runtimeHome:string,python:string,source:string|null},executionMode?:'headless'|'bridge',skillSha256?:string,planHash:string,inputHashes:Record<string,string>,projectRevision:string|null,runtimeIdentity:string,authorization:Authorization};
const digest=(v:any)=>createHash('sha256').update(canonical(v)).digest('hex');

/** 规范化资源身份；符号链接别名不能取得第二份工程占用。 */
export function resourcePath(path:string):string {
  const absolute=resolve(path);
  return existsSync(absolute)?realpathSync(absolute):resolve(resourcePath(dirname(absolute)),basename(absolute));
}

/** SQLite 持久账本：事务提交意图后才允许调用原生端。 */
export class Ledger {
  db:DatabaseSync;closed=false;schemaBackup?:{path:string,fromSchema:number,toSchema:number,sha256:string};
  constructor(path:string) {
    this.db=new DatabaseSync(path);this.db.exec('PRAGMA busy_timeout=3000; PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON;');
    const version=this.db.prepare('PRAGMA user_version').get() as any;
    if(version.user_version!==0&&version.user_version!==1&&version.user_version!==2&&version.user_version!==3){this.db.close();throw new Error('incompatible_state_schema');}
    if(version.user_version===1||version.user_version===2){
      // VACUUM INTO包含已提交WAL数据；先保留只读一致快照，备份失败不得继续迁移。
      const directory=resolve(dirname(resourcePath(path)),'state-schema-backups');
      const backup=resolve(directory,basename(path)+'.before-schema3-'+randomUUID()+'.sqlite');
      let staging:string|undefined;
      try{
        authorizedDirectory(directory,dirname(directory));
        // SQLite不能使用本机目录fd路径。只向宿主随机私有暂存写入，再安全发布备份。
        const temporaryRoot=realpathSync(tmpdir());
        const candidate=resolve(temporaryRoot,'vectorcraft-state-backup-'+randomUUID());
        authorizedDirectory(candidate,temporaryRoot,true);staging=candidate;
        const staged=resolve(staging,'snapshot.sqlite');
        this.db.prepare('VACUUM INTO ?').run(staged);
        const expected=authorizedDigest(staged,[staging]);
        const snapshot=new DatabaseSync(staged,{readOnly:true});let snapshotVersion:number;
        try{snapshotVersion=(snapshot.prepare('PRAGMA user_version').get() as any).user_version;}finally{snapshot.close();}
        if(snapshotVersion!==version.user_version)throw new Error('incompatible_backup_schema');
        authorizedCopy(staged,[staging],backup,directory,expected);
        if(authorizedDigest(backup,[directory])!==expected)throw new Error('state_backup_digest_mismatch');
        this.schemaBackup={path:backup,fromSchema:snapshotVersion,toSchema:3,sha256:expected};
      }catch(error){this.db.close();this.closed=true;throw new Error('state_backup_failed; schema not migrated: '+String(error));}
      finally{
        if(staging){try{rmSync(staging,{recursive:true,force:true});}catch(error){
          if(!this.closed){this.db.close();this.closed=true;}
          throw new Error('state_backup_failed; staging cleanup failed; schema not migrated: '+String(error));
        }}
      }
    }
    try{
      this.db.exec('BEGIN IMMEDIATE');
      this.db.exec(`CREATE TABLE IF NOT EXISTS tasks (
      id TEXT PRIMARY KEY, key TEXT UNIQUE NOT NULL, resource TEXT NOT NULL, output TEXT NOT NULL,
      binding_hash TEXT NOT NULL, binding TEXT NOT NULL, epoch INTEGER NOT NULL DEFAULT 1,
      state TEXT NOT NULL, attempts INTEGER NOT NULL DEFAULT 0, bytes INTEGER NOT NULL DEFAULT 0, reason TEXT);
      CREATE UNIQUE INDEX IF NOT EXISTS single_writer ON tasks(resource)
        WHERE state IN ('ready','running','reconciling','cancel_requested');
      CREATE TRIGGER IF NOT EXISTS single_output_owner BEFORE INSERT ON tasks
      WHEN EXISTS(SELECT 1 FROM tasks WHERE output=NEW.output AND state IN ('ready','running','reconciling','cancel_requested'))
      BEGIN SELECT RAISE(ABORT,'output_busy'); END;
      CREATE TABLE IF NOT EXISTS steps(task TEXT REFERENCES tasks(id), n INTEGER, intent TEXT NOT NULL,
        state TEXT NOT NULL, result TEXT, PRIMARY KEY(task,n));
      CREATE TABLE IF NOT EXISTS native_launches(task TEXT REFERENCES tasks(id),epoch INTEGER NOT NULL,
        protocol TEXT NOT NULL,state TEXT NOT NULL CHECK(state IN ('prepared','authorized','sealed')),
        intent_sha256 TEXT,PRIMARY KEY(task,epoch));
      CREATE TABLE IF NOT EXISTS budgets(id TEXT PRIMARY KEY,policy TEXT NOT NULL,attempts INTEGER NOT NULL DEFAULT 0,bytes INTEGER NOT NULL DEFAULT 0);
      CREATE TABLE IF NOT EXISTS budget_cancellations(id TEXT PRIMARY KEY REFERENCES budgets(id),task TEXT NOT NULL,epoch INTEGER NOT NULL,requested_at INTEGER NOT NULL);
      CREATE TRIGGER IF NOT EXISTS cancelled_budget_admission BEFORE INSERT ON tasks
      WHEN EXISTS(SELECT 1 FROM budget_cancellations WHERE id=COALESCE(json_extract(NEW.binding,'$.authorization.budgetId'),NEW.id))
      BEGIN SELECT RAISE(ABORT,'budget_cancel_requested'); END;
      CREATE TRIGGER IF NOT EXISTS cancelled_budget_step BEFORE INSERT ON steps
      WHEN EXISTS(SELECT 1 FROM tasks,budget_cancellations WHERE tasks.id=NEW.task AND budget_cancellations.id=COALESCE(json_extract(tasks.binding,'$.authorization.budgetId'),tasks.id))
      BEGIN SELECT RAISE(ABORT,'budget_cancel_requested'); END;
      CREATE TABLE IF NOT EXISTS late_receipts(id INTEGER PRIMARY KEY,task TEXT NOT NULL,epoch INTEGER NOT NULL,n INTEGER NOT NULL,result TEXT NOT NULL,received_at INTEGER NOT NULL);
      CREATE TABLE IF NOT EXISTS runtime_selection(id INTEGER PRIMARY KEY CHECK(id=1),active TEXT NOT NULL,previous TEXT);
      -- 旧阅读器可能已经打开连接；数据库触发器使它同样遵守新选择与schema约束。
      CREATE TRIGGER IF NOT EXISTS selected_runtime_writer BEFORE INSERT ON tasks
      WHEN EXISTS(SELECT 1 FROM runtime_selection WHERE id=1)
      BEGIN
        SELECT CASE
          WHEN (SELECT json_extract(active,'$.mode') FROM runtime_selection WHERE id=1)
            IS NOT COALESCE(json_extract(NEW.binding,'$.executionMode'),'headless')
            THEN RAISE(ABORT,'runtime_mode_mismatch')
          WHEN (SELECT json_extract(active,'$.binarySha256') FROM runtime_selection WHERE id=1)
            IS NOT json_extract(NEW.binding,'$.runtimeIdentity')
            THEN RAISE(ABORT,'runtime_selection_mismatch')
          WHEN NOT EXISTS(SELECT 1 FROM runtime_selection,json_each(runtime_selection.active,'$.stateSchemas')
            WHERE runtime_selection.id=1 AND json_each.value=(SELECT user_version FROM pragma_user_version))
            THEN RAISE(ABORT,'incompatible_state_schema')
        END;
      END;
      PRAGMA user_version=3;`);
      this.db.exec('COMMIT');
    }catch(error){try{this.db.exec('ROLLBACK');}catch{}this.db.close();this.closed=true;throw error;}
  }
  transaction<T>(fn:()=>T):T {
    this.db.exec('BEGIN IMMEDIATE');try{const result=fn();this.db.exec('COMMIT');return result;}
    catch(error){this.db.exec('ROLLBACK');throw error;}
  }
  get(id:string):any {
    const row=this.db.prepare('SELECT * FROM tasks WHERE id=?').get(id) as any;
    if(!row)throw new Error('unknown_task');
    return {...row,binding:strictJson(row.binding),bytesReserved:row.bytes};
  }
  checked(id:string,epoch:number):any {
    const row=this.get(id);if(row.epoch!==epoch)throw new Error('stale_epoch');return row;
  }
  claim(key:string,resource:string,output:string,binding:Binding):any {
    const auth=binding.authorization;
    if((binding.launchProtocol!==undefined&&(binding.launchProtocol!=='registered-go/v1'||!binding.launchContext))||(binding.executionMode!==undefined&&!['headless','bridge'].includes(binding.executionMode))||(binding.skillSha256!==undefined&&!/^[a-f0-9]{64}$/.test(binding.skillSha256))||!key||![binding.planHash,binding.runtimeIdentity,...Object.values(binding.inputHashes)].every(h=>/^[a-f0-9]{64}$/.test(h))
      ||(auth.budgetId!==undefined&&(typeof auth.budgetId!=='string'||!auth.budgetId))
      ||!Array.isArray(auth.objects)||auth.objects.some(x=>!Number.isSafeInteger(x)||x<=0)
      ||!Array.isArray(auth.fields)||auth.fields.some(x=>typeof x!=='string'||!x)
      ||![auth.deadline,auth.maxAttempts,auth.maxBytes].every(x=>Number.isSafeInteger(x)&&x>0)) throw new Error('invalid_task_binding');
    const owner=resourcePath(resource), destination=resourcePath(output),fingerprint=digest({owner,destination,binding});
    return this.transaction(()=>{
      const previous=this.db.prepare('SELECT id,binding_hash FROM tasks WHERE key=?').get(key) as any;
      if(previous){if(previous.binding_hash!==fingerprint)throw new Error('idempotency_conflict');return this.get(previous.id);}
      // 与升级激活共用BEGIN IMMEDIATE，阻止排空检查和新任务占用之间的竞争。
      if(this.db.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name='runtime_selection'").get()){
        const selected=this.db.prepare('SELECT active FROM runtime_selection WHERE id=1').get() as any;
        if(selected){const active=strictJson(selected.active);
          if(active.mode!==(binding.executionMode??'headless'))throw new Error('runtime_mode_mismatch');
          if(active.binarySha256!==binding.runtimeIdentity)throw new Error('runtime_selection_mismatch');
          if(!active.stateSchemas?.includes((this.db.prepare('PRAGMA user_version').get() as any).user_version))throw new Error('incompatible_state_schema');
        }
      }
      if(auth.deadline<=Date.now())throw new Error('budget_exceeded');
      if(this.db.prepare("SELECT id FROM tasks WHERE resource=? AND state IN ('ready','running','reconciling','cancel_requested')").get(owner))throw new Error('resource_busy');
      if(this.db.prepare("SELECT id FROM tasks WHERE output=? AND state IN ('ready','running','reconciling','cancel_requested')").get(destination))throw new Error('output_busy');
      const id=randomUUID(),budgetId=auth.budgetId??id;
      const policy=canonical({deadline:auth.deadline,maxAttempts:auth.maxAttempts,maxBytes:auth.maxBytes});
      const previousBudget=this.db.prepare('SELECT policy,attempts,bytes FROM budgets WHERE id=?').get(budgetId) as any;
      if(this.db.prepare('SELECT id FROM budget_cancellations WHERE id=?').get(budgetId))throw new Error('budget_cancel_requested');
      if(previousBudget&&previousBudget.policy!==policy)throw new Error('shared_budget_conflict');
      if(previousBudget&&(previousBudget.attempts>=auth.maxAttempts||previousBudget.bytes>=auth.maxBytes))throw new Error('budget_exceeded');
      this.db.prepare('INSERT OR IGNORE INTO budgets(id,policy) VALUES(?,?)').run(budgetId,policy);
      this.db.prepare('INSERT INTO tasks(id,key,resource,output,binding_hash,binding,state) VALUES(?,?,?,?,?,?,?)')
        .run(id,key,owner,destination,fingerprint,canonical(binding),'ready');
      if(binding.launchProtocol)this.db.prepare("INSERT INTO native_launches(task,epoch,protocol,state) VALUES(?,1,?,'prepared')").run(id,binding.launchProtocol);
      return this.get(id);
    });
  }
  intent(id:string,epoch:number,step:number,request:any,bytes:number):any {
    return this.transaction(()=>{
      const task=this.checked(id,epoch);
      if(task.state==='reconciling')throw new Error('reconcile_required');
      if(task.state==='cancel_requested'||task.state==='cancelled')throw new Error(task.state);
      if(!['ready','running'].includes(task.state))throw new Error('task_not_running');
      if(!Number.isSafeInteger(step)||step<0||!Number.isSafeInteger(bytes)||bytes<0)throw new Error('invalid_step_budget');
      if(this.db.prepare('SELECT n FROM steps WHERE task=? AND n=?').get(id,step))throw new Error('step_already_submitted');
      const auth=task.binding.authorization;
      const budgetId=auth.budgetId??task.id;
      // 旧 v1 账本的任务在首次继续时迁入私有预算，不能重置已经消耗的额度。
      this.db.prepare('INSERT OR IGNORE INTO budgets(id,policy,attempts,bytes) VALUES(?,?,?,?)').run(budgetId,canonical({deadline:auth.deadline,maxAttempts:auth.maxAttempts,maxBytes:auth.maxBytes}),task.attempts,task.bytes);
      const budget=this.db.prepare('SELECT attempts,bytes FROM budgets WHERE id=?').get(budgetId) as any;
      if(Date.now()>=auth.deadline||budget.attempts+1>auth.maxAttempts||budget.bytes+bytes>auth.maxBytes)throw new Error('budget_exceeded');
      this.db.prepare('UPDATE budgets SET attempts=attempts+1,bytes=bytes+? WHERE id=?').run(bytes,budgetId);
      this.db.prepare("INSERT INTO steps(task,n,intent,state) VALUES(?,?,?,'submitted')").run(id,step,canonical(request));
      this.db.prepare("UPDATE tasks SET state='running',attempts=attempts+1,bytes=bytes+? WHERE id=?").run(bytes,id);
      return this.get(id);
    });
  }
  /** 与恢复封存互斥地提交GO授权；提交完成之前不得写启动器stdin。 */
  authorizeLaunch(id:string,epoch:number){
    return this.transaction(()=>{
      const task=this.checked(id,epoch),gate=this.db.prepare('SELECT * FROM native_launches WHERE task=? AND epoch=?').get(id,epoch) as any;
      if(task.state!=='running'||Date.now()>=task.binding.authorization.deadline||task.binding.launchProtocol!=='registered-go/v1'||gate?.protocol!==task.binding.launchProtocol||gate.state!=='prepared')throw new Error('launch_not_authorized');
      const step=this.db.prepare('SELECT intent,state,result FROM steps WHERE task=? AND n=0').get(id) as any;
      if(!step||step.state!=='submitted'||step.result!==null)throw new Error('launch_not_authorized');
      if(!this.db.prepare('SELECT task FROM native_processes WHERE task=? AND epoch=?').get(id,epoch))throw new Error('native_process_identity_missing');
      this.db.prepare("UPDATE native_launches SET state='authorized',intent_sha256=? WHERE task=? AND epoch=?").run(digest(step.intent),id,epoch);
    });
  }
  /** 新协议的未授权任务先封存再检查；无门禁或旧协议不能凭缺少事件推断未调用。 */
  sealUnlaunched(id:string,epoch:number):any {
    return this.transaction(()=>{
      const task=this.checked(id,epoch);
      if(task.binding.launchProtocol===undefined)return null;
      const gate=this.db.prepare('SELECT * FROM native_launches WHERE task=? AND epoch=?').get(id,epoch) as any;
      if(task.binding.launchProtocol!=='registered-go/v1'||gate?.protocol!==task.binding.launchProtocol||!['prepared','authorized','sealed'].includes(gate.state))throw new Error('recovery_launch_identity_missing');
      if(gate.state==='authorized'){
        const step=this.db.prepare('SELECT intent FROM steps WHERE task=? AND n=0').get(id) as any;
        if(!step||gate.intent_sha256!==digest(step.intent))throw new Error('recovery_launch_identity_mismatch');
        return null;
      }
      if(gate.intent_sha256!==null)throw new Error('recovery_launch_identity_mismatch');
      if(!['ready','running','reconciling','cancel_requested'].includes(task.state))throw new Error('task_not_recoverable');
      this.db.prepare("UPDATE native_launches SET state='sealed' WHERE task=? AND epoch=?").run(id,epoch);
      this.db.prepare("UPDATE tasks SET state=CASE WHEN state='cancel_requested' THEN state ELSE 'reconciling' END WHERE id=?").run(id);
      return this.db.prepare('SELECT * FROM native_launches WHERE task=? AND epoch=?').get(id,epoch);
    });
  }
  receipt(id:string,epoch:number,step:number,result:any):any {
    const current=this.get(id);
    if(current.epoch!==epoch){
      this.db.prepare('INSERT INTO late_receipts(task,epoch,n,result,received_at) VALUES(?,?,?,?,?)').run(id,epoch,step,canonical(result),Date.now());
      throw new Error('stale_epoch: receipt quarantined');
    }
    return this.transaction(()=>{
      const task=this.checked(id,epoch);
      if(task.state==='cancel_requested'||task.state==='cancelled'){
        this.db.prepare("UPDATE steps SET state='quarantined',result=? WHERE task=? AND n=? AND state='submitted'").run(canonical(result),id,step);
        return {state:'quarantined',result};
      }
      if(task.state!=='running')throw new Error('task_not_running');
      const updated=this.db.prepare("UPDATE steps SET state='received',result=? WHERE task=? AND n=? AND state='submitted'").run(canonical(result),id,step);
      if(updated.changes!==1)throw new Error('unexpected_step_receipt');return this.get(id);
    });
  }
  unknown(id:string,epoch:number,reason:string):any {
    return this.transaction(()=>{const task=this.checked(id,epoch);
      if(!['running','reconciling','cancel_requested'].includes(task.state))throw new Error('task_not_running');
      this.db.prepare("UPDATE tasks SET state=CASE WHEN state='cancel_requested' THEN state ELSE 'reconciling' END,reason=? WHERE id=?").run(reason,id);
      return this.get(id);
    });
  }
  reconcile(id:string,epoch:number,observation:{stopped:boolean,verified:boolean}):any {
    return this.transaction(()=>{
      const task=this.checked(id,epoch);
      if(task.state!=='reconciling')throw new Error('task_not_reconciling');
      if(observation.stopped!==true)throw new Error('native_stop_unconfirmed');
      if(observation.verified!==true)throw new Error('original_artifact_unverified');
      throw new Error('native_observation_required: booleans cannot prove process stop or original artifact verification');
    });
  }
  cancel(id:string,epoch:number,confirmed:boolean):any {
    return this.transaction(()=>{
      const task=this.checked(id,epoch);
      if(!['ready','running','reconciling','cancel_requested'].includes(task.state))throw new Error('task_not_cancellable');
      if(confirmed)throw new Error('native_observation_required: cancellation cannot release a writer using a boolean');
      const auth=task.binding.authorization,budgetId=auth.budgetId??task.id;
      this.db.prepare('INSERT OR IGNORE INTO budgets(id,policy,attempts,bytes) VALUES(?,?,?,?)').run(budgetId,canonical({deadline:auth.deadline,maxAttempts:auth.maxAttempts,maxBytes:auth.maxBytes}),task.attempts,task.bytes);
      this.db.prepare('INSERT OR IGNORE INTO budget_cancellations(id,task,epoch,requested_at) VALUES(?,?,?,?)').run(budgetId,id,epoch,Date.now());
      this.db.prepare("UPDATE tasks SET state='cancel_requested' WHERE COALESCE(json_extract(binding,'$.authorization.budgetId'),id)=? AND state IN ('ready','running','reconciling','cancel_requested')").run(budgetId);
      return this.get(id);
    });
  }
  complete(id:string,epoch:number,proof?:{technical:boolean,accepted:boolean}):any {
    return this.transaction(()=>{
      const task=this.checked(id,epoch);
      if(task.state!=='review_ready'||proof?.technical!==true||proof?.accepted!==true)throw new Error('acceptance_required');
      this.db.prepare("UPDATE tasks SET state='completed' WHERE id=?").run(id);return this.get(id);
    });
  }
  verified(id:string,epoch:number,artifact:{path:string,sha256:string}):any {
    return this.transaction(()=>{
      const task=this.checked(id,epoch);
      if(task.state!=='running')throw new Error('task_not_running');
      if(this.db.prepare("SELECT n FROM steps WHERE task=? AND state!='received'").get(id))throw new Error('unresolved_native_step');
      if(authorizedDigest(artifact.path,[task.output])!==artifact.sha256)throw new Error('artifact_revision_conflict');
      this.db.prepare("UPDATE tasks SET state='review_ready' WHERE id=?").run(id);return this.get(id);
    });
  }
  close(){if(!this.closed){this.db.close();this.closed=true;}}
}
