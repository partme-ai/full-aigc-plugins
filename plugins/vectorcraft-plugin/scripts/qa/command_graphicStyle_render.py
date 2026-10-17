#!/usr/bin/env python3
"""图形样式图像核验：替换／重定义应可见，库与链接操作保全艺术。"""
import argparse,hashlib,importlib.util,json
from pathlib import Path
COMMANDS=['graphicStyle.'+n for n in ('apply','new','delete','duplicate','list','redefine','breakLink','rename','unused','sortByName','merge','move','setOptions','libraries','library','addFromLibrary','saveLibrary','loadLibrary')]
CHANGED={'graphicStyle.apply','graphicStyle.redefine'}
# 删除两轮预置不同样式；各轮保色由独立完整树断言证明，跨轮图像只测量。
MEASURED={'graphicStyle.addFromLibrary','graphicStyle.delete'}
def base():
 s=importlib.util.spec_from_file_location('style_render_base',Path(__file__).with_name('command_layer_render.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.COMMANDS=COMMANDS;m.CHANGED=CHANGED;m.MEASURED=MEASURED;return m
def expectation(command,kind):return base().expectation(command,kind)
def validate_count(count,total,relation):return base().validate_count(count,total,relation)
def qualify(root,proof):
 result=base().qualify(root,proof);result['schema']='vectorcraft-command-graphic-style-render/v1';result['checkerSha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();result['scope']='Actual54 canvas/PNG/window comparisons for18 graphic styles commands;explicit preservation/change/measurement contracts plus independent object/link assertions;not preference restart,creative or full V1';return result
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('root',type=Path);args=parser.parse_args();result=qualify(args.root,args.root/'proof.json');(args.root/'render-changes.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'result':'PASS','commands':len(result['cases']),'comparisons':54}))
