"""执行技能计划入口和真实PhotoCraft CLI，检查合成损伤、保护区及原层。"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from craft_cli_windows import Runner,require
from photo_restoration_smoke import fixture,verify_local_repair
from photo_playbook_smoke import rgb_pixels


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    g=p.add_mutually_exclusive_group(required=True);g.add_argument('--cli',type=Path);g.add_argument('--runtime-root',type=Path);a=p.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
    exe=a.cli.resolve() if a.cli else None
    if a.runtime_root:
        matches=list(a.runtime_root.resolve().rglob('photocraft-cli.exe'));require(len(matches)==1,'Expected one runtime');exe=matches[0]
        prior=json.loads((a.runtime_root/'result.json').read_text(encoding='utf-8'));require(hashlib.sha256(exe.read_bytes()).hexdigest()==prior['exeSha256'],'Runtime changed')
    source=a.source.resolve()/'skills/photocraft-restore-old-photo';sample=json.loads((source/'assets/local-repair-input.json').read_text(encoding='utf-8'));variants=[('mixed',sample)]
    for kind in ['spot','heal']:
        strokes=[{'kind':kind,'points':[[40,30],[44,32]],'size':5},{'kind':kind,'points':[[80,40],[84,42]],'size':6}]
        if kind=='heal':strokes[0]['source']=[20,30];strokes[1]['source']=[60,40]
        variants.append((kind,{**sample,'strokes':strokes}))
    work=out/'修复 中文 workspace';work.mkdir();r=Runner(exe,work,out);results=[]
    for name,data in variants:
        root=work/name;root.mkdir();r.work=root;fixture(root/'clean.png',False);fixture(root/'input.png',True);before=hashlib.sha256((root/'input.png').read_bytes()).hexdigest();inp=root/'修复参数.json';inp.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8');params_before=inp.read_bytes();plan_path=root/'计划.json';argv=[sys.executable,str(source/'scripts/repair_plan.py'),'--input',str(inp),'--output',str(plan_path)]
        run=subprocess.run(argv,capture_output=True,text=True,encoding='utf-8');require(run.returncode==0,'Skill plan CLI failed: '+run.stderr);plan_bytes=plan_path.read_bytes();plan=json.loads(plan_bytes)
        again=subprocess.run(argv,capture_output=True,text=True,encoding='utf-8');require(again.returncode!=0 and plan_path.read_bytes()==plan_bytes,'Existing plan overwritten')
        args=['run','input.png']
        for step in plan['steps']:args+=['--cmd',step['command'],'--params',json.dumps(step['params'],ensure_ascii=True)]
        r.run(*args,'--out','repaired.pcraft');r.run('convert','repaired.pcraft','repaired.png');info=json.loads(r.run('info','repaired.pcraft'));require(len(info['layers'])==2,'Original/working layers missing');working=next(x for x in info['layers'] if x['name']=='Restoration working copy')
        metrics=verify_local_repair(rgb_pixels(root/'clean.png')[2],rgb_pixels(root/'input.png')[2],rgb_pixels(root/'repaired.png')[2],256,[(36,26,49,37),(76,36,89,47)])
        r.run('run','repaired.pcraft','--cmd','layer.delete','--params',json.dumps({'layer':working['id']}),'--out','source-only.pcraft');r.run('convert','source-only.pcraft','source-only.png');require(rgb_pixels(root/'source-only.png')==rgb_pixels(root/'input.png'),'Original layer pixels changed');require(hashlib.sha256((root/'input.png').read_bytes()).hexdigest()==before and inp.read_bytes()==params_before,'Input changed')
        results.append({'name':name,'metrics':metrics,'originalLayerPixels':'PASS','inputUnchanged':'PASS','existingPlanProtection':'PASS','layers':2})
    report={'status':'PASS','platform':sys.platform,'nativeProcesses':len(r.calls),'variants':results,'scope':'synthetic256x192; helper-generated local repair; no real photo-quality claim','hostSync':'NOT_TESTED'};(out/'result.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
if __name__=='__main__':main()
