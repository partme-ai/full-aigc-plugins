#!/usr/bin/env python3
"""只读核验透明度修订的实际画布及PNG差异，复用冻结的像素校验。"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
COMMANDS=['transparency.set','transparency.makeOpacityMask','transparency.setOpacityMask']
def qualify(root,proof):
    """读取已完成命令族证据，不再次调用原生命令。"""
    path=Path(__file__).with_name('command_render.py');spec=importlib.util.spec_from_file_location('transparency_render_base',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.COMMANDS=COMMANDS
    result=m.qualify(root,proof);result['checkerSha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();result['scope']='Actual RGB changes for object opacity,mask creation and mask options;not OS-window screenshots or creative quality';return result
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('root',type=Path);args=parser.parse_args();result=qualify(args.root,args.root/'proof.json');(args.root/'render-changes.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'result':'PASS','commands':len(result['cases'])}))
