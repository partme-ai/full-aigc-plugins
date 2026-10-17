import { createHash,randomUUID } from 'node:crypto';
import { readFileSync,writeFileSync,mkdirSync,lstatSync,realpathSync } from 'node:fs';
import { dirname,join,relative,isAbsolute,resolve } from 'node:path';
import { canonical,strictJson } from '../strict_json.ts';
import { Ledger,resourcePath } from '../../scripts/harness/ledger.ts';
import { Controller } from '../../scripts/harness/controller.ts';
import { ReviewStore } from './review_store.ts';

const hash=(v:string|Buffer)=>createHash('sha256').update(v).digest('hex');
const inside=(root:string,path:string)=>{const sub=relative(resourcePath(root),resourcePath(path));return !isAbsolute(sub)&&sub!=='..'&&!sub.startsWith('../');};
const dimensions=['structure','text','brand','layout','legibility'];
type Policy={maxRounds:number,stagnationLimit:number,minImprovement:number};

/** 显式逐轮修订：共享预算不重置，原生执行与人工评审分别落账。 */
export class RevisionCycle {
  store:ReviewStore;ledger:Ledger;
  constructor(store:ReviewStore){
    this.store=store;this.ledger=new Ledger(store.path);
    this.ledger.db.exec(`CREATE TABLE IF NOT EXISTS revision_cycles(id TEXT PRIMARY KEY,budget TEXT UNIQUE NOT NULL,policy TEXT NOT NULL,authorization TEXT NOT NULL,goal TEXT NOT NULL,runtime TEXT NOT NULL,state TEXT NOT NULL,reason TEXT,rounds INTEGER NOT NULL DEFAULT 0,stagnation INTEGER NOT NULL DEFAULT 0,latest TEXT,best TEXT,best_score REAL);
      CREATE TABLE IF NOT EXISTS revision_members(review TEXT PRIMARY KEY,cycle TEXT NOT NULL);
      CREATE TABLE IF NOT EXISTS revision_observations(review TEXT PRIMARY KEY,cycle TEXT NOT NULL,score REAL,checkpoint TEXT NOT NULL,fingerprints TEXT NOT NULL,project TEXT NOT NULL);
      CREATE TABLE IF NOT EXISTS revision_proposals(id TEXT PRIMARY KEY,cycle TEXT NOT NULL,key TEXT NOT NULL,review TEXT NOT NULL,proposal TEXT NOT NULL,state TEXT NOT NULL,execution TEXT,UNIQUE(cycle,key));`);
  }
  get(id:string):any {
    const row=this.ledger.db.prepare('SELECT * FROM revision_cycles WHERE id=?').get(id) as any;
    if(!row)throw new Error('unknown_revision_cycle');
    return {...row,policy:strictJson(row.policy),authorization:strictJson(row.authorization),goal:strictJson(row.goal)};
  }
  goal(review:any):any {
    const input=review.input;
    return {targets:input.targets.map((t:any)=>({...t,sha256:review.fingerprints[t.path]})),rubric:{path:input.rubric,sha256:review.fingerprints[input.rubric]}};
  }
  checked(review:any){
    if(review.input.technicalEvidenceOrigin!=='checked-decoder'||review.input.technicalStatus!=='PASS'
      ||review.input.technicalEvidence?.artifactIntegrityStatus!=='PASS'||!['revision_proposed','review_ready','rejected'].includes(review.state))throw new Error('checked_review_required');
  }
  /** 建立固定策略，重复打开同一循环不重置计数或已消耗的预算。 */
  open(input:{id:string,requestId:string,policy:Policy}):any {
    const p=input.policy;
    if(!input.id||!p||Object.keys(p).sort().join(',')!=='maxRounds,minImprovement,stagnationLimit'
      ||!Number.isSafeInteger(p.maxRounds)||p.maxRounds<1||!Number.isSafeInteger(p.stagnationLimit)||p.stagnationLimit<1
      ||typeof p.minImprovement!=='number'||!Number.isFinite(p.minImprovement)||p.minImprovement<0||p.minImprovement>4)throw new Error('invalid_revision_policy');
    const review=this.store.current(input.requestId);this.checked(review);const auth=review.input.authorization;
    if(typeof auth.budgetId!=='string'||!auth.budgetId)throw new Error('shared_revision_budget_required');
    this.ledger.transaction(()=>{
      const previous=this.ledger.db.prepare('SELECT id FROM revision_cycles WHERE id=?').get(input.id);
      if(previous){const cycle=this.get(input.id);if(canonical(cycle.policy)!==canonical(p)||canonical(cycle.authorization)!==canonical(auth)||canonical(cycle.goal)!==canonical(this.goal(review))||cycle.runtime!==review.input.runtimeIdentity)throw new Error('revision_cycle_conflict');return;}
      if(this.ledger.db.prepare('SELECT id FROM revision_cycles WHERE budget=?').get(auth.budgetId))throw new Error('revision_budget_already_bound');
      this.ledger.db.prepare("INSERT INTO revision_cycles(id,budget,policy,authorization,goal,runtime,state) VALUES(?,?,?,?,?,?,'active')")
        .run(input.id,auth.budgetId,canonical(p),canonical(auth),canonical(this.goal(review)),review.input.runtimeIdentity);
      this.ledger.db.prepare('INSERT INTO revision_members(review,cycle) VALUES(?,?)').run(review.id,input.id);
    });
    const cycle=this.get(input.id);if(!cycle.latest)return this.observe(input.id,input.requestId);
    return cycle;
  }
  stop(id:string,reason:string):any {
    this.ledger.db.prepare("UPDATE revision_cycles SET state='stopped',reason=? WHERE id=? AND state='active'").run(reason,id);return this.get(id);
  }
  /** 新评分只能来自当前已检查的评审；后续候选还需已完成的原生执行与源谱系。 */
  observe(id:string,requestId:string,proposalId?:string):any {
    let cycle=this.get(id);
    if(this.ledger.db.prepare('SELECT review FROM revision_observations WHERE review=? AND cycle=?').get(requestId,id))return cycle;
    if(cycle.state!=='active')throw new Error('revision_cycle_stopped: '+cycle.reason);
    const review=this.store.current(requestId);
    if(review.input.runtimeIdentity!==cycle.runtime||canonical(review.input.authorization)!==canonical(cycle.authorization))throw new Error('revision_authorization_changed');
    if(canonical(this.goal(review))!==canonical(cycle.goal)){
      // 目标变化不是绕过可信来源和授权的捷径；保留原目标最佳候选，但报告最新已检查的问题。
      this.checked(review);
      this.ledger.transaction(()=>{
        const current=this.get(id);if(current.latest!==cycle.latest||current.state!=='active')throw new Error('stale_revision_cycle');
        const member=this.ledger.db.prepare('SELECT cycle FROM revision_members WHERE review=?').get(requestId) as any;
        if(member&&member.cycle!==id)throw new Error('review_already_bound_to_cycle');
        this.ledger.db.prepare('INSERT INTO revision_observations(review,cycle,score,checkpoint,fingerprints,project) VALUES(?,?,NULL,?,?,?)')
          .run(requestId,id,'','{}',review.input.projectRevision);
        this.ledger.db.prepare('INSERT OR IGNORE INTO revision_members(review,cycle) VALUES(?,?)').run(requestId,id);
        this.ledger.db.prepare("UPDATE revision_cycles SET latest=?,state='stopped',reason='goal_changed' WHERE id=?").run(requestId,id);
        if(proposalId)this.ledger.db.prepare("UPDATE revision_proposals SET state='reviewed' WHERE id=? AND cycle=? AND review=? AND state='awaiting_review'").run(proposalId,id,cycle.latest);
      });
      return this.get(id);
    }
    if(cycle.latest){
      const proposal=this.ledger.db.prepare('SELECT * FROM revision_proposals WHERE id=? AND cycle=?').get(proposalId??'',id) as any;
      if(!proposal||proposal.state!=='awaiting_review'||proposal.review!==cycle.latest)throw new Error('revision_execution_required');
      const task=this.ledger.get(proposal.execution),prior=this.ledger.db.prepare('SELECT project FROM revision_observations WHERE review=?').get(cycle.latest) as any;
      if(task.state!=='review_ready'||task.binding.projectRevision!==prior.project||task.binding.runtimeIdentity!==cycle.runtime
        ||resourcePath(dirname(review.input.native))!==task.output)throw new Error('revision_lineage_mismatch');
      const manifest=strictJson(readFileSync(join(task.output,'manifest.json'),'utf8'));
      if(manifest.sourceProjectSha256!==prior.project)throw new Error('revision_lineage_mismatch');
    }
    if(review.input.technicalStatus==='FAIL')return this.stop(id,'technical_failed');
    this.checked(review);
    const receipt=strictJson(review.receipt),score=dimensions.reduce((sum,k)=>sum+receipt.scores[k],0)/dimensions.length;
    const better=receipt.verdict!=='reject'&&(cycle.best===null||score>cycle.best_score);
    const improved=better&&(cycle.best===null||score-cycle.best_score>=cycle.policy.minImprovement);
    let checkpoint='',fingerprints:Record<string,string>={},budgetLimited=false;
    if(better){
      let kept;
      try{kept=this.checkpoint(cycle,review);}catch(error){
        if(!String(error).includes('budget_exceeded'))throw error;
        // 技术检查已经付费保留全部原生文件及依赖；额度不足时复用该只读副本。
        try{kept=this.checkedSnapshot(cycle,review);}catch(snapshotError){this.stop(id,'technical_snapshot_changed');throw snapshotError;}
        budgetLimited=true;
      }
      checkpoint=kept.path;fingerprints=kept.fingerprints;
    }
    this.ledger.transaction(()=>{
      // 其他进程已推进这一轮时，不允许用旧观察覆盖最新候选。
      const current=this.get(id);if(current.latest!==cycle.latest||current.state!=='active')throw new Error('stale_revision_cycle');
      this.ledger.db.prepare('INSERT INTO revision_observations(review,cycle,score,checkpoint,fingerprints,project) VALUES(?,?,?,?,?,?)')
        .run(requestId,id,score,checkpoint,canonical(fingerprints),review.input.projectRevision);
      const member=this.ledger.db.prepare('SELECT cycle FROM revision_members WHERE review=?').get(requestId) as any;
      if(member&&member.cycle!==id)throw new Error('review_already_bound_to_cycle');
      this.ledger.db.prepare('INSERT OR IGNORE INTO revision_members(review,cycle) VALUES(?,?)').run(requestId,id);
      const stagnation=improved?0:cycle.stagnation+1;
      const budget=this.ledger.db.prepare('SELECT attempts,bytes FROM budgets WHERE id=?').get(cycle.budget) as any;
      const exhausted=budgetLimited||!budget||Date.now()>=cycle.authorization.deadline||budget.attempts>=cycle.authorization.maxAttempts||budget.bytes>=cycle.authorization.maxBytes;
      const reason=exhausted?'budget_exceeded':receipt.verdict==='accept'?'review_ready':receipt.verdict==='reject'?'rejected':cycle.rounds>=cycle.policy.maxRounds?'round_limit':stagnation>=cycle.policy.stagnationLimit?'stagnation':null;
      this.ledger.db.prepare('UPDATE revision_cycles SET latest=?,best=?,best_score=?,stagnation=?,state=?,reason=? WHERE id=?')
        .run(requestId,better?requestId:cycle.best,better?score:cycle.best_score,stagnation,reason?'stopped':'active',reason,id);
      if(proposalId)this.ledger.db.prepare("UPDATE revision_proposals SET state='reviewed' WHERE id=?").run(proposalId);
    });
    return this.get(id);
  }
  /** 预算耗尽时复用账本已核验的只读技术副本，不再次复制或消耗额度。 */
  checkedSnapshot(cycle:any,review:any):{path:string,fingerprints:Record<string,string>}{
    const check=this.ledger.db.prepare('SELECT c.report,c.report_sha,t.output,t.state FROM technical_checks c JOIN tasks t ON t.id=c.task WHERE c.task=?').get(review.input.technicalCheckId) as any;
    if(!check||check.state!=='review_ready'||hash(check.report)!==check.report_sha||canonical(strictJson(check.report))!==canonical(review.input.technicalEvidence))throw new Error('verified_technical_snapshot_required');
    const path=join(check.output,'delivery');
    if(resourcePath(path)!==path||!cycle.authorization.writeRoots?.some((root:string)=>inside(root,path)))throw new Error('revision_checkpoint_outside_roots');
    const manifestPath=join(path,'manifest.json'),manifest=strictJson(readFileSync(manifestPath,'utf8')),fingerprints:Record<string,string>={};
    const expected=review.fingerprints[join(dirname(review.input.native),'manifest.json')];
    if(hash(readFileSync(manifestPath))!==expected||manifest.files['project.vectorcraft']!==review.input.projectRevision||canonical(manifest.files)!==canonical(review.input.technicalEvidence.files))throw new Error('technical_snapshot_changed');
    for(const [name,digest] of Object.entries({'manifest.json':expected,...manifest.files}) as [string,string][]){
      if(isAbsolute(name)||name.includes('\\')||name.split('/').some(p=>!p||p==='.'||p==='..'))throw new Error('invalid_artifact_path');
      const file=join(path,name),stat=lstatSync(file);
      if(resourcePath(file)!==file||!stat.isFile()||(stat.mode&0o222)!==0||this.store.fingerprint(file)!==digest)throw new Error('technical_snapshot_changed');
      fingerprints[name]=digest;
    }
    return {path,fingerprints};
  }
  checkpoint(cycle:any,review:any):{path:string,fingerprints:Record<string,string>}{
    const base=join(realpathSync(dirname(this.store.path)),'.revision-best');
    if(!cycle.authorization.writeRoots?.some((root:string)=>inside(root,base)))throw new Error('revision_checkpoint_outside_roots');
    try{if(lstatSync(base).isSymbolicLink())throw new Error('revision_checkpoint_symlink');}catch(e){if((e as NodeJS.ErrnoException).code!=='ENOENT')throw e;}
    const path=join(base,review.id),manifestPath=join(dirname(review.input.native),'manifest.json');
    const manifest=strictJson(readFileSync(manifestPath,'utf8'));
    const entries=new Map<string,Buffer>();let bytes=0;
    const add=(name:string,source:string)=>{
      if(lstatSync(source).size>64*1024*1024)throw new Error('revision_checkpoint_size');
      const content=readFileSync(source);bytes+=content.length;if(bytes>256*1024*1024)throw new Error('revision_checkpoint_size');
      if(hash(content)!==review.fingerprints[source])throw new Error('stale_review_binding');entries.set(name,content);
    };
    add('manifest.json',manifestPath);
    for(const name of Object.keys(manifest.files)){
      if(isAbsolute(name)||name.includes('\\')||name.split('/').some(p=>!p||p==='.'||p==='..'))throw new Error('invalid_artifact_path');
      add(name,join(dirname(review.input.native),name));
    }
    for(const [i,source] of [...review.input.targets.map((t:any)=>t.path),review.input.rubric,review.input.exchangeLoss].entries())add('inputs/'+i,source);
    const budget=this.ledger.db.prepare('SELECT attempts,bytes FROM budgets WHERE id=?').get(cycle.budget) as any;
    if(Date.now()>=cycle.authorization.deadline||budget&&(budget.attempts>=cycle.authorization.maxAttempts||budget.bytes+bytes>cycle.authorization.maxBytes))throw new Error('budget_exceeded');
    const task=this.ledger.claim('revision-best:'+cycle.id+':'+review.id,path,path,{planHash:hash(canonical({cycle:cycle.id,review:review.binding_hash})),inputHashes:review.fingerprints,
      projectRevision:review.input.projectRevision,runtimeIdentity:cycle.runtime,authorization:cycle.authorization});
    if(task.state!=='ready')throw new Error('reconcile_required');
    this.ledger.intent(task.id,task.epoch,0,{kind:'preserve-best',review:review.id},bytes);
    try{
      mkdirSync(base,{recursive:true});mkdirSync(path);const fingerprints:Record<string,string>={};
      for(const [name,content] of entries){const destination=join(path,name);mkdirSync(dirname(destination),{recursive:true});writeFileSync(destination,content,{flag:'wx',mode:0o400,flush:true});fingerprints[name]=hash(content);}
      this.store.current(review.id);
      this.ledger.receipt(task.id,task.epoch,0,{files:fingerprints});this.ledger.verified(task.id,task.epoch,{path:join(path,'project.vectorcraft'),sha256:review.input.projectRevision});
      return {path,fingerprints};
    }catch(error){if(this.ledger.get(task.id).state==='running')this.ledger.unknown(task.id,task.epoch,String(error));throw error;}
  }
  /** 生成一份有轮次身份的建议；同键重试不占用新轮次，旧入口不能绕开循环。 */
  propose(id:string,requestId:string,changes:any[],key:string):any {
    if(!Array.isArray(changes)||!changes.length||changes.some(c=>!c||Object.keys(c).sort().join(',')!=='field,objectId,value')
      ||new Set(changes.map(c=>canonical([c.objectId,c.field]))).size!==changes.length)throw new Error('invalid_revision_targets');
    try{return this.ledger.transaction(()=>{
      const previous=this.ledger.db.prepare('SELECT proposal FROM revision_proposals WHERE cycle=? AND key=?').get(id,key) as any;
      if(previous){const proposal=strictJson(previous.proposal);if(proposal.requestId!==requestId||canonical(proposal.changes)!==canonical(changes))throw new Error('revision_proposal_conflict');this.store.current(requestId);return proposal;}
      const cycle=this.get(id);if(cycle.state!=='active')throw new Error('revision_cycle_stopped: '+cycle.reason);
      if(!key||cycle.latest!==requestId)throw new Error('stale_revision_cycle');
      if(cycle.rounds>=cycle.policy.maxRounds)throw new Error('revision_round_limit');
      if(this.ledger.db.prepare("SELECT id FROM revision_proposals WHERE cycle=? AND state IN ('proposed','executing','awaiting_review','unknown')").get(id))throw new Error('revision_round_pending');
      const proposal=this.store.validateRevision(requestId,changes),budget=this.ledger.db.prepare('SELECT attempts,bytes FROM budgets WHERE id=?').get(cycle.budget) as any;
      if(Date.now()>=cycle.authorization.deadline||!budget||budget.attempts>=cycle.authorization.maxAttempts||budget.bytes>=cycle.authorization.maxBytes)throw new Error('budget_exceeded');
      const auth={...cycle.authorization,objects:[...new Set(changes.map(c=>c.objectId))].sort(),fields:[...new Set(changes.map(c=>c.field))].sort()};
      const result={...proposal,id:randomUUID(),cycleId:id,round:cycle.rounds+1,authorization:auth};
      this.ledger.db.prepare("INSERT INTO revision_proposals(id,cycle,key,review,proposal,state) VALUES(?,?,?,?,?,'proposed')").run(result.id,id,key,requestId,canonical(result));
      this.ledger.db.prepare('UPDATE revision_cycles SET rounds=rounds+1 WHERE id=?').run(id);return result;
    });}catch(error){
      if(String(error).includes('budget_exceeded'))this.stop(id,'budget_exceeded');
      if(String(error).includes('revision_round_limit'))this.stop(id,'round_limit');
      throw error;
    }
  }
  /** 运行显式提交的计划；执行未知不重放，原生输出满足目标值后才允许下一次评审。 */
  async execute(id:string,proposalId:string,request:any):Promise<any>{
    const row=this.ledger.db.prepare('SELECT * FROM revision_proposals WHERE id=? AND cycle=?').get(proposalId,id) as any;
    if(!row||row.state!=='proposed')throw new Error('revision_execution_requires_new_intent');
    const cycle=this.get(id),proposal=strictJson(row.proposal),review=this.store.current(row.review);
    if(cycle.state!=='active'||cycle.latest!==row.review)throw new Error('stale_revision_cycle');
    const budget=this.ledger.db.prepare('SELECT attempts,bytes FROM budgets WHERE id=?').get(cycle.budget) as any;
    if(Date.now()>=cycle.authorization.deadline||!budget||budget.attempts>=cycle.authorization.maxAttempts||budget.bytes>=cycle.authorization.maxBytes){
      this.stop(id,'budget_exceeded');throw new Error('budget_exceeded');
    }
    this.store.validateRevision(row.review,proposal.changes);
    const runtime=strictJson(readFileSync(join(request.skill,'scripts/runtime.lock.json'),'utf8'));
    if(runtime.artifacts?.['darwin-arm64']?.binarySha256!==cycle.runtime)throw new Error('revision_runtime_mismatch');
    if(request.source&&resourcePath(request.source)!==resourcePath(dirname(review.input.native)))throw new Error('revision_source_mismatch');
    const before=strictJson(readFileSync(join(dirname(review.input.native),'native.json'),'utf8'));
    for(const change of proposal.changes)this.field(before,change.objectId,change.field);
    if(this.ledger.db.prepare("UPDATE revision_proposals SET state='executing' WHERE id=? AND state='proposed'").run(proposalId).changes!==1)throw new Error('revision_execution_requires_new_intent');
    const controller=new Controller(this.store.path);
    try{
      const task=await controller.run({...request,key:'revision:'+proposalId,source:dirname(review.input.native),inputFingerprints:review.fingerprints,authorization:proposal.authorization});
      if(task.state!=='review_ready')throw new Error('revision_execution_unknown');
      const native=strictJson(readFileSync(join(task.output,'native.json'),'utf8'));
      for(const change of proposal.changes)if(canonical(this.field(native,change.objectId,change.field))!==canonical(change.value))throw new Error('revision_target_not_reached');
      this.ledger.db.prepare("UPDATE revision_proposals SET state='awaiting_review',execution=? WHERE id=?").run(task.id,proposalId);
      return {cycleId:id,proposalId,executionTaskId:task.id,state:'awaiting_review',output:task.output,acceptanceStatus:'pending'};
    }catch(error){
      const task=this.ledger.db.prepare('SELECT id FROM tasks WHERE key=?').get('revision:'+proposalId) as any;
      this.ledger.db.prepare("UPDATE revision_proposals SET state='unknown',execution=? WHERE id=?").run(task?.id??null,proposalId);
      this.stop(id,'execution_unknown');throw error;
    }
    finally{controller.close();}
  }
  field(document:any,objectId:number,field:string):any {
    const matches:any[]=[];
    const walk=(value:any)=>{if(!value||typeof value!=='object')return;if(!Array.isArray(value)&&value.id===objectId)matches.push(value);for(const child of Object.values(value))walk(child);};
    walk(document.layers);if(matches.length!==1||!field||field.split('.').some(p=>!p||['__proto__','constructor','prototype'].includes(p)))throw new Error('revision_field_unresolved');
    let value=matches[0];for(const part of field.split('.')){if(value===null||typeof value!=='object'||!Object.hasOwn(value,part))throw new Error('revision_field_unresolved');value=value[part];}return value;
  }
  /** 只返回仍可按摘要核对的最佳技术候选，不宣称工程或创作最终接受。 */
  best(id:string):any {
    const cycle=this.get(id);if(!cycle.best)throw new Error('no_verified_revision_candidate');
    const row=this.ledger.db.prepare('SELECT * FROM revision_observations WHERE review=?').get(cycle.best) as any;
    const fingerprints=strictJson(row.fingerprints);
    for(const [name,expected] of Object.entries(fingerprints))if(this.store.fingerprint(join(row.checkpoint,name))!==expected)throw new Error('best_candidate_changed');
    const latest=this.ledger.db.prepare('SELECT receipt FROM reviews WHERE id=?').get(cycle.latest) as any;
    const budget=this.ledger.db.prepare('SELECT attempts,bytes FROM budgets WHERE id=?').get(cycle.budget) as any;
    return {cycleId:id,requestId:row.review,score:row.score,path:row.checkpoint,fingerprints,projectRevision:row.project,
      latestRequestId:cycle.latest,goal:cycle.goal,unresolvedIssues:latest?.receipt?strictJson(latest.receipt).issues:[],rounds:cycle.rounds,stagnation:cycle.stagnation,
      sharedBudget:{id:cycle.budget,attempts:budget?.attempts,bytes:budget?.bytes},technicalStatus:'PASS',engineeringStatus:'NOT_RUN',acceptanceStatus:'pending',reason:cycle.reason};
  }
  close(){this.ledger.close();}
}
