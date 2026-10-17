// Web引擎返回字节；文件路径只由宿主工作区写入器处理。
export async function exportWithHostPath(params, call, save) {
 if (params.name !== 'export' || typeof params.arguments?.path !== 'string') return call(params);
 const {path, ...args} = params.arguments;
 const extension = /\.([^./\\]+)$/.exec(path)?.[1]?.toLowerCase();
 const format = args.format || (extension === 'jpeg' ? 'jpg' : extension);
 if (!format) throw Error('Export format is required when the destination has no extension');
 const result = await call({...params,arguments:{...args,format}});
 if (result.isError) return result;
 const outputs = [];
 for (const item of result.content || []) {
  if (item.type !== 'text') continue;
  let value;
  try { value=JSON.parse(item.text); } catch { continue; }
  if (typeof value.dataBase64 === 'string') outputs.push(value);
 }
 if (outputs.length !== 1) throw Error('Expected one byte export; select one artboard or export without a destination path');
 const {dataBase64,...metadata} = outputs[0];
 if (dataBase64.length > 180 * 1024 * 1024) throw Error('Export exceeds 128 MiB');
 const bytes = Buffer.from(dataBase64,'base64');
 if (bytes.length > 128 * 1024 * 1024) throw Error('Export exceeds 128 MiB');
 const saved = await save(path,bytes);
 return {...result,content:[{type:'text',text:JSON.stringify({...metadata,path:saved,bytes:bytes.length})}]};
}
