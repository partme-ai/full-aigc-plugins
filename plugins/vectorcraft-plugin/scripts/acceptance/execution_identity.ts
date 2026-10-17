import { createHash } from 'node:crypto';
import { readdirSync, readFileSync, lstatSync } from 'node:fs';
import { dirname,join,relative } from 'node:path';
import { fileURLToPath } from 'node:url';
const root=join(dirname(fileURLToPath(import.meta.url)),'../..');
/** 在运行开始采样验收代码，不允许归档时绑定后续源码。 */
export function executionIdentity():Record<string,string>{
 const result:Record<string,string>={};
 const walk=(directory:string)=>{for(const name of readdirSync(directory).sort()){
  const path=join(directory,name),stat=lstatSync(path);
  if(stat.isSymbolicLink())throw new Error('execution_identity_symlink');
  if(stat.isDirectory())walk(path);
  else if(/\.(ts|py|json)$/.test(name))result[relative(root,path)]=createHash('sha256').update(readFileSync(path)).digest('hex');
 }};
 for(const folder of ['src','scripts/acceptance','schemas'])walk(join(root,folder));
 return result;
}
