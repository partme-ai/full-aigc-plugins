"""冻结根内的目录创建与快照树复制；所有遍历均持有描述符并拒绝链接。"""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys


def checked(path):
    """只接受绝对且没有上级跳转的路径，不重新解析冻结根。"""
    value = Path(path)
    if not value.is_absolute() or '..' in value.parts or any(ord(c) < 32 for c in str(path)):
        raise ValueError('authorized_tree_outside_root')
    return value


def directory(path, root=None, exclusive=False):
    """逐层打开目录；只在显式写入根内创建，返回调用方负责关闭的描述符。"""
    path = checked(path)
    root = checked(root) if root is not None else None
    if root is not None and not path.is_relative_to(root):
        raise ValueError('authorized_tree_outside_root')
    descriptor = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
    current = Path('/')
    try:
        for index, part in enumerate(path.parts[1:], 1):
            current = current / part
            last = index == len(path.parts) - 1
            if exclusive and last:
                os.mkdir(part, 0o700, dir_fd=descriptor)
                os.fsync(descriptor)
            try:
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=descriptor)
            except FileNotFoundError:
                if root is None or not current.is_relative_to(root):
                    raise
                try:
                    os.mkdir(part, 0o700, dir_fd=descriptor)
                except FileExistsError:
                    pass
                os.fsync(descriptor)
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
        return descriptor
    except Exception:
        os.close(descriptor)
        raise


def identity(info):
    """读取期间的大小及时间变化使当前复制／摘要失效。"""
    return info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns


def walk(source, target, prefix, records):
    """不跟随链接遍历源目录；复制与摘要使用同一组实际读取字节。"""
    before = os.fstat(source)
    for name in sorted(os.listdir(source)):
        path = prefix + name
        info = os.stat(name, dir_fd=source, follow_symlinks=False)
        if stat.S_ISDIR(info.st_mode):
            child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=source)
            destination = None
            try:
                if target is not None:
                    os.mkdir(name, 0o700, dir_fd=target)
                    destination = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=target)
                walk(child, destination, path + '/', records)
            finally:
                os.close(child)
                if destination is not None:
                    os.close(destination)
        elif stat.S_ISREG(info.st_mode):
            descriptor = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=source)
            destination = None
            try:
                opened = os.fstat(descriptor)
                if not stat.S_ISREG(opened.st_mode) or identity(info) != identity(opened):
                    raise ValueError('authorized_tree_identity_changed')
                if target is not None:
                    destination = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                                          0o600, dir_fd=target)
                digest = hashlib.sha256()
                while True:
                    block = os.read(descriptor, 1024 * 1024)
                    if not block:
                        break
                    digest.update(block)
                    if destination is not None:
                        view = memoryview(block)
                        while view:
                            written = os.write(destination, view)
                            if written <= 0:
                                raise OSError('short_write')
                            view = view[written:]
                if identity(opened) != identity(os.fstat(descriptor)):
                    raise ValueError('authorized_tree_identity_changed')
                if destination is not None:
                    os.fchmod(destination, stat.S_IMODE(opened.st_mode) & 0o777)
                    os.fsync(destination)
                records[path] = digest.hexdigest()
            finally:
                os.close(descriptor)
                if destination is not None:
                    os.close(destination)
        else:
            raise ValueError('authorized_tree_entry_invalid')
    if identity(before) != identity(os.fstat(source)):
        raise ValueError('authorized_tree_identity_changed')
    if target is not None:
        os.fsync(target)


def main(request):
    """创建目录或复制／摘要快照；失败保留根内部分产物，不运行用户代码。"""
    operation = request['operation']
    if operation == 'directory':
        descriptor = directory(request['path'], request['root'], request.get('exclusive', False))
        os.close(descriptor)
        return {'result': 'PASS'}
    if operation not in ('copy-tree', 'tree-digest'):
        raise ValueError('authorized_tree_entry_invalid')
    source = directory(request['source'])
    target = None
    try:
        if operation == 'copy-tree':
            target = directory(request['target'], request['root'], True)
        records = {}
        walk(source, target, '', records)
        digest = hashlib.sha256()
        # Node相对路径排序按UTF-16代码单元；保持含非BMP文件名的技能摘要兼容。
        for name in sorted(records, key=lambda value: value.encode('utf-16-be', errors='surrogatepass')):
            digest.update((name + '\0' + records[name] + '\n').encode('utf-8'))
        result = digest.hexdigest()
        if operation == 'copy-tree' and result != request['expected']:
            raise ValueError('skill_snapshot_mismatch')
        return {'sha256': result}
    finally:
        os.close(source)
        if target is not None:
            os.close(target)


if __name__ == '__main__':
    try:
        print(json.dumps(main(json.load(sys.stdin))))
    except Exception as error:
        allowed = {'authorized_tree_outside_root', 'authorized_tree_identity_changed',
                   'authorized_tree_entry_invalid', 'skill_snapshot_mismatch'}
        code = str(error) if isinstance(error, ValueError) and str(error) in allowed else 'authorized_tree_failed'
        print(json.dumps({'error': code}))
        raise SystemExit(1)
