"""单技能自包含的平台识别、文件互斥及 Windows 管道适配。"""
from contextlib import contextmanager
import os
from pathlib import Path
import platform
import queue
import stat
import threading
import time
import subprocess


def owned_listener(process, port):
    """只接受自有存活进程上的 IPv4 回环监听，不能以端口可达替代所有权。"""
    if process.poll() is not None:return False
    if platform.system()=='Windows':
        command='Get-NetTCPConnection -State Listen -LocalPort '+str(int(port))+' -ErrorAction SilentlyContinue | Where-Object { $_.LocalAddress -eq "127.0.0.1" -and $_.OwningProcess -eq '+str(int(process.pid))+' } | Select-Object -ExpandProperty OwningProcess'
        result=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',command],capture_output=True,text=True,timeout=5)
        return result.returncode==0 and str(process.pid) in result.stdout.split()
    if platform.system()=='Linux':
        try:
            sockets={os.readlink(p)[8:-1] for p in (Path('/proc')/str(process.pid)/'fd').iterdir() if os.readlink(p).startswith('socket:[')}
            for line in (Path('/proc')/str(process.pid)/'net/tcp').read_text(encoding='utf-8').splitlines()[1:]:
                row=line.split()
                if row[1]=='0100007F:'+format(int(port),'04X') and row[3]=='0A' and row[9] in sockets:return True
            return False
        except (OSError,IndexError):return False
    result=subprocess.run(['/usr/sbin/lsof','-nP','-a','-p',str(process.pid),'-iTCP:'+str(int(port)),'-sTCP:LISTEN','-Fn'],capture_output=True,text=True,timeout=3)
    return result.returncode==0 and ('n127.0.0.1:'+str(port)) in result.stdout.splitlines()


def platform_key(system=None, machine=None):
    """返回锁文件的平台键；拒绝未知架构，不做静默架构回退。"""
    system = (system or platform.system()).lower()
    machine = (machine or platform.machine()).lower()
    arch = {'amd64': 'x86_64', 'x64': 'x86_64', 'i386': 'x86',
            'i686': 'x86', 'aarch64': 'arm64'}.get(machine, machine)
    if system == 'linux' and arch == 'arm64':
        arch = 'aarch64'
    if system not in ('darwin', 'windows', 'linux', 'freebsd') or arch not in ('x86', 'x86_64', 'arm64', 'aarch64'):
        raise ValueError('unsupported_platform: ' + system + '-' + machine)
    return system + '-' + arch


def check_minimum(requirement):
    """在启动原生二进制前检查锁定的系统与 libc 下限。"""
    def version(value):return tuple(int(x) for x in value.split('.') if x.isdigit())
    if 'macOS' in requirement and version(platform.mac_ver()[0])<version(requirement['macOS']):
        raise ValueError('minimum_macos_required: '+requirement['macOS'])
    if 'windows' in requirement and version(platform.version())<version(requirement['windows']):
        raise ValueError('minimum_windows_required: '+requirement['windows'])
    if 'glibc' in requirement:
        kind,current=platform.libc_ver()
        if kind!='glibc' or version(current)<version(requirement['glibc']):
            raise ValueError('minimum_glibc_required: '+requirement['glibc'])


def lock_stream(stream):
    """尝试独占已打开的文件；冲突统一返回 BlockingIOError。"""
    if os.name == 'nt':
        import msvcrt
        position = stream.tell()
        stream.seek(0)
        try:
            msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError as error:
            raise BlockingIOError('lock_busy') from error
        finally:
            stream.seek(position)
    else:
        import fcntl
        fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)


def unlock_stream(stream):
    """释放本进程持有的互斥，不删除锁文件。"""
    if os.name == 'nt':
        import msvcrt
        position = stream.tell()
        stream.seek(0)
        msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
        stream.seek(position)
    else:
        import fcntl
        fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def open_regular(path, flags, mode=0o600):
    """拒绝路径中的链接、目录及 Windows 重解析点。"""
    path = Path(path).absolute()
    path = path.parent.resolve() / path.name
    for part in (path,):
        if part.is_symlink() or (hasattr(part, 'is_junction') and part.is_junction()):
            raise OSError('unsafe_link: ' + str(part))
    fd = os.open(path, flags | getattr(os, 'O_NOFOLLOW', 0), mode)
    try:
        info = os.fstat(fd)
        current = path.lstat()
        if not stat.S_ISREG(info.st_mode) or stat.S_ISLNK(current.st_mode) or (info.st_dev, info.st_ino) != (current.st_dev, current.st_ino):
            raise ValueError('not_regular_file')
        return fd
    except BaseException:
        os.close(fd)
        raise


@contextmanager
def exclusive_lock(path, timeout=120):
    """有界等待互斥，进程退出后由操作系统释放。"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with os.fdopen(open_regular(path, os.O_CREAT | os.O_RDWR), 'r+b') as stream:
        deadline = time.monotonic() + timeout
        while True:
            try:
                lock_stream(stream)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise TimeoutError('runtime_install_busy: lock_busy') from None
                time.sleep(min(.05, max(0, deadline - time.monotonic())))
        try:
            yield stream
        finally:
            unlock_stream(stream)


class PipeReader:
    """用有界队列读取管道，避免 Windows select 不支持匿名管道。"""
    def __init__(self, stream, max_bytes=64 * 1024 * 1024):
        self.stream = stream
        self.max_bytes = max_bytes
        self.items = queue.Queue(maxsize=128)
        self.buffer = b''
        self.closed = threading.Event()
        threading.Thread(target=self._read, daemon=True).start()

    def _read(self):
        try:
            while not self.closed.is_set():
                block = os.read(self.stream.fileno(), 65536)
                while not self.closed.is_set():
                    try:
                        self.items.put(block, timeout=.1)
                        break
                    except queue.Full:
                        pass
                if not block:
                    return
        except (OSError, ValueError):
            if not self.closed.is_set():
                try:
                    self.items.put(b'', timeout=.1)
                except queue.Full:
                    pass

    def readline(self, timeout):
        deadline = time.monotonic() + timeout
        while b'\n' not in self.buffer:
            try:
                block = self.items.get(timeout=max(0, deadline - time.monotonic()))
            except queue.Empty:
                raise TimeoutError('outcome_unknown: pipe_timeout') from None
            if not block:
                raise EOFError('mcp_disconnected')
            self.buffer += block
            if len(self.buffer) > self.max_bytes:
                raise ValueError('mcp_response_too_large')
        line, self.buffer = self.buffer.split(b'\n', 1)
        return line + b'\n'

    def close(self):
        self.closed.set()
