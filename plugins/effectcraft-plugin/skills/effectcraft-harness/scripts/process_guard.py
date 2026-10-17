"""独立监督通道与原生进程树守护；父监督器消失时仍完成清理。"""
import argparse
import ctypes
import importlib.util
import os
from pathlib import Path
import signal
import subprocess
import sys
import threading
import time

sys.dont_write_bytecode=True


def load(name):
    spec=importlib.util.spec_from_file_location('guard_'+name,Path(__file__).with_name(name+'.py'))
    value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value);return value


class WindowsJob:
    """以 Job Object 持有整个进程树；句柄关闭时内核终止遗留成员。"""
    def __init__(self):
        from ctypes import wintypes as w
        class Limits(ctypes.Structure):
            _fields_=[('processTime',ctypes.c_int64),('jobTime',ctypes.c_int64),('flags',w.DWORD),
                ('minimum',ctypes.c_size_t),('maximum',ctypes.c_size_t),('active',w.DWORD),
                ('affinity',ctypes.c_size_t),('priority',w.DWORD),('scheduling',w.DWORD)]
        class Counters(ctypes.Structure):
            _fields_=[('values',ctypes.c_uint64*6)]
        class Extended(ctypes.Structure):
            _fields_=[('limits',Limits),('io',Counters),('processMemory',ctypes.c_size_t),
                ('jobMemory',ctypes.c_size_t),('peakProcess',ctypes.c_size_t),('peakJob',ctypes.c_size_t)]
        class Accounting(ctypes.Structure):
            _fields_=[('user',ctypes.c_int64),('kernel',ctypes.c_int64),('periodUser',ctypes.c_int64),
                ('periodKernel',ctypes.c_int64),('faults',w.DWORD),('total',w.DWORD),('active',w.DWORD),('terminated',w.DWORD)]
        self.Accounting=Accounting;self.api=ctypes.WinDLL('kernel32',use_last_error=True)
        self.api.CreateJobObjectW.argtypes=[ctypes.c_void_p,w.LPCWSTR];self.api.CreateJobObjectW.restype=w.HANDLE
        self.api.SetInformationJobObject.argtypes=[w.HANDLE,ctypes.c_int,ctypes.c_void_p,w.DWORD]
        self.api.AssignProcessToJobObject.argtypes=[w.HANDLE,w.HANDLE]
        self.api.QueryInformationJobObject.argtypes=[w.HANDLE,ctypes.c_int,ctypes.c_void_p,w.DWORD,ctypes.c_void_p]
        self.api.TerminateJobObject.argtypes=[w.HANDLE,w.UINT];self.api.CloseHandle.argtypes=[w.HANDLE]
        self.handle=self.api.CreateJobObjectW(None,None)
        if not self.handle:raise ctypes.WinError(ctypes.get_last_error())
        limits=Extended();limits.limits.flags=0x2000 # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not self.api.SetInformationJobObject(self.handle,9,ctypes.byref(limits),ctypes.sizeof(limits)):
            self.close();raise ctypes.WinError(ctypes.get_last_error())

    def assign(self,child):
        if not self.api.AssignProcessToJobObject(self.handle,int(child._handle)):
            raise ctypes.WinError(ctypes.get_last_error())

    def alive(self):
        value=self.Accounting()
        if not self.api.QueryInformationJobObject(self.handle,1,ctypes.byref(value),ctypes.sizeof(value),None):
            raise ctypes.WinError(ctypes.get_last_error())
        return value.active>0

    def terminate(self):
        if not self.api.TerminateJobObject(self.handle,1):raise ctypes.WinError(ctypes.get_last_error())

    def close(self):
        if self.handle:self.api.CloseHandle(self.handle);self.handle=None


def group_alive(group,*,timeout=5):
    """僵尸不再执行或写入；查询失败不能被当作进程已停止。"""
    if type(group) is not int or group<=0:raise ValueError('owned_process_group_invalid')
    try:
        # 本任务租约内的原进程组；信号0只探测存在性，不发送停止信号。
        os.killpg(group,0)
    except ProcessLookupError:
        return False
    except PermissionError:
        # macOS对僵尸组也可能返回EPERM；此时仍须取得有效成员证据。
        pass
    except OSError as error:
        raise ValueError('process_tree_inspection_failed') from error
    try:
        result=subprocess.run(['ps','-axo','pgid=,stat='],capture_output=True,text=True,timeout=timeout)
    except (OSError,subprocess.SubprocessError,UnicodeError) as error:
        raise ValueError('process_tree_inspection_failed') from error
    if result.returncode:raise ValueError('process_tree_inspection_failed')
    rows=[line.split() for line in result.stdout.splitlines() if line.strip()]
    # 成员表损坏或空输出不能证明组已停止；必须先核对完整表的结构。
    if not rows or any(len(fields)!=2 or not fields[0].isdigit() for fields in rows):
        raise ValueError('process_tree_inspection_failed')
    return any(fields[0]==str(group) and not fields[1].startswith('Z') for fields in rows)


def guard(command,receipt,lease,grace=2):
    """持有生命周期锁直到整个自有组停止；stdin EOF 请求取消。"""
    if os.name!='nt':return load('posix_group_lease').guard(command,receipt,lease,grace,group_alive)
    closed=threading.Event()
    def watch():
        os.read(sys.stdin.fileno(),1);closed.set()
    threading.Thread(target=watch,daemon=True).start()
    for name in (signal.SIGTERM,signal.SIGINT):signal.signal(name,lambda *_:closed.set())
    store=load('task_store');job=None;child=None
    with load('platform_support').exclusive_lock(lease,timeout=0):
        # 门控包装器在加入 Job/进程组前不启动任何用户命令，避免分配竞态。
        options={'start_new_session':True} if os.name!='nt' else {}
        args=[sys.executable,'-I','-B',str(Path(__file__).resolve()),'_gate',*command]
        record={'schema':'effectcraft-process-lifecycle/v1','status':'starting','guardianPid':os.getpid()}
        store.atomic_json(receipt,record)
        try:
            if os.name=='nt':job=WindowsJob()
            child=subprocess.Popen(args,stdin=subprocess.PIPE,**options)
            if job:job.assign(child)
            record.update(status='running',workerGroup=child.pid,startedAt=time.time())
            store.atomic_json(receipt,record)
            child.stdin.write(b'G');child.stdin.flush();child.stdin.close()
            while child.poll() is None and not closed.wait(.05):pass
            reason='supervisor_channel_closed' if closed.is_set() else 'worker_exited'
            record.update(status='draining',reason=reason);store.atomic_json(receipt,record)
            alive=job.alive if job else lambda:group_alive(child.pid)
            if alive():
                if job:job.terminate()
                else:
                    try:os.killpg(child.pid,signal.SIGTERM)
                    except ProcessLookupError:pass
                deadline=time.monotonic()+grace
                while alive() and time.monotonic()<deadline:time.sleep(.05)
                if alive():
                    if job:job.terminate()
                    else:
                        try:os.killpg(child.pid,signal.SIGKILL)
                        except ProcessLookupError:pass
            child.wait(timeout=5)
            deadline=time.monotonic()+5
            while alive() and time.monotonic()<deadline:time.sleep(.05)
            if alive():raise ValueError('owned_processes_still_running')
            record.update(status='stopped',returncode=child.returncode,stoppedAt=time.time())
            store.atomic_json(receipt,record)
            return child.returncode if child.returncode>=0 else 1
        except BaseException as error:
            # 未取得完整停止证据时仅记录 unknown；不能放行编辑恢复。
            record.update(status='unknown',error=str(error));store.atomic_json(receipt,record)
            if child and child.poll() is None:
                if not child.stdin.closed:child.stdin.close()
                if job:job.terminate()
                elif os.name!='nt':
                    try:os.killpg(child.pid,signal.SIGKILL)
                    except ProcessLookupError:pass
                if child.poll() is None:child.kill()
                child.wait(timeout=5)
            raise
        finally:
            if job:job.close()


def main():
    # 固定重定向输出编码，Windows默认代码页也能返回中文帮助和回执。
    import sys
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,"reconfigure"):stream.reconfigure(encoding="utf-8")
    if len(sys.argv)>1 and sys.argv[1]=='_posix_gate':
        return load('posix_group_lease').gate(int(sys.argv[2]),sys.argv[3],sys.argv[4:])
    if len(sys.argv)>1 and sys.argv[1]=='_gate':
        if sys.stdin.buffer.read(1)!=b'G':return 1
        child=subprocess.Popen(sys.argv[2:],stdin=subprocess.DEVNULL)
        return child.wait()
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt',type=Path,required=True);parser.add_argument('--lease',type=Path,required=True)
    parser.add_argument('--grace',type=float,default=2);parser.add_argument('command',nargs=argparse.REMAINDER)
    args=parser.parse_args();command=args.command
    if command[:1]==['--']:command=command[1:]
    if not command or not 0<=args.grace<=10:parser.error('command and bounded grace required')
    return guard(command,args.receipt,args.lease,args.grace)


if __name__=='__main__':raise SystemExit(main())
