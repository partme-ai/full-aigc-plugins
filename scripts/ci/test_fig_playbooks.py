import unittest
from fig_playbook_smoke import verify


class FigChecks(unittest.TestCase):
    def test_parent_membership_is_not_optional(self):
        with self.assertRaisesRegex(AssertionError,'outside target frame'):
            verify({'root':{'width':390,'height':884,'children':[]}}, {'label':{'id':27}}, {'rootSize':[390,884],'children':['label']})
    def test_auto_layout_field_is_not_enough(self):
        root={'width':640,'height':96,'layout':{'mode':'horizontal','gap':24},'children':[{'id':11},{'id':12}]}
        ns={'root':root,'a':{'x':24,'width':130},'b':{'x':175,'width':80}}
        with self.assertRaisesRegex(AssertionError,'Actual auto layout spacing'):
            verify(ns,{'a':{'id':11},'b':{'id':12}}, {'rootSize':[640,96],'children':[], 'layout':{'mode':'horizontal','gap':24}} | {'children':['a','b']})
    def test_fill_width_is_measured(self):
        with self.assertRaisesRegex(AssertionError,'Fill width'):
            verify({'root':{'width':640,'height':220},'child':{'width':312,'x':24}}, {}, {'rootSize':[640,220],'fillWidths':{'child':592}})


if __name__=='__main__':unittest.main()
