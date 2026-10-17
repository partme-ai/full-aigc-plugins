"""POSIX私有通道持有进程组归属；业务退出与组清理分别取证。"""
import importlib.util,json,os,re,secrets,select,signal,stat,subprocess,sys,threading,time
from pathlib import Path


def load(name):
    spec=importlib.util.spec_from_file_location('posix_lease_'+name,Path(__file__).with_name(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def pairs(items):
    value={}
    for k,v in items:
        if k in value:raise ValueError('owned_worker_result_invalid')
        value[k]=v
    return value


class ResultReader:
    """只接受原持有者匿名管道的一份有界、nonce绑定退出回执。"""
    def __init__(self,fd,nonce):self.fd=fd;self.nonce=nonce;self.data=b'';self.ended=False;self.code=None
    def consume(self,data):
        if self.ended:raise ValueError('owned_worker_result_invalid')
        if data:
            self.data+=data
            if len(self.data)>4096:raise ValueError('owned_worker_result_invalid')
            return None
        self.ended=True
        try:value=json.loads(self.data.decode('utf-8'),object_pairs_hook=pairs)
        except (ValueError,UnicodeError) as error:raise ValueError('owned_worker_result_invalid') from error
        if (not isinstance(value,dict) or set(value)!={'schema','nonce','returncode'}
                or value['schema']!='effectcraft-posix-worker-result/v1' or value['nonce']!=self.nonce
                or type(value['returncode']) is not int or not -255<=value['returncode']<=255):
            raise ValueError('owned_worker_result_invalid')
        self.code=value['returncode'];return self.code
    def read(self,timeout=0):
        if self.ended:return self.code
        if select.select([self.fd],[],[],timeout)[0]:return self.consume(os.read(self.fd,4097))
        return None


def other_members(group):
    """枚举必须同时观察到活着的持有者，才能证明没有其他活动成员。"""
    try:r=subprocess.run(['ps','-axo','pid=,pgid=,stat='],capture_output=True,text=True,timeout=5)
    except (OSError,subprocess.SubprocessError,UnicodeError) as error:raise ValueError('process_tree_inspection_failed') from error
    if r.returncode:raise ValueError('process_tree_inspection_failed')
    anchor=False;others=False
    for line in r.stdout.splitlines():
        if not line.strip():continue
        fields=line.split()
        if len(fields)!=3 or not fields[0].isdigit() or not fields[1].isdigit():raise ValueError('process_tree_inspection_failed')
        pid,pgid=int(fields[0]),int(fields[1]);active=not fields[2].startswith('Z')
        if pgid==group and active:
            if pid==group:anchor=True
            else:others=True
    if not anchor:raise ValueError('owned_group_anchor_missing')
    return others


def signal_owned(child,number):
    """只向仍由原Popen持有且尚活着的隔离组持有者所在组发送信号。"""
    if child.poll() is not None or os.getpgid(child.pid)!=child.pid:raise ValueError('owned_group_anchor_lost')
    os.killpg(child.pid,number)


def gate(fd,nonce,command):
    """业务进程退出后仍保留组持有者；守护通道EOF立即终止本隔离组。"""
    if (fd<3 or not stat.S_ISFIFO(os.fstat(fd).st_mode) or not re.fullmatch('[a-f0-9]{32}',nonce)
            or not command or os.getpgrp()!=os.getpid() or os.getsid(0)!=os.getpid()):
        raise ValueError('owned_group_gate_invalid')
    for sig in (signal.SIGTERM,signal.SIGINT):signal.signal(sig,lambda *_:None)
    if sys.stdin.buffer.read(1)!=b'G':return 1
    released=threading.Event()
    def watch():
        try:data=os.read(sys.stdin.fileno(),1)
        except OSError:data=b''
        if data==b'R':released.set()
        else:os.killpg(os.getpgrp(),signal.SIGKILL)
    threading.Thread(target=watch,daemon=True).start()
    child=subprocess.Popen(command,stdin=subprocess.DEVNULL,close_fds=True)
    code=child.wait()
    value={'schema':'effectcraft-posix-worker-result/v1','nonce':nonce,'returncode':code}
    os.write(fd,(json.dumps(value,separators=(',',':'))+'\n').encode());os.close(fd)
    released.wait();return code if code>=0 else 1


def guard(command,receipt,lease,grace,group_alive):
    closed=threading.Event()
    def watch():
        os.read(sys.stdin.fileno(),1);closed.set()
    threading.Thread(target=watch,daemon=True).start()
    for sig in (signal.SIGTERM,signal.SIGINT):signal.signal(sig,lambda *_:closed.set())
    store=load('task_store');child=None;read_fd=None;write_fd=None;reader=None;nonce=secrets.token_hex(16)
    record={'schema':'effectcraft-process-lifecycle/v1','status':'starting','guardianPid':os.getpid(),
            'ownership':{'schema':'effectcraft-posix-group-lease/v1','nonce':nonce,'workerResultVerified':False}}
    with load('platform_support').exclusive_lock(lease,timeout=0):
        store.atomic_json(receipt,record)
        try:
            read_fd,write_fd=os.pipe();reader=ResultReader(read_fd,nonce)
            args=[sys.executable,'-I','-B',str(Path(__file__).with_name('process_guard.py')),'_posix_gate',str(write_fd),nonce,*command]
            child=subprocess.Popen(args,stdin=subprocess.PIPE,start_new_session=True,pass_fds=(write_fd,))
            os.close(write_fd);write_fd=None
            record.update(status='running',workerGroup=child.pid,startedAt=time.time());store.atomic_json(receipt,record)
            child.stdin.write(b'G');child.stdin.flush()
            while reader.code is None and not closed.is_set():
                reader.read(.05)
                if child.poll() is not None:raise ValueError('owned_group_anchor_lost')
            record.update(status='draining',reason='supervisor_channel_closed' if closed.is_set() else 'worker_exited');store.atomic_json(receipt,record)
            signal_owned(child,signal.SIGTERM);deadline=time.monotonic()+grace;released=False
            while time.monotonic()<deadline:
                if not reader.ended:reader.read(0)
                try:empty=not other_members(child.pid)
                except ValueError:empty=False
                if empty and reader.code is not None:
                    child.stdin.write(b'R');child.stdin.flush();released=True;break
                time.sleep(.02)
            if not released:signal_owned(child,signal.SIGKILL)
            child.wait(timeout=5)
            if not reader.ended:
                result_deadline=time.monotonic()+5
                while not reader.ended and time.monotonic()<result_deadline:
                    try:reader.read(.05)
                    except ValueError:
                        if not (closed.is_set() and not released and not reader.data and child.returncode<0):raise
                if not reader.ended:raise ValueError('owned_worker_result_missing')
            deadline=time.monotonic()+5;observation_error=None
            while True:
                remaining=deadline-time.monotonic()
                if remaining<=0:
                    if observation_error is not None:raise observation_error
                    raise ValueError('owned_processes_still_running')
                try:
                    if not group_alive(child.pid,timeout=remaining):break
                    observation_error=None
                except ValueError as error:
                    # 查询异常不是停止证明；仅在原截止窗口内等待一次有效观察。
                    if str(error)!='process_tree_inspection_failed':raise
                    observation_error=error
                remaining=deadline-time.monotonic()
                if remaining<=0:
                    if observation_error is not None:raise observation_error
                    raise ValueError('owned_processes_still_running')
                time.sleep(min(.05,remaining))
            # 组持有者可能因排空被KILL；业务结果来自独立管道，不以该退出码代替。
            code=reader.code
            if code is None:
                if not (closed.is_set() and not released and not reader.data and child.returncode<0):raise ValueError('owned_worker_result_invalid')
                code=child.returncode
            record['ownership'].update(workerResultVerified=reader.code is not None,workerReturncode=reader.code,
                exitCodeSource='business-result' if reader.code is not None else 'group-holder-forced-stop',
                gateReturncode=child.returncode,forcedDrain=not released)
            record.update(status='stopped',returncode=code,stoppedAt=time.time());store.atomic_json(receipt,record)
            return code if code>=0 else 1
        except BaseException as error:
            record.update(status='unknown',error=str(error));store.atomic_json(receipt,record)
            if child and child.poll() is None:
                try:signal_owned(child,signal.SIGKILL)
                except (ValueError,ProcessLookupError):pass
                child.wait(timeout=5)
            raise
        finally:
            if child and child.stdin:child.stdin.close()
            if read_fd is not None:os.close(read_fd)
            if write_fd is not None:os.close(write_fd)
