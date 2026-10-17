"""锁定原生秒／帧时间合同；实际合成必须与计划预期匹配才允许渲染。"""
import copy,json,math
from fractions import Fraction

TICKS=254016000000
COMMON=[Fraction(24000,1001),Fraction(24),Fraction(25),Fraction(30000,1001),Fraction(30),Fraction(48),Fraction(50),Fraction(60000,1001),Fraction(60),Fraction(120000,1001),Fraction(120)]
FIELDS=('width','height','frameRate','duration','workArea')

def number(value):return type(value) in (int,float) and math.isfinite(value)
def rate(value):
    if not number(value) or not .001<=value<=240:raise ValueError('invalid_document_timing')
    return next((r for r in COMMON if abs(float(r)-value)<.005),Fraction(math.floor(value*1000+.5),1000))
def tick(value):return math.floor(value*TICKS+.5)
def duration(value,fps):
    if not number(value) or not 0<value<=3600:raise ValueError('invalid_document_timing')
    t=tick(value);f=t*fps.numerator//(TICKS*fps.denominator)
    a=f*TICKS*fps.denominator//fps.numerator;b=(f+1)*TICKS*fps.denominator//fps.numerator
    return max(a if t-a<=b-t else b,TICKS*fps.denominator//fps.numerator)/TICKS

def area(value,config):
    if (not isinstance(value,list) or len(value)!=2 or not all(number(v) for v in value)
            or not 0<=value[0]<value[1]<=config['duration']+1/TICKS
            or tick(value[1])-tick(value[0])<TICKS*rate(config['frameRate']).denominator//rate(config['frameRate']).numerator):
        raise ValueError('invalid_work_area')
    return [tick(v)/TICKS for v in value]

def document(value,work_area=None):
    if not isinstance(value,dict):raise ValueError('invalid_document')
    for field in ('width','height'):
        if type(value.get(field)) is not int or not 0<value[field]<=16384:raise ValueError('invalid_document_size')
    fps=rate(value.get('frameRate'));result={field:value[field] for field in ('width','height')}
    result.update(frameRate=float(fps),duration=duration(value.get('duration'),fps))
    result['workArea']=area([0,result['duration']] if work_area is None else work_area,result)
    return result

def observed(value):
    if not isinstance(value,dict):raise ValueError('composition_config_mismatch: invalid composition')
    result={field:value.get(field) for field in FIELDS}
    for field in ('width','height'):
        if type(result[field]) is not int or not 0<result[field]<=16384:raise ValueError('composition_config_mismatch: '+field)
    if not number(result['frameRate']) or not .001<=result['frameRate']<=240 or not number(result['duration']) or result['duration']<=0:raise ValueError('composition_config_mismatch: timing')
    try:result['workArea']=area(result['workArea'],result)
    except ValueError as error:raise ValueError('composition_config_mismatch: workArea') from error
    return result

def current_time(reply):
    state=reply.get('state',{})
    if number(state.get('time')):return state['time']
    # 固定0.4.0的editor.state使用按合成ID索引的整数tick，而研究HEAD使用秒。
    value=state.get('times',{}).get(str(state.get('active_comp')))
    if type(value) is not int:raise ValueError('composition_current_time_unavailable')
    return value/TICKS

def updated(expected,command,params,composition,current_time=None):
    result=copy.deepcopy(expected)
    if params.get('comp',composition)!=composition:return result
    if command=='comp.settings':
        for field in ('width','height'):
            if field in params:
                if type(params[field]) is not int or not 0<params[field]<=16384:raise ValueError('invalid_document_size')
                result[field]=params[field]
        if 'frameRate' in params or 'fps' in params:result['frameRate']=float(rate(params.get('frameRate',params.get('fps'))))
        if 'duration' in params:
            old=result['duration'];result['duration']=duration(params['duration'],rate(result['frameRate']))
            if result['workArea'][1]==old:result['workArea'][1]=result['duration']
            result['workArea'][1]=min(result['workArea'][1],result['duration'])
    elif command=='comp.workArea':
        fps=rate(result['frameRate']);fd=TICKS*fps.denominator//fps.numerator
        start,end=map(tick,result['workArea']);limit=tick(result['duration'])
        if params.get('set') in ('begin','end'):
            if not number(current_time):raise ValueError('composition_current_time_unavailable')
            now=tick(current_time)
            if params['set']=='begin':start=min(now,end-fd)
            else:end=min(max(now+fd,start+fd),limit)
        if number(params.get('start')):start=min(max(tick(params['start']),0),limit-fd)
        if number(params.get('end')):end=min(max(tick(params['end']),start+fd),limit)
        result['workArea']=[start/TICKS,end/TICKS]
    return result

def verify(expected,actual):
    if not isinstance(actual,dict):raise ValueError('composition_config_mismatch: invalid composition')
    differences={}
    for field in FIELDS:
        requested=expected[field];value=actual.get(field)
        if field=='workArea':match=isinstance(value,list) and len(value)==2 and all(number(v) and abs(v-e)<=1e-9 for v,e in zip(value,requested))
        elif field in ('width','height'):match=type(value) is int and value==requested
        else:match=number(value) and abs(value-requested)<=1e-9
        if not match:differences[field]={'expected':requested,'observed':value}
    if differences:raise ValueError('composition_config_mismatch: '+json.dumps(differences,sort_keys=True,default=str))
    return {'schema':'effectcraft-composition-validation/v1','status':'PASS','timeUnit':'seconds','ticksPerSecond':TICKS,'expected':copy.deepcopy(expected),'observed':{field:actual[field] for field in FIELDS}}
