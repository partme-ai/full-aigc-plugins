import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('data_story',Path(__file__).parents[1]/'scripts/data_story.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class DataStoryTests(unittest.TestCase):
    def fixture(self):
        return dict(title='本月签约额增长',unit='万元',period='2026年9至10月',source='已核对合同台账',definition='已签合同金额，不含意向',limitations='不代表已回款',action='核查回款计划',categories=['9月','10月'],series=[{'name':'签约额','values':[21,42]}])
    def test_values_and_provenance(self):
        p=module.compile_story(self.fixture())
        self.assertEqual(p['commands'][2]['params']['series'][0]['values'],[21,42])
        self.assertIn('万元',p['commands'][1]['params']['title'])
        self.assertIn('已核对合同台账',p['commands'][4]['params']['text'])
        self.assertEqual(p['commands'][0]['command'],'file.new')
        self.assertEqual(p['commands'][3],{'command':'chart.options','params':{'title':'2026年9至10月','dataLabels':True,'gridlines':True,'legend':'r'}})
    def test_missing_values_are_not_zero(self):
        d=self.fixture();d['series'][0]['values']=[21,None]
        with self.assertRaises(ValueError):module.compile_story(d)
    def test_reject_mismatch_bool_nan(self):
        for values in ([21],[True,2],[float('nan'),2],[float('inf'),2]):
            d=self.fixture();d['series'][0]['values']=values
            with self.subTest(values=values),self.assertRaises(ValueError):module.compile_story(d)
    def test_reject_ambiguous_categories(self):
        for categories in (['A','A'],['A','A\nB'],[],['A']*13):
            d=self.fixture();d['categories']=categories
            with self.subTest(categories=categories),self.assertRaises(ValueError):module.compile_story(d)
    def test_negative_and_zero_preserved(self):
        d=self.fixture();d['series'][0]['values']=[-2,0]
        self.assertEqual(module.compile_story(d)['commands'][2]['params']['series'][0]['values'],[-2,0])
    def test_required_source_and_limits(self):
        for field in ('source','unit','definition','limitations','period'):
            d=self.fixture();d[field]=''
            with self.subTest(field=field),self.assertRaises(ValueError):module.compile_story(d)

if __name__=='__main__':unittest.main()
