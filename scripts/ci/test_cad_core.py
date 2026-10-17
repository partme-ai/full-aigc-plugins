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

    def test_part_dimensions_have_real_part_geometry(self):
        path = ROOT / 'full-aigc-skills-repositories/cadcraft-skills/skills/cadcraft-dimension-part/references/craft-steps.json'
        if not path.exists():
            self.skipTest('Source checkout is unavailable')
        recipe = json.loads(path.read_text())
        self.assertEqual(sum(step['command'] == 'circle' for step in recipe['steps']), 2, 'Hole dimensions require actual circles')
        self.assertEqual(sum(step['command'].startswith('dim') for step in recipe['steps']), 4)
        self.assertEqual(recipe['assertions']['dimensionValues'], [80, 40, 40, 5])

    def test_layer_cleanup_reads_layer_state_before_editing(self):
        path = ROOT / 'full-aigc-skills-repositories/cadcraft-skills/skills/cadcraft-layer-cleanup/references/craft-steps.json'
        if not path.exists():
            self.skipTest('Source checkout unavailable')
        recipe = json.loads(path.read_text())
        self.assertEqual(recipe['steps'][0]['command'], 'layer', 'Entity-only inspection does not enumerate layer properties')
        self.assertEqual(recipe['steps'][1]['command'], 'getvar')

    def test_identical_revisions_do_not_request_a_change_region(self):
        path = ROOT / 'full-aigc-skills-repositories/cadcraft-skills/skills/cadcraft-compare-revisions/references/craft-steps.json'
        if not path.exists():
            self.skipTest('Source checkout unavailable')
        recipe = json.loads(path.read_text())
        step = next(row for row in recipe['steps'] if row['command'] == 'compare.next')
        self.assertEqual(step.get('when'), 'comparison_has_regions')

    def test_sheet_export_checks_units_before_plot(self):
        path = ROOT / 'full-aigc-skills-repositories/cadcraft-skills/skills/cadcraft-sheet-export/references/craft-steps.json'
        if not path.exists():
            self.skipTest('Source checkout unavailable')
        recipe = json.loads(path.read_text())
        self.assertEqual(recipe['steps'][0]['command'], 'getvar')
        self.assertEqual(recipe['steps'][0]['params']['name'], 'INSUNITS')
        plot = next(s['params'] for s in recipe['steps'] if s['command'] == 'plot')
        self.assertFalse(plot['fit'])
        self.assertEqual(plot['scale'], '1:50')

if __name__ == '__main__':
    unittest.main()
