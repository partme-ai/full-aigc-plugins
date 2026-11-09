import {fail} from './workflow_data.mjs';

const DIGEST=/^[a-f0-9]{64}$/;

function uniqueStrings(values,name) {
  if(!Array.isArray(values)||values.some(value=>typeof value!=='string'||!value.trim())||new Set(values).size!==values.length)
    fail('multi_output_quality_invalid',`${name} must contain unique non-empty strings`);
}

/** 汇总逐输出质量结论。父工作流只有所有必需输出独立通过后才能完成。 */
export function evaluateMultiOutputCompletion({requiredOutputs,verdicts,blockedOutputs=[]}) {
  uniqueStrings(requiredOutputs,'required outputs'); uniqueStrings(blockedOutputs,'blocked outputs');
  if(!Array.isArray(verdicts)) fail('multi_output_quality_invalid','verdicts must be an array');
  const required=new Set(requiredOutputs),seen=new Set(),byOutput=new Map();
  for(const verdict of verdicts) {
    if(!verdict||typeof verdict.output_id!=='string'||!required.has(verdict.output_id)||seen.has(verdict.output_id)||
      !['pass','revise','blocked','stop'].includes(verdict.decision)||!Number.isSafeInteger(verdict.revision)||verdict.revision<1||
      !DIGEST.test(verdict.input_digest??'')) fail('multi_output_quality_invalid','each required output needs one bound verdict');
    seen.add(verdict.output_id); byOutput.set(verdict.output_id,verdict);
  }
  const passed=requiredOutputs.filter(id=>byOutput.get(id)?.decision==='pass'&&!blockedOutputs.includes(id));
  const revisions=requiredOutputs.filter(id=>byOutput.get(id)?.decision==='revise');
  const blocked=requiredOutputs.filter(id=>blockedOutputs.includes(id)||['blocked','stop'].includes(byOutput.get(id)?.decision));
  const missing=requiredOutputs.filter(id=>!byOutput.has(id));
  const terminal=passed.length===requiredOutputs.length?'completed':revisions.length?'revision_required':blocked.length?'partially_completed':'awaiting_evaluation';
  return {terminal_state:terminal,passed_outputs:passed,revision_outputs:revisions,blocked_outputs:blocked,
    missing_outputs:missing,completed_outputs:terminal==='completed'?[...requiredOutputs]:[]};
}

/** 验证局部返工只改变获准输出，避免兄弟输出被隐式重建或污染。 */
export function verifyOutputRevisionIsolation({before,after,expectedChanged}) {
  if(!before||!after||typeof before!=='object'||typeof after!=='object'||Array.isArray(before)||Array.isArray(after))
    fail('output_revision_isolation_invalid','before and after digest maps are required');
  uniqueStrings(expectedChanged,'expected changed outputs');
  const beforeIds=Object.keys(before).sort(),afterIds=Object.keys(after).sort();
  if(JSON.stringify(beforeIds)!==JSON.stringify(afterIds)||beforeIds.some(id=>!DIGEST.test(before[id])||!DIGEST.test(after[id])))
    fail('output_revision_isolation_invalid','output sets and digests must be stable and valid');
  const changed=beforeIds.filter(id=>before[id]!==after[id]);
  const expected=[...expectedChanged].sort();
  if(JSON.stringify(changed)!==JSON.stringify(expected))
    fail('output_revision_isolation_failed','revision changed outputs outside the approved isolation boundary');
  return {changed_outputs:changed,unchanged_outputs:beforeIds.filter(id=>!changed.includes(id)),isolated:true};
}

/** 按用途和逐输出清单应用授权；私人用途授权不能提升为商业授权。 */
export function authorizePurposeOutputs({outputs,approvals}) {
  if(!Array.isArray(outputs)||!Array.isArray(approvals)) fail('purpose_approval_invalid','outputs and approvals are required');
  const outputById=new Map();
  for(const output of outputs) {
    if(!output||typeof output.output_id!=='string'||!output.output_id.trim()||typeof output.purpose!=='string'||!output.purpose.trim()||outputById.has(output.output_id))
      fail('purpose_approval_invalid','outputs require unique identities and explicit purposes');
    outputById.set(output.output_id,output);
  }
  const authorized=new Set();
  for(const approval of approvals) {
    if(!approval||typeof approval.approval_id!=='string'||!approval.approval_id.trim()||typeof approval.purpose!=='string')
      fail('purpose_approval_invalid','approval identity and purpose are required');
    uniqueStrings(approval.output_ids,'approval output IDs');
    for(const id of approval.output_ids) {
      const output=outputById.get(id);
      if(!output||output.purpose!==approval.purpose)
        fail('purpose_approval_mismatch','approval purpose does not match the enumerated output');
      authorized.add(id);
    }
  }
  const authorizedOutputs=outputs.map(item=>item.output_id).filter(id=>authorized.has(id));
  const blockedOutputs=outputs.filter(item=>!authorized.has(item.output_id)).map(item=>({output_id:item.output_id,
    code:item.purpose==='commercial'?'commercial_approval_required':'purpose_approval_required'}));
  return {authorized_outputs:authorizedOutputs,blocked_outputs:blockedOutputs};
}
