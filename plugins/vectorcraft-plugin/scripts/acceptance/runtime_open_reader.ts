import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {resolve,join} from 'node:path';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const [output,implementation]=process.argv.slice(2);if(!output||!implementation)throw new Error('usage: runtime_open_reader.ts NEW_ROOT INSTALLED_PLUGIN');
const root=resolve(output),installed=resolve(implementation);mkdirSync(root);const sha=(p:string)=>createHash('sha256').update(readFileSync(p)).digest('hex');
const {Ledger:Previous}=await import(pathToFileURL(join(installed,'docs/evidence/pre-runtime-boundaries-identity/src/harness/ledger.ts')).href);
const {Ledger}=await import(pathToFileURL(join(installed,'src/harness/ledger.ts')).href);
const database=join(root,'legacy-fixture.sqlite'),previous=new Previous(database),binding={planHash:'a'.repeat(64),inputHashes:{},projectRevision:null,runtimeIdentity:'b'.repeat(64),authorization:{objects:[],fields:[],deadline:Date.now()+60000,maxAttempts:3,maxBytes:100,budgetId:'original-budget'}};
const task=previous.claim('original',join(root,'original-resource'),join(root,'original-output'),binding);previous.intent(task.id,1,0,{fixture:true},17);
previous.db.exec('CREATE TABLE runtime_selection(id INTEGER PRIMARY KEY,active TEXT NOT NULL,previous TEXT)');previous.db.prepare('INSERT INTO runtime_selection VALUES(1,?,NULL)').run(JSON.stringify({mode:'headless',binarySha256:binding.runtimeIdentity,stateSchemas:[2]}));
let current:any;
try{
 current=new Ledger(database);assert.equal(current.schemaBackup.fromSchema,2);assert.equal(current.schemaBackup.toSchema,3);
 assert.throws(()=>previous.claim('refused-old-writer',join(root,'refused-resource'),join(root,'refused-output'),{...binding,authorization:{...binding.authorization,budgetId:'must-not-leak'}}),/incompatible_state_schema/);
 assert.equal((current.db.prepare('SELECT COUNT(*) AS n FROM tasks').get() as any).n,1);
 assert.equal(current.db.prepare('SELECT * FROM budgets WHERE id=?').get('must-not-leak'),undefined);
 const original=current.db.prepare('SELECT attempts,bytes FROM budgets WHERE id=?').get('original-budget') as any;assert.equal(original.attempts,1);assert.equal(original.bytes,17);
 assert.equal(current.get(task.id).attempts,1);assert.equal(current.get(task.id).bytes,17);
 const paths=['src/harness/ledger.ts','src/strict_json.ts','docs/evidence/pre-runtime-boundaries-identity/src/harness/ledger.ts','docs/evidence/pre-runtime-boundaries-identity/src/strict_json.ts','plugin.json'];
 const proof={schema:'vectorcraft-installed-open-reader/v1',result:'PASS',pluginVersion:JSON.parse(readFileSync(join(installed,'plugin.json'),'utf8')).version,backupSha256:sha(current.schemaBackup.path),fromSchema:2,toSchema:3,originalTasks:1,refusedNewTasks:0,leakedNewBudgets:0,preservedAttempts:original.attempts,preservedBytes:original.bytes,fingerprints:Object.fromEntries(paths.map(p=>[p,sha(join(installed,p))])),driverFingerprints:{'scripts/acceptance/runtime_open_reader.ts':sha(resolve('scripts/acceptance/runtime_open_reader.ts'))},scope:'Explicit schema2 fixture through actual previous reader, kept open with committed WAL during installed plugin43 migration; new budget/task rollback proved. No historical production database or native execution claimed.'};
 writeFileSync(join(root,'proof.json'),JSON.stringify(proof,null,2)+'\n');console.log(JSON.stringify({result:'PASS',leakedNewBudgets:0}));
}finally{previous.close();current?.close();}
