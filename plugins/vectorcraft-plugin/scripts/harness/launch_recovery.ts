import {nativeEnvironment} from './native_environment.ts';
import {createHash,randomUUID} from 'node:crypto';
import {readFileSync,lstatSync,readdirSync} from 'node:fs';
import {join,dirname,isAbsolute} from 'node:path';
import {spawn} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {canonical,strictJson} from '../../src/strict_json.ts';
import {Ledger,resourcePath} from './ledger.ts';
import {ProcessRegistry} from './process_registry.ts';
import {skillDigest} from './skill_digest.ts';
const sha=(value:string|Buffer)=>createHash('sha256').update(value).digest('hex');
const hash=(path:string)=>sha(readFileSync(path));

/** GO未授权的任务单独核验原输入；缺少暂存目录并不是该结论的依据。 */
export class LaunchRecovery {
  ledger:Ledger;processes:ProcessRegistry;
  constructor(ledger:Ledger,processes:ProcessRegistry){this.ledger=ledger;this.processes=processes;}
  /** 每次核验都重读已封存门禁、原请求和文件，不能在结算时重新封存改变后的门禁。 */
  validate(taskId:string,epoch:number):any {
    const task=this.ledger.checked(taskId,epoch),context=task.binding.launchContext;
    const gate=this.ledger.db.prepare('SELECT * FROM native_launches WHERE task=? AND epoch=?').get(taskId,epoch) as any;
    if(task.binding.launchProtocol!=='registered-go/v1'||gate?.protocol!==task.binding.launchProtocol||gate.state!=='sealed'||gate.intent_sha256!==null)throw new Error('recovery_launch_identity_mismatch');
    if(!['reconciling','cancel_requested'].includes(task.state)||!context||typeof context.python!=='string'||!context.python)throw new Error('recovery_launch_identity_mismatch');
    const outputStat=lstatSync(task.output,{throwIfNoEntry:false});
    if(outputStat)throw new Error('unlaunched_output_present');
    for(const path of [context.skill,context.plan,context.runtimeHome,task.output,...(context.source?[context.source]:[])]){
      if(typeof path!=='string'||!isAbsolute(path)||resourcePath(path)!==path)throw new Error('recovery_path_changed');
    }
    const step=this.ledger.db.prepare('SELECT intent,state,result FROM steps WHERE task=? AND n=0').get(taskId) as any;
    const count=(this.ledger.db.prepare('SELECT COUNT(*) AS n FROM steps WHERE task=?').get(taskId) as any).n;
    if(count!==(step?1:0)||step&&(step.state!=='submitted'||step.result!==null))throw new Error('recovery_launch_identity_mismatch');
    const files:Record<string,any>={},directories:Record<string,any>={},absent:string[]=[];
    const file=(path:string,expected?:string)=>{
      const stat=lstatSync(path);
      if(!stat.isFile()||stat.isSymbolicLink()||resourcePath(path)!==path)throw new Error('recovery_snapshot_symlink');
      const digest=hash(path);if(expected!==undefined&&digest!==expected)throw new Error('recovery_input_mismatch');
      files[path]={sha256:digest,inode:stat.ino,device:stat.dev,bytes:stat.size};
    };
    file(context.plan);const plan=strictJson(readFileSync(context.plan,'utf8'));
    if(sha(canonical(plan))!==task.binding.planHash)throw new Error('recovery_plan_mismatch');
    if(skillDigest(context.skill)!==task.binding.skillSha256)throw new Error('skill_snapshot_mismatch');
    let inspectionSkill=context.skill;
    if(step){
      const intent=strictJson(step.intent);
      if(!/^[a-f0-9]{64}$/.test(intent.controlSha256??'')||!task.binding.skillSha256)throw new Error('recovery_identity_missing');
      if(intent.skillSha256!==task.binding.skillSha256||skillDigest(intent.skillSnapshot)!==task.binding.skillSha256)throw new Error('skill_snapshot_mismatch');
      file(intent.planSnapshot);file(intent.controlFile);
      if(hash(intent.planSnapshot)!==task.binding.planHash||intent.planHash!==task.binding.planHash||canonical(strictJson(readFileSync(intent.planSnapshot,'utf8')))!==canonical(intent.plan))throw new Error('recovery_plan_mismatch');
      if(hash(intent.controlFile)!==intent.controlSha256)throw new Error('recovery_control_mismatch');
      const profile=strictJson(readFileSync(intent.controlFile,'utf8'));
      if(profile.task!==taskId||profile.epoch!==epoch||profile.planHash!==task.binding.planHash||profile.runtimeIdentity!==task.binding.runtimeIdentity||canonical(profile.authorization)!==canonical(task.binding.authorization))throw new Error('recovery_binding_mismatch');
      file(profile.eventFile);const event=files[profile.eventFile];
      if(event.inode!==profile.eventInode||event.device!==profile.eventDevice)throw new Error('execution_event_identity_mismatch');
      if(event.bytes!==0)throw new Error('recovery_launch_evidence_conflict');
      if(intent.source!==context.source||intent.output!==task.output||intent.runtimeHome!==context.runtimeHome||intent.python!==context.python)throw new Error('recovery_binding_mismatch');
      if(context.source){
        if(typeof intent.sourceSnapshot!=='string'||!/^[a-f0-9]{64}$/.test(intent.sourceSnapshotSha256??''))throw new Error('recovery_identity_missing');
        if(skillDigest(intent.sourceSnapshot)!==intent.sourceSnapshotSha256)throw new Error('recovery_source_snapshot_mismatch');
      }
      inspectionSkill=intent.skillSnapshot;
    }
    const source=context.source;
    if(source){
      if(join(source,'project.vectorcraft')!==task.resource||task.binding.projectRevision===null)throw new Error('recovery_binding_mismatch');
      const walk=(directory:string)=>{
        const stat=lstatSync(directory);if(!stat.isDirectory()||stat.isSymbolicLink()||resourcePath(directory)!==directory)throw new Error('recovery_path_changed');
        directories[directory]={inode:stat.ino,device:stat.dev};
        for(const name of readdirSync(directory).sort()){
          const path=join(directory,name),entry=lstatSync(path);
          if(entry.isDirectory())walk(path);else file(path);
          if(Object.keys(files).length+Object.keys(directories).length>4096)throw new Error('recovery_inspection_limit');
        }
      };walk(source);
      if(files[task.resource]?.sha256!==task.binding.projectRevision)throw new Error('revision_conflict');
    }else if(task.binding.projectRevision!==null||task.resource!==join(task.output,'project.vectorcraft'))throw new Error('recovery_binding_mismatch');
    for(const [name,expected] of Object.entries(task.binding.inputHashes) as [string,string][]){
      if(name.startsWith('source:file:'))file(join(source,name.slice('source:file:'.length)),expected);
      else if(name==='source:manifest.json')file(join(source,'manifest.json'),expected);
      else if(name.startsWith('source:optional:')){
        const relative=name.slice('source:optional:'.length),path=join(source,relative);
        if(expected===sha('absent:'+relative)){if(lstatSync(path,{throwIfNoEntry:false}))throw new Error('recovery_input_mismatch');absent.push(path);}
        else file(path,expected);
      }else if(name.startsWith('guard:'))file(name.slice('guard:'.length),expected);
    }
    for(const asset of Object.values(plan.assets??{}) as any[])file(asset.path,asset.sha256);
    if(Object.values(files).reduce((sum:number,f:any)=>sum+f.bytes,0)>task.binding.authorization.maxBytes)throw new Error('recovery_budget_exceeded');
    const registered=this.ledger.db.prepare('SELECT task FROM native_processes WHERE task=? AND epoch=?').get(taskId,epoch);
    if(registered&&!this.processes.observe(taskId,epoch).stopped)throw new Error('native_stop_unconfirmed');
    return {gate,stepIdentity:sha(canonical(step??null)),bindingHash:task.binding_hash,attempts:task.attempts,bytes:task.bytes,
      files,directories,absent,inspectionSkill,source,launchObservation:registered?'registered-launcher-stopped':'GO-sealed-no-registered-launcher'};
  }
  /** 存在原工程时只读重开并核对链接；新建任务明确没有可重开的产物。 */
  async inspect(taskId:string,epoch:number):Promise<any>{
    const before=this.validate(taskId,epoch),task=this.ledger.checked(taskId,epoch),context=task.binding.launchContext;
    const checkId=randomUUID(),owner=before.source?taskId+':inspect:'+checkId:null;
    this.ledger.db.prepare('INSERT INTO recovery_checks(id,task,epoch,intent) VALUES(?,?,?,?)').run(checkId,taskId,epoch,canonical({kind:'unlaunched',before,owner}));
    let reopened:any=null;
    if(owner){
      const binary=join(context.runtimeHome,'vectorcraft/0.2.0-craft.2/vectorcraft-cli');
      if(hash(binary)!==task.binding.runtimeIdentity)throw new Error('runtime_identity_mismatch');
      const code=`import importlib.util,json,sys\ns=importlib.util.spec_from_file_location('session',sys.argv[1]);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)\nwith m.Session([sys.argv[2],'mcp','--headless']) as session:\n session.command('document.open',{'path':sys.argv[3]})\n doc=session.command('document.json',{})\n if not isinstance(doc.get('layers'),list) or not isinstance(doc.get('artboards'),list):raise ValueError('invalid_native_document')\n links=session.command('links.check',{})\n if links.get('missing') or links.get('modified'):raise ValueError('original_dependency_unverified')\n print(json.dumps({'layers':len(doc['layers']),'artboards':len(doc['artboards']),'dependencies':links}))`;
      let stdout='',stderr='';
      await new Promise<void>((accept,reject)=>{
        const child=spawn(context.python,['-I','-B',fileURLToPath(new URL('./process_runner.py',import.meta.url)),owner,'-I','-B','-c',code,join(before.inspectionSkill,'scripts/mcp_session.py'),binary,task.resource],{env:nativeEnvironment(),detached:true,stdio:['pipe','pipe','pipe']});
        let failure:unknown,stopping:Promise<any>|undefined;
        const stop=(error:unknown)=>{failure??=error;stopping??=this.processes.stop(owner,epoch,100).catch(e=>{failure=e;});};
        const timer=setTimeout(()=>stop(new Error('recovery_timeout')),30000);
        child.on('spawn',()=>{try{this.processes.register(owner,epoch,child.pid!,owner);child.stdin.end(canonical({task:owner,go:true})+'\n');}catch(error){failure=error;child.kill('SIGKILL');child.stdin.destroy();}});
        child.stdin.on('error',()=>{});
        child.stdout.on('data',data=>{stdout+=data.toString();if(stdout.length>1024*1024)stop(new Error('recovery_output_limit'));});
        child.stderr.on('data',data=>{stderr+=data.toString();if(stderr.length>1024*1024)stop(new Error('recovery_output_limit'));});
        child.on('error',error=>{clearTimeout(timer);reject(error);});
        child.on('exit',()=>{try{if(!this.processes.observe(owner,epoch).stopped)stop(new Error('recovery_descendant_alive'));}catch(error){failure=error;}});
        child.on('close',async code=>{clearTimeout(timer);await stopping;try{if(!this.processes.observe(owner,epoch).stopped)throw new Error('native_stop_unconfirmed');if(code!==0||failure)throw failure??new Error('recovery_failed: child output withheld');accept();}catch(error){reject(error);}});
      });
      reopened=strictJson(stdout);
    }
    if(canonical(this.validate(taskId,epoch))!==canonical(before))throw new Error('unlaunched_input_changed');
    const proof={schema:'vectorcraft-unlaunched-inspection/v1',checkId,task:taskId,epoch,owner,validation:before,reopened,
      nativeInspection:owner?'readonly-original-source':'not-applicable-no-source',classification:'verified-never-authorized; not successful delivery'};
    this.ledger.db.prepare('UPDATE recovery_checks SET result=? WHERE id=?').run(canonical(proof),checkId);
    return proof;
  }
  /** 使用原检查身份结算，不执行工作流、不重置预算、不清理部分快照。 */
  settle(taskId:string,epoch:number,proof:any){
    if(canonical(this.validate(taskId,epoch))!==canonical(proof.validation))throw new Error('unlaunched_input_changed');
    if(proof.owner&&!this.processes.observe(proof.owner,epoch).stopped)throw new Error('native_stop_unconfirmed');
    const task=this.ledger.checked(taskId,epoch);
    this.ledger.db.prepare('UPDATE tasks SET state=?,epoch=epoch+1,reason=? WHERE id=?').run(task.state==='cancel_requested'?'cancelled':'interrupted_verified',canonical({checkId:proof.checkId,classification:proof.classification}),taskId);
    return this.ledger.get(taskId);
  }
}
