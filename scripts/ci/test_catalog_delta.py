import unittest
from craft_catalog_delta import compare


class CatalogDeltaTest(unittest.TestCase):
    def test_state_change_is_not_new_capability(self):
        a = [{'id': 'undo', 'params': '{}', 'enabled': False, 'disabled_reason': 'empty'}]
        b = [{'id': 'undo', 'params': '{}', 'enabled': True, 'disabled_reason': None}]
        self.assertEqual(compare(a, b)['contractsChanged'], [])

    def test_removed_and_changed_parameters_are_reported(self):
        d = compare([{'id': 'old'}, {'id': 'run', 'params': '{x}'}],
                    [{'id': 'run', 'params': '{x,y}'}, {'id': 'new'}])
        self.assertEqual(d['added'], ['new'])
        self.assertEqual(d['removed'], ['old'])
        self.assertEqual(d['contractsChanged'][0]['id'], 'run')

    def test_tool_schemas_compared(self):
        d = compare([{'name': 'execute', 'inputSchema': {'type': 'object'}}],
                    [{'name': 'execute', 'inputSchema': {'type': 'object', 'required': ['id']}}])
        self.assertEqual(len(d['contractsChanged']), 1)

    def test_duplicate_ids_are_not_silently_overwritten(self):
        with self.assertRaises(ValueError):
            compare([{'id': 'run'}, {'id': 'run'}], [])
