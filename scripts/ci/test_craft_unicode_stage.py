"""完整包不能因Git路径引用丢失中文文件。"""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import zipfile

class StageTests(unittest.TestCase):
    def test_tracked_unicode_file_and_pinned_runtime_reach_zip(self):
        source=Path(__file__).resolve().parents[1]/'stage-craft-market-release.py'
        spec=importlib.util.spec_from_file_location('unicode_craft_stage',source);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);hub=root/'hub';hub.mkdir();m.ROOT=hub
            repo=root/'full-aigc-plugins-repositories/fixture-plugin';repo.mkdir(parents=True)
            (repo/'docs').mkdir();(repo/'docs/中文说明.md').write_text('可编辑交付',encoding='utf-8');(repo/'ui').mkdir()
            runtime=root/'runtime';runtime.mkdir();(runtime/'adapter.mjs').write_text('// pinned fixture\n')
            digest=hashlib.sha256((runtime/'adapter.mjs').read_bytes()).hexdigest()
            (repo/'ui/runtime.lock.json').write_text(json.dumps({'files':{'adapter.mjs':digest}}));(repo/'ui/editor.lock.json').write_text('{}')
            subprocess.run(['git','init','-q',str(repo)],check=True);subprocess.run(['git','-C',str(repo),'add','.'],check=True)
            out=root/'release';out.mkdir();(out/'index.json').write_text(json.dumps([{'plugin':'fixture','version':'0.0.1','runtimeDirectory':str(runtime)}]))
            m.stage(out)
            with zipfile.ZipFile(out/'fixture-plugin-0.0.1.zip') as archive:
                self.assertEqual(archive.read('fixture-plugin/docs/中文说明.md').decode(),'可编辑交付')
                self.assertEqual(hashlib.sha256(archive.read('fixture-plugin/ui/dist/adapter.mjs')).hexdigest(),digest)
