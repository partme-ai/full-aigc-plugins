"""发行升级预检的模拟 Git 边界；不建立仓库、不发布。"""
import hashlib,importlib.util,json
from pathlib import Path
import shutil,tempfile,unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]

class ReleaseUpgrade(unittest.TestCase):
    def test_prepare_binds_tag_commit_and_preserves_user_changes(self):
        spec=importlib.util.spec_from_file_location('upgrade',ROOT/'scripts/release_upgrade.py')
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)/'plugin';shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('__pycache__'))
            suite=json.loads((root/'source-suite.json').read_text());suite['version']='0.1.0-dev.2'
            commit='a'*40;tag='v'+suite['version']
            blobs={str(path.relative_to(root/'skills')):path.read_bytes() for path in (root/'skills').rglob('*') if path.is_file()}
            changed=next(key for key in blobs if key.endswith('SKILL.md'));blobs[changed]+=b'\n'
            def git(source,*args,binary=False):
                if args[0]=='rev-parse':return commit
                if args[0]=='remote':return 'https://github.com/full-aigc-skills/lightcraft-skills.git'
                if args[0]=='ls-tree':return '\n'.join('skills/'+key for key in blobs)
                if args[0]=='show' and args[1].endswith(':skill-suite.json'):return json.dumps(suite)
                if args[0]=='show':return blobs[args[1].split(':skills/',1)[1]]
                raise AssertionError(args)
            with patch.object(m,'ROOT',root),patch.object(m,'git',side_effect=git):
                history=root/'source-migrations';history.mkdir(exist_ok=True)
                (history/'existing.json').write_text('{"status":"APPLIED_HOST_NOT_VERIFIED"}\n')
                history_before={f.name:f.read_bytes() for f in history.iterdir() if f.is_file()}
                before=(root/'candidate-source.json').read_bytes()
                result=m.prepare(Path(temporary)/'source',tag,commit)
                self.assertEqual(result['changed'],[changed])
                self.assertEqual(result['newSource']['skillFileSha256'][changed],hashlib.sha256(blobs[changed]).hexdigest())
                self.assertEqual(result['hostUpdate'],'NOT_RUN')
                self.assertEqual(before,(root/'candidate-source.json').read_bytes())
                self.assertEqual(history_before,{f.name:f.read_bytes() for f in history.iterdir() if f.is_file()})
                with self.assertRaisesRegex(ValueError,'tag_commit'):m.prepare(root,tag,'b'*40)
                (root/'skills'/changed).write_bytes(b'user change')
                with self.assertRaisesRegex(ValueError,'preserve_modified'):m.prepare(root,tag,commit)

if __name__=='__main__':unittest.main()
