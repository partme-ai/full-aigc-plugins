import test from 'node:test';
import assert from 'node:assert/strict';
import {extendDiscoveryTool, callDiscoveryTool} from '../catalog-filter.mjs';

const rows=[{id:'path.join',label:'Join',menu:['Object','Path'],params:'{ids}',enabled:true},
 {id:'graph.create',label:'Create Graph',menu:[],params:'{rows}',enabled:true},
 {id:'path.reverse',label:'Reverse',menu:['Object','Path'],params:'{}',enabled:false}];

test('advertises query/menu/brief for existing editor catalogs',()=>{
 const original={name:'command_list',inputSchema:{type:'object',additionalProperties:false,properties:{filter:{type:'string'}}}};
 const next=extendDiscoveryTool(original);
 for(const key of ['query','menu','brief'])assert.ok(next.inputSchema.properties[key]);
 assert.equal(original.inputSchema.properties.query,undefined);
});
test('filters old backend results and strips params without altering enabled state',async()=>{
 let forwarded;
 const result=await callDiscoveryTool({name:'command_list',arguments:{query:'path.',menu:'object > path',brief:true}},async p=>{
  forwarded=p;return {content:[{type:'text',text:JSON.stringify(rows)}]};
 });
 assert.deepEqual(forwarded.arguments,{filter:'path.'});
 const list=JSON.parse(result.content[0].text);
 assert.deepEqual(list.map(x=>x.id),['path.join','path.reverse']);
 assert.equal(list[1].enabled,false);
 assert.equal(list[0].params,undefined);
 assert.equal(rows[0].params,'{ids}');
});
test('filter wins over query and full detail remains available',async()=>{
 const result=await callDiscoveryTool({name:'list_commands',arguments:{filter:'graph.create',query:'path.'}},async()=>({content:[{type:'text',text:JSON.stringify(rows)}]}));
 const list=JSON.parse(result.content[0].text);assert.equal(list.length,1);assert.equal(list[0].params,'{rows}');
});
test('does not hide backend failures or accept malformed catalogs',async()=>{
 const failed={isError:true,content:[{type:'text',text:'editor unavailable'}]};
 assert.equal(await callDiscoveryTool({name:'command_list',arguments:{}},async()=>failed),failed);
 await assert.rejects(()=>callDiscoveryTool({name:'command_list',arguments:{brief:true}},async()=>({content:[{type:'text',text:'not JSON'}]})));
});
