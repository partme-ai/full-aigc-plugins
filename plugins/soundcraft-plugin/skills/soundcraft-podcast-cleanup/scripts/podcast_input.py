"""将已核实的单片段边缘整理需求转换为 Craft 配方；不执行编辑。"""
import argparse
import copy
import json
import math
from pathlib import Path

FIELDS={'track','startSeconds','endSeconds','fadeInSeconds','fadeOutSeconds','gainDb','output'}

def build_recipe(data,template):
    """保留模板，按实际轨道和绝对会话时间生成参数。"""
    if not isinstance(data,dict) or set(data)!=FIELDS:
        raise ValueError('Provide exactly: '+', '.join(sorted(FIELDS)))
    track=data['track']
    if not isinstance(track,str) or not track.strip() or any(ord(c)<32 for c in track):
        raise ValueError('track must be a nonblank actual track name')
    for key in FIELDS-{'track','output'}:
        value=data[key]
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value):
            raise ValueError(key+' must be a finite number')
    start,end=data['startSeconds'],data['endSeconds'];fade_in,fade_out=data['fadeInSeconds'],data['fadeOutSeconds']
    if start<0 or end<=start or fade_in<0 or fade_out<0 or fade_in+fade_out>end-start:
        raise ValueError('Invalid range or overlapping edge fades')
    if not -60<=data['gainDb']<=12:
        raise ValueError('gainDb must be between -60 and 12; verify peaks separately')
    output=data['output']
    if not isinstance(output,str):raise ValueError('output must be relative WAV path')
    output=output.replace('\\','/')
    if (any(ord(c)<32 for c in output) or ':' in output or output.startswith('/') or
        any(p in ('','.','..') for p in output.split('/')) or not output.lower().endswith('.wav')):
        raise ValueError('output must be a safe relative WAV path')
    result=copy.deepcopy(template);result.pop('limitedTechnicalValidation',None);steps=[]
    for step in result['steps']:
        command=step['command'];params=step['params']
        if command=='edit.select':params.update(tracks=[track],start={'seconds':start},end={'seconds':end})
        elif command=='clip.gain':params['db']=data['gainDb']
        elif command=='edit.fades_create':
            # 模板两行分别对应头部与尾部；只替换已知边缘，不新增处理算法。
            leading=params['start']['seconds']==0
            length=fade_in if leading else fade_out
            if length==0:continue
            params.update(tracks=[track],start={'seconds':start if leading else end-length},end={'seconds':start+length if leading else end})
        elif command=='file.bounce_mix':params.update(path=output,start={'seconds':start},end={'seconds':end})
        step['purpose']={'session.inspect':'核对实际会话和片段','edit.select':'选择已核实的单片段范围','clip.gain':'设置选中片段增益','edit.fades_create':'按实际边界创建边缘淡变','engine.plugins':'仅查询效果目录，不执行处理','file.bounce_mix':'导出所选时间范围审核混音'}[command]
        steps.append(step)
    result['steps']=steps
    result['inputScope']='One independently verified clip on one named track. Gain applies to selected clips; no trim, noise reduction, EQ or loudness normalization is performed.'
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();template=Path(__file__).resolve().parents[1]/'references/craft-steps.json'
    recipe=build_recipe(json.loads(args.input.read_text(encoding='utf-8')),json.loads(template.read_text(encoding='utf-8')))
    with args.output.open('x',encoding='utf-8') as stream:json.dump(recipe,stream,ensure_ascii=True,indent=2);stream.write('\n')
if __name__=='__main__':main()
