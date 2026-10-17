import {mkdirSync,writeFileSync,readFileSync} from 'node:fs';
import {join} from 'node:path';
/** 仅用于协调器隔离单元测试；不能作为实际原生探测证据。 */
export function runtimeFixture(skill:string,identity:string){
 mkdirSync(join(skill,'references'),{recursive:true});
 writeFileSync(join(skill,'references/command-coverage.json'),JSON.stringify({runtimeSha256:identity,commands:[{id:'fixture.command',params:'{}'}]}));
 const tools=JSON.parse(readFileSync(new URL('../runtime/vectorcraft-headless-capabilities.json',import.meta.url),'utf8')).tools;
 return async()=>({schema:'vectorcraft-runtime-probe/v1',binarySha256:identity,version:'fixture',mode:'headless',commands:[{id:'fixture.command',params:'{}'}],tools:Object.entries(tools).map(([name,inputSchema])=>({name,inputSchema}))});
}
