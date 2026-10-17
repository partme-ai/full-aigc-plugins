import {spawnSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {strictJson} from '../../src/strict_json.ts';
import {nativeEnvironment} from './native_environment.ts';

/** 将内容写入宿主冻结根；返回已持有文件的摘要及身份，不按路径重新读取。 */
export function authorizedWrite(path:string,root:string,data:string|Buffer,mode:0o400|0o600,replace=false):{sha256:string,device:number,inode:number,size:number} {
 const bytes=typeof data==='string'?Buffer.from(data,'utf8'):data;
 if(bytes.length>64*1024*1024)throw new Error('authorized_write_size_limit');
 const helper=fileURLToPath(new URL('./authorized_write.py',import.meta.url));
 const result=spawnSync('python3',['-I','-B',helper],{input:JSON.stringify({path,root,base64:bytes.toString('base64'),mode,replace}),encoding:'utf8',env:nativeEnvironment(),timeout:30000,maxBuffer:4096});
 if(result.error)throw new Error('authorized_write_process_failed');
 let reply:any;try{reply=strictJson(result.stdout);}catch{throw new Error('authorized_write_reply_invalid');}
 if(result.status!==0){const allowed=new Set(['authorized_write_outside_root','authorized_write_size_limit']);throw new Error(allowed.has(reply?.error)?reply.error:'authorized_write_failed');}
 if(reply?.sha256!==createHash('sha256').update(bytes).digest('hex')||reply.size!==bytes.length
   ||!Number.isSafeInteger(reply.device)||!Number.isSafeInteger(reply.inode)||reply.device<0||reply.inode<=0)throw new Error('authorized_write_reply_invalid');
 return reply;
}
