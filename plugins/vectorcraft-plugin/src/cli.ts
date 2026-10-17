#!/usr/bin/env node
import {assertNoLiteralSecrets} from '../scripts/harness/input_policy.ts';
import {nativeEnvironment} from '../scripts/harness/native_environment.ts';
import { readFileSync,realpathSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { RuntimeGate,validateCapabilities } from './runtime/runtime_gate.ts';
import { strictJson } from './strict_json.ts';
import { Controller,skillDigest } from '../scripts/harness/controller.ts';
import { ReviewStore } from './evaluation/review_store.ts';
import { TechnicalReview } from './evaluation/technical_review.ts';
import { RevisionCycle } from './evaluation/revision_cycle.ts';

/** 文件形式的显式请求入口；普通任务沿用固定安装与能力探测，不发起外部评审、不自动生成下一轮。 */
async function main(){
  const [action,database,file]=process.argv.slice(2);
  if(!action||!database||!file)throw new Error('usage: node src/cli.ts run|cancel|reconcile|runtime-probe|runtime-activate|runtime-status|review-request|review-checked|review-import|revision|revision-cycle-open|revision-cycle-observe|revision-cycle-propose|revision-cycle-run|revision-cycle-best DATABASE REQUEST.json');
  const raw=readFileSync(file,'utf8');let input:any;
  try{input=strictJson(raw);}catch(error){
    if(action!=='review-import')throw error;
    // 畸形回执同样进入持久拒绝路径，存摘要而不回显可能含秘密的原文。
    const rejected=new ReviewStore(database);try{return rejected.importReceipt(raw);}finally{rejected.close();}
  }
  assertNoLiteralSecrets(input);
  if(['runtime-probe','runtime-activate','runtime-status'].includes(action)){
    const controller=new Controller(database);try{
      const gate=new RuntimeGate(controller.ledger);
      if(action==='runtime-status')return gate.current();
      if(skillDigest(input.skill)!==input.expectedSkillSha256)throw new Error('skill_snapshot_mismatch');
      let output:string;
      try{output=execFileSync(input.python??'python3',['-I','-B',fileURLToPath(new URL('./runtime/runtime_probe.py',import.meta.url))],
        {env:nativeEnvironment(),stdio:['pipe','pipe','pipe'],input:JSON.stringify(input),encoding:'utf8',timeout:40000,maxBuffer:8*1024*1024});}
      catch{throw new Error('runtime_probe_failed: child output withheld');}
      if(skillDigest(input.skill)!==input.expectedSkillSha256)throw new Error('skill_snapshot_mismatch');
      const report=strictJson(output);validateCapabilities(report,input.requirements);
      return action==='runtime-probe'?report:gate.activate(report,input.requirements,input.stateSchemas);
    }finally{controller.close();}
  }
  if(['run','cancel','reconcile'].includes(action)){
    const controller=new Controller(database);try{
      if(action==='cancel')return controller.requestCancel(input.taskId,input.epoch);
      if(action==='reconcile')return await controller.reconcileOriginal(input.taskId,input.epoch);
      return await controller.run(input);
    }finally{controller.close();}
  }
  const store=new ReviewStore(database,action==='review-import'?undefined:input.readRoots);
  try{
    if(action.startsWith('revision-cycle-')){
      const cycle=new RevisionCycle(store);try{
        if(action==='revision-cycle-open')return cycle.open(input);
        if(action==='revision-cycle-observe')return cycle.observe(input.cycleId,input.requestId,input.proposalId);
        if(action==='revision-cycle-propose')return cycle.propose(input.cycleId,input.requestId,input.changes,input.key);
        if(action==='revision-cycle-run')return await cycle.execute(input.cycleId,input.proposalId,input.run);
        if(action==='revision-cycle-best')return cycle.best(input.cycleId);
        throw new Error('unknown_action');
      }finally{cycle.close();}
    }
    if(action==='review-request')return store.request(input);
    if(action==='review-checked')return await new TechnicalReview(store).request(input);
    if(action==='review-import'){
      // 回执不能自行扩展根目录；重启只恢复已落账技术检查的授权范围。
      const row=typeof input.requestId==='string'?store.db.prepare('SELECT input FROM reviews WHERE id=?').get(input.requestId) as any:undefined;
      if(row){
        const saved=strictJson(row.input);
        if(saved.technicalEvidenceOrigin==='checked-decoder'){
          const roots=saved.authorization?.readRoots;
          if(!Array.isArray(roots)||!roots.length||roots.some((root:any)=>typeof root!=='string'))throw new Error('invalid_checked_read_roots');
          store.roots=roots.map((root:string)=>realpathSync(root));
        }
      }
      return store.importReceipt(input);
    }
    if(action==='revision')return store.revision(input.requestId,input.changes);
    throw new Error('unknown_action');
  }finally{store.close();}
}
try{console.log(JSON.stringify(await main(),null,2));}catch(error){console.error(JSON.stringify({state:'failed',error:String(error)}));process.exitCode=1;}
