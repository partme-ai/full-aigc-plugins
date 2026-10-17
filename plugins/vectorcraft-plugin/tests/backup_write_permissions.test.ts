/** 已登记备份目录随后被替换时，迁移不得向外部写入或修改旧schema。 */
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import childProcess from 'node:child_process';
import {syncBuiltinESMExports} from 'node:module';
import {DatabaseSync} from 'node:sqlite';
import {tmpdir} from 'node:os';
import {join,dirname} from 'node:path';
import {Ledger} from '../scripts/harness/ledger.ts';
test('migration refuses a backup directory swapped after reservation without writing outside or migrating',()=>{
 const root=fs.realpathSync(fs.mkdtempSync(join(tmpdir(),'vectorcraft-backup-write-'))),path=join(root,'state.sqlite'),directory=join(root,'state-schema-backups'),outside=join(root,'outside');fs.mkdirSync(outside);
 const legacy=new DatabaseSync(path);legacy.exec("PRAGMA journal_mode=WAL;CREATE TABLE preserved(value TEXT);INSERT INTO preserved VALUES('synthetic legacy state');PRAGMA user_version=1;");legacy.close();
 const open=fs.openSync,spawn=childProcess.spawnSync;let swapped=false,staging:string|undefined,ledger:Ledger|undefined;
 const swap=()=>{if(swapped)return;swapped=true;fs.renameSync(directory,directory+'-original');fs.symlinkSync(outside,directory,'dir');};
 try{
  fs.openSync=((file:any,...args:any[])=>{const result=(open as any)(file,...args);if(String(file).startsWith(directory+'/')&&args[0]==='wx')swap();return result;}) as typeof fs.openSync;
  childProcess.spawnSync=((command:any,args:any,options:any)=>{if(args?.some((arg:any)=>String(arg).endsWith('asset_digest.py'))){const request=JSON.parse(options.input);if(request.operation==='file-copy'&&request.target.startsWith(directory+'/')){staging=dirname(request.path);swap();}}return (spawn as any)(command,args,options);}) as typeof childProcess.spawnSync;syncBuiltinESMExports();
  let failure:unknown;try{ledger=new Ledger(path);}catch(error){failure=error;}
  assert(swapped);assert.deepEqual(fs.readdirSync(outside),[],'SQLite must not create an unreserved external backup');assert.match(String(failure),/state_backup_failed/);
  if(staging)assert(!fs.existsSync(staging),'owned private staging is removed after failed publication');
  const current=new DatabaseSync(path,{readOnly:true});try{assert.equal((current.prepare('PRAGMA user_version').get() as any).user_version,1);assert.equal(current.prepare('SELECT value FROM preserved').get()?.value,'synthetic legacy state');}finally{current.close();}
 }finally{ledger?.close();fs.openSync=open;childProcess.spawnSync=spawn;syncBuiltinESMExports();fs.rmSync(root,{recursive:true,force:true});}
});

test('failed exclusive staging creation never deletes an existing directory',()=>{
 const root=fs.realpathSync(fs.mkdtempSync(join(tmpdir(),'vectorcraft-staging-owner-'))),path=join(root,'state.sqlite');
 const legacy=new DatabaseSync(path);legacy.exec('PRAGMA user_version=1;CREATE TABLE preserved(value TEXT);');legacy.close();
 const spawn=childProcess.spawnSync;let collision:string|undefined;
 try{
  childProcess.spawnSync=((command:any,args:any,options:any)=>{if(args?.some((arg:any)=>String(arg).endsWith('authorized_tree.py'))){const request=JSON.parse(options.input);if(request.operation==='directory'&&request.exclusive&&request.path.includes('/vectorcraft-state-backup-')){collision=request.path;fs.mkdirSync(collision!);fs.writeFileSync(join(collision!,'sentinel'),'synthetic preexisting directory');}}return (spawn as any)(command,args,options);}) as typeof childProcess.spawnSync;syncBuiltinESMExports();
  assert.throws(()=>new Ledger(path),/state_backup_failed/);assert(collision);assert.equal(fs.readFileSync(join(collision,'sentinel'),'utf8'),'synthetic preexisting directory');
  const current=new DatabaseSync(path,{readOnly:true});try{assert.equal((current.prepare('PRAGMA user_version').get() as any).user_version,1);}finally{current.close();}
 }finally{childProcess.spawnSync=spawn;syncBuiltinESMExports();if(collision)fs.rmSync(collision,{recursive:true,force:true});fs.rmSync(root,{recursive:true,force:true});}
});

test('staging cleanup failure stops migration and retains the valid published backup',()=>{
 const root=fs.realpathSync(fs.mkdtempSync(join(tmpdir(),'vectorcraft-backup-cleanup-'))),path=join(root,'state.sqlite');
 const legacy=new DatabaseSync(path);legacy.exec("PRAGMA user_version=1;CREATE TABLE preserved(value TEXT);INSERT INTO preserved VALUES('retained');");legacy.close();
 const remove=fs.rmSync;let staging:string|undefined;
 try{
  fs.rmSync=((target:any,...args:any[])=>{if(String(target).includes('/vectorcraft-state-backup-')){staging=String(target);throw Object.assign(new Error('synthetic cleanup I/O failure'),{code:'EIO'});}return (remove as any)(target,...args);}) as typeof fs.rmSync;syncBuiltinESMExports();
  assert.throws(()=>new Ledger(path),/state_backup_failed; staging cleanup failed; schema not migrated/);assert(staging);
  const files=fs.readdirSync(join(root,'state-schema-backups'));assert.equal(files.length,1);
  for(const database of [path,join(root,'state-schema-backups',files[0])]){const saved=new DatabaseSync(database,{readOnly:true});try{assert.equal((saved.prepare('PRAGMA user_version').get() as any).user_version,1);assert.equal(saved.prepare('SELECT value FROM preserved').get()?.value,'retained');}finally{saved.close();}}
 }finally{fs.rmSync=remove;syncBuiltinESMExports();if(staging)fs.rmSync(staging,{recursive:true,force:true});fs.rmSync(root,{recursive:true,force:true});}
});
