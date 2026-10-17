"""片段存在不能代替定格、画中画或J-cut的结果。"""
import os
import json
from pathlib import Path
import unittest

class FilmDeliveryTests(unittest.TestCase):
    def test_three_scenes_are_independently_installable(self):
        root=Path(os.environ.get('CRAFT_FILM_SKILLS_ROOT',Path(__file__).resolve().parents[3]/'full-aigc-skills-repositories/filmcraft-skills/skills'))
        for name in ['freeze-explainer','presenter-inset','jcut-dialogue']:
            skill=root/('filmcraft-'+name)
            self.assertTrue((skill/'SKILL.md').is_file(),name+' missing standalone skill')
            recipe=json.loads((skill/'references/craft-steps.json').read_text(encoding='utf-8'))
            self.assertGreater(len(recipe['steps']),5)

    def test_frozen_first_frame_instead_of_selected_frame_is_rejected(self):
        from film_delivery_smoke import verify_hold
        with self.assertRaisesRegex(AssertionError,'selected'):
            verify_hold('wanted',['first','first','first'],'before','after')

    def test_hold_that_never_resumes_is_rejected(self):
        from film_delivery_smoke import verify_hold
        with self.assertRaisesRegex(AssertionError,'resume'):
            verify_hold('wanted',['wanted']*3,'before','wanted')

    def test_audio_that_starts_with_video_is_not_a_jcut(self):
        from film_delivery_smoke import verify_jcut
        with self.assertRaisesRegex(AssertionError,'lead'):
            verify_jcut([(0,50),(50,125)],[(0,50),(50,125)])

    def test_overlapping_dialogue_is_rejected(self):
        from film_delivery_smoke import verify_jcut
        with self.assertRaisesRegex(AssertionError,'overlap'):
            verify_jcut([(0,50),(50,125)],[(0,40),(25,125)])

    def test_full_frame_presenter_is_not_an_inset(self):
        from film_delivery_smoke import verify_inset_bounds
        with self.assertRaisesRegex(AssertionError,'PiP'):
            verify_inset_bounds([0,0,320,240])

    def test_expected_inset_bounds_pass(self):
        from film_delivery_smoke import verify_inset_bounds
        verify_inset_bounds([224,162,304,222])
