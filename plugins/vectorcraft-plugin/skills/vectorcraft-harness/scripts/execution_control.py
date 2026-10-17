"""可选的本地协作控制：逐调用检查，不把本地步骤当成原生幂等接口。"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import time

_spec=importlib.util.spec_from_file_location('craft_control_json',Path(__file__).with_name('commands.py'))
_json=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(_json)

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

class ExecutionControl:
    """读取不可变授权配置和原子替换的状态文件，持久化原位置调用记录。"""
    def __init__(self,path):
        path=Path(path)
        if path.is_symlink() or not path.is_file():raise ValueError('invalid_execution_control')
        self.profile=_json.reply_json(path.read_text());p=self.profile
        if (p.get('schema')!='vectorcraft-execution-control/v1' or not isinstance(p.get('task'),str)
                or type(p.get('epoch')) is not int or p['epoch']<=0
                or type(p.get('deadline')) is not int or type(p.get('maxBytes')) is not int or p['maxBytes']<=0):
            raise ValueError('invalid_execution_control')
        self.stage=None
        if digest(p['planFile'])!=p['planHash']:raise RuntimeError('plan_snapshot_mismatch')
        self.expected_plan=_json.reply_json(Path(p['planFile']).read_text())

    def check(self):
        """每次请求前检查撤销、epoch、时间、源工程和暂存资源预算。"""
        p=self.profile
        state_path=Path(p['stateFile'])
        if state_path.is_symlink():raise RuntimeError('invalid_execution_state')
        state=_json.reply_json(state_path.read_text())
        if state.get('task')!=p['task'] or state.get('epoch')!=p['epoch']:raise RuntimeError('stale_epoch')
        if state.get('state')!='running':raise RuntimeError('cancel_requested: execution is not running')
        if int(time.time()*1000)>=p['deadline']:raise RuntimeError('deadline_exceeded')
        if p.get('source') and digest(p['source']['path'])!=p['source']['sha256']:raise RuntimeError('revision_conflict')
        if self.stage:
            files=list(self.stage.rglob('*'))
            if any(f.is_symlink() for f in files):raise RuntimeError('unexpected_stage_symlink')
            if sum(f.stat().st_size for f in files if f.is_file())>p['maxBytes']:raise RuntimeError('output_budget_exceeded')

    def emit(self,event,**values):
        """在持有的事件文件上追加并fsync，拒绝链接和inode替换。"""
        p=self.profile;path=Path(p['eventFile'])
        if path.is_symlink():raise RuntimeError('execution_event_identity_mismatch')
        descriptor=os.open(path,os.O_WRONLY|os.O_APPEND|getattr(os,'O_NOFOLLOW',0))
        try:
            stat=os.fstat(descriptor)
            if (stat.st_dev,stat.st_ino)!=(p['eventDevice'],p['eventInode']):raise RuntimeError('execution_event_identity_mismatch')
            record={'event':event,'task':p['task'],'epoch':p['epoch'],'time':int(time.time()*1000),**values}
            encoded=(json.dumps(record,ensure_ascii=False,allow_nan=False,separators=(',',':'))+'\n').encode()
            while encoded:
                written=os.write(descriptor,encoded);encoded=encoded[written:]
            os.fsync(descriptor)
        finally:os.close(descriptor)

    def attach_stage(self,stage):
        self.check();stage=Path(stage).resolve();stat=stage.stat();self.stage=stage
        self.emit('stage_created',path=str(stage),device=stat.st_dev,inode=stat.st_ino)

    def prepare_delivery(self,stage,output):
        """重命名前持久登记实际交付子目录身份，覆盖链接素材打包产生的新目录。"""
        self.check();stage=Path(stage).resolve();output=Path(output).absolute()
        if not self.stage or not stage.is_relative_to(self.stage) or output.parent.resolve()!=self.stage.parent:
            raise RuntimeError('delivery_outside_stage')
        manifest=stage/'manifest.json'
        if manifest.is_symlink() or not manifest.is_file():raise RuntimeError('invalid_delivery_manifest')
        stat=stage.stat()
        self.emit('delivery_prepared',path=str(stage),output=str(output),device=stat.st_dev,inode=stat.st_ino,manifestSha256=digest(manifest))

    def before_request(self,method,params,request_id,pid):
        self.check();self.emit('submitted',method=method,params=params,requestId=request_id,pid=pid)

    def after_request(self,request_id,pid,result):
        encoded=json.dumps(result,ensure_ascii=False,allow_nan=False,sort_keys=True,separators=(',',':')).encode()
        self.emit('reply_received',requestId=request_id,pid=pid,replySha256=hashlib.sha256(encoded).hexdigest())

    def apply_limits(self):
        """仅约束原生子进程的单文件大小；累计暂存预算另在逐请求检查。"""
        import resource
        soft,hard=resource.getrlimit(resource.RLIMIT_FSIZE)
        maximum=self.profile['maxBytes'] if hard==resource.RLIM_INFINITY else min(hard,self.profile['maxBytes'])
        resource.setrlimit(resource.RLIMIT_FSIZE,(maximum,hard))

    def brand_module(self):
        spec=importlib.util.spec_from_file_location('craft_control_brand',Path(__file__).with_name('brand_variants.py'))
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

    def structural_module(self):
        spec=importlib.util.spec_from_file_location('craft_control_structure',Path(__file__).with_name('boolean_transactions.py'))
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

    def structural_authorization(self,command,params,before,selection=None):
        """结构修改须显式授权，选择整个子树时每个参与对象均须在范围内。"""
        auth=self.profile['authorization'];guard=self.structural_module();objects=guard.nodes(before)
        if not isinstance(params,dict):raise RuntimeError('revision_outside_authorization')
        ids=params.get('ids') if command=='select.set' else selection
        if (('structure' not in auth['fields']) or not isinstance(params,dict)
                or (set(params)!={'ids'} if command=='select.set' else bool(params))
                or not isinstance(ids,list) or not ids
                or any(type(i) is not int or i not in objects or i not in auth['objects'] for i in ids)
                or len(set(ids))!=len(ids)):
            raise RuntimeError('revision_outside_authorization')
        if command!='select.set':
            affected=guard.nodes({'layers':[objects[i] for i in ids]})
            if any(i not in auth['objects'] for i in affected):
                raise RuntimeError('revision_outside_authorization')
        return ids

    def allowed_field(self,path):
        return any(path==field or path.startswith(field+'.') for field in self.profile['authorization']['fields'])

    def authorize_operation(self,command,params,before,selection=None):
        """局部修订只接受已分类操作，并按真实对象与全局色板消费者核对授权。"""
        self.check();auth=self.profile.get('authorization')
        if not isinstance(auth,dict) or not isinstance(auth.get('objects'),list) or not isinstance(auth.get('fields'),list):
            raise RuntimeError('managed_revision_authorization_required')
        if command=='select.set' or command in self.structural_module().COMMANDS:
            self.structural_authorization(command,params,before,selection)
            return
        brand=self.brand_module();objects=brand.snapshot(before)
        if command=='swatch.edit':
            if set(params)-{'name','color'} or not isinstance(params.get('name'),str) or 'color' not in params:
                raise RuntimeError('managed_revision_command_unclassified')
            consumers={key:brand.bound_fields(value,params['name']) for key,value in objects.items() if brand.uses_token(value,params['name'])}
            if not consumers:raise RuntimeError('revision_swatch_consumers_missing')
            for key,fields in consumers.items():
                if key not in auth['objects'] or not fields or any(not self.allowed_field('.'.join(map(str,path))) for path in fields):
                    raise RuntimeError('revision_outside_authorization')
        elif command in ('paint.setFill','text.setText'):
            ids=params.get('ids',[params['id']] if 'id' in params else [])
            if not isinstance(ids,list) or not ids or any(type(i) is not int or i not in objects or i not in auth['objects'] for i in ids):
                raise RuntimeError('revision_outside_authorization')
        else:raise RuntimeError('managed_revision_command_unclassified')

    def verify_revision(self,before,after,command,params,result=None,selection=None,after_selection=None):
        """修改后逐字段比较；对象顺序、非目标对象与文档属性不能被评分豁免。"""
        guard=self.structural_module()
        if command=='select.set' or command in guard.COMMANDS:
            self.check();ids=self.structural_authorization(command,params,before,selection)
            if command=='select.set':
                if guard.normalized(before)!=guard.normalized(after):
                    raise RuntimeError('revision_selection_document_violation')
                if (not isinstance(after_selection,list) or any(type(i) is not int for i in after_selection)
                        or len(set(after_selection))!=len(after_selection) or set(after_selection)!=set(ids)):
                    raise RuntimeError('revision_selection_identity_mismatch')
                result_ids=ids
            else:
                result_ids=guard.verify_result(before,after,command,ids,result,after_selection)
            self.emit('revision_verified',command=command,objectIds=ids,resultIds=result_ids,fields=['structure'])
            return
        brand=self.brand_module();old,new=brand.snapshot(before),brand.snapshot(after)
        if old.keys()!=new.keys() or [o['id'] for o in before['layers']]!=[o['id'] for o in after['layers']]:
            raise RuntimeError('revision_structure_violation')
        def changed(a,b,path=''):
            if type(a)!=type(b):return [path]
            if isinstance(a,dict):
                if a.keys()!=b.keys():return [path]
                return [p for key in a for p in changed(a[key],b[key],(path+'.' if path else '')+key)]
            if isinstance(a,list):
                if len(a)!=len(b):return [path]
                return [p for i,(x,y) in enumerate(zip(a,b)) for p in changed(x,y,(path+'.' if path else '')+str(i))]
            return [] if a==b else [path]
        auth=self.profile['authorization']
        for key in old:
            fields=changed(old[key],new[key])
            if fields and (key not in auth['objects'] or any(not self.allowed_field(field) for field in fields)):
                raise RuntimeError('revision_field_violation: '+str(key)+':'+','.join(fields))
        first={k:v for k,v in before.items() if k!='layers'};second={k:v for k,v in after.items() if k!='layers'}
        import copy
        first,second=copy.deepcopy(first),copy.deepcopy(second)
        if first.get('metadata')!=second.get('metadata'):
            old_time=first.get('metadata',{}).get('modified');new_time=second.get('metadata',{}).get('modified')
            if (type(old_time) is not int or type(new_time) is not int or new_time<old_time
                    or new_time>int(time.time())+1):raise RuntimeError('revision_document_violation')
            first['metadata']['modified']=second['metadata']['modified']=None
        if command=='swatch.edit':
            # 仅该色板的 paint.color 可以变化，重命名、其他色板和作者模型仍被保护。
            import copy
            first,second=copy.deepcopy(first),copy.deepcopy(second)
            for doc in (first,second):
                matched=[s for s in doc.get('swatches',[]) if s.get('name')==params['name']]
                if len(matched)!=1:raise RuntimeError('revision_palette_violation')
                matched[0]['paint']['color']=None
        if first!=second:raise RuntimeError('revision_document_violation')
        self.emit('revision_verified',command=command,objectIds=auth['objects'],fields=auth['fields'])
