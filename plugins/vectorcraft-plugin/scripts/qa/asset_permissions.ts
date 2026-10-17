/** 真实受管素材创建与继承返工；不替代秘密引用或固定宿主分发验收。 */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFileSync,writeFileSync,mkdirSync,existsSync} from 'node:fs';
import {join} from 'node:path';
import {pathToFileURL} from 'node:url';
const c=JSON.parse(readFileSync(process.argv[2],'utf8'));
assert(!existsSync(c.output));mkdirSync(c.output,{recursive:true});
const {Controller,skillDigest}=await import(pathToFileURL(join(c.installed,'src/harness/controller.ts')).href);
const sha=(bytes:Buffer)=>createHash('sha256').update(bytes).digest('hex');
const lock=JSON.parse(readFileSync(join(c.installed,'skills.lock.json'),'utf8')).sources[0];
const skill=join(c.installed,'skills/vectorcraft-use'),before=skillDigest(skill);
const input=join(c.output,'authorized assets');mkdirSync(input);
const asset=join(input,'logo.svg');writeFileSync(asset,'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="16"><path fill="#ee5533" d="M0 0H24V16H0Z"/></svg>');
const assets={logo:{path:asset,sha256:sha(readFileSync(asset))}};
const exports=['svg','pdf','png'].map(format=>({format,artboard:0}));
const plan=join(c.output,'create.json');writeFileSync(plan,JSON.stringify({document:{width:96,height:80,units:'Pixels'},assets,
 operations:[{command:'asset.place',params:{asset:'logo',rect:[12,16,36,24]}}],exports}));
const controller=new Controller(join(c.output,'state.sqlite'));
const authorization={objects:[1,2,3],fields:['kind','appearance'],deadline:Date.now()+120000,maxAttempts:8,maxBytes:64*1024*1024,
 readRoots:[c.output,c.runtime],writeRoots:[c.output,c.runtime]};
const request=(key:string,planFile:string,output:string,source?:string)=>({key,skill,expectedSkillSha256:lock.sha256['vectorcraft-use'],plan:planFile,
 output,runtimeHome:c.runtime,python:c.python,estimatedBytes:8*1024*1024,authorization,...(source?{source}:{} )});
try {
 const first=join(c.output,'created with spaces');const created=await controller.run(request('create',plan,first));
 assert.equal(created.state,'review_ready');const manifest=JSON.parse(readFileSync(join(first,'manifest.json'),'utf8'));
 assert.equal(manifest.outputs.length,3);assert.equal(Object.keys(manifest.assets).length,1);
 const original=skillDigest(first),revisionPlan=join(c.output,'revise.json');
 writeFileSync(revisionPlan,JSON.stringify({expectedProjectSha256:manifest.files['project.vectorcraft'],operations:[],exports}));
 const second=join(c.output,'inherited revision');const revised=await controller.run(request('revision',revisionPlan,second,first));
 assert.equal(revised.state,'review_ready');assert.equal(skillDigest(first),original);
 const updated=JSON.parse(readFileSync(join(second,'manifest.json'),'utf8'));
 assert.equal(updated.outputs.length,3);assert.equal(updated.assets.logo.sha256,manifest.assets.logo.sha256);
 for(const m of [manifest,updated])assert(!('inputRoots' in m.assets.logo)&&!('inputIdentity' in m.assets.logo));
 const refusals=[];
 for(const fault of ['untrusted-command','outside-root']) {
  const bad=join(c.output,fault+'.json'),data=JSON.parse(readFileSync(plan,'utf8'));
  if(fault==='untrusted-command')data.assets.logo.command='file.open';
  writeFileSync(bad,JSON.stringify(data));const output=join(c.output,fault);
  const req=request(fault,bad,output);
  if(fault==='outside-root')req.authorization={...authorization,readRoots:[bad,c.runtime]};
  await assert.rejects(controller.run(req),fault==='untrusted-command'?/invalid_asset_record/:/outside_authorized_roots/);
  assert(!existsSync(output));refusals.push(fault);
 }
 const groups=controller.ledger.db.prepare('SELECT task,epoch FROM native_processes').all() as any[];
 assert(groups.length>=2&&groups.every(g=>controller.processes.observe(g.task,g.epoch).stopped));
 assert.equal(before,skillDigest(skill));
 const proof={schema:'vectorcraft-managed-asset-permissions/v1',result:'PASS',pluginVersion:JSON.parse(readFileSync(join(c.installed,'plugin.json'),'utf8')).version,
 sourceRef:lock.ref,sourceCommit:lock.sha,skillSha256:before,driverSha256:sha(readFileSync(process.argv[1])),platform:process.platform+'-'+process.arch,
 creation:manifest,revision:updated,sourceUnchanged:true,skillUnchanged:true,refusals,registeredGroups:groups.length,allGroupsStopped:true,
 scope:'Actual current candidate Controller native creation and inherited asset revision with six exports; two prelaunch refusals; no host-secret, fixed distribution or creative acceptance'};
 let encoded=JSON.stringify(proof,null,2)+'\n';for(const [from,to] of [[c.runtime,'RUNTIME'],[c.output,'QA_ROOT'],[c.installed,'PLUGIN']])encoded=encoded.split(from).join(to);
 writeFileSync(join(c.output,'proof.json'),encoded);console.log(JSON.stringify({result:'PASS',registeredGroups:groups.length,refusals:refusals.length}));
}finally{controller.close();}
