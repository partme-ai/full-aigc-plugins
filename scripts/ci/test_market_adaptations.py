"""商店适配不能用未知方法或缺失来源冒充现有可执行配方。"""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('playbooks', Path(__file__).resolve().parents[1] / 'validate-craft-playbooks.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

class MarketAdaptationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'SKILL.md').write_text('---\nname: fixture\ndescription: fixture\n---\n')
        (self.root / 'references').mkdir()
        self.data = {
            'schema': 'craft-market-adaptations/v1',
            'sources': [{'id':'skillhub:example', 'market':'SkillHub', 'version':'1.0', 'sha256':'a'*64, 'downloadUrl':'https://api.skillhub.cn/api/v1/download?slug=example'}],
            'adaptations':[{'id':'existing', 'sourceIds':['skillhub:example'], 'adaptation':'按实际任务适配', 'taskCheck':'检查结果', 'capabilityBoundary':'只检查已知能力', 'execution':'REFERENCE_ADAPTATION_NOT_NEW_RUNTIME_ACCEPTANCE', 'recipe':{'id':'existing','steps':[{'command':'inspect','params':{}}]}}],
            'observedCommands':{'inspect':{'input_schema':{'type':'object','properties':{},'additionalProperties':False}}}
        }
    def validate(self):
        (self.root / 'references/market-adaptations.json').write_text(json.dumps(self.data))
        return checker.validate_skill(self.root)[0]
    def test_existing_recipe_is_not_counted_as_new_scene(self):
        self.assertEqual(self.validate(), [])
        self.assertEqual(checker.validate_skill(self.root)[1],0)
    def test_unknown_method_is_rejected(self):
        self.data['adaptations'][0]['recipe']['steps'][0]['command']='invented.autoFixEverything'
        self.assertTrue(self.validate())
    def test_missing_market_source_is_rejected(self):
        self.data['adaptations'][0]['sourceIds']=['unknown']
        self.assertTrue(self.validate())
    def test_source_without_content_hash_is_rejected(self):
        self.data['sources'][0]['sha256']='not-a-digest'
        self.assertTrue(self.validate())
    def test_foreign_parameters_are_rejected(self):
        self.data['adaptations'][0]['recipe']['steps'][0]['params']={'adobePreset':True}
        self.assertTrue(self.validate())

if __name__ == '__main__': unittest.main()
