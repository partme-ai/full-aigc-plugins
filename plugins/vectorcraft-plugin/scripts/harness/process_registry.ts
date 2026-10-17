import {nativeEnvironment} from './native_environment.ts';
import { execFileSync } from 'node:child_process';
import { realpathSync } from 'node:fs';
import { basename } from 'node:path';
import type { DatabaseSync } from 'node:sqlite';
import { canonical, strictJson } from '../../src/strict_json.ts';

type Member={pid:number,pgid:number,start:string,command:string,status:string};
type Identity={root:Member,marker:string,known:Member[]};
const pause=(ms:number)=>new Promise(r=>setTimeout(r,ms));

/** 操作系统进程身份；读取失败不等于进程已经停止。 */
function processes():Member[]{
  const output=execFileSync('/bin/ps',['-axo','pid=,pgid=,stat=,lstart=,command='],{env:nativeEnvironment(),encoding:'utf8',maxBuffer:16*1024*1024});
  return output.split('\n').filter(line=>line.trim()).map(line=>{
    const match=line.trim().match(/^(\d+)\s+(\d+)\s+(\S+)\s+(\w+\s+\w+\s+\d+\s+\d+:\d+:\d+\s+\d+)\s+(.*)$/);
    if(!match)throw new Error('process_observation_failed');
    return {pid:Number(match[1]),pgid:Number(match[2]),status:match[3],start:match[4].replace(/\s+/g,' '),command:match[5]};
  });
}
const same=(a:Member,b:Member)=>a.pid===b.pid&&a.pgid===b.pgid&&a.start===b.start;
// macOS 在退出窗口可能只显示 (comm)，不能将同一出生身份误判为另一个进程。
const sameCommand=(current:Member,known:Member)=>{
  if(current.command===known.command)return true;
  if(!/^\([^()]+\)$/.test(current.command))return false;
  try{return current.command==='('+basename(realpathSync(known.command.split(' ')[0]))+')';}catch{return false;}
};

/** 持久记录自建进程组；没有身份依据时禁止向复用的 PID/PGID 发信号。 */
export class ProcessRegistry{
  db:DatabaseSync;
  constructor(db:DatabaseSync){
    this.db=db;
    db.exec(`CREATE TABLE IF NOT EXISTS native_processes(task TEXT NOT NULL,epoch INTEGER NOT NULL,identity TEXT NOT NULL,stopped_at INTEGER,PRIMARY KEY(task,epoch));`);
  }
  register(task:string,epoch:number,pid:number,marker:string){
    const all=processes(),root=all.find(p=>p.pid===pid);
    if(!marker||!root||root.pgid!==pid||!root.command.includes(marker))throw new Error('process_identity_mismatch');
    const identity:Identity={root,marker,known:all.filter(p=>p.pgid===pid&&!p.status.startsWith('Z'))};
    this.db.prepare('INSERT INTO native_processes(task,epoch,identity) VALUES(?,?,?)').run(task,epoch,canonical(identity));
  }
  observe(task:string,epoch:number):{stopped:boolean,owned:boolean,members:Member[]}{
    const row=this.db.prepare('SELECT identity FROM native_processes WHERE task=? AND epoch=?').get(task,epoch) as any;
    if(!row)throw new Error('native_process_identity_missing');
    const identity:Identity=strictJson(row.identity),members=processes().filter(p=>p.pgid===identity.root.pgid&&!p.status.startsWith('Z'));
    const root=members.find(p=>same(p,identity.root)&&p.command.includes(identity.marker));
    // exec 保留 PID 和启动时间，子进程的 argv 不必携带启动门禁的 nonce。
    const owned=!!root||members.some(p=>identity.known.some(k=>same(p,k)&&sameCommand(p,k)));
    if(owned){
      identity.known=[...identity.known,...members.filter(p=>!identity.known.some(k=>same(p,k)&&sameCommand(p,k)))];
      this.db.prepare('UPDATE native_processes SET identity=? WHERE task=? AND epoch=?').run(canonical(identity),task,epoch);
    }
    if(!members.length)this.db.prepare('UPDATE native_processes SET stopped_at=COALESCE(stopped_at,?) WHERE task=? AND epoch=?').run(Date.now(),task,epoch);
    return {stopped:members.length===0,owned,members};
  }
  signal(task:string,epoch:number,signal:NodeJS.Signals){
    const observed=this.observe(task,epoch);
    if(observed.stopped)return;
    if(!observed.owned)throw new Error('process_ownership_unconfirmed: '+canonical(observed.members));
    try{process.kill(-observed.members[0].pgid,signal);}catch(error){
      if((error as NodeJS.ErrnoException).code==='ESRCH'||this.observe(task,epoch).stopped)return;
      throw error;
    }
  }
  async stop(task:string,epoch:number,grace=2000){
    this.signal(task,epoch,'SIGTERM');
    const deadline=Date.now()+grace;
    while(Date.now()<deadline){const observed=this.observe(task,epoch);if(observed.stopped)return observed;await pause(25);}
    this.signal(task,epoch,'SIGKILL');
    const killedDeadline=Date.now()+2000;
    while(Date.now()<killedDeadline){const observed=this.observe(task,epoch);if(observed.stopped)return observed;await pause(25);}
    throw new Error('native_stop_unconfirmed');
  }
}
