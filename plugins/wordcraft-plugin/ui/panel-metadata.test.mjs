import test from 'node:test';
import assert from 'node:assert/strict';
import {withPanelMetadata} from './panel-metadata.mjs';
test('host capabilities are applied to listed and read HTML resources only',()=>{
 const extra={'test/csp':{wasmUnsafeEval:true}};
 const input={contents:[{uri:'ui://wordcraft/panel.html',mimeType:'text/html;profile=mcp-app',_meta:{ui:{prefersBorder:false}},text:'editor'},{uri:'ui://wordcraft/assets.json',mimeType:'application/json',text:'{}'}]};
 const out=withPanelMetadata(input,extra);
 assert.deepEqual(out.contents[0]._meta, {...input.contents[0]._meta,...extra});
 assert.equal(out.contents[1],input.contents[1]);
 assert.equal(input.contents[0]._meta['test/csp'],undefined);
 assert.deepEqual(withPanelMetadata({resources:input.contents},extra).resources,out.contents);
});
