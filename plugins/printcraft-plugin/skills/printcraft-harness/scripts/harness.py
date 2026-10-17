"""插件薄适配器：只委托公开命令或消费协议，不复制 PDF 执行代码。"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[3]
ROUTES={'setup':'printcraft-cli-setup','inspect':'printcraft-cli-inspect','pages':'printcraft-cli-pages','automation':'printcraft-cli-automation','tools':'printcraft-cli','general':'printcraft-use','ocr':'printcraft-use'}

def consume(data):
    protocol=data.get('protocol')
    if protocol not in {'printcraft.execution/1','printcraft.verification/1','printcraft.ocr/1'}:raise ValueError('upstream_protocol_missing_or_unsupported')
    if protocol in {'printcraft.execution/1','printcraft.ocr/1'} and (not isinstance(data.get('runId'),str) or not data['runId']):raise ValueError('run_id_required')
    status=data.get('status')
    if protocol=='printcraft.ocr/1':
        if status not in {'UNKNOWN','FAILED_OR_PARTIAL','DETERMINISTIC_PASS_REVIEW_REQUIRED','PRESERVATION_UNKNOWN_REVIEW_REQUIRED','INPUT_OR_BACKEND_OR_SKILL_CHANGED_REVIEW_REQUIRED'}:raise ValueError('upstream_ocr_status_invalid')
        return {'protocol':protocol,'runId':data['runId'],'status':status,'nextAction':'READ_ONLY_OCR_RECEIPT_AND_ARTIFACTS' if status in {'UNKNOWN','FAILED_OR_PARTIAL'} else 'REVIEW_ARTIFACTS','automaticReplay':False,'completeAcceptance':False,'inputs':data.get('inputSha256'),'artifacts':data.get('artifacts',[]),'backendIdentity':data.get('backendIdentity'),'nativeIdentity':data.get('nativeIdentity'),'visualReview':data.get('visualReview'),'losses':data.get('losses',[])}
    if status not in {'STARTED','UNKNOWN','FAILED_OR_PARTIAL','NATIVE_EXIT_ZERO_REVIEW_REQUIRED','INPUT_CHANGED_REVIEW_REQUIRED','SKILL_CHANGED_REVIEW_REQUIRED','INPUT_OR_SKILL_CHANGED_REVIEW_REQUIRED','OUTPUT_INVALID_REVIEW_REQUIRED','DETERMINISTIC_PASS_REVIEW_REQUIRED','FAILED','VERIFIED','REVISION_PROPOSED'}:raise ValueError('upstream_status_invalid')
    return {'protocol':protocol,'runId':data.get('runId'),'status':status,'nextAction':'READ_ONLY_RECONCILE' if status in {'STARTED','UNKNOWN','FAILED_OR_PARTIAL'} else 'REVIEW_ARTIFACTS','automaticReplay':False,'completeAcceptance':status=='VERIFIED' and data.get('completeAcceptance') is True,'inputs':data.get('inputSha256',{}),'artifacts':data.get('artifacts',[]),'requestSha256':data.get('requestSha256')}

def route(intent,explicit=None):
    if explicit:
        if explicit not in ROUTES.values():raise ValueError('unknown_explicit_skill')
        return explicit
    return ROUTES[intent]

def new_scope(previous,requested):
    """复用已授权范围，只返回新增范围；不在本地伪造授权。"""
    return sorted(set(requested)-set(previous))

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=('show','route','delegate','ocr'));p.add_argument('argument',nargs='?');p.add_argument('--explicit');args,extra=p.parse_known_args();args.arguments=extra
    try:
        if args.action not in {'delegate','ocr'} and args.arguments:raise ValueError('unexpected_arguments')
        if args.action=='show':result=consume(json.loads(Path(args.argument).read_text()))
        elif args.action=='route':result={'skill':route(args.argument,args.explicit)}
        elif args.action=='ocr':
            if args.argument not in {'diagnose','run'}:raise ValueError('unsupported_ocr_action')
            return subprocess.run([sys.executable,'-I','-B',str(ROOT/'skills/printcraft-use/scripts/ocr.py'),args.argument,*args.arguments]).returncode
        else:
            if args.argument not in {'list','describe','check','run','status','reconcile','verify','handoff'}:raise ValueError('unsupported_public_action')
            return subprocess.run([sys.executable,'-I','-B',str(ROOT/'skills/printcraft-use/scripts/commands.py'),args.argument,*args.arguments]).returncode
        print(json.dumps(result,ensure_ascii=False,indent=2));return 0
    except (ValueError,OSError) as error:print(json.dumps({'error':str(error),'automaticReplay':False}));return 1
if __name__=='__main__':raise SystemExit(main())
