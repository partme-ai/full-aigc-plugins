import unittest
from fig_core_smoke import verify_wireframe, verify_responsive

class FigCoreTests(unittest.TestCase):
    def test_old_wireframe_without_content_and_action_is_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'region missing'):
            verify_wireframe({'frame': {'width':1280,'height':1024,'children':[{'name':'Navigation'}]}})

    def test_fill_children_must_really_resize(self):
        nodes={'root':{'width':390,'height':884,'layout':{'mode':'vertical'}}}
        for name in ['heading','card','button']:
            nodes[name]={'x':24,'width':720,'y':24,'height':48}
        with self.assertRaisesRegex(AssertionError, 'did not fill'):
            verify_responsive(nodes,390,884)
