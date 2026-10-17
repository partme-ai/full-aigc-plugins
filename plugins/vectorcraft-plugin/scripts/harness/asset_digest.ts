import {spawnSync} from 'node:child_process';
import {join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {strictJson} from '../../src/strict_json.ts';
import {nativeEnvironment} from './native_environment.ts';

/** 由固定技能描述符读取器计算素材摘要；冻结根不会在子进程重新授权。 */
export function assetDigest(path:string,roots:string[],skill:string,python:string):string {
 const result=spawnSync(python,['-I','-B',fileURLToPath(new URL('./asset_digest.py',import.meta.url)),join(skill,'scripts/asset_reader.py')],
  {input:JSON.stringify({path,roots}),encoding:'utf8',env:nativeEnvironment(),timeout:30000,maxBuffer:4096});
 if(result.error)throw new Error('asset_preflight_process_failed');
 let reply:any;try{reply=strictJson(result.stdout);}catch{throw new Error('asset_preflight_reply_invalid');}
 if(result.status!==0){
  const allowed=new Set(['asset_read_outside_root','asset_read_roots_invalid','asset_path_invalid','asset_digest_mismatch','asset_input_identity_changed','asset_input_invalid']);
  throw new Error(allowed.has(reply?.error)?reply.error:'asset_preflight_failed');
 }
 if(!reply||typeof reply.sha256!=='string'||!/^[a-f0-9]{64}$/.test(reply.sha256))throw new Error('asset_preflight_reply_invalid');
 return reply.sha256;
}
