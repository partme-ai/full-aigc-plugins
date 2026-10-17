import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';
const names='cadcraft designcraft effectcraft photocraft figcraft filmcraft lightcraft printcraft vectorcraft deckcraft soundcraft gridcraft wordcraft'.split(' ');
const read=p=>JSON.parse(fs.readFileSync(new URL('../'+p,import.meta.url)));
test('13 Craft development candidates are discoverable, immutable and use official icons',()=>{
 const catalog=read('catalog.json');for(const name of names){const c=catalog.candidatePlugins.find(x=>x.id===name);assert.ok(c,name+' absent');assert.equal(c.status,'release_candidate_installable');assert.match(c.version,/dev\./);assert.equal(c.logo,'assets/official-logo.png');for(const file of ['.agents/plugins/marketplace.json','marketplace.json','kimi-marketplace.json']){const e=read(file).plugins.find(x=>(x.name||x.id)===name);assert.ok(e,file+' missing '+name);assert.match(e.description||c.description,/development|candidate/i);if(e.source?.ref)assert.equal(e.source.ref,'v'+c.version);}}
});
test('standalone candidate marketplace contains all 13 pinned plugins without replacing the main marketplace identity',()=>{
 const candidate=read('candidate-marketplace/.agents/plugins/marketplace.json');assert.equal(candidate.name,'full-aigc-craft-candidates');assert.notEqual(candidate.name,read('.agents/plugins/marketplace.json').name);assert.equal(candidate.plugins.length,13);
 for(const name of names){const c=candidate.plugins.find(e=>e.name===name);const main=read('.agents/plugins/marketplace.json').plugins.find(e=>e.name===name);const repo=read('catalog.json').candidatePlugins.find(p=>p.id===name);assert.deepEqual(c,{...main,source:main.source.source==='local'?{source:'url',url:'https://github.com/'+repo.repository+'.git',ref:'v'+repo.version}:main.source});}
});
test('Craft host ZIP listings bind complete release archives and exact digests',()=>{
 const releases=read('docs/craft-marketplace-candidate-releases.json');
 for(const prefix of ['', 'candidate-marketplace/'])for(const name of names){
  const row=releases.find(r=>r.plugin===name),entry=read(prefix+'marketplace.json').plugins.find(p=>p.name===name);
  if(row.maximumZipEntryBytes>50*1024*1024){assert.equal(entry.source.source,'github');assert.equal(entry.source.ref,'v'+row.version);continue;}
  assert.equal(entry.source.source,'url');assert.equal(entry.source.type,'zip');assert.equal(entry.source.sha256,row.archiveSha256);assert.equal(entry.source.path,name+'-plugin');assert.equal(entry.source.url,row.releaseUrl.replace('/tag/','/download/')+'/'+row.archive);
 }
});

test('Codex Craft entries resolve package icons before installation',()=>{
 for(const name of names){
  const entry=read('.agents/plugins/marketplace.json').plugins.find(p=>p.name===name);
  assert.equal(entry.source.source,'local',name+' cannot expose local logo from a Git fallback listing');
  const manifest=read(entry.source.path+'/plugin.json');
  assert.equal(manifest.name,name);assert.equal(manifest.version,entry.version);
  for(const field of ['logo','composerIcon']){const icon=manifest.extensions['com.openai'].interface[field];assert.ok(icon?.startsWith('./'));assert.ok(fs.existsSync(new URL('../'+entry.source.path+'/'+icon,import.meta.url)));}
 }
});
