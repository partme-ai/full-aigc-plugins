"""在冻结的读取根内安全读取素材，拒绝链接竞态、非普通文件及超限内容。"""
from contextlib import contextmanager
import hashlib
import os
from pathlib import Path
import stat

MAX_BYTES = 64 * 1024 * 1024

def normalize_roots(values):
    """规范化可信调用层的绝对读取根；模型计划不能提供该参数。"""
    if not isinstance(values, (list, tuple)) or len(values) > 256:
        raise ValueError('asset_read_roots_invalid')
    roots = []
    for value in values:
        if not isinstance(value, (str, Path)) or not str(value) or any(ord(c) < 32 for c in str(value)):
            raise ValueError('asset_read_roots_invalid')
        path = Path(value)
        if not path.is_absolute():
            raise ValueError('asset_read_roots_invalid')
        roots.append(str(path.resolve()))
    return tuple(sorted(set(roots)))

@contextmanager
def opened_authorized(path, roots, identity=None):
    """持有授权普通文件描述符；逐目录不跟随链接，核对身份及读期间变化。"""
    path = Path(path).resolve()
    if not any(path.is_relative_to(Path(root)) for root in roots):
        raise ValueError('asset_read_outside_root')
    descriptor = None
    try:
        descriptor = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
        for component in path.parts[1:-1]:
            child = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
        file_descriptor = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=descriptor)
        os.close(descriptor)
        descriptor = file_descriptor
        before = os.fstat(descriptor)
        actual = (before.st_dev, before.st_ino)
        if not stat.S_ISREG(before.st_mode):
            raise ValueError('asset_path_invalid')
        if identity is not None and tuple(identity) != actual:
            raise ValueError('asset_input_identity_changed')
        yield descriptor, before, actual
        after = os.fstat(descriptor)
        if (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (after.st_size, after.st_mtime_ns, after.st_ctime_ns):
            raise ValueError('asset_input_identity_changed')
    except OSError:
        raise ValueError('asset_path_invalid') from None
    finally:
        if descriptor is not None:
            os.close(descriptor)

def read_authorized(path, roots, identity=None):
    """返回授权素材的字节及设备/inode；保留素材原有64MiB内容上限。"""
    with opened_authorized(path, roots, identity) as (descriptor, before, actual):
        if before.st_size > MAX_BYTES:
            raise ValueError('asset_digest_mismatch')
        chunks = []
        size = 0
        while True:
            block = os.read(descriptor, min(1024 * 1024, MAX_BYTES + 1 - size))
            if not block:
                break
            size += len(block)
            if size > MAX_BYTES:
                raise ValueError('asset_digest_mismatch')
            chunks.append(block)
        return b''.join(chunks), actual

def digest_authorized(path, roots, identity=None, target=None):
    """流式校验或复制显式登记文件；不额外限制原生命令入口的工程大小。"""
    with opened_authorized(path, roots, identity) as (descriptor, _, actual):
        digest = hashlib.sha256()
        stream = None
        try:
            if target is not None:
                stream = Path(target).open('xb')
            while True:
                block = os.read(descriptor, 1024 * 1024)
                if not block:
                    break
                digest.update(block)
                if stream is not None:
                    stream.write(block)
        finally:
            if stream is not None:
                stream.close()
        return digest.hexdigest(), actual
