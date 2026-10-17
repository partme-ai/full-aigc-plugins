import {readFileSync} from 'node:fs';
import {join} from 'node:path';
import {pathToFileURL} from 'node:url';
const [implementation,database,action,reportPath,delay]=process.argv.slice(2);
const {Ledger}=await import(pathToFileURL(join(implementation,'src/harness/ledger.ts')).href),{RuntimeGate}=await import(pathToFileURL(join(implementation,'src/runtime/runtime_gate.ts')).href);
const ledger=new Ledger(database),gate=new RuntimeGate(ledger),report=JSON.parse(readFileSync(reportPath,'utf8'));
console.log(JSON.stringify({ready:true}));
const go=await new Promise<string>(ok=>{process.stdin.once('data',b=>ok(b.toString()));});if(go.trim()!=='go')throw new Error('race_gate_missing');await new Promise(r=>setTimeout(r,Number(delay)));
try{
 if(action==='activate')gate.activate(report,{mode:'headless',commands:{},tools:{}},[3]);
 else ledger.claim('race','/tmp/vector-runtime-race-resource','/tmp/vector-runtime-race-output',{planHash:'a'.repeat(64),inputHashes:{},projectRevision:null,runtimeIdentity:report.binarySha256,authorization:{objects:[],fields:[],deadline:Date.now()+60000,maxAttempts:1,maxBytes:100}});
 console.log(JSON.stringify({action,result:'PASS'}));
}catch(error){console.log(JSON.stringify({action,result:'REFUSED',reason:String(error)}));}finally{ledger.close();process.stdin.pause();}
