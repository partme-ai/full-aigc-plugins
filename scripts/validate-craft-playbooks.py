#!/usr/bin/env python3
"""检查场景技能独立分发、真实命令引用和来源完整性；不将静态检查称为场景运行验收。"""
import argparse
import hashlib
import json
from pathlib import Path
import re


def validate_skill(skill, plugin_skill=None):
    errors=[]; count=0
    if not (skill/'SKILL.md').is_file():return ['missing SKILL.md'],0
    for file in skill.rglob('*.md'):
        text=file.read_text(encoding='utf-8')
        if file.name=='SKILL.md' and len(text.splitlines())>500:errors.append(str(file)+': too many lines')
        for target in re.findall(r'\]\(([^)]+)\)',text):
            if '://' in target or target.startswith('#'):continue
            path=(file.parent/target.split('#')[0]).resolve()
            if not path.is_relative_to(skill.resolve()) or not path.exists():errors.append(str(file)+': invalid local reference '+target)
    paths=list(skill.glob('references/craft-steps.json'))+list(skill.glob('references/recipes.json'))
    for path in paths:
        data=json.loads(path.read_text(encoding='utf-8'));recipes=data.get('recipes',[data]); count+=len(recipes)
        evidence=path.with_name('command-evidence.json' if path.name=='recipes.json' else 'craft-command-evidence.json')
        record=json.loads(evidence.read_text(encoding='utf-8'));commands=record['observedCommands']
        for recipe in recipes:
            if not recipe.get('id') or not recipe.get('steps'):errors.append(str(path)+': empty scene')
            if not (recipe.get('checks') or recipe.get('check')) or not (recipe.get('limits') or recipe.get('boundary')):errors.append(str(path)+': missing checks or boundary')
            for step in recipe['steps']:
                name=step['command'];args=step['params']
                if name not in commands:errors.append(str(path)+': unknown method '+name);continue
                if not isinstance(args,dict):errors.append(str(path)+': params not object '+name);continue
                schema=commands[name].get('input_schema')
                if schema:
                    missing=set(schema.get('required',[]))-args.keys()
                    unknown=set(args)-schema.get('properties',{}).keys()
                    if missing or (unknown and schema.get('additionalProperties') is False):errors.append(str(path)+': schema parameters mismatch '+name)
                elif commands[name].get('params') is None and args:
                    errors.append(str(path)+': parameter evidence absent '+name)
        src=path.with_name('sources.json' if path.name=='recipes.json' else 'workflow-sources.json')
        sources=json.loads(src.read_text(encoding='utf-8')).get('sources',[])
        if not sources:errors.append(str(path)+': no workflow source')
        for source in sources:
            if not re.fullmatch('[0-9a-f]{40}',source.get('commit','')) or not source.get('readFiles'):errors.append(str(src)+': incomplete source')
    if plugin_skill:
        source_files={str(p.relative_to(skill)):hashlib.sha256(p.read_bytes()).hexdigest() for p in skill.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
        destination={str(p.relative_to(plugin_skill)):hashlib.sha256(p.read_bytes()).hexdigest() for p in plugin_skill.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
        if source_files!=destination:errors.append(str(plugin_skill)+': source/plugin content mismatch')
    return errors,count


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--workspace',type=Path,default=Path(__file__).resolve().parents[2]);a=parser.parse_args()
    rows=[];errors=[]
    for app in 'cadcraft designcraft effectcraft photocraft figcraft filmcraft lightcraft printcraft vectorcraft deckcraft soundcraft gridcraft wordcraft'.split():
        source=a.workspace/'full-aigc-skills-repositories'/(app+'-skills')/'skills';count=0;skills=0
        for skill in source.iterdir():
            if not ((skill/'references/craft-steps.json').exists() or (skill/'references/recipes.json').exists()):continue
            e,c=validate_skill(skill,a.workspace/'full-aigc-plugins-repositories'/(app+'-plugin')/'skills'/skill.name)
            errors.extend(e);count+=c;skills+=1
        rows.append({'application':app,'mappedScenes':count,'skills':skills})
        if count==0:errors.append(app+': no mapped scene')
    print(json.dumps({'scope':'static source, command reference and plugin copy checks only','applications':rows,'mappedScenes':sum(r['mappedScenes'] for r in rows),'errors':errors},ensure_ascii=False,indent=2))
    return bool(errors)

if __name__=='__main__':raise SystemExit(main())
