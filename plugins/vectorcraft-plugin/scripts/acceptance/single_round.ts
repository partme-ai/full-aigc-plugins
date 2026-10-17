/** 显式品牌单轮验收驱动：评审由外部回执输入，不生成评分或再次调用模型。 */
import assert from 'node:assert/strict';
import { executionIdentity } from './execution_identity.ts';
const executionFingerprints=executionIdentity();
import { readFileSync, writeFileSync, mkdirSync, copyFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { createHash } from 'node:crypto';
import { Controller, skillDigest } from '../../src/harness/controller.ts';
import { ReviewStore } from '../../src/evaluation/review_store.ts';
import { strictJson } from '../../src/strict_json.ts';

const [configFile]=process.argv.slice(2);
const input=strictJson(readFileSync(configFile,'utf8'));
const root=resolve(input.output),source=resolve(input.source),runtimeHome=resolve(input.runtimeHome),skill=resolve(input.skill);
mkdirSync(root,{recursive:true});
const manifest=strictJson(readFileSync(join(source,'manifest.json'),'utf8'));
const hash=(p:string)=>createHash('sha256').update(readFileSync(p)).digest('hex');
const original=Object.fromEntries(Object.keys(manifest.files).map(p=>[p,hash(join(source,p))]));
const rubric=join(root,'rubric.json');copyFileSync(resolve('docs/vector-review-rubric.json'),rubric);
const brief=join(root,'brief.txt');writeFileSync(brief,input.brief);
const authorization={...input.authorization,deadline:Date.now()+60000,budgetId:'single-round-brand-review',readRoots:[source,root],writeRoots:[root,runtimeHome]};
// 全局色板会改动所有消费者；不能仅凭一条对象建议扩大授权。
if(hash(join(source,'native.json'))!==manifest.files['native.json'])throw new Error('native_snapshot_mismatch');
const native=strictJson(readFileSync(join(source,'native.json'),'utf8'));
const consumers:{objectId:number,field:string}[]=[];
function boundPaths(value:any,path:string):string[]{
  if(!value||typeof value!=='object'||(path&&Number.isSafeInteger(value.id)&&value.kind))return [];
  const own=value.swatch==='Brand Primary'&&Object.hasOwn(value,'color')?[path+'.color']:[];
  return own.concat(Object.entries(value).flatMap(([key,child])=>boundPaths(child,path?path+'.'+key:key)));
}
function inspectObjects(value:any){
  if(!value||typeof value!=='object')return;
  if(Number.isSafeInteger(value.id)&&value.kind){
    for(const field of boundPaths(value,''))consumers.push({objectId:value.id,field});
  }
  for(const child of Object.values(value))inspectObjects(child);
}
inspectObjects(native.layers);
if(!consumers.length||consumers.some(c=>!authorization.objects.includes(c.objectId)||!authorization.fields.includes(c.field)
  ||!input.changes.some((change:any)=>change.objectId===c.objectId&&change.field===c.field&&change.value===input.targetColor)))throw new Error('brand_consumers_outside_authorization');
const store=new ReviewStore(join(root,'review.sqlite'),[source,root]);
let request:any;
try {
  request=store.request({projectRevision:manifest.files['project.vectorcraft'],runtimeIdentity:manifest.runtimeSha256,
    native:join(source,'project.vectorcraft'),candidates:[join(source,'artboard-1.png'),join(source,'artboard-3.png')],
    targets:[{path:brief,role:'target'}],rubric,exchangeLoss:join(source,'exchange-loss.json'),technicalStatus:'PASS',authorization});
  writeFileSync(join(root,'request.json'),JSON.stringify(request,null,2));
}finally{store.close();}
// 在另一个连接中导入；证明请求在进程重启后仍可读取，不把连接重开冒充独立评审。
const reopened=new ReviewStore(join(root,'review.sqlite'),[source,root]);
let imported:any,proposal:any;
try {
  const receipt={...strictJson(readFileSync(input.receipt,'utf8')),requestId:request.id,bindingHash:request.bindingHash};
  imported=reopened.importReceipt(receipt);assert.equal(imported.state,'revision_proposed');assert.equal(imported.independent,false);
  assert.throws(()=>reopened.importReceipt(receipt),/duplicate_review_receipt/);
  proposal=reopened.revision(request.id,input.changes);
  writeFileSync(join(root,'receipt.json'),JSON.stringify(receipt,null,2));
  writeFileSync(join(root,'proposal.json'),JSON.stringify(proposal,null,2));
}finally{reopened.close();}
const plan={expectedProjectSha256:proposal.expectedProjectRevision,operations:[{command:'swatch.edit',params:{name:'Brand Primary',color:input.targetColor}}]};
if(proposal.changes.some((c:any)=>c.value!==input.targetColor))throw new Error('proposal_target_mismatch');
const planFile=join(root,'revision-plan.json');writeFileSync(planFile,JSON.stringify(plan));
const controller=new Controller(join(root,'tasks.sqlite'));
let task:any;
try{
  task=await controller.run({key:'single-approved-round',skill,expectedSkillSha256:skillDigest(skill),plan:planFile,
    source,output:join(root,'revised'),runtimeHome,python:input.python,estimatedBytes:input.authorization.maxBytes,authorization});
  assert.equal(task.state,'review_ready');
}finally{controller.close();}
for(const [path,digest] of Object.entries(original))assert.equal(hash(join(source,path)),digest);
for(const suffix of ['png','svg','pdf'])assert.equal(hash(join(source,'artboard-2.'+suffix)),hash(join(root,'revised','artboard-2.'+suffix)));
const changed=strictJson(readFileSync(join(root,'revised','brand-dependencies.json'),'utf8'));
assert.equal(changed.checks[0].status,'passed');
const stale=new ReviewStore(join(root,'review.sqlite'),[source,root]);
try{writeFileSync(brief,input.brief+' changed');assert.throws(()=>stale.revision(request.id,input.changes),/stale_review_binding/);}finally{stale.close();}
const proof={result:'PASS',level:'native-candidate',fingerprints:executionFingerprints,scope:'single supplied host receipt, durable exchange, explicit brand revision and control preservation; not independent review or automatic loop',
  skillSha256:skillDigest(skill),runtimeSha256:manifest.runtimeSha256,sourceProjectSha256:manifest.files['project.vectorcraft'],
  reviewRequestSha256:hash(join(root,'request.json')),receiptSha256:hash(join(root,'receipt.json')),proposalSha256:hash(join(root,'proposal.json')),
  reviewState:imported.state,independent:false,revisionState:task.state,brandDependencyCheck:changed.checks[0],sourceUnchanged:true,
  unrelatedBoardBytesPreserved:true,duplicateReceiptRejected:true,staleTargetRejected:true};
writeFileSync(join(root,'proof.json'),JSON.stringify(proof,null,2)+'\n');console.log(JSON.stringify(proof,null,2));
