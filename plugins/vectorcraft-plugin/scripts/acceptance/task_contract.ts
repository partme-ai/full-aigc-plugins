/** 真实源分支、交付保护、异步授权快照与GUI源变更后的旧计划拒绝。 */
import assert from 'node:assert/strict';
import {mkdirSync,readFileSync,writeFileSync,existsSync,cpSync,readdirSync,lstatSync,chmodSync,realpathSync,symlinkSync,unlinkSync,renameSync} from 'node:fs';
import {join,resolve,dirname,relative} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {executionIdentity} from './execution_identity.ts';
const fingerprints=executionIdentity(),config=JSON.parse(readFileSync(process.argv[2],'utf8'));
const root=resolve(config.output),implementationRoot=resolve(config.implementationRoot??join(dirname(fileURLToPath(import.meta.url)),'../..'));
const {Controller,skillDigest}=await import(pathToFileURL(join(implementationRoot,'src/harness/controller.ts')).href);
const {prepareRuntime}=await import(pathToFileURL(join(implementationRoot,'src/runtime/prepare_runtime.ts')).href);
const hash=(p:string)=>createHash('sha256').update(readFileSync(p)).digest('hex');
const tree=(directory:string)=>{const files:Record<string,string>={};const walk=(d:string)=>{for(const name of readdirSync(d).sort()){const p=join(d,name),s=lstatSync(p);assert.equal(s.isSymbolicLink(),false);if(s.isDirectory())walk(p);else files[relative(directory,p)]=hash(p);}};walk(directory);return files;};
assert.equal(existsSync(root),false,'fresh root required');mkdirSync(root,{recursive:true});
const source=resolve(config.source),skill=resolve(config.skill),runtime=resolve(config.runtimeHome),original=tree(source),sourceSha256=hash(join(source,'project.vectorcraft'));
const plan=join(root,'plan.json');writeFileSync(plan,JSON.stringify({expectedProjectSha256:sourceSha256,operations:[{command:'swatch.edit',params:{name:'Brand Primary',color:config.targetColor}}]}));
const base={key:'contract',skill,expectedSkillSha256:skillDigest(skill),plan,source,output:join(root,'output'),runtimeHome:runtime,python:config.python,estimatedBytes:10000000,
 authorization:{...config.authorization,deadline:Date.now()+180000,maxAttempts:1,maxBytes:10000000,readRoots:[root,source],writeRoots:[root,runtime]}};
const cases:any[]=[];
// 同一不可变输入建立独立文档资源；每个分支的源字节保持原样。
const branches=['branch-a','branch-b'].map(name=>{const path=join(root,name);cpSync(source,path,{recursive:true,errorOnExist:true,force:false});for(const file of Object.keys(tree(path)))chmodSync(join(path,file),0o400);return path;});
const shared=new Controller(join(root,'branches.sqlite'));
try{
 const results=await Promise.all(branches.map((path,i)=>shared.run({...base,key:'branch-'+i,source:path,output:join(root,'branch-output-'+i)})));
 assert.notEqual(results[0].resource,results[1].resource);
 for(let i=0;i<2;i++){
  const task=results[i];assert.equal(task.state,'review_ready');assert.equal(task.binding.projectRevision,sourceSha256);assert.deepEqual(tree(branches[i]),original);
  const intent=JSON.parse((shared.ledger.db.prepare('SELECT intent FROM steps WHERE task=? AND n=0').get(task.id) as any).intent);
  assert.ok(intent.sourceSnapshot&&intent.sourceSnapshotSha256);assert.equal(skillDigest(intent.sourceSnapshot),intent.sourceSnapshotSha256);
  assert.equal(hash(join(intent.sourceSnapshot,'project.vectorcraft')),sourceSha256);
  assert.equal(task.binding.inputHashes['source:manifest.json'],hash(join(branches[i],'manifest.json')));
  for(const [name,digest] of Object.entries(JSON.parse(readFileSync(join(branches[i],'manifest.json'),'utf8')).files))assert.equal(task.binding.inputHashes['source:file:'+name],digest);
 }
 cases.push({scenario:'VC-TX-001-P/SOURCE',name:'independent immutable source branches',resources:results.map((r:any)=>r.resource),projectRevision:sourceSha256,branchesUnchanged:true,deliveries:results.map((r:any)=>({taskId:r.id,planHash:r.binding.planHash,inputHashes:r.binding.inputHashes,runtimeIdentity:r.binding.runtimeIdentity,authorization:r.binding.authorization,manifestSha256:hash(join(r.output,'manifest.json'))}))});
}finally{shared.close();}
// 已存在目录、未知文件与符号链接目标在原生探测前拒绝。
let probes=0;const refusal=new Controller(join(root,'refusal.sqlite'),async(o:any)=>{probes++;return prepareRuntime(o);});
try{
 const directory=join(root,'user-directory');mkdirSync(directory);const unknown=join(directory,'unknown.txt');writeFileSync(unknown,'preserve user file');
 const linked=join(root,'linked-output');symlinkSync(directory,linked);
 for(const path of [directory,unknown,linked])await assert.rejects(()=>refusal.run({...base,key:'existing-'+path,output:path}),/output_exists/);
 await assert.rejects(()=>refusal.run({...base,key:'staging-parent',output:join(root,'only-output'),authorization:{...base.authorization,writeRoots:[join(root,'only-output'),runtime]}}),/staging_parent_not_authorized/);
 assert.equal(probes,0);assert.equal(readFileSync(unknown,'utf8'),'preserve user file');assert.equal(lstatSync(linked).isSymbolicLink(),true);assert.equal((refusal.ledger.db.prepare('SELECT COUNT(*) AS n FROM tasks').get() as any).n,0);
 cases.push({scenario:'VC-TX-001-OUTPUT/AUTH-SNAPSHOT',name:'existing outputs and unauthorized staging parent',refusals:4,probes:0,editingSessions:0,userFilesPreserved:true});
}finally{refusal.close();}
// 使用真实默认探测；探测后修改原授权数组和目录别名不改变有效物理范围。
const authorized=join(root,'authorized'),outside=join(root,'outside'),alias=join(root,'alias');mkdirSync(authorized);mkdirSync(outside);cpSync(source,join(authorized,'source'),{recursive:true});cpSync(plan,join(authorized,'plan.json'));symlinkSync(authorized,alias);
const fields=[...base.authorization.fields],objects=[...base.authorization.objects];
const aliasRequest={...base,key:'alias',plan:join(alias,'plan.json'),source:join(alias,'source'),output:join(alias,'output'),authorization:{...base.authorization,fields:[...fields],objects:[...objects],readRoots:[alias],writeRoots:[alias,runtime]}};
const frozen=new Controller(join(root,'frozen.sqlite'),async(o:any)=>{const result=await prepareRuntime(o);unlinkSync(alias);symlinkSync(outside,alias);aliasRequest.authorization.fields.push('structure');aliasRequest.authorization.objects.push(999);return result;});
try{
 const task=await frozen.run(aliasRequest);assert.equal(task.state,'review_ready');assert.equal(task.output,join(realpathSync(authorized),'output'));assert.equal(existsSync(join(outside,'output')),false);
 assert.deepEqual(task.binding.authorization.fields,fields);assert.deepEqual(task.binding.authorization.objects,objects);assert.equal(task.binding.authorization.writeRoots[0],realpathSync(authorized));
 cases.push({scenario:'VC-TX-001-AUTH-SNAPSHOT',name:'real probe with retargeted alias and broadened caller arrays',taskId:task.id,authorization:task.binding.authorization,deliveredToOriginalPhysicalRoot:true,outsideUntouched:true,manifestSha256:hash(join(task.output,'manifest.json'))});
}finally{frozen.close();}
// 真实headless探测期间改变源元数据；编辑前必须拒绝，源原生文件保持不变。
for(const [name,file] of [['manifest','manifest.json'],['inherited-plan','plan.json'],['pdf-date','pdf-export-date.json'],['absent-date','pdf-export-date.json']]){
 const localSource=join(root,'input-'+name);cpSync(source,localSource,{recursive:true});
 if(name==='absent-date'){
  unlinkSync(join(localSource,file));const manifest=JSON.parse(readFileSync(join(localSource,'manifest.json'),'utf8'));delete manifest.files[file];writeFileSync(join(localSource,'manifest.json'),JSON.stringify(manifest));
 }
 let observedProbe=false;
 const guard=new Controller(join(root,'input-'+name+'.sqlite'),async(o:any)=>{
  const result=await prepareRuntime(o);observedProbe=true;
  if(name==='absent-date')writeFileSync(join(localSource,file),'{}');
  else writeFileSync(join(localSource,file),readFileSync(join(localSource,file),'utf8')+'\n');
  return result;
 });
 try{
  const output=join(root,'input-output-'+name);
  await assert.rejects(()=>guard.run({...base,key:'input-'+name,source:localSource,output}),/stale_source_dependencies/);
  assert.equal(observedProbe,true);assert.equal(existsSync(output),false);assert.equal(hash(join(localSource,'project.vectorcraft')),sourceSha256);
  assert.equal((guard.ledger.db.prepare('SELECT COUNT(*) AS n FROM tasks').get() as any).n,0);
  assert.equal((guard.ledger.db.prepare('SELECT COUNT(*) AS n FROM native_processes').get() as any).n,0);
  cases.push({scenario:'VC-TX-001-INPUTS',name:'real probe then changed '+name,editingSessions:0,registeredTasks:0,sourceProjectUnchanged:true,error:'stale_source_dependencies'});
 }finally{guard.close();}
}
// 解析后的物理根目录或输出父目录本身被替换时，真实探测后也不能越界。
for(const replacement of ['root','output-parent']){
 const originalRoot=join(root,'path-'+replacement),redirected=join(root,'escaped-'+replacement);mkdirSync(originalRoot);mkdirSync(redirected);mkdirSync(join(originalRoot,'parent'));mkdirSync(join(redirected,'parent'));
 cpSync(source,join(originalRoot,'source'),{recursive:true});cpSync(source,join(redirected,'source'),{recursive:true});cpSync(plan,join(originalRoot,'plan.json'));cpSync(plan,join(redirected,'plan.json'));
 let probed=false;
 const guarded=new Controller(join(root,'path-'+replacement+'.sqlite'),async(o:any)=>{
  const result=await prepareRuntime(o);probed=true;const path=replacement==='root'?originalRoot:join(originalRoot,'parent');renameSync(path,path+'-saved');symlinkSync(redirected,path);return result;
 });
 try{
  await assert.rejects(()=>guarded.run({...base,key:'path-'+replacement,plan:join(originalRoot,'plan.json'),source:join(originalRoot,'source'),output:join(originalRoot,'parent','output'),authorization:{...base.authorization,readRoots:[originalRoot],writeRoots:[originalRoot,runtime]}}),/authorization_path_changed/);
  assert.equal(probed,true);assert.equal((guarded.ledger.db.prepare('SELECT COUNT(*) AS n FROM tasks').get() as any).n,0);assert.equal(existsSync(join(redirected,'output')),false);assert.equal(existsSync(join(redirected,'parent','output')),false);
  cases.push({scenario:'VC-TX-001-AUTH-SNAPSHOT',name:'real probe then physical '+replacement+' replaced with redirecting alias',error:'authorization_path_changed',registeredTasks:0,editingSessions:0,redirectedOutputAbsent:true});
 }finally{guarded.close();}
}
// GUI桌面真正修改副本并保存；随后旧计划在启动新原生探测前拒绝。
const guiSource=join(root,'gui-source');cpSync(source,guiSource,{recursive:true});
const guiRaw=execFileSync(config.python,['-I','-B',join(dirname(fileURLToPath(import.meta.url)),'task_gui_edit.py'),skill,join(runtime,'vectorcraft/0.2.0-craft.2/vectorcraft-cli'),join(runtime,'vectorcraft-desktop/0.2.0'),join(guiSource,'project.vectorcraft'),join(root,'gui-session')],{encoding:'utf8',timeout:120000});
const gui=JSON.parse(guiRaw);assert.equal(gui.result,'PASS');assert.equal(gui.listenerOwnedByPID,true);assert.equal(gui.ownedProcessesStopped,true);
let guiProbes=0;const conflict=new Controller(join(root,'gui-conflict.sqlite'),async(o:any)=>{guiProbes++;return prepareRuntime(o);});
try{
 await assert.rejects(()=>conflict.run({...base,key:'old-gui-plan',source:guiSource,output:join(root,'gui-output')}),/revision_conflict/);
 assert.equal(guiProbes,0);assert.equal(hash(join(guiSource,'project.vectorcraft')),gui.sourceAfterSha256);assert.equal(existsSync(join(root,'gui-output')),false);
 cases.push({scenario:'VC-TX-001-N',name:'signed desktop bridge saved user-source edit then old plan refused',gui,probesAfterGuiEdit:0,changedSourcePreserved:true});
}finally{conflict.close();}
assert.deepEqual(tree(source),original);
const proof={result:'PASS',fingerprints,scope:'real immutable native source branches, output guards, captured effective authorization and signed GUI desktop bridge edit conflict; manual human GUI interaction and creative evaluation are not claimed',skillSha256:skillDigest(skill),sourceProjectSha256:sourceSha256,sourceFiles:original,sourceUnchanged:true,cases};
writeFileSync(join(root,'proof.json'),JSON.stringify(proof,null,2)+'\n');console.log(JSON.stringify({result:'PASS',cases:cases.length,sourceUnchanged:true}));
