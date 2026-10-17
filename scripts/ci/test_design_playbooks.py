import unittest
from design_playbook_smoke import verify,verify_table


def doc(story):return {'pageCount':1,'settings':{'pageWidth':595,'pageHeight':842},'spreads':[{'items':[{'id':8,'bounds':[42,100,553,520]}]}],'stories':[story]}


class DesignChecks(unittest.TestCase):
    def test_thread_requires_both_frames_in_order(self):
        s={'overset':False,'frames':[8,9]};a={'pages':1,'size':[595,842],'frameCount':1,'thread':['left','right']};b={'left':{'id':8},'right':{'id':9}}
        verify(doc(s),[],b,a);s['frames']=[9,8]
        with self.assertRaisesRegex(AssertionError,'threaded story'):verify(doc(s),[],b,a)
    def test_overset_is_not_silently_accepted(self):
        with self.assertRaisesRegex(AssertionError,'remains overset'):verify(doc({'overset':True}),[],{}, {'pages':1,'size':[595,842],'frameCount':1})
    def test_wrong_cell_values_fail(self):
        t={'rows':[{},{}],'columns':[{},{}],'headerRows':1,'cells':[{'text':x} for x in ['Plan','Price','A','19']]};a={'rows':2,'columns':2,'headerRows':1,'cells':['Plan','Price','A','19']};verify_table(t,a);t['cells'][-1]['text']='190'
        with self.assertRaisesRegex(AssertionError,'cell text'):verify_table(t,a)
    def test_old_brand_must_not_remain(self):
        with self.assertRaisesRegex(AssertionError,'Old brand'):verify(doc({'overset':False}),[{'text':'ACME'}],{}, {'pages':1,'size':[595,842],'frameCount':1,'absent':['ACME']})


if __name__=='__main__':unittest.main()
