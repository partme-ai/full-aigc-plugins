"""宿主私有快照写入：持有目录描述符，不跟随链接或覆盖已有排他文件。"""
import base64
import hashlib
import json
import os
from pathlib import Path
import secrets
import sys


def write(request):
    """在冻结写入根内持久化字节；原子更新与首次排他创建分别处理。"""
    target = Path(request['path'])
    root = Path(request['root'])
    mode = request['mode']
    replace = request['replace']
    if (not target.is_absolute() or not root.is_absolute()
            or '..' in target.parts or '..' in root.parts
            or not target.is_relative_to(root) or target == root
            or mode not in (0o400, 0o600) or not isinstance(replace, bool)):
        raise ValueError('authorized_write_outside_root')
    data = base64.b64decode(request['base64'], validate=True)
    if len(data) > 64 * 1024 * 1024:
        raise ValueError('authorized_write_size_limit')
    descriptor = None
    created = False
    name = '.craft-state-' + secrets.token_hex(16) if replace else target.name
    try:
        descriptor = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
        for part in target.parts[1:-1]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
        destination = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                              0o600, dir_fd=descriptor)
        created = True
        with os.fdopen(destination, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fchmod(stream.fileno(), mode)
            os.fsync(stream.fileno())
            info = os.fstat(stream.fileno())
        if replace:
            os.replace(name, target.name, src_dir_fd=descriptor, dst_dir_fd=descriptor)
            created = False
        os.fsync(descriptor)
        return {'sha256': hashlib.sha256(data).hexdigest(), 'device': info.st_dev,
                'inode': info.st_ino, 'size': info.st_size}
    except Exception:
        if created:
            os.unlink(name, dir_fd=descriptor)
        raise
    finally:
        if descriptor is not None:
            os.close(descriptor)


if __name__ == '__main__':
    try:
        print(json.dumps(write(json.load(sys.stdin))))
    except Exception as error:
        allowed = {'authorized_write_outside_root', 'authorized_write_size_limit'}
        code = str(error) if isinstance(error, ValueError) and str(error) in allowed else 'authorized_write_failed'
        print(json.dumps({'error': code}))
        raise SystemExit(1)
