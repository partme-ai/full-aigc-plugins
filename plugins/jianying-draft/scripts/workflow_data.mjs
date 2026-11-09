import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {AdapterError} from './runtime_adapter.mjs';

export const fail = (code, message) => { throw new AdapterError(code, message); };
export const sha256 = value => crypto.createHash('sha256').update(value).digest('hex');
export const canonical = value => JSON.stringify(normalize(value));
function normalize(value) {
  if (Array.isArray(value)) return value.map(normalize);
  if (value && typeof value === 'object') return Object.fromEntries(Object.keys(value).sort().map(k=>[k,normalize(value[k])]));
  return value;
}

/** 严格 JSON：重复键（含转义等价键）、过深嵌套均拒绝。 */
export function parseStrictJson(text) {
  const stack=[];
  const tokens=text.match(/"(?:\\.|[^"\\])*"|[{}\[\]:,]|-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?|true|false|null/g)??[];
  for (const token of tokens) {
    const top=stack.at(-1);
    if (token==='{' || token==='[') {
      if(stack.length>=64) fail('catalog_resource_limit','JSON nesting exceeds 64');
      stack.push({object:token==='{',key:token==='{',seen:new Set()});
    } else if(token==='}' || token===']') stack.pop();
    else if(top?.object && token===',') top.key=true;
    else if(top?.object && token===':') top.key=false;
    else if(top?.object && top.key && token.startsWith('"')) {
      let key;
      try {key=JSON.parse(token);} catch {fail('catalog_schema_invalid','invalid JSON string');}
      if(top.seen.has(key)) fail('catalog_duplicate_key',`duplicate key: ${key}`);
      top.seen.add(key);
    }
  }
  try {
    return JSON.parse(text,(_key,value)=>{
      if(typeof value==='number' && !Number.isFinite(value)) fail('catalog_schema_invalid','non-finite JSON number');
      return value;
    });
  } catch(error) {
    if(error instanceof AdapterError) throw error;
    fail('catalog_schema_invalid','invalid JSON');
  }
}

/** 只解释本项目已使用的 JSON Schema 子集，未知关键字不静默忽略。 */
export function validateSchema(value, rule, root=rule, location='$') {
  const known=new Set(['$schema','$id','$defs','$ref','type','const','enum','properties','required',
    'additionalProperties','items','minItems','uniqueItems','minLength','pattern']);
  for(const key of Object.keys(rule)) if(!known.has(key)) fail('catalog_schema_invalid',`unsupported schema keyword ${key}`);
  if(rule.$ref) {
    const name=rule.$ref.slice(8);
    if(!rule.$ref.startsWith('#/$defs/') || !Object.hasOwn(root.$defs??{},name)) fail('catalog_schema_invalid','invalid schema reference');
    return validateSchema(value,root.$defs[name],root,location);
  }
  const invalid=message=>fail('catalog_schema_invalid',`${location}: ${message}`);
  if(Object.hasOwn(rule,'const') && value!==rule.const) invalid('const mismatch');
  if(rule.enum && !rule.enum.includes(value)) invalid('enum mismatch');
  const type=Array.isArray(value)?'array':value===null?'null':typeof value;
  if(rule.type && type!==rule.type) invalid(`expected ${rule.type}`);
  if(rule.type==='object') {
    const props=rule.properties??{};
    for(const key of rule.required??[]) if(!Object.hasOwn(value,key)) invalid(`missing ${key}`);
    for(const [key,item] of Object.entries(value)) {
      if(Object.hasOwn(props,key)) validateSchema(item,props[key],root,`${location}.${key}`);
      else if(rule.additionalProperties===false) invalid(`unknown ${key}`);
      else if(typeof rule.additionalProperties==='object') validateSchema(item,rule.additionalProperties,root,`${location}.${key}`);
    }
  }
  if(rule.type==='array') {
    if(value.length<(rule.minItems??0)) invalid('too few items');
    if(rule.uniqueItems && new Set(value.map(canonical)).size!==value.length) invalid('duplicate items');
    value.forEach((item,index)=>validateSchema(item,rule.items??{},root,`${location}[${index}]`));
  }
  if(rule.type==='string') {
    if(value.trim().length<(rule.minLength??0)) invalid('empty string');
    if(rule.pattern && !new RegExp(rule.pattern).test(value)) invalid('pattern mismatch');
  }
}

/** 检查根内普通文件，不跟随引用中的符号链接，不接受跨平台绝对路径。 */
export function safeFile(root, relative, limit) {
  if(typeof relative!=='string' || /[\\:\0]/.test(relative) || relative.split('/').some(p=>!p || p==='.' || p==='..'))
    fail('catalog_path_invalid',`invalid resource path: ${relative}`);
  let file=root;
  try {
    if(fs.lstatSync(root).isSymbolicLink()) fail('catalog_path_invalid','symlink root');
    for(const part of relative.split('/')) {
      file=path.join(file,part);
      if(fs.lstatSync(file).isSymbolicLink()) fail('catalog_path_invalid',`symlink: ${relative}`);
    }
    const stat=fs.statSync(file);
    if(!stat.isFile()) fail('catalog_path_invalid',`not a regular file: ${relative}`);
    if(stat.size>limit) fail('catalog_resource_limit',`${relative}: ${stat.size} exceeds ${limit}`);
    return file;
  } catch(error) {
    if(error instanceof AdapterError) throw error;
    fail('catalog_path_invalid',`missing or unreadable resource: ${relative}`);
  }
}

/** 有界读取：文件增长不能绕过预检大小限制。 */
export function readBounded(file,limit) {
  const fd=fs.openSync(file,fs.constants.O_RDONLY|fs.constants.O_NOFOLLOW);
  try {
    const stat=fs.fstatSync(fd);
    if(!stat.isFile()) fail('catalog_path_invalid','not a regular file');
    if(stat.size>limit) fail('catalog_resource_limit',`${file}: exceeds ${limit}`);
    const buffer=Buffer.alloc(Math.min(stat.size+1,limit+1)); let count=0;
    while(count<buffer.length) {
      const read=fs.readSync(fd,buffer,count,buffer.length-count,null);
      if(!read) break;
      count+=read;
    }
    if(count>stat.size) fail('catalog_resource_limit','resource changed during read');
    return buffer.subarray(0,count);
  } finally {fs.closeSync(fd);}
}

/** 与技能发布摘要算法一致；限制总大小、文件数和目录深度。 */
export function boundedSkillDigest(root, parsedResources=new Map()) {
  const files=[]; let total=0; let entries=0;
  function walk(dir,depth=0) {
    if(depth>24) fail('catalog_resource_limit','skill depth exceeds 24');
    for(const entry of fs.readdirSync(dir,{withFileTypes:true})) {
      if(++entries>20000) fail('catalog_resource_limit','skill entries exceeds 20000');
      const file=path.join(dir,entry.name);
      if(entry.isSymbolicLink()) fail('catalog_path_invalid','skill symlink forbidden');
      if(entry.isDirectory()) walk(file,depth+1);
      else if(entry.isFile()) files.push(file);
      else fail('catalog_path_invalid','special skill file forbidden');
    }
  }
  if(fs.lstatSync(root).isSymbolicLink()) fail('catalog_path_invalid','skill root symlink forbidden');
  walk(root);
  const hash=crypto.createHash('sha256');
  for(const file of files.sort()) {
    const relative=path.relative(root,file).split(path.sep).join('/');
    // 已解析资源使用同一字节快照，避免哈希另一版文件却信任先前解析内容。
    const bytes=parsedResources.get(relative)??readBounded(file,64*1024*1024-total);
    total+=bytes.length;
    if(total>64*1024*1024) fail('catalog_resource_limit','skill total exceeds 64 MiB');
    hash.update(relative+'\0'+sha256(bytes)+'\n');
  }
  return hash.digest('hex');
}
