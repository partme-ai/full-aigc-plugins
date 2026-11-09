import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {AdapterError} from './runtime_adapter.mjs';
import {canonical,parseStrictJson,readBounded,sha256} from './workflow_data.mjs';

const TYPES=new Set(['draft_write','remote_evaluation','native_export']);
const fail=(code,message)=>{throw new AdapterError(code,message);};

function atomicJson(file,value) {
  fs.mkdirSync(path.dirname(file),{recursive:true});
  const temporary=`${file}.${process.pid}.${crypto.randomUUID()}.tmp`;
  fs.writeFileSync(temporary,`${JSON.stringify(value,null,2)}\n`,{encoding:'utf8',mode:0o600});
  fs.renameSync(temporary,file);
}

/** 为三类外部副作用提供写前持久化、单写 epoch 和结果未知对账。 */
export class SideEffectLedger {
  constructor({stateRoot}) {this.stateRoot=path.resolve(stateRoot);}
  id({type,scope}) {
    if(!TYPES.has(type) || !scope || typeof scope!=='object') fail('side_effect_scope_invalid','known type and structured scope required');
    return `${type}-${sha256(canonical(scope)).slice(0,24)}`;
  }
  file(id) {return path.join(this.stateRoot,id,'ledger.json');}
  lock(id) {return path.join(this.stateRoot,id,'writer.lock');}
  show(id) {return parseStrictJson(readBounded(this.file(id),1024*1024).toString('utf8'));}
  begin({type,scope}) {
    const id=this.id({type,scope}),file=this.file(id);
    if(fs.existsSync(file)) {
      const current=this.show(id);
      if(current.state==='succeeded') return {state:current,reused:true};
      if(['queued','running','ambiguous'].includes(current.state))
        fail('side_effect_reconciliation_required','existing side effect cannot be retried until reconciled');
    }
    const state={schema:'jianying-side-effect-ledger/v1',id,type,scope:structuredClone(scope),scope_digest:sha256(canonical(scope)),
      state:'queued',epoch:0,attempt:1,artifact:null,cost:null,history:[]};
    this.record(state,'queued'); atomicJson(file,state); return {state,reused:false};
  }
  claim(id) {
    const state=this.show(id); let descriptor;
    try {descriptor=fs.openSync(this.lock(id),'wx',0o600);} catch(error) {
      if(error.code==='EEXIST') fail('side_effect_writer_occupied','another writer owns this side effect');
      throw error;
    }
    state.epoch+=1;state.state='running';state.lease={epoch:state.epoch,token:crypto.randomUUID()};
    this.record(state,'claimed');atomicJson(this.file(id),state);
    fs.writeFileSync(descriptor,JSON.stringify(state.lease));fs.closeSync(descriptor);return state;
  }
  succeed(id,{artifact,cost=null}={}) {
    const state=this.show(id);if(state.state!=='running') fail('side_effect_state_invalid','running side effect required');
    state.state='succeeded';state.artifact=structuredClone(artifact);state.cost=structuredClone(cost);
    this.record(state,'succeeded');atomicJson(this.file(id),state);this.release(id);return state;
  }
  fail(id,{code}={}) {
    const state=this.show(id);if(state.state!=='running') fail('side_effect_state_invalid','running side effect required');
    state.state='failed';state.failure_code=String(code??'provider_failed');this.record(state,'failed',{code:state.failure_code});
    atomicJson(this.file(id),state);this.release(id);return state;
  }
  ambiguous(id,{reason='outcome_unknown'}={}) {
    const state=this.show(id);if(state.state!=='running') fail('side_effect_state_invalid','running side effect required');
    state.state='ambiguous';state.ambiguous_reason=reason;this.record(state,'ambiguous',{reason});
    atomicJson(this.file(id),state);this.release(id);return state;
  }
  reconcile(id,{outcome,artifact=null,cost=null}={}) {
    const state=this.show(id);if(state.state!=='ambiguous') fail('side_effect_reconcile_invalid','ambiguous side effect required');
    if(outcome==='succeeded') {state.state='succeeded';state.artifact=structuredClone(artifact);state.cost=structuredClone(cost);}
    else if(outcome==='not_executed') {state.state='failed';state.failure_code='reconciled_not_executed';}
    else fail('side_effect_reconcile_invalid','outcome must be succeeded or not_executed');
    this.record(state,`reconciled.${outcome}`);atomicJson(this.file(id),state);return state;
  }
  record(state,event,details={}) {state.history.push({sequence:state.history.length+1,event,details});}
  release(id) {const lock=this.lock(id);if(fs.existsSync(lock)) fs.unlinkSync(lock);}
}
