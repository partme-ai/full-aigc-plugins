import importlib.util
from pathlib import Path
import unittest
spec=importlib.util.spec_from_file_location('form_request',Path(__file__).parents[1]/'scripts/form_request.py')
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
class FormRequestTests(unittest.TestCase):
    def fields(self):return {'fields':[{'name':'customer.name','type':'text','read_only':False,'required':True,'multiline':False},{'name':'consent','type':'checkbox','read_only':False,'required':False}]}
    def test_exact_values_and_doc(self):
        r=m.build_request(self.fields(),{'customer.name':' 张三 '},7)
        self.assertEqual(r['arguments'],{'doc':7,'values':{'customer.name':' 张三 '}})
    def test_unknown_field(self):
        with self.assertRaises(ValueError):m.build_request(self.fields(),{'CustomerName':'A'},1)
    def test_read_only(self):
        d=self.fields();d['fields'][0]['read_only']=True
        with self.assertRaises(ValueError):m.build_request(d,{'customer.name':'A'},1)
    def test_checkbox_boolean(self):
        self.assertIs(m.build_request(self.fields(),{'consent':False},1)['arguments']['values']['consent'],False)
        with self.assertRaises(ValueError):m.build_request(self.fields(),{'consent':'false'},1)
    def test_required_blank(self):
        with self.assertRaises(ValueError):m.build_request(self.fields(),{'customer.name':' '},1)
    def test_singleline(self):
        with self.assertRaises(ValueError):m.build_request(self.fields(),{'customer.name':'A\nB'},1)
    def test_signature_not_fill(self):
        d=self.fields();d['fields'][0]['type']='signature'
        with self.assertRaises(ValueError):m.build_request(d,{'customer.name':'A'},1)
    def test_doc_and_empty_values(self):
        for doc in (True,0,-1):
            with self.subTest(doc=doc),self.assertRaises(ValueError):m.build_request(self.fields(),{'consent':True},doc)
        with self.assertRaises(ValueError):m.build_request(self.fields(),{},1)
    def test_duplicate_names(self):
        d=self.fields();d['fields'].append(d['fields'][0].copy())
        with self.assertRaises(ValueError):m.build_request(d,{'customer.name':'A'},1)
if __name__=='__main__':unittest.main()
