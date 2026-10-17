import {spawnSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {strictJson} from '../../src/strict_json.ts';
import {nativeEnvironment} from './native_environment.ts';

/** 可信宿主读取入口：固定技能读取器持有描述符，冻结根不会随目录替换扩张。 */
function inspect(path:string|string[],roots:string[],operation:'file-read'|'file-digest'|'file-digests'|'file-copy',copy?:{target:string,writeRoot:string,expected:string}):any {
 const helper=fileURLToPath(new URL('./asset_digest.py',import.meta.url));
 const reader=fileURLToPath(new URL('../../skills/vectorcraft-harness/scripts/asset_reader.py',import.meta.url));
 const result=spawnSync('python3',['-I','-B',helper,reader],{input:JSON.stringify({...(Array.isArray(path)?{paths:path}:{path}),roots,operation,...copy}),encoding:'utf8',env:nativeEnvironment(),timeout:30000,maxBuffer:operation==='file-read'?96*1024*1024:operation==='file-digests'?32*1024*1024:4096});
 if(result.error)throw new Error('authorized_read_process_failed');
 let reply:any;try{reply=strictJson(result.stdout);}catch{throw new Error('authorized_read_reply_invalid');}
 if(result.status!==0){
  const reasons=new Set(['asset_read_outside_root','asset_read_roots_invalid','asset_path_invalid','asset_digest_mismatch','asset_input_identity_changed','snapshot_write_outside_root','stale_source_dependencies']);
  throw new Error(reasons.has(reply?.error)?reply.error:'authorized_read_failed');
 }
 if(operation==='file-digests')return reply;
 if(!reply||!/^[a-f0-9]{64}$/.test(reply.sha256??''))throw new Error('authorized_read_reply_invalid');
 return reply;
}

/** 在冻结源根内流式复制；目标父目录不跟随链接，摘要匹配后持久化只读快照。 */
export function authorizedCopy(path:string,roots:string[],target:string,writeRoot:string,expected:string):void {
 if(!/^[a-f0-9]{64}$/.test(expected))throw new Error('stale_source_dependencies');
 if(inspect(path,roots,'file-copy',{target,writeRoot,expected}).sha256!==expected)throw new Error('stale_source_dependencies');
}

/** 读取不超过既有64MiB上限的授权文件；返回字节前核对传输摘要。 */
export function authorizedRead(path:string,roots:string[]):Buffer {
 const reply=inspect(path,roots,'file-read');
 if(typeof reply.base64!=='string'||reply.base64.length>Math.ceil(64*1024*1024/3)*4)throw new Error('authorized_read_reply_invalid');
 const bytes=Buffer.from(reply.base64,'base64');
 if(bytes.toString('base64')!==reply.base64||createHash('sha256').update(bytes).digest('hex')!==reply.sha256)throw new Error('authorized_read_reply_invalid');
 return bytes;
}

/** 流式计算授权文件摘要，不额外限制已有评审输入的大小。 */
export function authorizedDigest(path:string,roots:string[]):string {
 return inspect(path,roots,'file-digest').sha256;
}

/** 批量流式核验冻结根内的文件，避免轮询时每个输入启动一个辅助进程。 */
export function authorizedDigests(paths:string[],roots:string[]):Record<string,string> {
 const result:Record<string,string>=Object.create(null);
 for(let start=0;start<paths.length;start+=4096){
  const batch=[...new Set(paths.slice(start,start+4096))],reply=inspect(batch,roots,'file-digests');
  const digests=reply?.digests;
  if(!digests||typeof digests!=='object'||Array.isArray(digests)||Object.keys(digests).length!==batch.length
    ||batch.some(path=>!/^[a-f0-9]{64}$/.test(digests[path]??'')))throw new Error('authorized_read_reply_invalid');
  Object.assign(result,digests);
 }
 return result;
}
