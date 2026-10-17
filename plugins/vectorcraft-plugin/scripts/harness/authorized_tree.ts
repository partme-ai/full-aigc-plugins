import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {strictJson} from '../../src/strict_json.ts';
import {nativeEnvironment} from './native_environment.ts';

function inspect(request:Record<string,unknown>):any {
 const helper=fileURLToPath(new URL('./authorized_tree.py',import.meta.url));
 const result=spawnSync('python3',['-I','-B',helper],{input:JSON.stringify(request),encoding:'utf8',env:nativeEnvironment(),timeout:30000,maxBuffer:4096});
 if(result.error)throw new Error('authorized_tree_process_failed');
 let reply:any;try{reply=strictJson(result.stdout);}catch{throw new Error('authorized_tree_reply_invalid');}
 if(result.status!==0){const allowed=new Set(['authorized_tree_outside_root','authorized_tree_identity_changed','authorized_tree_entry_invalid','skill_snapshot_mismatch']);throw new Error(allowed.has(reply?.error)?reply.error:'authorized_tree_failed');}
 return reply;
}
/** 只在冻结写入根内创建目录；每一层均拒绝链接，排他创建保留已有目录。 */
export function authorizedDirectory(path:string,root:string,exclusive=false):void {
 if(inspect({operation:'directory',path,root,exclusive}).result!=='PASS')throw new Error('authorized_tree_reply_invalid');
}
/** 流式复制完整固定技能树，以实际复制字节的整树摘要核对预绑定身份。 */
export function authorizedTreeCopy(source:string,target:string,root:string,expected:string):void {
 if(!/^[a-f0-9]{64}$/.test(expected))throw new Error('skill_snapshot_mismatch');
 if(inspect({operation:'copy-tree',source,target,root,expected}).sha256!==expected)throw new Error('skill_snapshot_mismatch');
}
/** 持有目录描述符计算已复制源快照摘要，拒绝随后发生的目录链接替换。 */
export function authorizedTreeDigest(source:string):string {
 const digest=inspect({operation:'tree-digest',source}).sha256;
 if(!/^[a-f0-9]{64}$/.test(digest??''))throw new Error('authorized_tree_reply_invalid');
 return digest;
}
