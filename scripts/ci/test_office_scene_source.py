"""生成配方在任意目录仍解析同一技能源，而不是猜目录层级。"""
from pathlib import Path
import tempfile
import unittest
from office_playbook_smoke import source_skills
class SourceDirectoryTests(unittest.TestCase):
    def test_explicit_relative_source_is_resolved_from_recipe_file(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);skills=root/'source/skills';skills.mkdir(parents=True);recipe=root/'output/generated.json';recipe.parent.mkdir()
            self.assertEqual(source_skills(recipe,{'sourceSkills':'../source/skills'}),skills.resolve())
    def test_existing_in_skill_recipe_layout_keeps_source_root(self):
        p=Path('/tmp/example/skills/wordcraft-scenario-playbooks/references/recipes.json')
        self.assertEqual(source_skills(p,{}),Path('/tmp/example/skills').resolve())
