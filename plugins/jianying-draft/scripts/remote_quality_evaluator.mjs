import fs from 'node:fs';
import {AdapterError} from './runtime_adapter.mjs';
import {canonical,parseStrictJson,sha256} from './workflow_data.mjs';
import {qualityContractDigest,validateQualityContract} from './quality_contracts.mjs';
import {runEvaluator} from './quality_evaluator.mjs';
import {SideEffectLedger} from './side_effect_ledger.mjs';

const fail=(code,message)=>{throw new AdapterError(code,message);};
const DIGEST=/^[a-f0-9]{64}$/;
const MEDIA_MIME_TYPES=new Set(['video/mp4','video/quicktime','video/webm']);

function endpointAllowed(value) {
  let url;try {url=new URL(value);} catch {return false;}
  return url.protocol==='https:' || (url.protocol==='http:' && ['127.0.0.1','localhost','::1'].includes(url.hostname));
}
function prepareUploadResources(input,resources,maximumUploadBytes) {
  if(resources===undefined) return [];
  if(!Array.isArray(resources)) fail('model_upload_resource_invalid','upload resources must be an array');
  const artifacts=new Map(input.artifacts.map(item=>[item.artifact_id,item])),seen=new Set();
  let totalBytes=0;
  return resources.map(resource=>{
    if(!resource || typeof resource!=='object' || Array.isArray(resource) ||
      typeof resource.artifact_id!=='string' || !resource.artifact_id || seen.has(resource.artifact_id) ||
      typeof resource.path!=='string' || !resource.path || !MEDIA_MIME_TYPES.has(resource.mime_type))
      fail('model_upload_resource_invalid','upload resource declaration is invalid');
    seen.add(resource.artifact_id);
    const artifact=artifacts.get(resource.artifact_id);
    if(!artifact || artifact.type!=='proxy_media') fail('model_upload_resource_invalid','upload resource is not a declared proxy artifact');
    let stat,bytes;
    try {
      stat=fs.lstatSync(resource.path);
      if(stat.isSymbolicLink() || !stat.isFile()) fail('model_upload_resource_invalid','upload resource must be a regular file');
      bytes=fs.readFileSync(resource.path);
    } catch(error) {
      if(error instanceof AdapterError) throw error;
      fail('model_upload_resource_invalid','upload resource cannot be read');
    }
    totalBytes+=bytes.length;
    if(totalBytes>maximumUploadBytes) fail('model_upload_limit_exceeded','approved upload resources exceed the configured byte limit');
    if(bytes.length!==artifact.bytes || sha256(bytes)!==artifact.digest)
      fail('model_upload_resource_changed','upload resource no longer matches its approved artifact');
    return {artifact_id:resource.artifact_id,digest:artifact.digest,mime_type:resource.mime_type,bytes};
  });
}

function approvalScope({provider,model,input,profile,budget,uploads}) {
  const resources=uploads.map(item=>({artifact_id:item.artifact_id,digest:item.digest,mime_type:item.mime_type,bytes:item.bytes.length}))
    .sort((left,right)=>left.artifact_id.localeCompare(right.artifact_id));
  return {provider,model,input_digest:qualityContractDigest(input),profile_digest:qualityContractDigest(profile),
    resources,resource_ids:resources.map(item=>item.artifact_id),resource_digests:resources.map(item=>item.digest),
    currency:budget.currency,maximum_cost:budget.maximum,
    rate_card_digest:budget.rate_card?sha256(canonical(budget.rate_card)):null};
}
function validateApproval(approval,scope) {
  if(approval?.schema!=='jianying-model-upload-approval/v1' || canonical(approval.scope)!==canonical(scope) ||
    typeof approval.user_id!=='string' || !approval.user_id.trim() || !Number.isFinite(Date.parse(approval.expires_at)) ||
    Date.parse(approval.expires_at)<=Date.now()) fail('model_upload_approval_required','exact, unexpired upload approval required');
}
async function defaultTransport({endpoint,credential,body,timeoutMs,maxResponseBytes,requestId}) {
  const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),timeoutMs);
  try {
    const response=await fetch(endpoint,{method:'POST',signal:controller.signal,headers:{authorization:`Bearer ${credential}`,
      'content-type':'application/json','x-request-id':requestId},body:JSON.stringify(body)});
    const bytes=Buffer.from(await response.arrayBuffer());
    if(bytes.length>maxResponseBytes) fail('model_response_too_large','remote evaluator response exceeds configured limit');
    const costCurrency=response.headers.get('x-cost-currency'),costAmount=response.headers.get('x-cost-amount');
    return {status:response.status,body:bytes.toString('utf8'),provider_request_id:response.headers.get('x-request-id')??requestId,
      cost:costCurrency!==null&&costAmount!==null?{currency:costCurrency,amount:Number(costAmount)}:null};
  } finally {clearTimeout(timer);}
}

function providerRequest({model,requestId,input,profile,budget,uploads}) {
  const contract={schema:'jianying-remote-evaluation-request/v1',request_id:requestId,input,profile,
    budget:{currency:budget.currency,maximum:budget.maximum}};
  const instruction=`Produce a jianying-evaluation-verdict/v1 result for this contract:\n${canonical(contract)}`;
  const userContent=uploads.length===0?instruction:[
    ...uploads.map(item=>({type:'video_url',video_url:{url:`data:${item.mime_type};base64,${item.bytes.toString('base64')}`}})),
    {type:'text',text:instruction},
  ];
  return {model,temperature:0,max_tokens:2048,response_format:{type:'json_object'},messages:[
    {role:'system',content:'Return one JSON object only. Evaluate only the supplied evidence. Never invent media facts or timecodes.'},
    {role:'user',content:userContent},
  ]};
}

function usageCost(envelope,budget) {
  const usage=envelope?.usage,rate=budget.rate_card;
  if(!rate) return null;
  const fields=['version','input_per_million','output_per_million'];
  if(fields.some(field=>rate[field]===undefined) || typeof rate.version!=='string' || !rate.version.trim() ||
    ![rate.input_per_million,rate.output_per_million,rate.cached_input_per_million??rate.input_per_million]
      .every(value=>Number.isFinite(value)&&value>=0) ||
    !Number.isSafeInteger(usage?.prompt_tokens) || usage.prompt_tokens<0 ||
    !Number.isSafeInteger(usage?.completion_tokens) || usage.completion_tokens<0)
    fail('model_cost_unreconciled','provider usage or approved rate card cannot be reconciled');
  const cached=usage.prompt_tokens_details?.cached_tokens??usage.prompt_cache_hit_tokens??0;
  if(!Number.isSafeInteger(cached)||cached<0||cached>usage.prompt_tokens)
    fail('model_cost_unreconciled','provider cached-token usage is invalid');
  const amount=((usage.prompt_tokens-cached)*rate.input_per_million+
    cached*(rate.cached_input_per_million??rate.input_per_million)+usage.completion_tokens*rate.output_per_million)/1_000_000;
  return {currency:budget.currency,amount:Number(amount.toFixed(12)),usage:{prompt_tokens:usage.prompt_tokens,
    cached_prompt_tokens:cached,completion_tokens:usage.completion_tokens},rate_card_version:rate.version};
}

/** 创建显式上传批准、预算和对账约束下的 OpenAI-compatible 远程评估器。 */
export function createRemoteModelEvaluator({provider,model,version,endpoint,credential,stateRoot,timeoutMs=30_000,
  maxResponseBytes=256*1024,maxUploadBytes=7*1024*1024,transport=defaultTransport}={}) {
  if([provider,model,version].some(value=>typeof value!=='string'||!value.trim()) || !endpointAllowed(endpoint) ||
    typeof credential!=='string'||!credential || !Number.isSafeInteger(timeoutMs)||timeoutMs<1 ||
    !Number.isSafeInteger(maxResponseBytes)||maxResponseBytes<1 || !Number.isSafeInteger(maxUploadBytes)||maxUploadBytes<1)
    fail('remote_evaluator_invalid','provider configuration is invalid');
  const identity={type:'model',provider,model,version},ledger=new SideEffectLedger({stateRoot});
  return {identity,ledger,approvalScope:(args)=>{
    validateQualityContract(args.input);validateQualityContract(args.profile);
    const uploads=prepareUploadResources(args.input,args.resources,maxUploadBytes);
    return approvalScope({provider,model,...args,uploads});
  },
    async evaluate({input,profile,approval,budget,resources}) {
      validateQualityContract(input);validateQualityContract(profile);
      if(!budget || typeof budget.currency!=='string' || !Number.isFinite(budget.maximum) || budget.maximum<0)
        fail('remote_evaluator_invalid','bounded evaluator budget required');
      const uploads=prepareUploadResources(input,resources,maxUploadBytes);
      const scope=approvalScope({provider,model,input,profile,budget,uploads});validateApproval(approval,scope);
      if(scope.resource_digests.some(value=>!DIGEST.test(value))) fail('remote_evaluator_invalid','upload resources require sha256 digests');
      const requestId=`eval-${sha256(canonical(scope)).slice(0,24)}`;
      const begun=ledger.begin({type:'remote_evaluation',scope:{...scope,request_id:requestId}});
      if(begun.reused) return begun.state.artifact.verdict;
      ledger.claim(begun.state.id);
      try {
        const response=await transport({endpoint,credential,timeoutMs,maxResponseBytes,requestId,
          body:providerRequest({model,requestId,input,profile,budget,uploads})});
        const size=Buffer.byteLength(typeof response.body==='string'?response.body:JSON.stringify(response.body));
        if(size>maxResponseBytes) fail('model_response_too_large','remote evaluator response exceeds configured limit');
        if(!Number.isInteger(response.status) || response.status<200 || response.status>=300)
          fail('model_provider_failed','remote evaluator returned a definite failure');
        let raw=typeof response.body==='string'?parseStrictJson(response.body):structuredClone(response.body);
        const providerRequestId=response.provider_request_id??raw?.request_id??raw?.id??requestId;
        const cost=response.cost??usageCost(raw,budget);
        if(!cost) fail('model_cost_unreconciled','provider did not return cost or usage covered by an approved rate card');
        if(cost.currency!==budget.currency || !Number.isFinite(cost.amount) || cost.amount<0 || cost.amount>budget.maximum)
          fail('model_cost_exceeded','reported model cost exceeds approved budget');
        const content=raw?.choices?.[0]?.message?.content;
        if(typeof content==='string') raw=parseStrictJson(content);
        const verdict=runEvaluator({adapter:{identity,evaluate:()=>raw},input,profile});
        ledger.succeed(begun.state.id,{artifact:{verdict,provider_request_id:providerRequestId},cost});
        return verdict;
      } catch(error) {
        if(error.code==='model_provider_failed' || error.code==='quality_contract_invalid' || error.code==='model_response_too_large' || error.code==='model_cost_exceeded')
          ledger.fail(begun.state.id,{code:error.code});
        else ledger.ambiguous(begun.state.id,{reason:'timeout_or_transport_unknown'});
        if(error.name==='AbortError') fail('model_outcome_unknown','remote timeout requires provider reconciliation');
        throw error;
      }
    }};
}
