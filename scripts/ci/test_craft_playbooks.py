"""场景分发负例：未知方法、错误PDF参数和越界引用必须拒绝。"""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('playbooks',Path(__file__).resolve().parents[1]/'validate-craft-playbooks.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)


class PlaybookContractTests(unittest.TestCase):
    def fixture(self,path):
        (path/'references').mkdir()
        (path/'SKILL.md').write_text('---\nname: pdf-test\ndescription: test\n---\n[步骤](references/craft-steps.json)\n')
        step={'id':'pdf-edit','check':'reopen','boundary':'preserve original','steps':[{'command':'doc_info','params':{'doc':1}}]}
        (path/'references/craft-steps.json').write_text(json.dumps(step))
        evidence={'observedCommands':{'doc_info':{'input_schema':{'type':'object','properties':{'doc':{'type':'integer'}},'required':['doc'],'additionalProperties':False}}}}
        (path/'references/craft-command-evidence.json').write_text(json.dumps(evidence))
        (path/'references/workflow-sources.json').write_text(json.dumps({'sources':[{'commit':'a'*40,'readFiles':[{'path':'docs.md'}]}]}))

    def test_valid_self_contained_recipe(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);self.fixture(p)
            self.assertEqual(module.validate_skill(p),([],1))

    def test_unknown_method_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);self.fixture(p);f=p/'references/craft-steps.json';d=json.loads(f.read_text());d['steps'][0]['command']='photoshop.fakeRepair';f.write_text(json.dumps(d))
            errors,_=module.validate_skill(p);self.assertTrue(any('unknown method' in e for e in errors))

    def test_document_id_parameter_cannot_be_guessed(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);self.fixture(p);f=p/'references/craft-steps.json';d=json.loads(f.read_text());d['steps'][0]['params']={'document':1};f.write_text(json.dumps(d))
            errors,_=module.validate_skill(p);self.assertTrue(any('parameters mismatch' in e for e in errors))

    def test_cross_skill_reference_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);self.fixture(p);(p/'SKILL.md').write_text('[wrong](../other/SKILL.md)')
            errors,_=module.validate_skill(p);self.assertTrue(any('invalid local reference' in e for e in errors))

if __name__=='__main__':unittest.main()
