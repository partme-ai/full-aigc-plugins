import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {join,resolve} from 'node:path';
import {spawn} from 'node:child_process';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const [output,probeDirectory,implementation=process.cwd()]=process.argv.slice(2);if(!output||!probeDirectory)throw new Error('usage: runtime_activation_race.ts NEW_ROOT PROBES [INSTALLED_PLUGIN]');
const root=resolve(output),probes=resolve(probeDirectory),installed=resolve(implementation);mkdirSync(root);const read=(p:string)=>JSON.parse(readFileSync(p,'utf8')),sha=(p:string)=>createHash('sha256').update(readFileSync(p)).digest('hex');
const {Ledger}=await import(pathToFileURL(join(installed,'src/harness/ledger.ts')).href),{RuntimeGate}=await import(pathToFileURL(join(installed,'src/runtime/runtime_gate.ts')).href);
const old=read(join(probes,'old-probe.json')),current=read(join(probes,'new-probe.json')),cases:any[]=[];
function actor(database:string,action:string,delay:number){
 const child=spawn(process.execPath,[resolve('scripts/acceptance/runtime_activation_race_child.ts'),installed,database,action,join(probes,action==='activate'?'new-probe.json':'old-probe.json'),String(delay)],{stdio:['pipe','pipe','pipe']});let stdout='',stderr='';let release:()=>void;const ready=new Promise<void>(ok=>release=ok);child.stdout.on('data',b=>{stdout+=b;if(stdout.includes('"ready":true'))release();});child.stderr.on('data',b=>stderr+=b);
 const timeout=setTimeout(()=>child.kill('SIGKILL'),30000);const done=new Promise<any>((ok,no)=>{child.on('error',no);child.on('close',code=>{clearTimeout(timeout);if(code!==0)no(new Error(stderr||stdout));else ok(JSON.parse(stdout.trim().split('\n').at(-1)!));});});return {child,ready,done};
}
for(let round=0;round<8;round++){
 const database=join(root,'race-'+round+'.sqlite'),ledger=new Ledger(database),gate=new RuntimeGate(ledger);gate.activate(old,{mode:'headless',commands:{},tools:{}},[3]);
 const activate=actor(database,'activate',round%2?20:0),claim=actor(database,'claim',round%2?0:20);
 try{
  await Promise.all([activate.ready,claim.ready]);activate.child.stdin.end('go\n');claim.child.stdin.end('go\n');const [a,c]=await Promise.all([activate.done,claim.done]);
  assert.notEqual(a.result,c.result,'only activation or old-version claim may succeed');
  const count=Number((ledger.db.prepare('SELECT COUNT(*) AS n FROM tasks').get() as any).n);
  if(a.result==='PASS'){assert.match(c.reason,/runtime_selection_mismatch/);assert.equal(count,0);assert.equal(gate.current().active.binarySha256,current.binarySha256);}else{assert.match(a.reason,/runtime_tasks_not_drained/);assert.equal(count,1);assert.equal(gate.current().active.binarySha256,old.binarySha256);}
  cases.push({round,activate:a,claim:c,taskCount:count});
 }finally{activate.child.kill();claim.child.kill();ledger.close();}
}
assert.ok(cases.some(r=>r.activate.result==='PASS')&&cases.some(r=>r.claim.result==='PASS'));
const fingerprints=Object.fromEntries(['src/harness/ledger.ts','src/runtime/runtime_gate.ts','src/strict_json.ts','plugin.json'].map(p=>[p,sha(join(installed,p))]));
const driverFingerprints=Object.fromEntries(['scripts/acceptance/runtime_activation_race.ts','scripts/acceptance/runtime_activation_race_child.ts'].map(p=>[p,sha(p)]));
writeFileSync(join(root,'proof.json'),JSON.stringify({schema:'vectorcraft-runtime-activation-race/v1',result:'PASS',platform:process.platform+'-'+process.arch,pluginVersion:read(join(installed,'plugin.json')).version,cases,fingerprints,driverFingerprints,scope:'Eight two-process races against actual installed SQLite ledger; both winning orders observed, no stale-runtime writer after activation'},null,2)+'\n');console.log(JSON.stringify({result:'PASS',cases:cases.length}));
