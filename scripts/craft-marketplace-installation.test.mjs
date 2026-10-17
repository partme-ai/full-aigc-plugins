import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';
const names='cadcraft designcraft effectcraft photocraft figcraft filmcraft lightcraft printcraft vectorcraft deckcraft soundcraft gridcraft wordcraft'.split(' ');
const read=p=>JSON.parse(fs.readFileSync(new URL('../'+p,import.meta.url)));
test('13 Craft development candidates are discoverable, immutable and use official icons',()=>{
 const catalog=read('catalog.json');for(const name of names){const c=catalog.candidatePlugins.find(x=>x.id===name);assert.ok(c,name+' absent');assert.equal(c.status,'release_candidate_installable');assert.match(c.version,/dev\./);assert.equal(c.logo,'assets/official-logo.png');for(const file of ['.agents/plugins/marketplace.json','marketplace.json','kimi-marketplace.json']){const e=read(file).plugins.find(x=>(x.name||x.id)===name);assert.ok(e,file+' missing '+name);assert.match(e.description||c.description,/development|candidate/i);if(e.source?.ref)assert.equal(e.source.ref,'v'+c.version);}}
});
test('standalone candidate marketplace contains all 13 pinned plugins without replacing the main marketplace identity',()=>{
 const candidate=read('candidate-marketplace/.agents/plugins/marketplace.json');assert.equal(candidate.name,'full-aigc-craft-candidates');assert.notEqual(candidate.name,read('.agents/plugins/marketplace.json').name);assert.equal(candidate.plugins.length,13);
 for(const name of names){const c=candidate.plugins.find(e=>e.name===name);const main=read('.agents/plugins/marketplace.json').plugins.find(e=>e.name===name);assert.deepEqual(c,main);}
});
