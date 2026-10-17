import {canonical,strictJson} from '../strict_json.ts';
import type {Ledger} from '../../scripts/harness/ledger.ts';

type Requirements={mode:string,commands:Record<string,string>,tools:Record<string,any>};
/** 核对同一真实会话的命令参数签名与MCP工具schema；enabled属于执行时前置条件。 */
export function validateCapabilities(report:any,requirements:Requirements):any {
 if(report?.schema!=='vectorcraft-runtime-probe/v1'||!['headless','bridge'].includes(report.mode)
  ||! /^[a-f0-9]{64}$/.test(report.binarySha256)||typeof report.version!=='string'||!report.version)throw new Error('invalid_runtime_probe');
 if(!requirements||!['headless','bridge'].includes(requirements.mode)||report.mode!==requirements.mode)throw new Error('runtime_mode_mismatch');
 for(const key of ['commands','tools'])if(!requirements[key]||typeof requirements[key]!=='object'||Array.isArray(requirements[key]))throw new Error('invalid_runtime_requirements');
 const registry=(rows:any,key:string,field:string)=>{
  if(!Array.isArray(rows)||rows.some(r=>!r||typeof r[key]!=='string'||!r[key]||!(field in r))||new Set(rows.map(r=>r[key])).size!==rows.length)throw new Error('invalid_runtime_registry');
  return new Map(rows.map(r=>[r[key],r[field]]));
 };
 const commands=registry(report.commands,'id','params'),tools=registry(report.tools,'name','inputSchema');
 for(const [expected,actual] of [[requirements.commands,commands],[requirements.tools,tools]] as any){
  for(const [name,signature] of Object.entries(expected)){
   if(!actual.has(name))throw new Error('capability_missing: '+name);
   if(canonical(actual.get(name))!==canonical(signature))throw new Error('capability_schema_mismatch: '+name);
  }
 }
 return {commandCount:commands.size,toolCount:tools.size,mode:report.mode};
}

/** 在同一任务账本事务内切换已探测的版本；保留旧探测记录，不删除或安装二进制。 */
export class RuntimeGate {
 ledger:Ledger;
 constructor(ledger:Ledger){this.ledger=ledger;ledger.db.exec('CREATE TABLE IF NOT EXISTS runtime_selection(id INTEGER PRIMARY KEY CHECK(id=1),active TEXT NOT NULL,previous TEXT)');}
 current():any {const row=this.ledger.db.prepare('SELECT * FROM runtime_selection WHERE id=1').get() as any;return row?{active:strictJson(row.active),previous:row.previous?strictJson(row.previous):null}:null;}
 initialize(report:any,requirements:Requirements,stateSchemas:number[]):any {return this.activate(report,requirements,stateSchemas,true);}
 activate(report:any,requirements:Requirements,stateSchemas:number[],initialOnly=false):any {
  const capabilities=validateCapabilities(report,requirements);
  if(!Array.isArray(stateSchemas)||!stateSchemas.length||stateSchemas.some(x=>!Number.isSafeInteger(x)||x<1))throw new Error('invalid_state_compatibility');
  return this.ledger.transaction(()=>{
   const version=(this.ledger.db.prepare('PRAGMA user_version').get() as any).user_version;
   if(!stateSchemas.includes(version))throw new Error('incompatible_state_schema');
   const current=this.current();
   if(initialOnly&&current){
    if(current.active.mode!==report.mode)throw new Error('runtime_mode_mismatch');
    if(current.active.binarySha256!==report.binarySha256)throw new Error('runtime_selection_mismatch');
    if(current.active.stateSchemas?.includes(version))return current;
   }
   if(this.ledger.db.prepare("SELECT id FROM tasks WHERE state IN ('ready','running','reconciling','cancel_requested') LIMIT 1").get())throw new Error('runtime_tasks_not_drained');
   if(this.ledger.db.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name='native_processes'").get()
    &&this.ledger.db.prepare('SELECT task FROM native_processes WHERE stopped_at IS NULL LIMIT 1').get())throw new Error('runtime_process_stop_unconfirmed');
   const old=this.current(),active={...report,requirements,stateSchemas,capabilities};
   if(old&&canonical(old.active)===canonical(active))return old;
   this.ledger.db.prepare('INSERT INTO runtime_selection(id,active,previous) VALUES(1,?,?) ON CONFLICT(id) DO UPDATE SET active=excluded.active,previous=excluded.previous')
    .run(canonical(active),old?canonical(old.active):null);
   return this.current();
  });
 }
}
