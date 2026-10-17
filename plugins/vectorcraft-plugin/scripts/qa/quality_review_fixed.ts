/** 对公开安装副本执行只读质量合同；故障与高分回执均明确标为 QA 注入。 */
import assert from 'node:assert/strict';
import { spawn,spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { cpSync,mkdirSync,readFileSync,writeFileSync,chmodSync,statSync,existsSync,readdirSync } from 'node:fs';
import { dirname,join,resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { DatabaseSync } from 'node:sqlite';

const config=JSON.parse(readFileSync(process.argv[2],'utf8'));
const installed=resolve(config.installed),native=resolve(config.native),root=resolve(config.output);
mkdirSync(root,{recursive:true});
const python='/opt/anaconda3/bin/python3',node=process.execPath;
const { ReviewStore }=await import(pathToFileURL(join(installed,'src/evaluation/review_store.ts')).href);
const { ProcessRegistry }=await import(pathToFileURL(join(installed,'src/harness/process_registry.ts')).href);
const { canonical }=await import(pathToFileURL(join(installed,'src/strict_json.ts')).href);
const sha=(v:string|Buffer)=>createHash('sha256').update(v).digest('hex');
const read=(p:string)=>JSON.parse(readFileSync(p,'utf8'));
const tree=(base:string):Record<string,string>=>Object.fromEntries(readdirSync(base,{recursive:true,encoding:'utf8'}).filter(n=>statSync(join(base,n)).isFile()).sort().map(n=>[n,sha(readFileSync(join(base,n)))]));
const original=tree(native),checkerOriginal=tree(join(installed,'src'));
const brief=join(root,'brief.txt'),rubric=join(root,'rubric.json');
writeFileSync(brief,'Preserve editable native text and freeform gradient; inspect SVG/PDF/PNG separately.');
writeFileSync(rubric,JSON.stringify({structure:4,text:4,brand:4,layout:4,legibility:4,scope:'QA receipt scoring contract, not an actual creative assessment'}));
const deadline=Date.now()+180000;
const records:any[]=[];
function inputFor(delivery:string,budget:string,policy:any={}){
 const manifest=read(join(delivery,'manifest.json'));
 return {native:join(delivery,'project.vectorcraft'),projectRevision:manifest.files['project.vectorcraft'],runtimeIdentity:manifest.runtimeSha256,
  candidates:manifest.outputs.map((x:any)=>join(delivery,x.path)),targets:[{path:brief,role:'target'}],rubric,exchangeLoss:join(delivery,'exchange-loss.json'),technicalStatus:'PASS',readRoots:[root,native],
  authorization:{objects:[2],fields:['paint.color'],deadline,maxAttempts:12,maxBytes:64*1024*1024,budgetId:budget,readRoots:[root,native],writeRoots:[root],...policy}};
}
function cli(action:string,db:string,input:any,options:{path?:string,plugin?:string}={}){
 const request=join(root,'request.json');writeFileSync(request,JSON.stringify(input));
 const child=spawnSync(node,[join(options.plugin??installed,'src/cli.ts'),action,db,request],{encoding:'utf8',timeout:20000,
  env:{...process.env,PATH:(options.path??dirname(python))+':'+process.env.PATH}});
 assert.equal(child.error,undefined);
 const text=child.status===0?child.stdout:child.stderr.trim().split('\n').find((s:string)=>s.startsWith('{'));
 return {status:child.status,value:JSON.parse(text!)};
}
function checked(db:string,input:any,options:any={}){const result=cli('review-checked',db,input,options);assert.equal(result.status,0,JSON.stringify(result));return result.value;}
function failure(action:string,db:string,input:any,reason:string,options:any={}){const result=cli(action,db,input,options);assert.notEqual(result.status,0);assert.match(result.value.error,new RegExp(reason));return result.value;}
function receipt(request:any){return {schema:'vectorcraft-review-receipt/v1',requestId:request.id,bindingHash:request.bindingHash,
 reviewer:{kind:'host-model',identity:'explicit QA injected maximal score; not actual visual judgment',contextOrigin:'same acceptance driver; no independent reviewer',independenceEvidence:null},
 verdict:'accept',issues:[],scores:{structure:4,text:4,brand:4,layout:4,legibility:4}};}
function sql(db:string,query:string,parameters:any[]=[]){const c=new DatabaseSync(db);try{return c.prepare(query).all(...parameters);}finally{c.close();}}
function verifySnapshot(db:string,request:any){
 const task:any=sql(db,'SELECT * FROM tasks WHERE id=?',[request.input.technicalCheckId])[0];
 const report=request.input.technicalEvidence,manifest=read(join(dirname(request.input.native),'manifest.json'));
 assert.equal(task.state,'review_ready');assert.equal(task.attempts,1);
 assert.equal(sha(canonical({input:request.input,fingerprints:request.fingerprints})),request.bindingHash);
 assert.equal(report.manifestSha256,sha(readFileSync(join(dirname(request.input.native),'manifest.json'))));
 assert.deepEqual(report.files,manifest.files);
 for(const [name,digest] of Object.entries(manifest.files)){
  const p=join(task.output,'delivery',name);assert.equal(sha(readFileSync(p)),digest);assert.equal(statSync(p).mode&0o777,0o400);
 }
 for(const [name,digest] of Object.entries(report.checkerFiles)){
  const p=join(task.output,'checker',name);assert.equal(sha(readFileSync(p)),digest);assert.equal(statSync(p).mode&0o777,0o400);
 }
 const usage:any=sql(db,'SELECT * FROM budgets WHERE id=?',[request.input.authorization.budgetId])[0];
 assert.equal(usage.attempts,1);assert(usage.bytes>0);
 return {taskId:task.id,state:task.state,attempts:task.attempts,bytes:task.bytes,budget:{attempts:usage.attempts,bytes:usage.bytes},
  readonlySnapshotFiles:Object.keys(manifest.files).length+1,checkerFiles:report.checkerFiles,bindingVerified:true};
}

// 两次独立 CLI 进程代表持久重启；去重不重复消耗共享额度。
const healthy=join(native,'exported'),healthyDb=join(root,'healthy.sqlite'),healthyInput=inputFor(healthy,'healthy');
const healthyRequest=checked(healthyDb,healthyInput),healthySnapshot=verifySnapshot(healthyDb,healthyRequest);
assert.equal(healthyRequest.input.technicalStatus,'PASS');assert.equal(healthyRequest.input.technicalEvidence.engineeringStatus,'NOT_RUN');
assert.equal(healthyRequest.input.technicalEvidence.creativeStatus,'NOT_RUN');assert.equal(healthyRequest.input.technicalEvidence.acceptanceStatus,'pending');
assert.equal(checked(healthyDb,healthyInput).id,healthyRequest.id);
assert.equal((sql(healthyDb,'SELECT attempts FROM budgets WHERE id=?',['healthy'])[0] as any).attempts,1);
records.push({case:'healthy-persistent-decode',result:'PASS',request:healthyRequest,snapshot:healthySnapshot,restartDeduplicated:true,engineeringNativeReopenNotPromoted:true});

for(const fmt of ['png','pdf','svg']){
 const input=inputFor(join(native,'corrupt-'+fmt),'corrupt-'+fmt),db=join(root,'corrupt-'+fmt+'.sqlite');
 const request=checked(db,input),snapshot=verifySnapshot(db,request),technical=request.input.technicalEvidence;
 assert.equal(technical.artifactIntegrityStatus,'PASS');assert.equal(technical.technicalStatus,'FAIL');
 const response=cli('review-import',db,receipt(request));assert.equal(response.status,0);
 assert.equal(response.value.creativeStatus,'PASS');assert.equal(response.value.technicalStatus,'FAIL');assert.equal(response.value.engineeringStatus,'NOT_RUN');
 assert.equal(response.value.acceptanceStatus,'blocked');assert.equal(response.value.state,'technical_failed');assert.equal(response.value.independent,false);
 assert.equal((sql(db,'SELECT state FROM reviews WHERE id=?',[request.id])[0] as any).state,'technical_failed');
 records.push({case:'undecodable-'+fmt+'-maximal-qa-score',result:'PASS',explicitQaMutation:true,explicitQaReceipt:true,request,snapshot,receipt:receipt(request),response:response.value,
  duplicateReceiptRefusal:failure('review-import',db,receipt(request),'duplicate_review_receipt')});
}

// 同一原生交付，在不安装任何包的本地隔离虚拟环境中必须保持未执行。
const missing=join(root,'no-decoders');mkdirSync(missing);
const environment=join(missing,'environment');const created=spawnSync(python,['-I','-B','-m','venv','--without-pip',environment],{encoding:'utf8'});assert.equal(created.status,0,created.stderr);
const emptyPython=join(environment,'bin/python3');
writeFileSync(join(missing,'python3'),'#!'+python+'\nimport os,sys\nos.execv('+JSON.stringify(emptyPython)+',['+JSON.stringify(emptyPython)+',*sys.argv[1:]])\n');chmodSync(join(missing,'python3'),0o700);
const probe=spawnSync(emptyPython,['-I','-B','-c','import importlib.util,json; print(json.dumps({n:importlib.util.find_spec(n) is None for n in ["PIL","fitz"]}))'],{encoding:'utf8'});
assert.deepEqual(JSON.parse(probe.stdout),{PIL:true,fitz:true});
const missingDb=join(root,'missing.sqlite'),missingRequest=checked(missingDb,inputFor(healthy,'missing'),{path:missing});
assert.equal(missingRequest.input.technicalStatus,'NOT_RUN');assert.equal(missingRequest.input.technicalEvidence.artifactIntegrityStatus,'PASS');
const missingResponse=cli('review-import',missingDb,receipt(missingRequest));assert.equal(missingResponse.status,0);assert.equal(missingResponse.value.state,'technical_pending');assert.equal(missingResponse.value.acceptanceStatus,'pending');
records.push({case:'real-decoder-unavailable',result:'PASS',missingModules:JSON.parse(probe.stdout),request:missingRequest,response:missingResponse.value,explicitQaReceipt:true,snapshot:verifySnapshot(missingDb,missingRequest)});

records.push({case:'json-evidence-injection',result:'PASS',refusals:['review-request','review-checked'].map(action=>failure(action,join(root,'injection.sqlite'),{...healthyInput,technicalEvidenceOrigin:'checked-decoder',technicalEvidence:{technicalStatus:'PASS'}},'technical_evidence_requires_check'))});
const legacy=cli('review-request',join(root,'legacy.sqlite'),healthyInput);assert.equal(legacy.status,0);assert.equal(legacy.value.input.technicalEvidenceOrigin,'caller_unverified');
records.push({case:'legacy-unverified-origin',result:'PASS',origin:legacy.value.input.technicalEvidenceOrigin});

// 各项故障只改独立 QA 副本，绝不改动公开安装字节或原始原生交付。
for(const name of ['native','candidate','manifest','auxiliary','target','rubric']){
 const area=join(root,'stale-'+name);mkdirSync(area);const delivery=join(area,'delivery');cpSync(healthy,delivery,{recursive:true});
 const input=inputFor(delivery,'stale-'+name);input.targets=[{path:join(area,'target.txt'),role:'target'}];input.rubric=join(area,'rubric.json');
 writeFileSync(input.targets[0].path,readFileSync(brief));writeFileSync(input.rubric,readFileSync(rubric));
 const db=join(area,'review.sqlite'),request=checked(db,input),manifest=read(join(delivery,'manifest.json'));
 const file=name==='native'?input.native:name==='candidate'?input.candidates[0]:name==='manifest'?join(delivery,'manifest.json'):name==='auxiliary'?join(delivery,'native.json'):name==='target'?input.targets[0].path:input.rubric;
 const before=sha(readFileSync(file));writeFileSync(file,Buffer.concat([readFileSync(file),Buffer.from('\nexplicit QA drift')]));
 records.push({case:'stale-'+name,result:'PASS',explicitQaMutation:true,previousBindingHash:request.bindingHash,beforeSha256:before,afterSha256:sha(readFileSync(file)),manifestFiles:Object.keys(manifest.files).length,
  refusal:failure('review-import',db,receipt(request),'stale_review_binding')});
}
for(const name of ['src/evaluation/delivery_quality.py','src/harness/process_runner.py','skills/vectorcraft-use/scripts/exchange_loss.py']){
 const area=join(root,'checker-'+name.split('/').at(-1));mkdirSync(area);const copy=join(area,'plugin');mkdirSync(copy);cpSync(join(installed,'src'),join(copy,'src'),{recursive:true});
 mkdirSync(join(copy,'skills/vectorcraft-use/scripts'),{recursive:true});cpSync(join(installed,'skills/vectorcraft-use/scripts/exchange_loss.py'),join(copy,'skills/vectorcraft-use/scripts/exchange_loss.py'));
 const db=join(area,'review.sqlite'),request=checked(db,inputFor(healthy,'checker-'+name),{plugin:copy});const file=join(copy,name),before=sha(readFileSync(file));
 assert.equal(before,request.input.technicalEvidence.checkerFiles[name]);writeFileSync(file,Buffer.concat([readFileSync(file),Buffer.from('\n# explicit isolated QA drift\n')]));
 records.push({case:'stale-checker-'+name,result:'PASS',isolatedPublishedCodeCopy:true,beforeSha256:before,afterSha256:sha(readFileSync(file)),
  refusal:failure('review-import',db,receipt(request),'stale_review_binding',{plugin:copy})});
}

function slow(area:string,db:string){
 const dir=join(area,'bin');mkdirSync(dir);const trace=join(area,'before-decoder.json');
 const code='#!'+python+'\nimport sqlite3,json,time\nfrom pathlib import Path\ndb=sqlite3.connect('+JSON.stringify(db)+')\nr=db.execute("SELECT output,attempts,bytes FROM tasks").fetchone()\nb=db.execute("SELECT attempts,bytes FROM budgets").fetchone()\nfiles=[p for p in Path(r[0]).rglob("*") if p.is_file()]\nPath('+JSON.stringify(trace)+').write_text(json.dumps({"taskAttempts":r[1],"budgetAttempts":b[0],"budgetBytes":b[1],"snapshotFiles":len(files),"allReadonly":all(p.stat().st_mode&0o777==0o400 for p in files)}))\ntime.sleep(20)\n';
 writeFileSync(join(dir,'python3'),code);chmodSync(join(dir,'python3'),0o700);return {dir,trace};
}
const timeoutArea=join(root,'timeout');mkdirSync(timeoutArea);const timeoutDb=join(timeoutArea,'review.sqlite'),timeoutWrapper=slow(timeoutArea,timeoutDb);
const timeoutInput=inputFor(healthy,'timeout',{deadline:Date.now()+1800});const timeoutError=failure('review-checked',timeoutDb,timeoutInput,'technical_check_interrupted',{path:timeoutWrapper.dir});
const beforeTimeout=read(timeoutWrapper.trace);assert(beforeTimeout.allReadonly&&beforeTimeout.taskAttempts===1&&beforeTimeout.budgetAttempts===1&&beforeTimeout.snapshotFiles>3);
const timeoutTask:any=sql(timeoutDb,'SELECT id,epoch,state FROM tasks')[0];const timeoutConnection=new DatabaseSync(timeoutDb);const timeoutStopped=new ProcessRegistry(timeoutConnection).observe(timeoutTask.id,timeoutTask.epoch);timeoutConnection.close();assert(timeoutStopped.stopped);
const timeoutRestart=failure('review-checked',timeoutDb,timeoutInput,'reconcile_required');
assert.equal((sql(timeoutDb,'SELECT attempts FROM budgets')[0] as any).attempts,1);
records.push({case:'timeout-owned-group-and-restart',result:'PASS',beforeDecoder:beforeTimeout,state:timeoutTask.state,error:timeoutError,restart:timeoutRestart,stopped:timeoutStopped.stopped,budgetAttemptsAfterRestart:1});

const crashArea=join(root,'crash');mkdirSync(crashArea);const crashDb=join(crashArea,'review.sqlite'),crashWrapper=slow(crashArea,crashDb),crashInput=inputFor(healthy,'crash');
const crashRequest=join(crashArea,'input.json');writeFileSync(crashRequest,JSON.stringify(crashInput));
const coordinator=spawn(node,[join(installed,'src/cli.ts'),'review-checked',crashDb,crashRequest],{stdio:['ignore','pipe','pipe'],env:{...process.env,PATH:crashWrapper.dir+':'+process.env.PATH}});
let ended=false;coordinator.once('close',()=>{ended=true;});const limit=Date.now()+10000;
while(!existsSync(crashWrapper.trace)||!sql(crashDb,'SELECT * FROM native_processes').length){assert(!ended&&Date.now()<limit,'coordinator did not register decoder');await new Promise(r=>setTimeout(r,25));}
coordinator.kill('SIGKILL');while(!ended)await new Promise(r=>setTimeout(r,25));
const crashConnection=new DatabaseSync(crashDb),registry=new ProcessRegistry(crashConnection),crashTask:any=sql(crashDb,'SELECT id,epoch,state FROM tasks')[0];
const observed=registry.observe(crashTask.id,crashTask.epoch);assert(observed.owned&&!observed.stopped);
const crashRestart=failure('review-checked',crashDb,crashInput,'reconcile_required');await registry.stop(crashTask.id,crashTask.epoch);const stopped=registry.observe(crashTask.id,crashTask.epoch);crashConnection.close();assert(stopped.stopped);
assert.equal((sql(crashDb,'SELECT attempts FROM budgets')[0] as any).attempts,1);
records.push({case:'coordinator-sigkill-unknown-no-replay',result:'PASS',beforeDecoder:read(crashWrapper.trace),recordedState:crashTask.state,liveOwnedGroupAfterCrash:observed.owned,restart:crashRestart,ownedGroupStopped:stopped.stopped,budgetAttemptsAfterRestart:1});

const budgetDb=join(root,'budget.sqlite'),budgetInput=inputFor(healthy,'one-attempt',{maxAttempts:1});checked(budgetDb,budgetInput);
const nextBrief=join(root,'second-target.txt');writeFileSync(nextBrief,'Explicit second candidate target');
const snapshotsBeforeBudgetRefusal=tree(join(root,'.technical-checks'));
const budgetError=failure('review-checked',budgetDb,{...budgetInput,targets:[{path:nextBrief,role:'target'}]},'budget_exceeded');
const tasks=sql(budgetDb,'SELECT state,output FROM tasks') as any[];assert.equal(tasks.length,1);assert.equal(tasks[0].state,'review_ready');assert.deepEqual(tree(join(root,'.technical-checks')),snapshotsBeforeBudgetRefusal);
assert.equal((sql(budgetDb,'SELECT attempts FROM budgets')[0] as any).attempts,1);
records.push({case:'shared-budget-before-snapshot',result:'PASS',error:budgetError,unlaunchedSnapshotAbsent:true,budgetAttempts:1});

assert.deepEqual(tree(native),original);assert.deepEqual(tree(join(installed,'src')),checkerOriginal);
const report={schema:'vectorcraft-quality-fixed-native/v1',result:'PASS',level:config.level??'fixed-install',pluginVersion:read(join(installed,'plugin.json')).version,
 platform:process.platform+'-'+process.arch,driverSha256:sha(readFileSync(process.argv[1])),runtimeIdentity:healthyInput.runtimeIdentity,
 nativeProofSha256:sha(readFileSync(join(native,'proof.json'))),originalFiles:original,records,
 nativeSourceAndExportsPreserved:true,installedCodePreserved:true,
 scope:'supplied code snapshot and newly created/reopened native source; maximal-score receipts are explicitly synthetic QA, not creative judgment; engineering remains NOT_RUN in readonly decoder',
 excluded:['actual creative review','GUI','other platforms','complete V1']};
const replacements:[[string,string],[string,string],[string,string]]=[[native,'QA_NATIVE'],[root,'QA_ROOT'],[installed,'INSTALLED_PLUGIN']];
let text=JSON.stringify(report,null,2)+'\n';for(const [from,to] of replacements)text=text.split(from).join(to);
writeFileSync(join(root,'proof.json'),text);console.log(JSON.stringify({result:'PASS',cases:records.length}));
