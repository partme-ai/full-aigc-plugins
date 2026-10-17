import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,realpathSync,mkdirSync,writeFileSync,existsSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {Controller,skillDigest} from '../scripts/harness/controller.ts';
import {runtimeFixture} from './runtime_fixture.ts';
test('expired ready resume requests cancellation instead of preparing or launching again',async()=>{
 const root=realpathSync(mkdtempSync(join(tmpdir(),'vector-expired-resume-'))),skill=join(root,'skill');mkdirSync(join(skill,'scripts'),{recursive:true});
 writeFileSync(join(skill,'scripts/workflow.py'),'raise RuntimeError("must never launch")\n');writeFileSync(join(skill,'scripts/execution_control.py'),'# unit fixture only\n');writeFileSync(join(skill,'scripts/runtime.lock.json'),JSON.stringify({artifacts:{'darwin-arm64':{binarySha256:'c'.repeat(64)}}}));runtimeFixture(skill,'c'.repeat(64));
 const plan=join(root,'plan.json');writeFileSync(plan,'{"operations":[]}');const controller=new Controller(join(root,'state.sqlite'),runtimeFixture(skill,'c'.repeat(64))),now=Date.now;
 const request={key:'ready-expiry',skill,expectedSkillSha256:skillDigest(skill),plan,output:join(root,'out'),runtimeHome:join(root,'runtime'),estimatedBytes:1000,authorization:{budgetId:'one',objects:[],fields:[],deadline:Date.now()+60000,maxAttempts:1,maxBytes:1000,readRoots:[root],writeRoots:[root]}};
 try{
  const claim=controller.ledger.claim.bind(controller.ledger);controller.ledger.claim=(...args:any[])=>{claim(...args);throw new Error('unit crash after claim');};
  await assert.rejects(()=>controller.run(request),/unit crash/);controller.ledger.claim=claim;
  Date.now=()=>request.authorization.deadline+1;const resumed=await controller.run(request);assert.equal(resumed.state,'cancel_requested');assert.equal(resumed.attempts,0);assert.equal(existsSync(request.output),false);
  assert.ok(controller.ledger.db.prepare('SELECT id FROM budget_cancellations WHERE id=?').get('one'));
 }finally{Date.now=now;controller.close();rmSync(root,{recursive:true,force:true});}
});
