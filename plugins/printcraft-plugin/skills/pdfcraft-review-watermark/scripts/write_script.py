"""将明确的文档槽位转成全新原生CLI脚本；不处理PDF业务。"""
import argparse
import json
from pathlib import Path


def compile_steps(recipe,preopen=()):
    paths=list(preopen)+recipe['sourceFiles']
    if not recipe['sourceFiles']:raise ValueError('No source PDF')
    out=[{'tool':'doc_open','args':{'path':path}} for path in paths]
    for step in recipe['steps']:
        args=dict(step['params'])
        for field in ['doc','other']:
            if field in args:
                slot=args[field]
                if type(slot) is not int or not 1<=slot<=len(recipe['sourceFiles']):raise ValueError('Unknown document slot')
                args[field]=slot+len(preopen)
        out.append({'tool':step['command'],'args':args})
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--recipe',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    with a.output.open('x',encoding='utf-8') as out:json.dump(compile_steps(json.loads(a.recipe.read_text(encoding='utf-8'))),out,ensure_ascii=False,indent=2)
