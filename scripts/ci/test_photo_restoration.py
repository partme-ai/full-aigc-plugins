import unittest
import json
import os
from pathlib import Path
from photo_restoration_smoke import verify_local_repair

class RestorationTests(unittest.TestCase):
    def test_independent_restore_skill_contains_exact_canonical_plan(self):
        root=Path(os.environ.get('CRAFT_PHOTO_SKILLS_ROOT',Path(__file__).resolve().parents[3]/'full-aigc-skills-repositories/photocraft-skills/skills'))
        plan=root/'photocraft-restore-old-photo/references/restoration-plan.json'
        self.assertTrue(plan.is_file(),'Independent old-photo skill lacks concrete phase plan')
        data=json.loads(plan.read_text(encoding='utf-8'))
        canonical=next(x for x in json.loads((root/'photocraft-scenario-playbooks/references/recipes.json').read_text(encoding='utf-8'))['recipes'] if x['id']=='old-photo-conservative')
        self.assertEqual(data['canonicalRecipeId'],canonical['id'])
        self.assertEqual([step for phase in data['phases'] for step in phase['steps']],canonical['steps'])
        self.assertTrue(data['countsAsNewScene'] is False)

    def test_unchanged_damage_is_rejected(self):
        with self.assertRaisesRegex(AssertionError,'reduce'):
            verify_local_repair(bytes([90]*36),bytes([255]*36),bytes([255]*36),4,[(1,0,3,3)])

    def test_repair_outside_damage_regions_is_rejected(self):
        clean=bytes([90]*36);damaged=bytearray(clean);damaged[3:6]=b'\xff'*3;repaired=bytearray(clean);repaired[0]=50
        with self.assertRaisesRegex(AssertionError,'protected'):
            verify_local_repair(clean,bytes(damaged),bytes(repaired),4,[(1,0,2,1)])

    def test_local_repair_with_preserved_surroundings_passes(self):
        clean=bytes([90]*36);damaged=bytearray(clean);damaged[3:6]=b'\xff'*3
        result=verify_local_repair(clean,bytes(damaged),clean,4,[(1,0,2,1)])
        self.assertEqual(result['targetErrorAfter'],0)
