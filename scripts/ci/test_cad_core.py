"""CAD核心房间流程必须提供完整门洞、两个真实尺寸和新建边界。"""
import json
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[3]

class CoreFloorPlanTests(unittest.TestCase):
    def test_floorplan_is_more_than_a_closed_rectangle(self):
        path = ROOT / 'full-aigc-skills-repositories/cadcraft-skills/skills/cadcraft-floor-plan/references/craft-steps.json'
        if not path.exists():
            self.skipTest('Standalone source checkout not present; native CI validates the pinned scene-source copy')
        recipe = json.loads(path.read_text())
        steps = recipe['steps']
        dimensions = [step['params'] for step in steps if step['command'] == 'dimlinear']
        self.assertEqual(len(dimensions), 2, 'Room width and height need native dimensions')
        self.assertTrue(any(step['command'] == 'arc' for step in steps), 'Door swing is missing')
        self.assertFalse(any(step['command'] == 'pline' and step['params'].get('closed') for step in steps), 'Closed room contour obstructs the door gap')
        self.assertTrue(all(step.get('newDocumentOnly') for step in steps if step['command'] in ['new', 'setvar']))
        self.assertEqual(recipe['assertions']['doorGap'], [2000, 3000])

if __name__ == '__main__':
    unittest.main()
