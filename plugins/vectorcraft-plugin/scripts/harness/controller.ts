import {assetDigest} from './asset_digest.ts';
import {authorizedRead,authorizedDigest,authorizedDigests,authorizedCopy} from './authorized_file.ts';
import {authorizedWrite} from './authorized_write.ts';
import {authorizedDirectory,authorizedTreeCopy,authorizedTreeDigest} from './authorized_tree.ts';
import {assertNoLiteralSecrets,validateAssetRecords} from './input_policy.ts';
import {nativeEnvironment} from './native_environment.ts';
import { createHash } from 'node:crypto';
import { existsSync, lstatSync, readFileSync } from 'node:fs';
import { relative, resolve, join, isAbsolute, dirname } from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { prepareRuntime } from '../../src/runtime/prepare_runtime.ts';
import type { RuntimeProbe } from '../../src/runtime/prepare_runtime.ts';
import { RuntimeGate,validateCapabilities } from '../../src/runtime/runtime_gate.ts';
import { ProcessRegistry } from './process_registry.ts';
import { Recovery } from './recovery.ts';
import { Ledger, resourcePath } from './ledger.ts';
import type { Authorization } from './ledger.ts';
import { strictJson, canonical } from '../../src/strict_json.ts';
import { validateGeometryContract,verifyGeometry } from '../../src/planning/geometry.ts';
import type { GeometryContract } from '../../src/planning/geometry.ts';

const sha=(value:string|Buffer)=>createHash('sha256').update(value).digest('hex');
// 交付验收绑定实际检查过的清单字节；不向公开清单添加可伪造的证明字段。
const verifiedManifests=new WeakMap<object,string>();
const inside=(root:string,path:string)=>{const sub=relative(resourcePath(root),resourcePath(path));return !isAbsolute(sub)&&sub!=='..'&&!sub.startsWith('../');};

import {skillDigest} from './skill_digest.ts';
export {skillDigest} from './skill_digest.ts';

type RunRequest={key:string,skill:string,expectedSkillSha256:string,plan:string,output:string,source?:string,
  runtimeHome:string,python?:string,estimatedBytes:number,inputFingerprints?:Record<string,string>,geometryContract?:GeometryContract,authorization:Authorization&{readRoots:string[],writeRoots:string[]}};

/** 仅协调已固定的独立技能；原生命令语义与失败工程保留由源技能负责。 */
export class Controller {
  ledger:Ledger;snapshotRoot:string;processes:ProcessRegistry;probe:RuntimeProbe;
  constructor(database:string,probe:RuntimeProbe=prepareRuntime){this.probe=probe;this.ledger=new Ledger(database);this.processes=new ProcessRegistry(this.ledger.db);this.snapshotRoot=join(resourcePath(dirname(resolve(database))),'plan-snapshots');}
  /** 原子公布撤销状态；这里只请求取消，停止和原文件核验之前不释放资源。 */
  requestCancel(id:string,epoch:number):any {
    const task=this.ledger.cancel(id,epoch,false),budgetId=task.binding.authorization.budgetId??task.id;
    const members=this.ledger.db.prepare("SELECT id,epoch FROM tasks WHERE COALESCE(json_extract(binding,'$.authorization.budgetId'),id)=? AND state='cancel_requested'").all(budgetId) as any[];
    // 先持久封存整个工作流，再逐个公布控制状态和停止已登记的组；一个失败不跳过其他组。
    for(const member of members){
      const failures:string[]=[];
      try{this.publishState(member.id,member.epoch,'cancel_requested');}catch(error){failures.push('cancel_state_publish_failed: '+String(error));}
      const registered=this.ledger.db.prepare('SELECT task FROM native_processes WHERE task=? AND epoch=?').get(member.id,member.epoch);
      if(registered){try{this.processes.signal(member.id,member.epoch,'SIGTERM');}catch(error){failures.push('native_stop_unconfirmed: '+String(error));}}
      if(failures.length)this.ledger.unknown(member.id,member.epoch,failures.join('; '));
    }
    return this.ledger.get(id);
  }
  publishState(id:string,epoch:number,state:string){
    authorizedDirectory(this.snapshotRoot,dirname(this.snapshotRoot));
    const path=join(this.snapshotRoot,id+'-state.json');
    authorizedWrite(path,this.snapshotRoot,canonical({task:id,epoch,state}),0o600,true);
  }
  async reconcileOriginal(id:string,epoch:number){
    const recovery=new Recovery(this.ledger,this.processes);
    const proof=await recovery.inspect(id,epoch);
    return {proof,task:recovery.settle(id,epoch,proof.checkId)};
  }
  verifyDelivery(output:string,runtime:string,geometryContract?:GeometryContract,readRoots=[resourcePath(output)]):any {
    const manifestBytes=authorizedRead(join(output,'manifest.json'),readRoots);
    const manifest=strictJson(manifestBytes.toString('utf8'));
    if(manifest.schema!=='vectorcraft-delivery/v1'||manifest.runtimeSha256!==runtime)throw new Error('runtime_identity_mismatch');
    if(!manifest.files||typeof manifest.files!=='object'||Array.isArray(manifest.files)||Object.keys(manifest.files).length>4096||!manifest.files['project.vectorcraft'])throw new Error('invalid_delivery_manifest');
    for(const [path,digest] of Object.entries(manifest.files)){
      if(isAbsolute(path)||path.split('/').some(p=>['','..','.'].includes(p))||path.includes('\\'))throw new Error('invalid_artifact_path');
      const file=join(output,path);
      if(typeof digest!=='string'||!/^[a-f0-9]{64}$/.test(digest)||!inside(output,file)||lstatSync(file).isSymbolicLink()||!lstatSync(file).isFile())throw new Error('artifact_digest_mismatch');
    }
    const hashes=authorizedDigests(Object.keys(manifest.files).map(path=>join(output,path)),readRoots);
    for(const [path,digest] of Object.entries(manifest.files))if(hashes[join(output,path)]!==digest)throw new Error('artifact_digest_mismatch');
    if(geometryContract){
      if(!manifest.files['native.json'])throw new Error('geometry_native_snapshot_missing');
      const nativeBytes=authorizedRead(join(output,'native.json'),readRoots);
      if(sha(nativeBytes)!==manifest.files['native.json'])throw new Error('artifact_digest_mismatch');
      const report=verifyGeometry(strictJson(nativeBytes.toString('utf8')),manifest.bindings??{},geometryContract);
      const bound={...report,nativeSha256:manifest.files['native.json'],projectRevision:manifest.files['project.vectorcraft'],runtimeIdentity:runtime,contractSha256:sha(canonical(geometryContract))};
      if(report.status!=='PASS')throw new Error('geometry_acceptance_failed: '+canonical(bound));
      manifest.geometryVerification=bound;
    }
    verifiedManifests.set(manifest,sha(manifestBytes));
    return manifest;
  }
  async run(request:RunRequest):Promise<any> {
    assertNoLiteralSecrets(request);
    const geometryContract=request.geometryContract===undefined?undefined:strictJson(canonical(request.geometryContract));
    if(geometryContract!==undefined)validateGeometryContract(geometryContract);
    const suppliedAuthorization=request.authorization;
    if(!Array.isArray(suppliedAuthorization?.readRoots)||!Array.isArray(suppliedAuthorization?.writeRoots))throw new Error('authorization_roots_required');
    // 调用方对象和目录别名在异步探测期间不能重写授权或重定向交付。
    const auth={...strictJson(canonical(suppliedAuthorization)),
      readRoots:suppliedAuthorization.readRoots.map(resourcePath),writeRoots:suppliedAuthorization.writeRoots.map(resourcePath)};
    request={...request,authorization:auth,skill:resourcePath(request.skill),plan:resourcePath(request.plan),
      output:resourcePath(request.output),runtimeHome:resourcePath(request.runtimeHome),
      ...(request.source?{source:resourcePath(request.source)}:{}),
      ...(request.inputFingerprints?{inputFingerprints:strictJson(canonical(request.inputFingerprints))}:{})};
    for(const path of [request.plan,...(request.source?[request.source]:[])])if(!auth.readRoots.some(root=>inside(root,path)))throw new Error('outside_authorized_roots');
    for(const path of [request.output,request.runtimeHome])if(!auth.writeRoots.some(root=>inside(root,path)))throw new Error('outside_authorized_roots');
    if(!auth.writeRoots.some((root:string)=>inside(root,dirname(request.output))))throw new Error('staging_parent_not_authorized');
    if(skillDigest(request.skill)!==request.expectedSkillSha256)throw new Error('skill_snapshot_mismatch');
    if(!existsSync(join(request.skill,'scripts/execution_control.py')))throw new Error('managed_execution_control_required');
    const plan=strictJson(authorizedRead(request.plan,auth.readRoots).toString('utf8'));
    assertNoLiteralSecrets(plan);validateAssetRecords(plan);
    if(plan.schema)throw new Error('workflow_plan_required; complete-command plans use the independent commands entry');
    const lock=strictJson(readFileSync(join(request.skill,'scripts/runtime.lock.json'),'utf8'));
    let projectRevision:string|null=null;
    if(request.source){
      if(!auth.readRoots.some(root=>inside(root,join(request.source!,'project.vectorcraft'))))throw new Error('outside_authorized_roots');
      if(lstatSync(join(request.source,'project.vectorcraft')).isSymbolicLink())throw new Error('invalid_source_path');
      projectRevision=authorizedDigest(join(request.source,'project.vectorcraft'),auth.readRoots);
      if(projectRevision!==plan.expectedProjectSha256)throw new Error('revision_conflict');
    }
    const inputHashes:Record<string,string>={};
    const sourceDependencies:Record<string,string|null>=Object.create(null);
    const sourcePathLinked=(name:string)=>name.split('/').some((_,i,parts)=>lstatSync(join(request.source!,...parts.slice(0,i+1)),{throwIfNoEntry:false})?.isSymbolicLink());
    if(request.source){
      const manifestFile=join(request.source,'manifest.json'),stat=lstatSync(manifestFile,{throwIfNoEntry:false});
      if(!stat?.isFile()||stat.isSymbolicLink())throw new Error('invalid_source_dependency');
      const manifestBytes=authorizedRead(manifestFile,auth.readRoots),manifest=strictJson(manifestBytes.toString());
      if(manifest.schema!=='vectorcraft-delivery/v1'||!manifest.files||typeof manifest.files!=='object'||Array.isArray(manifest.files)||Object.keys(manifest.files).length>4096||manifest.files['project.vectorcraft']!==projectRevision)throw new Error('invalid_source_dependency');
      sourceDependencies['manifest.json']=sha(manifestBytes);inputHashes['source:manifest.json']=sha(manifestBytes);
      for(const [name,expected] of Object.entries(manifest.files) as [string,any][]){
        if(isAbsolute(name)||name.includes('\\')||name.split('/').some(p=>['','..','.'].includes(p))||typeof expected!=='string'||!/^[a-f0-9]{64}$/.test(expected))throw new Error('invalid_source_dependency');
        const file=join(request.source,name),stat=lstatSync(file,{throwIfNoEntry:false});
        if(!stat?.isFile()||sourcePathLinked(name)||!auth.readRoots.some(root=>inside(root,file)))throw new Error('invalid_source_dependency');
        sourceDependencies[name]=expected;inputHashes['source:file:'+name]=expected;
      }
      const initialHashes=authorizedDigests(Object.keys(manifest.files).map(name=>join(request.source!,name)),auth.readRoots);
      for(const [name,expected] of Object.entries(manifest.files))if(initialHashes[join(request.source,name)]!==expected)throw new Error('source_dependency_digest_mismatch');
      // 这些可选元数据也会改变继承导出；缺失本身必须被绑定，防止探测后补入。
      for(const name of ['plan.json','pdf-export-date.json']){
        if(name in sourceDependencies)continue;
        const file=join(request.source,name),stat=lstatSync(file,{throwIfNoEntry:false});
        if(stat&&(!stat.isFile()||stat.isSymbolicLink()))throw new Error('invalid_source_dependency');
        const expected=stat?authorizedDigest(file,auth.readRoots):null;sourceDependencies[name]=expected;
        inputHashes['source:optional:'+name]=expected??sha('absent:'+name);
      }
    }
    const guards=request.inputFingerprints??{};
    if(!guards||typeof guards!=='object'||Array.isArray(guards)||Object.keys(guards).length>4096)throw new Error('invalid_input_fingerprints');
    const checkInputs=()=>{
      // 解析后的物理目录本身或其父目录被替换为链接时，也不能重定向授权。
      for(const path of [...auth.readRoots,...auth.writeRoots,request.skill,request.plan,request.output,request.runtimeHome,...(request.source?[request.source]:[])]){
        if(resourcePath(path)!==path)throw new Error('authorization_path_changed');
      }
      const digestInputs:string[]=[];
      if(request.source){
        const project=join(request.source,'project.vectorcraft');
        if(lstatSync(project).isSymbolicLink())throw new Error('invalid_source_path');
        digestInputs.push(project);
      }
      for(const [name,expected] of Object.entries(sourceDependencies)){
        const file=join(request.source!,name),stat=lstatSync(file,{throwIfNoEntry:false});
        if(expected===null){if(stat)throw new Error('stale_source_dependencies');}
        else{
          if(!stat?.isFile()||sourcePathLinked(name)||!auth.readRoots.some(root=>inside(root,file)))throw new Error('stale_source_dependencies');
          digestInputs.push(file);
        }
      }
      for(const [path,expected] of Object.entries(guards)){
        if(!/^[a-f0-9]{64}$/.test(expected)||!auth.readRoots.some(root=>inside(root,path)))throw new Error('outside_authorized_roots');
        digestInputs.push(path);
      }
      const currentHashes=authorizedDigests(digestInputs,auth.readRoots);
      if(request.source&&currentHashes[join(request.source,'project.vectorcraft')]!==projectRevision)throw new Error('revision_conflict');
      for(const [name,expected] of Object.entries(sourceDependencies))if(expected!==null&&currentHashes[join(request.source!,name)]!==expected)throw new Error('stale_source_dependencies');
      for(const [path,expected] of Object.entries(guards))if(currentHashes[path]!==expected)throw new Error('stale_execution_inputs');
    };
    checkInputs();
    for(const [path,expected] of Object.entries(guards))inputHashes['guard:'+path]=expected;
    for(const [name,asset] of Object.entries(plan.assets??{}) as [string,any][]){
      if(!auth.readRoots.some(root=>inside(root,asset.path)))throw new Error('outside_authorized_roots');
      if(!isAbsolute(asset.path)||lstatSync(asset.path).isSymbolicLink()||!lstatSync(asset.path).isFile())throw new Error('invalid_asset_path');
      const hash=assetDigest(asset.path,auth.readRoots,request.skill,request.python??'python3');if(hash!==asset.sha256)throw new Error('asset_digest_mismatch');inputHashes[name]=hash;
    }
    if(geometryContract)inputHashes['contract:geometry']=sha(canonical(geometryContract));
    const runtimeIdentity=lock.artifacts['darwin-arm64'].binarySha256;
    const gate=new RuntimeGate(this.ledger),existing=this.ledger.db.prepare('SELECT id FROM tasks WHERE key=?').get(request.key) as any;
    if(existing){
      const previous=this.ledger.get(existing.id);
      const fingerprint=previous.binding.inputHashes['runtime:capabilities'];
      if(fingerprint)inputHashes['runtime:capabilities']=fingerprint;
      else if(previous.state==='ready')throw new Error('legacy_ready_requires_runtime_reconciliation');
    }else{
      if(existsSync(request.output))throw new Error('output_exists');
      const catalog=strictJson(readFileSync(join(request.skill,'references/command-coverage.json'),'utf8'));
      if(catalog.runtimeSha256!==runtimeIdentity)throw new Error('capability_catalog_identity_mismatch');
      const tools=strictJson(readFileSync(fileURLToPath(new URL('../../runtime/vectorcraft-headless-capabilities.json',import.meta.url)),'utf8')).tools;
      const requirements={mode:'headless',commands:Object.fromEntries(catalog.commands.map((r:any)=>[r.id,r.params])),tools};
      const selected=gate.current();
      if(selected){
        if(selected.active.mode!=='headless')throw new Error('runtime_mode_mismatch');
        if(selected.active.binarySha256!==runtimeIdentity)throw new Error('runtime_selection_mismatch');
      }
      const report=await this.probe({skill:request.skill,runtimeHome:request.runtimeHome,install:true,plan,platform:'darwin-arm64',requirements,python:request.python,deadline:auth.deadline});
      if(skillDigest(request.skill)!==request.expectedSkillSha256)throw new Error('skill_snapshot_mismatch');
      checkInputs();
      if(request.source&&authorizedDigest(join(request.source,'project.vectorcraft'),auth.readRoots)!==projectRevision)throw new Error('revision_conflict');
      if(report.binarySha256!==runtimeIdentity)throw new Error('runtime_identity_mismatch');
      validateCapabilities(report,requirements);
      const active=gate.initialize(report,requirements,[3]).active;
      validateCapabilities(active,requirements);
      inputHashes['runtime:capabilities']=sha(canonical({commands:active.commands,tools:active.tools,mode:active.mode}));
    }

    const launchBinding=existing?(()=>{const previous=this.ledger.get(existing.id).binding;return previous.launchProtocol?{launchProtocol:previous.launchProtocol,launchContext:previous.launchContext}:{};})():{
      launchProtocol:'registered-go/v1' as const,launchContext:{skill:request.skill,plan:request.plan,runtimeHome:request.runtimeHome,python:request.python??'python3',source:request.source??null}};
    const binding={...launchBinding,skillSha256:request.expectedSkillSha256,planHash:sha(canonical(plan)),inputHashes,projectRevision,runtimeIdentity,authorization:auth};
    let task=this.ledger.claim(request.key,request.source?join(request.source,'project.vectorcraft'):join(request.output,'project.vectorcraft'),request.output,binding);
    if(existing&&task.binding.authorization.deadline<=Date.now()&&['ready','running','reconciling','cancel_requested'].includes(task.state))task=this.requestCancel(task.id,task.epoch);
    if(task.state!=='ready'||existing){
      let geometryVerification:any;
      if(task.state==='review_ready'||task.state==='completed'){
        const manifest=this.verifyDelivery(request.output,runtimeIdentity,geometryContract,[request.output]);
        geometryVerification=manifest.geometryVerification;
        const received=this.ledger.db.prepare('SELECT result FROM steps WHERE task=? AND n=0').get(task.id) as any;
        const checked=verifiedManifests.get(manifest);
        if(!received?.result||strictJson(received.result).manifestSha256!==checked||authorizedDigest(join(request.output,'manifest.json'),[request.output])!==checked)throw new Error('receipt_manifest_mismatch');
      }
      return {...task,...(geometryContract&&geometryVerification?{geometryVerification}:{}),resumePolicy:'inspect original files and request; no automatic replay'};
    }
    if(existsSync(request.output))throw new Error('output_exists');
    authorizedDirectory(this.snapshotRoot,dirname(this.snapshotRoot));
    const skillSnapshot=join(this.snapshotRoot,task.id+'-skill');
    authorizedTreeCopy(request.skill,skillSnapshot,this.snapshotRoot,request.expectedSkillSha256);
    let sourceSnapshot:string|undefined,sourceSnapshotSha256:string|undefined;
    if(request.source){
      sourceSnapshot=join(this.snapshotRoot,task.id+'-source');authorizedDirectory(sourceSnapshot,this.snapshotRoot,true);
      for(const [name,expected] of Object.entries(sourceDependencies)){
        if(expected===null)continue;
        const original=join(request.source,name),snapshot=join(sourceSnapshot,name);
        if(sourcePathLinked(name))throw new Error('invalid_source_dependency');
        authorizedDirectory(dirname(snapshot),sourceSnapshot);
        authorizedCopy(original,auth.readRoots,snapshot,sourceSnapshot,expected);
      }
      checkInputs();sourceSnapshotSha256=authorizedTreeDigest(sourceSnapshot);
    }
    const planSnapshot=join(this.snapshotRoot,task.id+'.json');
    authorizedWrite(planSnapshot,this.snapshotRoot,canonical(plan),0o400);
    const eventFile=join(this.snapshotRoot,task.id+'-events.jsonl');
    const eventStat=authorizedWrite(eventFile,this.snapshotRoot,'',0o600);
    this.publishState(task.id,task.epoch,'running');
    const controlFile=join(this.snapshotRoot,task.id+'-control.json');
    const controlBytes=canonical({schema:'vectorcraft-execution-control/v1',task:task.id,epoch:task.epoch,
      deadline:auth.deadline,maxBytes:Math.min(auth.maxBytes,request.estimatedBytes),runtimeIdentity,authorization:auth,
      planFile:planSnapshot,planHash:binding.planHash,stateFile:join(this.snapshotRoot,task.id+'-state.json'),
      eventFile,eventDevice:eventStat.device,eventInode:eventStat.inode,
      ...(request.source?{source:{path:join(resourcePath(request.source),'project.vectorcraft'),sha256:projectRevision}}:{})});
    const controlIdentity=authorizedWrite(controlFile,this.snapshotRoot,controlBytes,0o400);
    this.ledger.intent(task.id,task.epoch,0,{skillSha256:request.expectedSkillSha256,planHash:binding.planHash,plan,planSnapshot,skillSnapshot,output:resourcePath(request.output),controlFile,controlSha256:controlIdentity.sha256,runtimeHome:resourcePath(request.runtimeHome),source:request.source?resourcePath(request.source):null,python:request.python??'python3',...(sourceSnapshot?{sourceSnapshot,sourceSnapshotSha256}:{}),...(geometryContract?{geometryContract}:{})},request.estimatedBytes);
    const args=['-I','-B',join(skillSnapshot,'scripts/workflow.py'),planSnapshot,'--output',request.output,'--runtime-home',request.runtimeHome,'--control',controlFile];
    if(sourceSnapshot)args.push('--source',sourceSnapshot);
    let stdout='',stderr='';
    try {
      await new Promise<void>((accept,reject)=>{
        const launcher=fileURLToPath(new URL('./process_runner.py',import.meta.url));
        const child=spawn(request.python??'python3',['-I','-B',launcher,task.id,...args],{env:nativeEnvironment(),detached:true,stdio:['pipe','pipe','pipe']});
        let interrupted=false,stopping:Promise<any>|undefined,observationError:unknown;
        const interrupt=()=>{
          if(interrupted)return;interrupted=true;
          try{if(this.ledger.get(task.id).state!=='cancel_requested')this.requestCancel(task.id,task.epoch);
            else this.publishState(task.id,task.epoch,'cancel_requested');}
          catch(error){observationError=error;}
          stopping=this.processes.stop(task.id,task.epoch).catch(error=>{observationError=error;});
        };
        const timer=setInterval(()=>{
          try{
            checkInputs();
            const state=this.ledger.get(task.id).state;
            this.processes.observe(task.id,task.epoch);
            if(Date.now()>=auth.deadline||state==='cancel_requested'||state==='cancelled')interrupt();
          }catch(error){observationError=error;interrupt();}
        },50);
        const capture=(kind:'out'|'err',data:Buffer)=>{
          const remaining=8*1024*1024-Buffer.byteLength(stdout)-Buffer.byteLength(stderr);
          const chunk=data.subarray(0,Math.max(0,remaining)).toString();
          if(kind==='out')stdout+=chunk;else stderr+=chunk;
          if(data.length>=remaining)interrupt();
        };
        child.stdout.on('data',data=>capture('out',data));child.stderr.on('data',data=>capture('err',data));
        child.on('error',error=>{clearInterval(timer);reject(error);});
        child.on('spawn',()=>{
          try{this.processes.register(task.id,task.epoch,child.pid!,task.id);checkInputs();
            if(binding.launchProtocol)this.ledger.authorizeLaunch(task.id,task.epoch);
            child.stdin.end(canonical({task:task.id,go:true})+'\n');}
          catch(error){observationError=error;child.kill('SIGKILL');child.stdin.destroy();}
        });
        child.stdin.on('error',()=>{});
        child.on('exit',()=>{
          // 父进程退出后仍要终止已经确认归属的后代，否则 pipe 和工程占用都可能持续。
          try{if(!this.processes.observe(task.id,task.epoch).stopped)interrupt();}
          catch(error){observationError=error;}
        });
        child.on('close',async code=>{
          clearInterval(timer);await stopping;
          try{if(!this.processes.observe(task.id,task.epoch).stopped)throw new Error('native_stop_unconfirmed');}
          catch(error){observationError=error;}
          if(code===0&&!interrupted&&!observationError)accept();
          else reject(new Error('outcome_unknown: original native workflow needs reconciliation; '+String(observationError??'')+'; child output withheld'));
        });
      });
      if(['cancel_requested','cancelled'].includes(this.ledger.get(task.id).state))return {id:task.id,state:'quarantined',output:request.output};
      const manifest=this.verifyDelivery(request.output,runtimeIdentity,geometryContract,[request.output]);
      checkInputs();
      const bytes=Object.keys(manifest.files).reduce((total,path)=>total+lstatSync(join(request.output,path)).size,0);
      if(bytes>request.estimatedBytes||bytes>auth.maxBytes)throw new Error('budget_exceeded: output exceeds reservation');
      if(request.source&&authorizedDigest(join(request.source,'project.vectorcraft'),auth.readRoots)!==projectRevision)throw new Error('revision_conflict');
      const checked=verifiedManifests.get(manifest);
      if(!checked||authorizedDigest(join(request.output,'manifest.json'),[request.output])!==checked)throw new Error('receipt_manifest_mismatch');
      this.ledger.receipt(task.id,task.epoch,0,{manifestSha256:checked,runtimeIdentity,...(geometryContract?{geometryVerification:manifest.geometryVerification}:{})});
      const verified=this.ledger.verified(task.id,task.epoch,{path:join(request.output,'project.vectorcraft'),sha256:manifest.files['project.vectorcraft']});
      return {...verified,...(geometryContract?{geometryVerification:manifest.geometryVerification}:{})};
    }catch(error){this.ledger.unknown(task.id,task.epoch,String(error));throw error;}
  }
  close(){this.ledger.close();}
}
