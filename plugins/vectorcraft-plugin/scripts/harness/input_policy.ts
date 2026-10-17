/** 保留字段表示凭据内容，必须由宿主秘密引用代替；不回显键名或值。 */
export function assertNoLiteralSecrets(value:unknown):void {
 const forbidden=new Set(['apikey','accesstoken','refreshtoken','clientsecret','password','privatekey','secretvalue','credentials']);
 const visit=(item:unknown,depth:number)=>{
  if(depth>64)throw new Error('invalid_input_depth');
  if(item===null||typeof item!=='object')return;
  for(const [key,child] of Object.entries(item)){
   if(forbidden.has(key.replace(/[_-]/g,'').toLowerCase()))throw new Error('literal_secret_forbidden');
   visit(child,depth+1);
  }
 };
 visit(value,0);
}

/** 素材登记只接受路径和摘要；附加命令、元数据指令均不得进入执行快照。 */
export function validateAssetRecords(plan:any):void {
 const assets=plan.assets===undefined?{}:plan.assets;
 if(!assets||typeof assets!=='object'||Array.isArray(assets))throw new Error('invalid_asset_record');
 for(const [name,asset] of Object.entries(assets) as [string,any][]){
  if(!/^[A-Za-z][A-Za-z0-9_-]{0,63}$/.test(name)||!asset||typeof asset!=='object'||Array.isArray(asset)
   ||Object.keys(asset).sort().join(',')!=='path,sha256'||typeof asset.path!=='string'||!asset.path
   ||typeof asset.sha256!=='string'||!/^[a-f0-9]{64}$/.test(asset.sha256))throw new Error('invalid_asset_record');
 }
}
