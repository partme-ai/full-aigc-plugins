import {createHash} from 'node:crypto';
import {lstatSync,readdirSync,readFileSync} from 'node:fs';
import {join,relative} from 'node:path';
const sha=(value:string|Buffer)=>createHash('sha256').update(value).digest('hex');

/** 与固定快照工具一致的整技能摘要，不读取目录链接或额外文件类型。 */
export function skillDigest(root:string):string {
  const files:string[]=[];
  const walk=(path:string)=>{
    if(lstatSync(path).isSymbolicLink())throw new Error('skill_snapshot_symlink');
    for(const name of readdirSync(path).sort()){
      const entry=join(path,name),stat=lstatSync(entry);
      if(stat.isSymbolicLink())throw new Error('skill_snapshot_symlink');
      if(stat.isDirectory())walk(entry);else if(stat.isFile())files.push(entry);else throw new Error('skill_snapshot_entry');
    }
  };
  walk(root);const hash=createHash('sha256');
  for(const file of files.sort((a,b)=>relative(root,a)<relative(root,b)?-1:1))hash.update(relative(root,file)+'\0'+sha(readFileSync(file))+'\n');
  return hash.digest('hex');
}
