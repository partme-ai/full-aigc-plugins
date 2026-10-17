/** 严格 JSON：重复键与有限数字在任何信封层级使用相同规则。 */
export function strictJson(text: string): any {
  if (typeof text !== 'string' || text.length > 8 * 1024 * 1024) throw new Error('invalid_json_size');
  let position=0;
  const space=()=>{while (/\s/.test(text[position] ?? '') && position<text.length) {
    if (!' \t\r\n'.includes(text[position])) throw new Error('invalid_json_whitespace');
    position++;
  }};
  const string=()=>{
    const expression=/"(?:[^"\\\u0000-\u001f]|\\(?:["\\/bfnrt]|u[0-9a-fA-F]{4}))*"/y;
    expression.lastIndex=position;
    const match=expression.exec(text);
    if(!match) throw new Error('invalid_json_string');
    position=expression.lastIndex;return JSON.parse(match[0]);
  };
  const value=(depth=0):any=>{
    if(depth>64) throw new Error('invalid_json_depth');
    space();const first=text[position];
    if(first==='"') return string();
    if(first==='{' || first==='[') {
      const object=first==='{'?{}:[];const keys=new Set();const end=first==='{'?'}':']';
      position++;space();if(text[position]===end){position++;return object;}
      while(position<text.length) {
        let key:string|undefined;
        if(first==='{') {
          space();key=string();if(keys.has(key)) throw new Error('duplicate_json_key');keys.add(key);
          space();if(text[position++]!==':') throw new Error('invalid_json_separator');
        }
        const child=value(depth+1);
        if(first==='{') Object.defineProperty(object,key!,{value:child,enumerable:true,writable:true,configurable:true});
        else (object as any[]).push(child);
        space();if(text[position]===end){position++;return object;}
        if(text[position++]!==',') throw new Error('invalid_json_separator');
      }
      throw new Error('invalid_json_unclosed');
    }
    for(const [literal,decoded] of [['true',true],['false',false],['null',null]] as const) {
      if(text.startsWith(literal,position)){position+=literal.length;return decoded;}
    }
    const match=/^-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?/.exec(text.slice(position));
    if(!match) throw new Error('invalid_json_value');
    position+=match[0].length;const number=Number(match[0]);
    if(!Number.isFinite(number)) throw new Error('nonfinite_json_value');
    return number;
  };
  const result=value();space();if(position!==text.length) throw new Error('invalid_json_trailing');return result;
}

/** 排序对象键用于内容指纹；不接受不可序列化或非有限数值。 */
export function canonical(value:any):string {
  if(typeof value==='number'&&!Number.isFinite(value)) throw new Error('nonfinite_json_value');
  if(value===null||typeof value!=='object') {
    const text=JSON.stringify(value);if(text===undefined) throw new Error('invalid_json_value');return text;
  }
  if(Array.isArray(value)) return '['+value.map(canonical).join(',')+']';
  return '{'+Object.keys(value).sort().map(k=>JSON.stringify(k)+':'+canonical(value[k])).join(',')+'}';
}
