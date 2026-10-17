"""用原生FigCraft CLI分批执行步骤，仅绑定真实返回值，不实现图形业务。"""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def resolve(value,bindings):
    if isinstance(value,dict):
        if set(value)=={'$ref'}:
            parts=value['$ref'].split('.')
            if not parts or parts[0] not in bindings:raise ValueError('Unresolved return binding: '+value['$ref'])
            found=bindings[parts[0]]
            for key in parts[1:]:
                if not isinstance(found,dict) or key not in found:raise ValueError('Missing returned field: '+value['$ref'])
                found=found[key]
            return found
        return {k:resolve(v,bindings) for k,v in value.items()}
    if isinstance(value,list):return [resolve(v,bindings) for v in value]
    return value


def execute_recipe(recipe,run,work,output,input_file=None):
    work=Path(work);output=Path(output).resolve()
    if output.exists():raise ValueError('Output already exists: '+str(output))
    if input_file is not None and not Path(input_file).is_file():raise ValueError('Input file missing')
    output.parent.mkdir(parents=True,exist_ok=True)
    bindings={};receipts=[];pending=[];current=str(Path(input_file).resolve()) if input_file else None
    with tempfile.TemporaryDirectory(prefix='figcraft-steps-',dir=work) as tmp:
        tmp=Path(tmp)
        def flush(capture=None):
            nonlocal current
            if not pending:return
            index=len(receipts);script=tmp/f'steps-{index}.json';saved=tmp/f'phase-{index}.figcraft'
            script.write_text(json.dumps(pending,ensure_ascii=False),encoding='utf-8')
            args=['run',str(script)]+(['--in',current] if current else [])+['--out',str(saved)]
            rows=[json.loads(line) for line in run(*args).splitlines() if line.strip()]
            if len(rows)!=len(pending) or any(row.get('ok') is not True for row in rows):raise ValueError('Native step response failed')
            if capture:
                if capture in bindings:raise ValueError('Duplicate capture: '+capture)
                bindings[capture]=rows[-1]['result']
            receipts.extend(rows);current=str(saved);pending.clear()
        for step in recipe['steps']:
            if input_file and step.get('newDocumentOnly'):continue
            pending.append({'command':step['command'],'params':resolve(step['params'],bindings)})
            if step.get('capture'):flush(step['capture'])
        flush()
        if current is None:raise ValueError('Recipe executed no steps')
        # Exclusive create refuses overwrite even if a target appears while native commands run.
        with open(output,'xb') as dest,open(current,'rb') as src:shutil.copyfileobj(src,dest)
    return {'bindings':bindings,'steps':receipts,'output':str(output)}


def main():
    p=argparse.ArgumentParser();p.add_argument('--recipes',type=Path,required=True);p.add_argument('--scene',required=True);p.add_argument('--cli',default='figcraft-cli');p.add_argument('--output',type=Path,required=True);p.add_argument('--input',type=Path);a=p.parse_args()
    data=json.loads(a.recipes.read_text(encoding='utf-8'));recipe=next(r for r in data['recipes'] if r['id']==a.scene)
    def run(*args):
        r=subprocess.run([a.cli,*args],capture_output=True,text=True,encoding='utf-8',timeout=120)
        if r.returncode:raise RuntimeError(r.stderr or r.stdout)
        return r.stdout
    result=execute_recipe(recipe,run,Path.cwd(),a.output,a.input)
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
