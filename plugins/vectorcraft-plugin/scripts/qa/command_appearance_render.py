#!/usr/bin/env python3
"""外观两轮图像核验：改变、保全与只测量契约，原生探针另行断言。"""
import argparse,hashlib,importlib.util,json
from pathlib import Path
COMMANDS=['appearance.'+n for n in ('addFill','addStroke','clear','reduceToBasic','setItem','removeItem','addEffect','duplicateItem','moveItem','copyFrom','setActiveItem','showAllHidden','targetContents','transfer','setNewArtBasic','newArt')]
CHANGED={'appearance.setItem','appearance.removeItem','appearance.addEffect','appearance.transfer'}
MEASURED={'appearance.addFill','appearance.addStroke','appearance.reduceToBasic','appearance.duplicateItem','appearance.moveItem','appearance.copyFrom'}
def base():
 s=importlib.util.spec_from_file_location('appearance_render_base',Path(__file__).with_name('command_layer_render.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.COMMANDS=COMMANDS;m.CHANGED=CHANGED;m.MEASURED=MEASURED;return m
def expectation(command,kind):return base().expectation(command,kind)
def validate_count(count,total,relation):return base().validate_count(count,total,relation)
def qualify(root,proof):
 result=base().qualify(root,proof);result['schema']='vectorcraft-command-appearance-render/v1';result['checkerSha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();result['scope']='Actual48 canvas/PNG/window comparisons for16 appearance commands;explicit preservation/change/measurement contracts;active-item and new-art edits are independently probed and restored by native saved-checkpoint reopen;not preference restart,creative or full V1';return result
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('root',type=Path);args=parser.parse_args();result=qualify(args.root,args.root/'proof.json');(args.root/'render-changes.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'result':'PASS','commands':len(result['cases']),'comparisons':48}))
