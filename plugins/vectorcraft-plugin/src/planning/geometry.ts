import { canonical } from '../strict_json.ts';

type Point=[number,number];
type Anchor={p:Point,in?:Point,out?:Point,kind?:string};
type Subpath={closed:boolean,anchors:Anchor[]};
type Stroke={width:number,paint:Record<string,unknown>};
type PathExpectation={objectId?:number,binding?:string,artboardId:number,subpaths:Subpath[],strokes:Stroke[]};
export type GeometryContract={schema:'vectorcraft-geometry-contract/v1',units:'Pixels'|'Points',coordinateSpace:'document'|'artboard-local',tolerance:number,
  artboards:{id:number,rect:[number,number,number,number]}[],paths:PathExpectation[]};
const object=(v:any)=>v!==null&&typeof v==='object'&&!Array.isArray(v);
const keys=(v:any,required:string[],optional:string[]=[])=>object(v)&&required.every(k=>Object.hasOwn(v,k))&&Object.keys(v).every(k=>[...required,...optional].includes(k));
const id=(v:any)=>Number.isSafeInteger(v)&&v>0;
const point=(v:any)=>Array.isArray(v)&&v.length===2&&v.every(n=>typeof n==='number'&&Number.isFinite(n));
const anchor=(v:any)=>keys(v,['p'],['in','out','kind'])&&point(v.p)&&['in','out'].every(k=>v[k]===undefined||point(v[k]))&&(v.kind===undefined||typeof v.kind==='string'&&!!v.kind);
const stroke=(v:any)=>keys(v,['width','paint'])&&typeof v.width==='number'&&Number.isFinite(v.width)&&v.width>=0&&object(v.paint);

/** 校验显式原生几何合同；预览像素空间及缺失单位不能作为路径事实。 */
export function validateGeometryContract(value:any):asserts value is GeometryContract {
  if(!keys(value,['schema','units','coordinateSpace','tolerance','artboards','paths'])||value.schema!=='vectorcraft-geometry-contract/v1'
    ||!['Pixels','Points'].includes(value.units)||!['document','artboard-local'].includes(value.coordinateSpace)
    ||typeof value.tolerance!=='number'||!Number.isFinite(value.tolerance)||value.tolerance<0||value.tolerance>0.001
    ||!Array.isArray(value.artboards)||!value.artboards.length||value.artboards.length>4096
    ||value.artboards.some((v:any)=>!keys(v,['id','rect'])||!id(v.id)||!Array.isArray(v.rect)||v.rect.length!==4||v.rect.some((n:any)=>typeof n!=='number'||!Number.isFinite(n))||v.rect[2]<=v.rect[0]||v.rect[3]<=v.rect[1])
    ||new Set(value.artboards.map((v:any)=>v.id)).size!==value.artboards.length
    ||!Array.isArray(value.paths)||!value.paths.length||value.paths.length>4096)throw new Error('invalid_geometry_contract');
  const targets=new Set<string>();let anchors=0;
  for(const path of value.paths){
    if(!keys(path,['artboardId','subpaths','strokes'],['objectId','binding'])||('objectId' in path)===('binding' in path)
      ||path.objectId!==undefined&&!id(path.objectId)||path.binding!==undefined&&(typeof path.binding!=='string'||!/^\w[\w-]*(?:\.(?:[A-Za-z][\w-]*|\d+))*$/.test(path.binding)||path.binding.split('.').some((v:string)=>['__proto__','constructor','prototype'].includes(v)))
      ||!value.artboards.some((v:any)=>v.id===path.artboardId)||!Array.isArray(path.subpaths)||!path.subpaths.length||path.subpaths.length>4096
      ||!Array.isArray(path.strokes)||path.strokes.length>64||path.strokes.some((v:any)=>!stroke(v)))throw new Error('invalid_geometry_contract');
    const target=canonical([path.objectId??null,path.binding??null]);if(targets.has(target))throw new Error('invalid_geometry_contract');targets.add(target);
    for(const sub of path.subpaths){
      if(!keys(sub,['closed','anchors'])||typeof sub.closed!=='boolean'||!Array.isArray(sub.anchors)||!sub.anchors.length||sub.anchors.some((v:any)=>!anchor(v)))throw new Error('invalid_geometry_contract');
      anchors+=sub.anchors.length;if(anchors>100000)throw new Error('invalid_geometry_contract');
    }
  }
}

/** 从绑定原生对象核对单位、坐标、控制点、闭合性和描边；不读取预览像素。 */
export function verifyGeometry(document:any,bindings:any,contract:GeometryContract):any {
  validateGeometryContract(contract);
  const issues:any[]=[],checked:number[]=[],objects=new Map<number,any[]>(),boards=new Map<number,any[]>(),contexts=new Map<number,boolean>();
  const near=(a:any,b:number)=>typeof a==='number'&&Number.isFinite(a)&&Math.abs(a-b)<=contract.tolerance;
  const walk=(v:any,supported=true)=>{
    if(!object(v)&&!Array.isArray(v))return;
    if(object(v)&&id(v.id)&&object(v.kind)){
      supported=supported&&Object.keys(v).every(k=>['id','kind','appearance','name'].includes(k))
        &&Object.keys(v.kind).every(k=>['path','children','text','runs','image','symbol','type','color','printable','template'].includes(k));
      objects.set(v.id,[...(objects.get(v.id)??[]),v]);contexts.set(v.id,supported);
    }
    for(const child of Object.values(v))walk(child,supported);
  };
  walk(document?.layers);
  if(Array.isArray(document?.artboards))for(const board of document.artboards)if(id(board?.id))boards.set(board.id,[...(boards.get(board.id)??[]),board]);
  const problem=(objectId:number|null,reason:string,detail:any={})=>issues.push({objectId,reason,...detail});
  const resolve=(path:PathExpectation):number|null=>{
    if(path.objectId!==undefined)return path.objectId;
    let value=bindings;
    for(const part of path.binding!.split('.')){if(!object(value)&&!Array.isArray(value)||!Object.hasOwn(value,part))return null;value=value[part];}
    return id(value)?value:null;
  };
  const resolved=new Set<number>();
  for(const expected of contract.paths){
    const objectId=resolve(expected);if(objectId===null){problem(null,'unresolved_native_binding',{binding:expected.binding});continue;}
    if(resolved.has(objectId)){problem(objectId,'duplicate_native_target');continue;}resolved.add(objectId);checked.push(objectId);
    if(document?.units!==contract.units)problem(objectId,'units_mismatch',{expected:contract.units,observed:document?.units??null});
    const expectedBoard=contract.artboards.find(v=>v.id===expected.artboardId)!;
    const actualBoards=boards.get(expected.artboardId)??[];
    if(actualBoards.length!==1){problem(objectId,'artboard_identity_mismatch',{artboardId:expected.artboardId});continue;}
    const rect=actualBoards[0].rect;
    if(!rect||!['x0','y0','x1','y1'].every((k,i)=>near(rect[k],expectedBoard.rect[i]))){problem(objectId,'artboard_coordinates_mismatch',{artboardId:expected.artboardId});continue;}
    const matches=objects.get(objectId)??[];
    if(matches.length!==1||!object(matches[0]?.kind?.path)){problem(objectId,'native_path_identity_mismatch');continue;}
    const native=matches[0],subpaths=native.kind.path.subpaths;
    if(contexts.get(objectId)!==true){problem(objectId,'unsupported_native_geometry_context');continue;}
    if(!Array.isArray(subpaths)||subpaths.length!==expected.subpaths.length){problem(objectId,'subpath_count_mismatch');continue;}
    const offset=contract.coordinateSpace==='artboard-local'?[rect.x0,rect.y0]:[0,0];
    for(const [i,sub] of expected.subpaths.entries()){
      const actual=subpaths[i];
      if(actual?.closed!==sub.closed)problem(objectId,'path_closed_mismatch',{subpath:i});
      if(!Array.isArray(actual?.anchors)||actual.anchors.length!==sub.anchors.length){problem(objectId,'anchor_count_mismatch',{subpath:i});continue;}
      for(const [j,wanted] of sub.anchors.entries()){
        const observed=actual.anchors[j];if(!anchor(observed)){problem(objectId,'unsupported_native_anchor',{subpath:i,anchor:j});continue;}
        for(const k of ['p','in','out'] as const){
          const p=wanted[k],q=observed[k];
          if(p===undefined&&q===undefined)continue;
          if(!p||!q||!p.every((n,axis)=>near(q[axis],n+offset[axis])))problem(objectId,'path_control_point_mismatch',{subpath:i,anchor:j,field:k});
        }
        if(wanted.kind!==undefined&&wanted.kind!==observed.kind)problem(objectId,'anchor_kind_mismatch',{subpath:i,anchor:j});
      }
    }
    const items=native.appearance?.items;
    if(!Array.isArray(items)){problem(objectId,'native_strokes_unavailable');continue;}
    const strokes=items.filter((v:any)=>v?.kind==='stroke');
    if(strokes.length!==expected.strokes.length)problem(objectId,'stroke_count_mismatch');
    else for(const [i,wanted] of expected.strokes.entries())if(!near(strokes[i].width,wanted.width)||canonical(strokes[i].paint)!==canonical(wanted.paint))problem(objectId,'stroke_mismatch',{stroke:i});
  }
  return {schema:'vectorcraft-geometry-verification/v1',status:issues.length?'FAIL':'PASS',units:contract.units,coordinateSpace:contract.coordinateSpace,
    checkedObjectIds:checked,issues,scope:'explicit native JSON geometry only; no preview inference, native reopening or creative acceptance claim'};
}
