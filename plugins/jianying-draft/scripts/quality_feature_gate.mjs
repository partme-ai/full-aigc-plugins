import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

import {canonical,fail,parseStrictJson,readBounded,sha256} from './workflow_data.mjs';

const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const DEFAULT_CONFIG=path.join(ROOT,'runtime/feature-flags.json');
const MAX_CONFIG_BYTES=16*1024;
const FEATURE='iterative_video_quality_loop';
const ROLLBACK='preserve_ledgers_and_pending_occupancy';
const DIGEST=/^[a-f0-9]{64}$/;

function exactKeys(value,allowed,location,code='quality_feature_config_invalid') {
  if(!value || typeof value!=='object' || Array.isArray(value))
    fail(code,`${location} must be an object`);
  const unknown=Object.keys(value).filter(key=>!allowed.includes(key));
  if(unknown.length) fail(code,`${location} contains unknown fields: ${unknown.join(',')}`);
}

/**
 * 读取随插件发布的严格 Feature Flag 配置并生成内容摘要。
 * 配置必须是普通文件；符号链接、未知字段和 preview 阶段默认开启均失败关闭。
 */
export function loadQualityFeatureFlags({configPath=DEFAULT_CONFIG}={}) {
  let parsed;
  try {
    const stat=fs.lstatSync(configPath);
    if(stat.isSymbolicLink() || !stat.isFile() || stat.size>MAX_CONFIG_BYTES)
      fail('quality_feature_config_invalid','feature flag config must be a bounded regular file');
    parsed=parseStrictJson(readBounded(configPath,MAX_CONFIG_BYTES).toString('utf8'));
  } catch(error) {
    if(error?.code==='quality_feature_config_invalid') throw error;
    fail('quality_feature_config_invalid','feature flag config is missing, unreadable or malformed');
  }
  exactKeys(parsed,['schema','features'],'feature flag config');
  if(parsed.schema!=='jianying-plugin-feature-flags/v1')
    fail('quality_feature_config_invalid','unsupported feature flag schema');
  exactKeys(parsed.features,[FEATURE],'features');
  const quality=parsed.features[FEATURE];
  exactKeys(quality,['default_enabled','stage','rollback'],FEATURE);
  if(typeof quality.default_enabled!=='boolean' || !['preview','production'].includes(quality.stage) ||
    quality.rollback!==ROLLBACK)
    fail('quality_feature_config_invalid','quality loop feature settings are invalid');
  if(quality.default_enabled && quality.stage!=='production')
    fail('quality_feature_config_invalid','preview quality loop cannot be enabled by default');
  return {config:parsed,digest:sha256(canonical(parsed)),path:configPath};
}

/**
 * 解析质量循环入口。默认关闭时必须由调用方显式 opt-in；返回值可绑定到 WorkflowPlan。
 */
export function resolveQualityLoopGate({optIn=false,configPath=DEFAULT_CONFIG}={}) {
  if(typeof optIn!=='boolean') fail('quality_feature_config_invalid','quality loop opt-in must be boolean');
  const {config,digest}=loadQualityFeatureFlags({configPath});
  const settings=config.features[FEATURE];
  if(!settings.default_enabled && !optIn)
    fail('quality_loop_disabled','iterative video quality loop requires explicit opt-in');
  return {schema:'jianying-quality-loop-gate/v1',feature:FEATURE,
    activation:settings.default_enabled?'default':'explicit_opt_in',config_digest:digest};
}

/**
 * 校验计划中的门禁记录，并复核它仍绑定当前发布包的配置。
 */
export function validateQualityLoopGate(gate,{configPath=DEFAULT_CONFIG}={}) {
  exactKeys(gate,['schema','feature','activation','config_digest'],'quality loop gate','quality_feature_gate_invalid');
  if(gate.schema!=='jianying-quality-loop-gate/v1' || gate.feature!==FEATURE ||
    !['default','explicit_opt_in'].includes(gate.activation) || !DIGEST.test(gate.config_digest))
    fail('quality_feature_gate_invalid','quality loop gate record is invalid');
  const {config,digest}=loadQualityFeatureFlags({configPath});
  if(gate.config_digest!==digest)
    fail('quality_feature_gate_stale','quality loop gate does not match the packaged feature config');
  if(gate.activation==='default' && !config.features[FEATURE].default_enabled)
    fail('quality_feature_gate_invalid','default activation is not enabled by the packaged feature config');
  return {valid:true};
}
