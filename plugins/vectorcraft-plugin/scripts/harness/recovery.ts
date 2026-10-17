import {nativeEnvironment} from './native_environment.ts';
import { createHash,randomUUID } from 'node:crypto';
import { readFileSync, lstatSync, readdirSync, existsSync } from 'node:fs';
import { join,dirname,relative,isAbsolute } from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import type { Ledger } from './ledger.ts';
import { ProcessRegistry } from './process_registry.ts';
import {LaunchRecovery} from './launch_recovery.ts';
import {skillDigest} from './skill_digest.ts';
import { strictJson,canonical } from '../../src/strict_json.ts';
const hash=(p:string)=>createHash('sha256').update(readFileSync(p)).digest('hex');
const inside=(root:string,p:string)=>{const r=relative(root,p);return !isAbsolute(r)&&r!=='..'&&!r.startsWith('../');};

/** 停止后只读核验原暂存文件；未知阶段不会因此成为成功交付。 */
export class Recovery {
  ledger:Ledger;processes:ProcessRegistry;
  constructor(ledger:Ledger,processes:ProcessRegistry){this.ledger=ledger;this.processes=processes;
    ledger.db.exec('CREATE TABLE IF NOT EXISTS recovery_checks(id TEXT PRIMARY KEY,task TEXT NOT NULL,epoch INTEGER NOT NULL,intent TEXT NOT NULL,result TEXT);');
  }
  /** 已有完成回执必须绑定原清单及全部文件；检查后不能换用另一个步骤回执。 */
  receiptIdentity(task:any,stage:string,files:Record<string,{sha256:string}>,expected?:string):string {
    const step=this.ledger.db.prepare('SELECT intent,state,result FROM steps WHERE task=? AND n=0').get(task.id) as any;
    if(!step)throw new Error('original_request_missing');
    const identity=createHash('sha256').update(canonical(step)).digest('hex');
    if(expected!==undefined&&identity!==expected)throw new Error('recovery_receipt_changed');
    if(step.result===null){
      if(step.state!=='submitted')throw new Error('recovery_receipt_mismatch');
      return identity;
    }
    try{
      if(!['received','quarantined'].includes(step.state))throw new Error('invalid_receipt_state');
      const receipt=strictJson(step.result),path=join(stage,'manifest.json');
      if(!receipt||typeof receipt!=='object'||Array.isArray(receipt)||receipt.runtimeIdentity!==task.binding.runtimeIdentity
          ||!files[path]||receipt.manifestSha256!==files[path].sha256)throw new Error('invalid_receipt_binding');
      this.deliveryIdentity(task,stage,files,receipt.manifestSha256);
    }catch{throw new Error('recovery_receipt_mismatch');}
    return identity;
  }
  /** 清单必须绑定同一运行时、源修订和全部真实文件，不以清单存在代替一致性。 */
  deliveryIdentity(task:any,stage:string,files:Record<string,{sha256:string}>,expected:string){
    const path=join(stage,'manifest.json');
    if(!/^[a-f0-9]{64}$/.test(expected)||files[path]?.sha256!==expected)throw new Error('invalid_delivery_digest');
      const manifest=strictJson(readFileSync(path,'utf8'));
      if(manifest.schema!=='vectorcraft-delivery/v1'||manifest.runtimeSha256!==task.binding.runtimeIdentity
          ||manifest.sourceProjectSha256!==task.binding.projectRevision||!manifest.files||typeof manifest.files!=='object'
          ||Array.isArray(manifest.files)||!manifest.files['project.vectorcraft'])throw new Error('invalid_receipt_manifest');
      for(const [name,digest] of Object.entries(manifest.files)){
        if(isAbsolute(name)||name.includes('\\')||name.split('/').some(part=>['','..','.'].includes(part))
            ||typeof digest!=='string'||!/^[a-f0-9]{64}$/.test(digest)||files[join(stage,name)]?.sha256!==digest)throw new Error('invalid_receipt_artifact');
      }
  }
  async inspect(taskId:string,epoch:number):Promise<any>{
    if(this.ledger.sealUnlaunched(taskId,epoch))return new LaunchRecovery(this.ledger,this.processes).inspect(taskId,epoch);
    const task=this.ledger.checked(taskId,epoch);
    if(!['cancel_requested','reconciling'].includes(task.state))throw new Error('task_not_recoverable');
    if(!this.processes.observe(taskId,epoch).stopped)throw new Error('native_stop_unconfirmed');
    const step=this.ledger.db.prepare('SELECT intent FROM steps WHERE task=? AND n=0').get(taskId) as any;
    if(!step)throw new Error('original_request_missing');
    const intent=strictJson(step.intent);
    // 未记录控制文件摘要的旧任务保持占用，不能执行未经绑定的恢复脚本。
    if(!/^[a-f0-9]{64}$/.test(intent.controlSha256??'')||!task.binding.skillSha256)throw new Error('recovery_identity_missing');
    if(intent.skillSha256!==task.binding.skillSha256||skillDigest(intent.skillSnapshot)!==task.binding.skillSha256)throw new Error('skill_snapshot_mismatch');
    for(const file of [intent.planSnapshot,intent.controlFile])if(lstatSync(file).isSymbolicLink())throw new Error('recovery_snapshot_symlink');
    const plan=strictJson(readFileSync(intent.planSnapshot,'utf8'));
    if(hash(intent.planSnapshot)!==task.binding.planHash||intent.planHash!==task.binding.planHash||canonical(plan)!==canonical(intent.plan))throw new Error('recovery_plan_mismatch');
    if(hash(intent.controlFile)!==intent.controlSha256)throw new Error('recovery_control_mismatch');
    const profile=strictJson(readFileSync(intent.controlFile,'utf8'));
    if(profile.task!==taskId||profile.epoch!==epoch||profile.planHash!==task.binding.planHash)throw new Error('recovery_binding_mismatch');
    // 恢复使用原请求的源快照身份；0400 权限不能替代重启后的字节校验。
    if(intent.source||intent.sourceSnapshot||intent.sourceSnapshotSha256){
      if(typeof intent.sourceSnapshot!=='string'||!/^[a-f0-9]{64}$/.test(intent.sourceSnapshotSha256??''))throw new Error('recovery_identity_missing');
      let digest:string;
      try{digest=skillDigest(intent.sourceSnapshot);}catch{throw new Error('recovery_source_snapshot_mismatch');}
      if(digest!==intent.sourceSnapshotSha256)throw new Error('recovery_source_snapshot_mismatch');
    }
    const eventStat=lstatSync(profile.eventFile);
    if(eventStat.isSymbolicLink()||eventStat.ino!==profile.eventInode||eventStat.dev!==profile.eventDevice)throw new Error('execution_event_identity_mismatch');
    const events=readFileSync(profile.eventFile,'utf8').split('\n').filter(Boolean).map(line=>strictJson(line));
    if(events.some(event=>event.task!==taskId||event.epoch!==epoch))throw new Error('recovery_binding_mismatch');
    const original=events.find(event=>event.event==='stage_created');
    if(!original)throw new Error('original_stage_identity_missing');
    const preparations=events.filter(event=>event.event==='delivery_prepared');
    if(preparations.length>1)throw new Error('recovery_delivery_mismatch');
    const prepared=preparations[0];
    if(prepared){
      if(prepared.output!==task.output||typeof prepared.path!=='string'||!inside(original.path,prepared.path)
          ||!/^[a-f0-9]{64}$/.test(prepared.manifestSha256??''))throw new Error('recovery_delivery_mismatch');
      if(existsSync(original.path)){
        const root=lstatSync(original.path);
        if(root.isSymbolicLink()||!root.isDirectory()||root.ino!==original.inode||root.dev!==original.device)throw new Error('original_stage_identity_mismatch');
        const parts=relative(original.path,prepared.path).split('/').filter(Boolean);
        for(let i=1;i<=parts.length;i++)if(lstatSync(join(original.path,...parts.slice(0,i)),{throwIfNoEntry:false})?.isSymbolicLink())throw new Error('recovery_delivery_mismatch');
      }
    }
    const recorded=prepared??original;
    const stage=existsSync(recorded.path)?recorded.path:task.output;
    if(!inside(dirname(task.output),stage))throw new Error('original_stage_outside_authorization');
    const identity=lstatSync(stage);
    if(!identity.isDirectory()||identity.isSymbolicLink()||identity.ino!==recorded.inode||identity.dev!==recorded.device)throw new Error('original_stage_identity_mismatch');
    const files:Record<string,{sha256:string,bytes:number,inode:number}>={};
    const walk=(path:string)=>{
      for(const name of readdirSync(path).sort()){
        const file=join(path,name),stat=lstatSync(file);
        if(stat.isSymbolicLink())throw new Error('unexpected_stage_symlink');
        if(stat.isDirectory())walk(file);else if(stat.isFile())files[file]={sha256:hash(file),bytes:stat.size,inode:stat.ino};
        else throw new Error('unexpected_stage_entry');
      }
    };walk(stage);
    if(Object.keys(files).length>4096||Object.values(files).reduce((sum,f)=>sum+f.bytes,0)>task.binding.authorization.maxBytes)throw new Error('recovery_budget_exceeded');
    if(prepared){try{this.deliveryIdentity(task,stage,files,prepared.manifestSha256);}catch{throw new Error('recovery_delivery_mismatch');}}
    const stepIdentity=this.receiptIdentity(task,stage,files);
    const projects=Object.keys(files).filter(file=>file.endsWith('.vectorcraft'));
    if(projects.length>32)throw new Error('recovery_inspection_limit');
    const binary=join(intent.runtimeHome,'vectorcraft/0.2.0-craft.2/vectorcraft-cli');
    if(hash(binary)!==task.binding.runtimeIdentity)throw new Error('runtime_identity_mismatch');
    const checkId=randomUUID(),owner=taskId+':inspect:'+checkId;
    this.ledger.db.prepare('INSERT INTO recovery_checks(id,task,epoch,intent) VALUES(?,?,?,?)').run(checkId,taskId,epoch,canonical({stage,files,projects,binary,owner}));
    const python=`import importlib.util,json,sys\ns=importlib.util.spec_from_file_location('session',sys.argv[1]);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)\nresult=[]\nfor path in json.loads(sys.argv[3]):\n with m.Session([sys.argv[2],'mcp','--headless']) as session:\n  session.command('document.open',{'path':path})\n  doc=session.command('document.json',{})\n  if not isinstance(doc.get('layers'),list) or not isinstance(doc.get('artboards'),list):raise ValueError('invalid_native_document')\n  links=session.command('links.check',{})\n  if links.get('missing') or links.get('modified'):raise ValueError('original_dependency_unverified')\n  result.append({'path':path,'layers':len(doc['layers']),'artboards':len(doc['artboards']),'dependencies':links})\nprint(json.dumps(result))`;
    let output='',errorOutput='';
    await new Promise<void>((accept,reject)=>{
      const child=spawn(intent.python,['-I','-B',fileURLToPath(new URL('./process_runner.py',import.meta.url)),owner,'-I','-B','-c',python,join(intent.skillSnapshot,'scripts/mcp_session.py'),binary,canonical(projects)],{env:nativeEnvironment(),detached:true,stdio:['pipe','pipe','pipe']});
      let failure:unknown,stopping:Promise<any>|undefined;
      const stop=(error:unknown)=>{failure??=error;stopping??=this.processes.stop(owner,epoch,100).catch(e=>{failure=e;});};
      const timer=setTimeout(()=>stop(new Error('recovery_timeout')),30000);
      child.on('spawn',()=>{try{this.processes.register(owner,epoch,child.pid!,owner);child.stdin.end(canonical({task:owner,go:true})+'\n');}catch(error){failure=error;child.kill('SIGKILL');child.stdin.destroy();}});
      child.stdin.on('error',()=>{});
      child.stdout.on('data',data=>{output+=data.toString();if(output.length>1024*1024)stop(new Error('recovery_output_limit'));});
      child.stderr.on('data',data=>{errorOutput+=data.toString();if(errorOutput.length>1024*1024)stop(new Error('recovery_output_limit'));});
      child.on('error',error=>{clearTimeout(timer);reject(error);});
      child.on('exit',()=>{try{if(!this.processes.observe(owner,epoch).stopped)stop(new Error('recovery_descendant_alive'));}catch(error){failure=error;}});
      child.on('close',async code=>{clearTimeout(timer);await stopping;
        try{if(!this.processes.observe(owner,epoch).stopped)throw new Error('native_stop_unconfirmed');if(code!==0||failure)throw failure??new Error('recovery_failed: child output withheld');accept();}catch(error){reject(error);}
      });
    });
    const reopened=strictJson(output);
    this.ledger.checked(taskId,epoch);
    if(!this.processes.observe(taskId,epoch).stopped)throw new Error('native_stop_unconfirmed');
    const current:Record<string,{sha256:string,bytes:number,inode:number}>={};
    Object.assign(current,files);for(const key of Object.keys(files))delete files[key];walk(stage);
    if(canonical(files)!==canonical(current))throw new Error('original_artifact_changed');
    this.receiptIdentity(task,stage,files,stepIdentity);
    const proof={stepIdentity,...(prepared?{preparedManifestSha256:prepared.manifestSha256}:{}),schema:'vectorcraft-original-inspection/v1',checkId,task:taskId,epoch,owner,stage,stageInode:identity.ino,stageDevice:identity.dev,files,reopened,nativeStopped:true,classification:'verified-interrupted-files; not successful delivery'};
    this.ledger.db.prepare('UPDATE recovery_checks SET result=? WHERE id=?').run(canonical(proof),checkId);
    return proof;
  }
  settle(taskId:string,epoch:number,checkId:string){
    return this.ledger.transaction(()=>{
      const task=this.ledger.checked(taskId,epoch);
      if(!['cancel_requested','reconciling'].includes(task.state))throw new Error('task_not_recoverable');
      const row=this.ledger.db.prepare('SELECT result FROM recovery_checks WHERE id=? AND task=? AND epoch=?').get(checkId,taskId,epoch) as any;
      if(!row?.result)throw new Error('native_inspection_required');
      const proof=strictJson(row.result);
      if(proof.schema==='vectorcraft-unlaunched-inspection/v1')return new LaunchRecovery(this.ledger,this.processes).settle(taskId,epoch,proof);
      if(!/^[a-f0-9]{64}$/.test(proof.stepIdentity??''))throw new Error('recovery_receipt_identity_missing');
      this.receiptIdentity(task,proof.stage,proof.files,proof.stepIdentity);
      if(proof.preparedManifestSha256){try{this.deliveryIdentity(task,proof.stage,proof.files,proof.preparedManifestSha256);}catch{throw new Error('recovery_delivery_mismatch');}}
      if(!this.processes.observe(taskId,epoch).stopped||!this.processes.observe(proof.owner,epoch).stopped)throw new Error('native_stop_unconfirmed');
      const stage=lstatSync(proof.stage);
      if(stage.isSymbolicLink()||stage.ino!==proof.stageInode||stage.dev!==proof.stageDevice)throw new Error('original_stage_identity_mismatch');
      const present:string[]=[];
      const walk=(directory:string)=>{for(const name of readdirSync(directory)){
        const path=join(directory,name),stat=lstatSync(path);
        if(stat.isSymbolicLink())throw new Error('original_artifact_changed');
        if(stat.isDirectory())walk(path);else if(stat.isFile())present.push(path);else throw new Error('original_artifact_changed');
      }};walk(proof.stage);
      if(canonical(present.sort())!==canonical(Object.keys(proof.files).sort()))throw new Error('original_artifact_changed');
      for(const [path,record] of Object.entries(proof.files) as [string,any][]){
        const stat=lstatSync(path);if(stat.isSymbolicLink()||stat.ino!==record.inode||stat.size!==record.bytes||hash(path)!==record.sha256)throw new Error('original_artifact_changed');
      }
      this.ledger.db.prepare('UPDATE tasks SET state=?,epoch=epoch+1,reason=? WHERE id=?').run(task.state==='cancel_requested'?'cancelled':'interrupted_verified',canonical({checkId,classification:proof.classification}),taskId);
      return this.ledger.get(taskId);
    });
  }
}
