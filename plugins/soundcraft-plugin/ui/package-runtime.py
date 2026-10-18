"""生成 bootstrap 可读取的确定性 USTAR 运行包，拒绝链接及覆盖已有输出。"""
import argparse
import gzip
import hashlib
from pathlib import Path
import tarfile


def package(runtime,output):
    runtime=Path(runtime).resolve();output=Path(output)
    entries=sorted(runtime.rglob('*'))
    if not entries or any(p.is_symlink() or not (p.is_file() or p.is_dir()) for p in entries):
        raise ValueError('Runtime must contain only regular files/directories')
    if output.resolve().is_relative_to(runtime):raise ValueError('Archive must be outside runtime')
    # USTAR 不生成 PAX x/g 扩展头；固定元数据使跨平台运行包可复核。
    with output.open('xb') as stream:
        with gzip.GzipFile(filename='',mode='wb',fileobj=stream,mtime=0) as compressed:
            with tarfile.open(fileobj=compressed,mode='w',format=tarfile.USTAR_FORMAT) as archive:
                for path in entries:
                    info=archive.gettarinfo(str(path),arcname=path.relative_to(runtime).as_posix())
                    info.mtime=0;info.uid=info.gid=0;info.uname=info.gname='';info.pax_headers={}
                    info.mode=0o755 if path.is_dir() else 0o644
                    if path.is_file():
                        with path.open('rb') as data:archive.addfile(info,data)
                    else:archive.addfile(info)
    return hashlib.sha256(output.read_bytes()).hexdigest()

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--runtime',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();print(package(a.runtime,a.output))
