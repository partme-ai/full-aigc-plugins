import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
def load(name,root=ROOT):
    spec=importlib.util.spec_from_file_location(name,root/'scripts'/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class Updates(unittest.TestCase):
    def test_compatibility_manifest_is_generated_from_portable(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)/'plugin';shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('__pycache__','.DS_Store','.git','node_modules','.local','dist'))
            generated=load('generate_host_manifest',root).generate();portable=json.loads((root/'plugin.json').read_text());self.assertEqual(generated['name'],portable['name']);self.assertEqual(generated['version'],portable['version']);self.assertEqual(generated['skills'],'./skills/')
    def test_update_preserves_user_data_rejects_rollback_and_legacy(self):
        with tempfile.TemporaryDirectory() as t:
            base=Path(t);old=base/'old';new=base/'new';data=base/'tasks';data.mkdir();(data/'receipt.json').write_text('user task survives')
            for target in (old,new):shutil.copytree(ROOT,target,ignore=shutil.ignore_patterns('__pycache__','.DS_Store','.git','node_modules','.local','dist'))
            p=new/'plugin.json';manifest=json.loads(p.read_text());prefix,number=manifest['version'].rsplit('.',1);manifest['version']=prefix+'.'+str(int(number)+1);p.write_text(json.dumps(manifest));lockpath=new/'source-release.lock.json';lock=json.loads(lockpath.read_text());lock['pluginVersion']=manifest['version'];lockpath.write_text(json.dumps(lock));load('generate_host_manifest',new).generate()
            m=load('check_update');self.assertEqual(m.check(old,new,data)['status'],'UPDATE_ELIGIBLE');self.assertEqual((data/'receipt.json').read_text(),'user task survives')
            with self.assertRaisesRegex(ValueError,'rollback'):m.check(new,old,data)
            manifest['extensions']['org.full-aigc.printcraft']['contracts']['execution']='printcraft.execution/2';p.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError,'incompatible'):m.check(old,new,data)
    def test_missing_replaced_component_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)/'plugin';shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('__pycache__','.DS_Store','.git','node_modules','.local','dist'));(root/'skills/printcraft-harness').rename(root/'skills/printcraft-foreign')
            with self.assertRaisesRegex(ValueError,'skill_set_mismatch'):load('validate_package',root).validate()
if __name__=='__main__':unittest.main()

class ReleaseHostManifests(unittest.TestCase):
    def test_marketplace_host_metadata_is_generated_without_identity_drift(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)/'plugin';shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('__pycache__','.DS_Store','.git','node_modules','.local','dist'))
            load('generate_host_manifest',root).generate()
            portable=json.loads((root/'plugin.json').read_text())
            for relative in ('.claude-plugin/plugin.json','kimi.plugin.json'):
                host=json.loads((root/relative).read_text())
                self.assertEqual((host['name'],host['version']),(portable['name'],portable['version']))
                self.assertEqual(host['skills'],'./skills/')

    def test_generated_host_identity_drift_blocks_packaging(self):
        for relative in ('.claude-plugin/plugin.json','kimi.plugin.json'):
            with self.subTest(host=relative),tempfile.TemporaryDirectory() as t:
                root=Path(t)/'plugin';shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('__pycache__','.DS_Store','.git','node_modules','.local','dist'))
                path=root/relative;data=json.loads(path.read_text());data['version']='9.9.9';path.write_text(json.dumps(data))
                with self.assertRaisesRegex(ValueError,'host_manifest_drift'):load('validate_package',root).validate()

class OptionalOcrContractCompatibility(unittest.TestCase):
    def test_known_optional_ocr_contracts_extend_core_without_rejecting_old(self):
        m=load('check_update')
        core={'execution':'printcraft.execution/1','verification':'printcraft.verification/1'}
        def manifest(contracts):return {'extensions':{'org.full-aigc.printcraft':{'contracts':contracts}}}
        m.validate_contracts(manifest(core))
        current=dict(core,ocr='printcraft.ocr/1',ocrBackend='printcraft.ocr-backend/1')
        m.validate_contracts(manifest(current))
        for key,value in [('execution','printcraft.execution/2'),('ocr','printcraft.ocr/2'),('unknown','x')]:
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'incompatible'):
                m.validate_contracts(manifest(dict(current,**{key:value})))
