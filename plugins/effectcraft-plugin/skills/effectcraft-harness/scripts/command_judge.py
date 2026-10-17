"""命令/桌面原生观察的Judge适配；各合成版本独立绑定帧和素材。"""
from fractions import Fraction
import importlib.util
import math
from pathlib import Path
import uuid


def load(name):
    spec=importlib.util.spec_from_file_location('craft_command_judge_'+name,Path(__file__).with_name(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


class Quality:
    """向既有任务族账本提供命令交付的只读质量合同。"""
    def __init__(self,store,task):self.store=store;self.task=task

    def binding(self,root):
        state=self.store.read(self.task)
        if Path(root)!=Path(state['output']):raise ValueError('review_output_mismatch')
        data=load('command_delivery').document(self.store,self.task)
        return {'commandDeliverySha256':state['delivery']['commandDeliverySha256'],
                'receiptSha256':data['receiptSha256'],'filesHash':load('task_store').digest(data['files'])}

    def inspect_delivery(self,root,runtime_home=None):
        if Path(root)!=Path(self.store.read(self.task)['output']):raise ValueError('review_output_mismatch')
        return load('command_delivery').inspect(self.store,self.task,runtime_home)

    def scope(self,root,report):
        """每个原生版本/合成分别建立时间基准，不合并异源帧覆盖。"""
        tasks=load('task_store');judge=load('judge_contract');quality=load('quality_review')
        data=load('command_delivery').document(self.store,self.task)
        frames={frame['path']:frame for frame in data['frames']};contexts={};media=[]
        for row in report['technical']['media']:
            frame=frames[row['path']];comp=frame['composition'];rate=Fraction(str(comp['frameRate']));duration=Fraction(str(comp['duration']))
            count=math.ceil(rate*duration);seconds=Fraction(str(frame['seconds']))
            if not 1<=rate<=240 or duration<=0 or not 1<=count<=10000 or not 0<=seconds<duration:
                raise ValueError('judge_timing_invalid')
            identity={'compositionId':comp['id'],'nativeVersion':frame['nativeVersion'],
                      'snapshotHash':tasks.digest(frame['snapshot']),'dependenciesHash':tasks.digest(frame['dependencies'])}
            key=tasks.digest(identity)
            contexts[key]={'id':key,**identity,'sourceProjects':row['sourceProjects'],
                'frameRate':judge.rational(rate),'frameRange':{'start':0,'endExclusive':count},
                'timeRange':{'start':judge.rational(Fraction(0)),'end':judge.rational(duration)},
                'requiredFrameIndices':sorted({0,count//4,count//2,3*count//4,count-1})}
            media.append({'path':row['path'],'sha256':quality.sha(quality.contained(Path(root),row['path'])),
                          'context':key,'kind':'preview','frameIndices':[math.floor(seconds*rate)],'seconds':judge.rational(seconds)})
        if not contexts:raise ValueError('judge_media_missing')
        return {'schema':'effectcraft-evaluation-scope/v1','coverage':'sampled',
                'contexts':[contexts[key] for key in sorted(contexts)],'media':media,'requiredMediaPaths':sorted(row['path'] for row in media)}

    def temporal(self,root,report):
        return any(row['frameRange']['endExclusive']>1 for row in self.scope(root,report)['contexts'])

    def judge_request(self,task,root,report,criteria,temporal):
        tasks=load('task_store');current=self.binding(root)
        if task!=self.task or current!=report.get('binding'):raise ValueError('artifact_changed')
        scope=self.scope(root,report)
        return {'schema':'effectcraft-judge-request/v2','requestId':uuid.uuid4().hex,'taskId':task,
                'binding':current,'criteria':criteria,'criteriaHash':tasks.digest(criteria),'temporalRequired':bool(temporal),
                'scope':scope,'scopeHash':tasks.digest(scope),'media':report['technical']['media'],
                'requiredResponse':['schema','requestId','taskId','binding','criteriaHash','scopeHash','status',
                    'capabilities','observations','score','passed','issues','temporalReviewed'],
                'instruction':'Observe every bound media path and requested frames separately for each native composition/version context. Missing capability or context coverage is NOT_RUN. Sampled PASS does not assert all-frame acceptance.'}

    def accept_judge(self,root,report,request,response):
        if report['technical']['status']!='PASS':raise ValueError('technical_gate')
        if report['engineering']['status']!='PASS':raise ValueError('engineering_gate')
        expected=self.judge_request(self.task,root,report,request['criteria'],self.temporal(root,report));expected['requestId']=request['requestId']
        if request!=expected:raise ValueError('judge_request_changed')
        return load('judge_contract').accept_response(report,expected,response)
