import {assertNoLiteralSecrets} from '../../scripts/harness/input_policy.ts';
import {authorizedRead,authorizedDigests} from '../../scripts/harness/authorized_file.ts';
import {authorizedDirectory} from '../../scripts/harness/authorized_tree.ts';
import {authorizedWrite} from '../../scripts/harness/authorized_write.ts';
import {nativeEnvironment} from '../../scripts/harness/native_environment.ts';
import { spawn } from 'node:child_process';
import { createHash,randomUUID } from 'node:crypto';
import { lstatSync,realpathSync } from 'node:fs';
import { dirname,resolve,relative,isAbsolute,join } from 'node:path';
import { Ledger,resourcePath } from '../../scripts/harness/ledger.ts';
import { ProcessRegistry } from '../../scripts/harness/process_registry.ts';
import { canonical,strictJson } from '../strict_json.ts';
import { ReviewStore } from './review_store.ts';
import { captureChecker,checkerFiles } from './checker_bundle.ts';

const hash=(value:string|Buffer)=>createHash('sha256').update(value).digest('hex');
const inside=(root:string,path:string)=>{const sub=relative(root,path);return !isAbsolute(sub)&&sub!=='..'&&!sub.startsWith('../');};
const pause=(ms:number)=>new Promise(r=>setTimeout(r,ms));

/** 只读技术解码协调器：先持久化共享预算，再检查快照，未知执行禁止自动重放。 */
export class TechnicalReview {
  store:ReviewStore;
  constructor(store:ReviewStore){this.store=store;}
  async request(input:any,options:{python?:string}={}):Promise<any>{
    assertNoLiteralSecrets(input);
    // 冻结调用方数据及写入根，异步解码期间不能改写授权或延长截止时间。
    input=strictJson(canonical(input));
    if(input?.technicalEvidence!==undefined||input?.technicalEvidenceOrigin!==undefined)throw new Error('technical_evidence_requires_check');
    const source=resolve(dirname(input.native)),manifest=join(source,'manifest.json');
    if(resolve(input.native)!==join(source,'project.vectorcraft'))throw new Error('invalid_native_path');
    if(!Array.isArray(input.authorization?.readRoots))throw new Error('technical_read_outside_roots');
    const readRoots=input.authorization.readRoots.map((root:string)=>realpathSync(root));
    const parent=realpathSync(dirname(this.store.path)),base=join(parent,'.technical-checks');
    const writeRoots=input.authorization?.writeRoots;
    const frozenWriteRoots=Array.isArray(writeRoots)?writeRoots.map((root:string)=>resourcePath(root)):undefined;
    const sources:Record<string,string>={},contents=new Map<string,Buffer>();let bytes=0;
    const capture=(path:string)=>{
      const physical=realpathSync(path);
      if(!readRoots.some((root:string)=>inside(root,physical)))throw new Error('technical_read_outside_roots');
      if(!this.store.roots.some(root=>inside(root,physical)))throw new Error('review_path_outside_roots');
      const roots=readRoots.flatMap((readRoot:string)=>this.store.roots.flatMap(storeRoot=>inside(readRoot,storeRoot)?[storeRoot]:inside(storeRoot,readRoot)?[readRoot]:[]));
      const value=authorizedRead(physical,roots);sources[path]=hash(value);return value;
    };
    const manifestBytes=capture(manifest);contents.set('manifest.json',manifestBytes);bytes+=manifestBytes.length;
    const data=strictJson(manifestBytes.toString('utf8'));
    if(data.schema!=='vectorcraft-delivery/v1'||data.runtimeSha256!==input.runtimeIdentity||data.files?.['project.vectorcraft']!==input.projectRevision
      ||!data.files||Array.isArray(data.files)||Object.keys(data.files).length>4096||!Array.isArray(data.outputs))throw new Error('invalid_delivery_binding');
    for(const [name,expected] of Object.entries(data.files)){
      if(!name||name==='manifest.json'||name.includes('\\')||isAbsolute(name)||name.split('/').some(p=>!p||p==='.'||p==='..'))throw new Error('invalid_artifact_path');
      const path=join(source,name);
      for(let part=path;part!==source;part=dirname(part))if(lstatSync(part).isSymbolicLink())throw new Error('invalid_artifact_path');
      if(!lstatSync(path).isFile()||lstatSync(path).size>64*1024*1024)throw new Error('artifact_size_limit');
      const value=capture(path);if(hash(value)!==expected||sources[path]!==expected)throw new Error('artifact_identity_mismatch');
      bytes+=value.length;if(bytes>256*1024*1024)throw new Error('artifact_size_limit');contents.set(name,value);
    }
    if(!Array.isArray(input.candidates)||!input.candidates.length||input.candidates.some((p:string)=>!data.outputs.some((o:any)=>typeof o.path==='string'&&resolve(source,o.path)===resolve(p)&&o.path in data.files)))throw new Error('unbound_candidate');
    for(const path of [...input.candidates,...input.targets.map((t:any)=>t.path),input.rubric,input.exchangeLoss])capture(path);
    const checker=captureChecker(),checkerSha=checker.files['src/evaluation/delivery_quality.py'],launcherSha=checker.files['scripts/harness/process_runner.py'];
    const digest=hash(canonical({input,sources,checkerFiles:checker.files}));
    if(!frozenWriteRoots?.some((root:string)=>inside(root,base)))throw new Error('technical_write_outside_roots');
    // 不沿用调用者可控制的链接；快照目录与报告都必须是新建普通路径。
    try{if(lstatSync(base).isSymbolicLink())throw new Error('technical_write_outside_roots');}catch(e){if((e as NodeJS.ErrnoException).code!=='ENOENT')throw e;}
    const output=join(base,digest),ledger=new Ledger(this.store.path),processes=new ProcessRegistry(ledger.db);
    ledger.db.exec('CREATE TABLE IF NOT EXISTS technical_checks(task TEXT PRIMARY KEY,report TEXT NOT NULL,report_sha TEXT NOT NULL,sources TEXT NOT NULL,review_id TEXT);');
    let task:any;
    try{
      task=ledger.claim('technical-review:'+digest,output,output,{planHash:hash(canonical(input)),inputHashes:{...sources,checkerBundle:hash(canonical(checker.files))},
        projectRevision:input.projectRevision,runtimeIdentity:input.runtimeIdentity,authorization:input.authorization});
      if(task.state==='review_ready')return this.store.requestFromCheck(input,task.id);
      if(task.state!=='ready')throw new Error('reconcile_required');
      this.store.validateInput(input);
      ledger.intent(task.id,task.epoch,0,{kind:'readonly-delivery-decode',checkerFiles:checker.files,sources},bytes+[...checker.contents.values()].reduce((total,value)=>total+value.length,0)+1024*1024);
      try{
        authorizedDirectory(base,parent);authorizedDirectory(output,base,true);const snapshot=join(output,'delivery');authorizedDirectory(snapshot,output,true);
        for(const [name,value] of contents){const path=join(snapshot,name);authorizedDirectory(dirname(path),snapshot);authorizedWrite(path,snapshot,value,0o400);}
        const checkerRoot=join(output,'checker');
        for(const [name,value] of checker.contents){const path=join(checkerRoot,name);authorizedDirectory(dirname(path),output);authorizedWrite(path,output,value,0o400);}
        const helper=join(checkerRoot,'src/evaluation/delivery_quality.py'),launcher=join(checkerRoot,'scripts/harness/process_runner.py');
        const marker=randomUUID();
        // nonce 留在 exec 后的命令行，供持久进程组身份核对；不向解码器增加公开参数。
        const code=`import runpy,sys\nsys.argv=${JSON.stringify([helper,snapshot,'--runtime-sha256',input.runtimeIdentity,'--project-sha256',input.projectRevision])}\nrunpy.run_path(${JSON.stringify(helper)},run_name='__main__')\n# ${marker}`;
        const child=spawn(options.python??'python3',['-I','-B',launcher,marker,'-c',code],{env:nativeEnvironment(),detached:true,stdio:['pipe','pipe','pipe']});
        let text='',errorText='',ended=false,exitCode:number|null=null,spawnError:Error|undefined,overflow=false;
        child.on('error',e=>{spawnError=e;ended=true;});child.on('close',code=>{exitCode=code;ended=true;});
        child.stdout.on('data',b=>{if(text.length+b.length>1024*1024)overflow=true;else text+=b.toString();});
        child.stderr.on('data',b=>{if(errorText.length+b.length>1024*1024)overflow=true;else errorText+=b.toString();});
        child.stdin.on('error',()=>{});
        await new Promise<void>(r=>{child.once('spawn',()=>r());child.once('error',()=>r());});
        if(spawnError||!child.pid)throw new Error('technical_check_interrupted');
        try{processes.register(task.id,task.epoch,child.pid,marker);}catch(error){child.kill('SIGKILL');throw error;}
        child.stdin.end(JSON.stringify({task:marker,go:true})+'\n');
        try{
          while(!ended){if(Date.now()>=input.authorization.deadline||overflow)throw new Error('technical_check_interrupted');processes.observe(task.id,task.epoch);await pause(25);}
          if(!processes.observe(task.id,task.epoch).stopped||exitCode!==0||overflow)throw new Error('technical_check_interrupted');
        }catch(error){await processes.stop(task.id,task.epoch);throw error;}
        const report=strictJson(text);
        if(report.schema!=='vectorcraft-technical-review/v1'||report.projectRevision!==input.projectRevision||report.runtimeIdentity!==input.runtimeIdentity
          ||report.manifestSha256!==sources[manifest]||canonical(report.files)!==canonical(data.files)||!['PASS','FAIL','NOT_RUN'].includes(report.technicalStatus)
          ||report.engineeringStatus!=='NOT_RUN'||report.nativeReopenStatus!=='NOT_RUN')throw new Error('invalid_technical_report');
        for(const [path,expected] of Object.entries(sources))if(hash(capture(path))!==expected)throw new Error('stale_review_binding');
        const capturedChecker=authorizedDigests(Object.keys(checker.files).map(name=>join(checkerRoot,name)),[checkerRoot]);
        if(canonical(checkerFiles())!==canonical(checker.files)||Object.entries(checker.files).some(([name,expected])=>capturedChecker[join(checkerRoot,name)]!==expected))throw new Error('technical_checker_changed');
        report.checkId=task.id;report.checkerSha256=checkerSha;report.launcherSha256=launcherSha;report.checkerFiles=checker.files;
        const serialized=canonical(report),reportPath=join(output,'report.json'),written=authorizedWrite(reportPath,output,serialized,0o400);
        ledger.receipt(task.id,task.epoch,0,{reportSha256:written.sha256});ledger.verified(task.id,task.epoch,{path:reportPath,sha256:written.sha256});
        ledger.db.prepare('INSERT INTO technical_checks(task,report,report_sha,sources) VALUES(?,?,?,?)').run(task.id,serialized,hash(serialized),canonical(sources));
        return this.store.requestFromCheck(input,task.id);
      }catch(error){if(ledger.get(task.id).state==='running')ledger.unknown(task.id,task.epoch,String(error));throw error;}
    }finally{ledger.close();}
  }
}
