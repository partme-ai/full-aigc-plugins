import {fail} from './workflow_data.mjs';
import {validateQualityContract} from './quality_contracts.mjs';

function validateRequiredTypes(requiredTypes) {
  if(!Array.isArray(requiredTypes) || !requiredTypes.length || requiredTypes.some(type=>typeof type!=='string' || !type.trim()) ||
    new Set(requiredTypes).size!==requiredTypes.length) fail('evidence_requirements_invalid','required evidence types must be unique non-empty strings');
}

/** 汇总已取得的分项证据；结论由实际条目计算，调用者不能直接指定更高等级。 */
export function buildEvidenceBundle({workflowId,revision,outputId,artifactDigest,items,requiredTypes,metadata={}}) {
  validateRequiredTypes(requiredTypes);
  if(!Array.isArray(items)) fail('evidence_requirements_invalid','evidence items must be an array');
  const passedTypes=new Set(items.filter(item=>item.passed).map(item=>item.type));
  const conclusion=items.some(item=>!item.passed)?'failed':
    requiredTypes.every(type=>passedTypes.has(type))?'passed':'incomplete';
  const bundle={schema:'jianying-evidence-bundle/v1',workflow_id:workflowId,revision,output_id:outputId,
    artifact_digest:artifactDigest,items:structuredClone(items),conclusion,metadata:structuredClone(metadata)};
  validateQualityContract(bundle);
  return bundle;
}

/** 复核证据与当前工件/修订绑定，防止同路径换内容后复用旧结论。 */
export function verifyEvidenceBundle(bundle,{workflowId,revision,outputId,artifactDigest,requiredTypes}) {
  validateQualityContract(bundle); validateRequiredTypes(requiredTypes);
  if(bundle.workflow_id!==workflowId || bundle.revision!==revision || bundle.output_id!==outputId || bundle.artifact_digest!==artifactDigest)
    fail('evidence_binding_mismatch','evidence bundle does not belong to the current output revision and artifact');
  const passedTypes=new Set(bundle.items.filter(item=>item.passed).map(item=>item.type));
  const expected=bundle.items.some(item=>!item.passed)?'failed':requiredTypes.every(type=>passedTypes.has(type))?'passed':'incomplete';
  if(bundle.conclusion!==expected) fail('evidence_conclusion_invalid','evidence conclusion exceeds the actual evidence');
  return {valid:true,conclusion:bundle.conclusion};
}
