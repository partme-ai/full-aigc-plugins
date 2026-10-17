"""宿主中立Judge v2：显式绑定评价范围与媒体观察，不把能力声明当作证据。"""
from fractions import Fraction
import importlib.util
import math
from pathlib import Path
import uuid


def load(name):
    spec=importlib.util.spec_from_file_location('craft_judge_'+name,Path(__file__).with_name(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def rational(value):
    return {'num':value.numerator,'den':value.denominator}


def scope(root, report):
    """从当前原生合成与已经技术复检的媒体构建有限抽样请求。"""
    quality=load('quality_review');root=Path(root);manifest=quality.read(root/'manifest.json')
    comp=quality.read(root/'native.json')['composition']
    rate=Fraction(str(comp['frameRate']));duration=Fraction(str(comp['duration']))
    count=math.ceil(rate*duration)
    if not 1<=rate<=240 or duration<=0 or not 1<=count<=10000:
        raise ValueError('judge_timing_invalid')
    indices=sorted({0,count//4,count//2,3*count//4,count-1})
    previews={frame['path']:frame for frame in manifest.get('frames',[])}
    media=[]
    for row in report['technical']['media']:
        path=row['path'];fact={'path':path,'sha256':quality.sha(quality.contained(root,path))}
        if path in previews:
            seconds=Fraction(str(previews[path].get('seconds',0)))
            if not 0<=seconds<=duration:raise ValueError('judge_preview_timing_invalid')
            fact.update(kind='preview',frameIndices=[min(count-1,math.floor(seconds*rate))],seconds=rational(seconds))
        else:
            fact.update(kind='video' if row.get('decoded') else 'sequence',frameIndices=indices)
        media.append(fact)
    return {'schema':'effectcraft-evaluation-scope/v1','coverage':'sampled',
            'frameRate':rational(rate),'frameRange':{'start':0,'endExclusive':count},
            'timeRange':{'start':rational(Fraction(0)),'end':rational(duration)},
            'requiredFrameIndices':indices,'media':media}


def request(task, root, report, criteria, temporal):
    """产生不调用外部付费模型的请求；全帧评价与抽样评价明确区分。"""
    quality=load('quality_review');tasks=load('task_store');current=quality.binding(root)
    if current!=report.get('binding'):raise ValueError('artifact_changed')
    evaluation=scope(root,report)
    return {'schema':'effectcraft-judge-request/v2','requestId':uuid.uuid4().hex,'taskId':task,
            'binding':current,'criteria':criteria,'criteriaHash':tasks.digest(criteria),
            'temporalRequired':bool(temporal),'scope':evaluation,'scopeHash':tasks.digest(evaluation),
            'media':report['technical']['media'],
            'requiredResponse':['schema','requestId','taskId','binding','criteriaHash','scopeHash','status',
                'capabilities','observations','score','passed','issues','temporalReviewed'],
            'instruction':'Observe actual bound media at requested sample frames. Missing capability/coverage is NOT_RUN. Sampled PASS does not assert all-frame creative acceptance.'}


def not_run(report, response, reason):
    result=dict(report)
    result['creative']={'status':'NOT_RUN','reason':reason,'receipt':response}
    result['readyForAcceptance']=False
    return result


def accept(root, report, expected, response):
    """回执身份错误拒绝；宿主能力或样本不足保留NOT_RUN，不猜测评分。"""
    refreshed=request(expected['taskId'],root,report,expected['criteria'],expected['temporalRequired'])
    refreshed['requestId']=expected['requestId']
    if refreshed!=expected:raise ValueError('judge_request_changed')
    return accept_response(report,expected,response)


def accept_response(report,expected,response):
    """已核对请求来源后共用v2回执校验；按各上下文独立计算覆盖。"""
    if not isinstance(response,dict) or response.get('schema')!='effectcraft-judge-receipt/v2':
        raise ValueError('judge_schema_mismatch')
    for key in ('requestId','taskId','binding','criteriaHash','scopeHash'):
        if response.get(key)!=expected[key]:raise ValueError('judge_binding_mismatch: '+key)
    if response.get('status') not in ('PASS','FAIL','NOT_RUN'):
        raise ValueError('judge_response_invalid')
    capabilities=response.get('capabilities',{})
    if not isinstance(capabilities,dict):raise ValueError('judge_response_invalid')
    if capabilities.get('visual') is not True:return not_run(report,response,'visual_capability_missing')
    if expected['temporalRequired'] and (capabilities.get('temporal') is not True or response.get('temporalReviewed') is not True):
        return not_run(report,response,'temporal_capability_missing')
    observations=response.get('observations',[])
    if not isinstance(observations,list):raise ValueError('judge_observation_invalid')
    media={row['path']:row for row in expected['scope']['media']};observed=set()
    contexts={row['id']:row for row in expected['scope'].get('contexts',[])}
    covered={key:set() for key in contexts};paths=set()
    count=expected['scope'].get('frameRange',{}).get('endExclusive')
    for row in observations:
        if not isinstance(row,dict) or row.get('path') not in media:raise ValueError('judge_observation_invalid')
        bound=media[row['path']]
        limit=contexts[bound['context']]['frameRange']['endExclusive'] if contexts else count
        frames=row.get('frameIndices')
        if (row.get('sha256')!=bound['sha256'] or not isinstance(frames,list) or not frames
                or any(type(frame) is not int or not 0<=frame<limit for frame in frames)
                or len(frames)!=len(set(frames))
                or not isinstance(row.get('method'),str) or not row['method'].strip()
                or not isinstance(row.get('description'),str) or not row['description'].strip()):
            raise ValueError('judge_observation_invalid')
        if bound['kind']=='preview' and frames!=bound['frameIndices']:
            raise ValueError('judge_observation_invalid')
        observed.update(frames);paths.add(row['path'])
        if contexts:covered[bound['context']].update(frames)
    if response['status']=='NOT_RUN':return not_run(report,response,'host_review_not_run')
    if contexts:
        if any(not set(context['requiredFrameIndices']).issubset(covered[key]) for key,context in contexts.items()):
            return not_run(report,response,'sample_coverage_missing')
        if not set(expected['scope']['requiredMediaPaths']).issubset(paths):
            return not_run(report,response,'media_coverage_missing')
    else:
        required=expected['scope']['requiredFrameIndices'] if expected['temporalRequired'] else [0]
        if not set(required).issubset(observed):return not_run(report,response,'sample_coverage_missing')
    issues=response.get('issues')
    if (type(response.get('score')) not in (float,int) or not math.isfinite(response['score'])
            or not 0<=response['score']<=1 or type(response.get('passed')) is not bool
            or not isinstance(issues,list) or any(not isinstance(issue,dict)
                or not isinstance(issue.get('description'),str) or not issue['description'].strip() for issue in issues)
            or response['passed']!=(response['status']=='PASS')
            or (response['passed'] and issues)):
        raise ValueError('judge_response_invalid')
    result=dict(report)
    result['creative']={'status':response['status'],'receipt':response,'scope':expected['scope']}
    result['readyForAcceptance']=response['passed'] and report['engineering']['status']=='PASS'
    return result
