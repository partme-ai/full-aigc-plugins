import test from 'node:test';
import assert from 'node:assert/strict';
import {installCanvasCapture} from './runtime/canvas-capture.mjs';
test('capture keeps WebGL drawing buffers without changing 2d options',()=>{
 class Canvas {getContext(kind, options){return {kind,options,canvas:this};}}
 installCanvasCapture(Canvas);const c=new Canvas();
 for(const kind of ['webgl','webgl2','experimental-webgl']) {
  const options={alpha:false};const v=c.getContext(kind,options);
  assert.equal(v.canvas,c);assert.deepEqual(v.options,{alpha:false,preserveDrawingBuffer:true});
  assert.deepEqual(options,{alpha:false});
 }
 const options={willReadFrequently:true};assert.equal(c.getContext('2d',options).options,options);
});
