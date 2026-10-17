import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { randomUUID } from 'node:crypto';
import { ProcessRegistry } from '../scripts/harness/process_registry.ts';
import { DatabaseSync } from 'node:sqlite';

const sleep=(ms:number)=>new Promise(r=>setTimeout(r,ms));
test('durable ownership survives registry restart and stops a TERM-ignoring descendant',async()=>{
  const db=new DatabaseSync(':memory:'),registry=new ProcessRegistry(db),marker=randomUUID();
  const child=spawn('python3',['-I','-B','-c',`import subprocess,sys,time\nsubprocess.Popen([sys.executable,'-c','import signal,time;signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(30)'])\nprint('ready',flush=True)\ntime.sleep(30)`,marker],{detached:true,stdio:['ignore','pipe','pipe']});
  await new Promise<void>(r=>child.stdout.once('data',()=>r()));
  try {
    registry.register('task',1,child.pid!,marker);
    assert.equal(registry.observe('task',1).stopped,false);
    const restarted=new ProcessRegistry(db);
    const proof=await restarted.stop('task',1,100);
    assert.equal(proof.stopped,true);
    assert.equal(restarted.observe('task',1).stopped,true);
    assert.ok(JSON.parse((db.prepare('SELECT identity FROM native_processes').get() as any).identity).known.length>=2);
  } finally {try{process.kill(-child.pid!,'SIGKILL');}catch{} db.close();}
});
test('a forged root identity never authorizes signalling a live group',async()=>{
  const db=new DatabaseSync(':memory:'),registry=new ProcessRegistry(db),marker=randomUUID();
  const child=spawn('python3',['-I','-B','-c','import time;time.sleep(30)',marker],{detached:true,stdio:'ignore'});
  await sleep(50);
  try{
    assert.throws(()=>registry.register('bad',1,child.pid!,'wrong-marker'),/process_identity_mismatch/);
    registry.register('task',1,child.pid!,marker);
    const record=JSON.parse((db.prepare('SELECT identity FROM native_processes').get() as any).identity);
    record.root.start='wrong';record.known=[];
    db.prepare('UPDATE native_processes SET identity=?').run(JSON.stringify(record));
    await assert.rejects(()=>registry.stop('task',1,50),/process_ownership_unconfirmed/);
    assert.doesNotThrow(()=>process.kill(child.pid!,0));
  }finally{try{process.kill(-child.pid!,'SIGKILL');}catch{}db.close();}
});
