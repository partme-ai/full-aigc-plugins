import {runtimeFixture} from './runtime_fixture.ts';
import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync,mkdirSync,writeFileSync,rmSync,existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { Controller,skillDigest } from '../scripts/harness/controller.ts';

// 合成协调器fixture，不充当真实原生或像素验收。
function fixture(){
 const root=mkdtempSync(join(tmpdir(),'vector geometry ')),skill=join(root,'skill');mkdirSync(join(skill,'scripts'),{recursive:true});
 writeFileSync(join(skill,'scripts/workflow.py'),`import argparse,pathlib,json,hashlib\np=argparse.ArgumentParser();p.add_argument('plan');p.add_argument('--output');p.add_argument('--runtime-home');p.add_argument('--control');a=p.parse_args();o=pathlib.Path(a.output);o.mkdir();(o/'project.vectorcraft').write_bytes(b'native');m={'schema':'vectorcraft-delivery/v1','runtimeSha256':'${'a'.repeat(64)}','files':{'project.vectorcraft':hashlib.sha256(b'native').hexdigest()}};(o/'manifest.json').write_text(json.dumps(m))\n`);
 writeFileSync(join(skill,'scripts/execution_control.py'),'# synthetic control fixture\n');writeFileSync(join(skill,'scripts/runtime.lock.json'),JSON.stringify({artifacts:{'darwin-arm64':{binarySha256:'a'.repeat(64)}}}));
 runtimeFixture(skill,'a'.repeat(64));
  const plan=join(root,'plan.json');writeFileSync(plan,'{"operations":[]}');const controller=new Controller(join(root,'state.sqlite'),runtimeFixture(skill,'a'.repeat(64)));
 const request={key:'geometry',skill,expectedSkillSha256:skillDigest(skill),plan,output:join(root,'output'),runtimeHome:join(root,'runtime'),estimatedBytes:10000,authorization:{objects:[2],fields:['kind.path'],deadline:Date.now()+10000,maxAttempts:2,maxBytes:100000,readRoots:[root],writeRoots:[root]}};
 return {root,controller,request,close:()=>{controller.close();rmSync(root,{recursive:true,force:true});}};
}

test('preview pixel geometry and unspecified units are refused before effects',async()=>{
 const f=fixture();try{
  await assert.rejects(()=>f.controller.run({...f.request,geometryContract:{schema:'vectorcraft-geometry-contract/v1',coordinateSpace:'preview-pixels',units:'Millimeters'}} as any),/invalid_geometry_contract/);
  assert.equal(existsSync(f.request.output),false);assert.equal((f.controller.ledger.db.prepare('SELECT COUNT(*) AS n FROM tasks').get() as any).n,0);
 }finally{f.close();}
});

import { validateGeometryContract,verifyGeometry } from '../src/planning/geometry.ts';
function data(){
 const anchors=[{p:[120,80],out:[130,90]},{p:[150,100],in:[140,95]}];
 const native={units:'Points',artboards:[{id:2,rect:{x0:100,y0:60,x1:300,y1:200}}],layers:[{id:1,kind:{type:'layer',children:[{id:4,kind:{type:'path',path:{subpaths:[{closed:false,anchors}]}},appearance:{items:[{kind:'stroke',width:2,paint:{type:'none'}}]}}]}}]};
 const contract:any={schema:'vectorcraft-geometry-contract/v1',units:'Points',coordinateSpace:'artboard-local',tolerance:0.000001,artboards:[{id:2,rect:[100,60,300,200]}],paths:[{binding:'curve.id',artboardId:2,subpaths:[{closed:false,anchors:[{p:[20,20],out:[30,30]},{p:[50,40],in:[40,35]}]}],strokes:[{width:2,paint:{type:'none'}}]}]};
 return {native,contract,bindings:{curve:{id:4}}};
}
test('artboard-local controls are verified against native coordinates without previews',()=>{
 const f=data();const r=verifyGeometry(f.native,f.bindings,f.contract);assert.equal(r.status,'PASS');assert.deepEqual(r.checkedObjectIds,[4]);
});
test('closure and unit mismatches report real object IDs',()=>{
 const f=data();f.contract.units='Pixels';f.contract.paths[0].subpaths[0].closed=true;const r=verifyGeometry(f.native,f.bindings,f.contract);
 assert.equal(r.status,'FAIL');assert.deepEqual(new Set(r.issues.map((i:any)=>i.reason)),new Set(['units_mismatch','path_closed_mismatch']));assert.ok(r.issues.every((i:any)=>i.objectId===4));
});
test('point, handle and stroke drift cannot be masked by a matching anchor count',()=>{
 const f=data();f.contract.paths[0].subpaths[0].anchors[0].out=[31,30];f.contract.paths[0].strokes[0].width=3;
 const r=verifyGeometry(f.native,f.bindings,f.contract);assert.equal(r.status,'FAIL');assert.ok(r.issues.some((i:any)=>i.reason==='path_control_point_mismatch'));assert.ok(r.issues.some((i:any)=>i.reason==='stroke_mismatch'));
});
test('duplicate binding aliases and missing actual IDs never become successful geometry',()=>{
 const f=data();f.contract.paths.push({...structuredClone(f.contract.paths[0]),binding:undefined,objectId:4});delete f.contract.paths[1].binding;
 assert.ok(verifyGeometry(f.native,f.bindings,f.contract).issues.some((i:any)=>i.reason==='duplicate_native_target'));
 f.contract.paths.splice(1);assert.equal(verifyGeometry(f.native,{curve:{id:999}},f.contract).issues[0].reason,'native_path_identity_mismatch');
});
test('ambiguous boards and unknown inherited transformations are refused',()=>{
 const f=data();f.native.artboards.push(structuredClone(f.native.artboards[0]));assert.equal(verifyGeometry(f.native,f.bindings,f.contract).issues[0].reason,'artboard_identity_mismatch');
 f.native.artboards.pop();(f.native.layers[0] as any).transform=[1,0,0,1,20,0];assert.equal(verifyGeometry(f.native,f.bindings,f.contract).issues[0].reason,'unsupported_native_geometry_context');
});
test('nonfinite controls, duplicate targets and relaxed tolerances fail contract validation',()=>{
 for(const mutate of [(c:any)=>c.paths[0].subpaths[0].anchors[0].p=[Infinity,0],(c:any)=>c.paths.push(c.paths[0]),(c:any)=>c.tolerance=1,(c:any)=>c.paths[0].binding='curve.__proto__.id']){
  const f=data();mutate(f.contract);assert.throws(()=>validateGeometryContract(f.contract),/invalid_geometry_contract/);
 }
});
