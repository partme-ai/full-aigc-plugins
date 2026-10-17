import {assertNoLiteralSecrets} from '../../scripts/harness/input_policy.ts';
import {nativeEnvironment} from '../../scripts/harness/native_environment.ts';
import {spawn} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {strictJson} from '../strict_json.ts';

export type RuntimeProbe=(request:any)=>Promise<any>;
/** 默认首用只安装固定版本并只读探测；独立进程组超时整体停止，不重试。 */
export const prepareRuntime:RuntimeProbe=async(request)=>{
 assertNoLiteralSecrets(request);
 const remaining=request.deadline-Date.now();
 if(remaining<=0)throw new Error('budget_exceeded');
 return await new Promise((accept,reject)=>{
  const child=spawn(request.python??'python3',['-I','-B',fileURLToPath(new URL('./runtime_probe.py',import.meta.url))],{env:nativeEnvironment(),detached:true,stdio:['pipe','pipe','pipe']});
  let stdout='',stderr='',failure:Error|undefined;
  const stop=(reason:string)=>{failure??=new Error(reason);try{process.kill(-child.pid!,'SIGKILL');}catch(error){if((error as NodeJS.ErrnoException).code!=='ESRCH')failure=new Error('runtime_probe_stop_unconfirmed: '+String(error));}};
  const timer=setTimeout(()=>stop('runtime_probe_timeout; no automatic retry'),Math.min(180000,remaining));
  child.stdout.on('data',b=>{stdout+=b.toString();if(Buffer.byteLength(stdout)>8*1024*1024)stop('runtime_probe_output_limit');});
  child.stderr.on('data',b=>{stderr=(stderr+b.toString()).slice(-8192);});
  child.on('error',error=>{clearTimeout(timer);reject(error);});
  child.on('close',code=>{clearTimeout(timer);if(failure)return reject(failure);if(code!==0)return reject(new Error('runtime_probe_failed: child output withheld'));try{accept(strictJson(stdout));}catch(error){reject(error);}});
  child.stdin.on('error',()=>stop('runtime_probe_write_failed'));
  child.stdin.end(JSON.stringify(request));
 });
};
