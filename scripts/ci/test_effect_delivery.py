"""片头片尾的时间与内容检查，拒绝静帧冒充动画。"""
import unittest
import os
from pathlib import Path
import json
from effect_delivery_smoke import verify_countdown, verify_credit_motion, verify_chapter

class EffectDeliveryTests(unittest.TestCase):
    def test_three_scenes_are_independently_distributed(self):
        root=Path(os.environ.get('CRAFT_EFFECT_SKILLS_ROOT',Path(__file__).resolve().parents[3]/'full-aigc-skills-repositories/effectcraft-skills/skills'))
        for name in ['chapter-card','countdown-intro','credits-roll']:
            skill=root/('effectcraft-'+name)
            self.assertTrue((skill/'SKILL.md').is_file(),name+' missing independent skill')
            recipe=json.loads((skill/'references/craft-steps.json').read_text())
            self.assertGreater(len(recipe['steps']),5)

    def test_countdown_rejects_overlapping_digits(self):
        with self.assertRaisesRegex(AssertionError,'timing'):
            verify_countdown({'Three':('3',0,2),'Two':('2',1,2),'One':('1',2,3),'Start':('START',3,4)},['a','a','b','b','c','c','d','d'])

    def test_static_countdown_frame_fails(self):
        with self.assertRaisesRegex(AssertionError,'distinct'):
            verify_countdown({'Three':('3',0,1),'Two':('2',1,2),'One':('1',2,3),'Start':('START',3,4)},['a']*8)

    def test_credit_scroll_rejects_static_position(self):
        with self.assertRaisesRegex(AssertionError,'scroll'):
            verify_credit_motion([[960,1180,0],[960,1180,0],[960,1180,0]],1180)

    def test_credit_scroll_rejects_wrong_direction(self):
        with self.assertRaisesRegex(AssertionError,'scroll'):
            verify_credit_motion([[960,1180,0],[960,2195,0],[960,3210,0]],1180)

    def test_chapter_rejects_missing_subtitle(self):
        with self.assertRaisesRegex(AssertionError,'subtitle'):
            verify_chapter([0,100,100],[0,0,0],[0,100,100])

    def test_expected_values_pass(self):
        verify_countdown({'Three':('3',0,1),'Two':('2',1,2),'One':('1',2,3),'Start':('START',3,4)},['a','a','b','b','c','c','d','d'])
        verify_credit_motion([[960,1180,0],[960,165,0],[960,-850,0]],1180)
        verify_chapter([0,100,100],[0,100,100],[0,100,100])
