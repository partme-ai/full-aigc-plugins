#!/usr/bin/env python3
"""魔棒会话设置固定验收：独立合并、上下界、工具切换与重开保全。"""
import copy, importlib.util, json, math, sys
from pathlib import Path
FAMILY='magicWand'
COMMANDS=['magicWand.set','magicWand.options']
DEFAULT=dict(fillColor=True,fillTolerance=32.,strokeColor=False,strokeTolerance=32.,strokeWeight=False,weightTolerance=5.,opacity=False,opacityTolerance=5.,blendingMode=False)
LIMITS=dict(fillTolerance=255.,strokeTolerance=255.,weightTolerance=1000.,opacityTolerance=100.)
def load_local(name):
 s=importlib.util.spec_from_file_location('wand_'+name,Path(__file__).with_name(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
shape=load_local('command_shape')
def expected(before,params):
 """只接受已知字段；重置后应用本次覆盖，数值按四种独立范围限制。"""
 out=copy.deepcopy(DEFAULT if params.get('reset',False) else before)
 for k,v in params.items():
  if k not in DEFAULT:continue
  if k in LIMITS:
   if type(v) not in (int,float) or not math.isfinite(v):raise ValueError('wand_number_type')
   out[k]=min(LIMITS[k],max(0.,v))
  else:
   if type(v) is not bool:raise ValueError('wand_boolean_type')
   out[k]=v
 return out

def validate_transition(command,s):
 if command not in COMMANDS:raise ValueError('wand_unknown')
 f=s['fixture'];want=expected(f['settingsBefore'],s['params']) if command=='magicWand.set' else f['settingsBefore']
 if s['returned']!=want:raise ValueError('wand_return')
 o=s['observed']
 if any(o[k]!=want for k in ('immediate','afterToolSwitch','afterNativeReopen')):raise ValueError('wand_session_preservation')
 if s['ui']['ui'].get('open_panel')!='magicWand':raise ValueError('wand_panel_context')
 for a in ('after','reopened'):shape.near(shape.stable(s['before']),shape.stable(s[a]),'wand_document_preservation')
 shape.near(shape.stable(s['after']),shape.stable(o['reopenedDocument']),'wand_checkpoint_preservation')
 if s['round']==2:
  prior=copy.deepcopy(f['revisionBefore']);shape.find(prior,2)['name']=f['revisionName'];shape.near(shape.stable(prior),shape.stable(s['before']),'wand_local_revision')
  if shape.find(f['revisionBefore'],2).get('name')==f['revisionName']:raise ValueError('wand_local_revision')
 if s['listBefore']!=s['listAfter'] or s['listAfter']!=s['listReopened']:raise ValueError('wand_swatch_preservation')

def initialize(call):
 call('view.drawMode',mode='normal');call('magicWand.set',reset=True)
 panel=call('window.panel',panel='magicWand')
 if panel.get('open') is None:call('window.panel',panel='magicWand')
 return {'settings':copy.deepcopy(DEFAULT)}
def prepare(call,command,number,directory,state):
 f={}
 if number==2:
  f={'revisionBefore':call('document.json'),'revisionName':'Owned revised magic wand control'};call('layer.setProps',id=2,name=f['revisionName'])
 if command=='magicWand.options':
  p={'fillColor':False,'strokeColor':True,'strokeWeight':True,'opacity':True,'blendingMode':True,'fillTolerance':0,'strokeTolerance':255,'weightTolerance':3.75,'opacityTolerance':12.5} if number==1 else {'reset':True,'fillTolerance':7.5}
  call('magicWand.set',**p);state['settings']=expected(state['settings'],p);params={}
 else:
  params={'fillColor':False,'strokeColor':True,'strokeWeight':True,'opacity':True,'blendingMode':True,'fillTolerance':-1,'strokeTolerance':300,'weightTolerance':1200,'opacityTolerance':-4,'unknownOwnedQA':True} if number==1 else {'reset':True,'opacity':True,'opacityTolerance':12.5}
 f['settingsBefore']=copy.deepcopy(state['settings']);actual=call('magicWand.options')
 if actual!=state['settings']:raise ValueError('wand_prepared_settings')
 if command=='magicWand.set':state['settings']=expected(state['settings'],params)
 return params,f

def observe(call,command,params,returned,directory,fixture):
 immediate=call('magicWand.options');call('tool.select',tool='pen');switched=call('magicWand.options');call('tool.select',tool='selection')
 path=directory/'wand-checkpoint.vectorcraft';call('document.save',path=str(path),modified=946684800);call('document.open',path=str(path));reopened=call('magicWand.options');document=call('document.json')
 return {'immediate':immediate,'afterToolSwitch':switched,'afterNativeReopen':reopened,'reopenedDocument':document,'checkpointSha256':load_local('command_family_window_diagnostic').sha(path),'preferenceRestartAcceptance':'NOT_RUN'}
if __name__=='__main__':
 family=type('WandFamily',(),{'FAMILY':FAMILY,'COMMANDS':COMMANDS,'__file__':__file__,**{n:staticmethod(globals()[n]) for n in ('initialize','prepare','observe','validate_transition')}});load_local('command_family_window_diagnostic').run(json.loads(Path(sys.argv[1]).read_text()),family)
