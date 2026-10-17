// 在宿主适配层支持新版目录检索；原编辑引擎与其 enabled 状态保持为事实源。
const listings = new Set(['command_list', 'list_commands']);
const lower = value => typeof value === 'string' ? value.toLowerCase() : '';

export function extendDiscoveryTool(tool) {
 if (!listings.has(tool.name)) return tool;
 return {...tool, inputSchema:{...tool.inputSchema, properties:{...tool.inputSchema.properties,
  query:{type:'string',description:'Alias of filter; match command id, label or menu.'},
  menu:{type:'string',description:'Case-insensitive menu path substring; levels joined by > with spaces.'},
  brief:{type:'boolean',description:'Omit params from listings. Query a specific id without brief to read its parameters.'},
 }}};
}

export async function callDiscoveryTool(params, call) {
 if (!listings.has(params.name)) return call(params);
 const {query, menu, brief, ...args} = params.arguments || {};
 const needle = lower(args.filter) || lower(query);
 if (needle) args.filter = needle;
 const result = await call({...params, arguments:args});
 if (result.isError) return result;
 const index = result.content?.findIndex(item=>item.type==='text');
 if (index === undefined || index < 0) throw Error('Command catalog has no text result');
 const rows = JSON.parse(result.content[index].text);
 if (!Array.isArray(rows)) throw Error('Command catalog must be an array');
 const filtered = rows.filter(row=>{
  const path = Array.isArray(row.menu) ? row.menu.join(' > ') : '';
  if (menu && !lower(path).includes(lower(menu))) return false;
  return !needle || [row.id,row.label,Array.isArray(row.menu)?row.menu.join(' '):''].some(value=>lower(value).includes(needle));
 }).map(row=>{
  if (brief !== true) return row;
  const {params:omitted, ...summary} = row;
  return summary;
 });
 return {...result,content:result.content.map((item,i)=>i===index ? {...item,text:JSON.stringify(filtered)} : item)};
}
