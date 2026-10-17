"""报价单业务输入与十进制计算回归。"""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
HOME=Path(__file__).resolve().parents[1]/'skills/wordcraft-quotation'
spec=importlib.util.spec_from_file_location('quote',HOME/'scripts/quotation.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class QuotationTests(unittest.TestCase):
    def setUp(self):self.data=json.loads((HOME/'assets/example-input.json').read_text())
    def test_native_editable_table_and_exact_total(self):
        p=m.compile_quote(self.data)
        self.assertEqual(p['total'],'2740.80');self.assertEqual(p['itemCount'],2)
        self.assertIn({'command':'table.fromText','params':{'separator':'tab'}},p['steps'])
        self.assertTrue(any(s['command']=='text.insert' and '2500.20' in s['params']['text'] for s in p['steps']))
    def test_decimal_prices_do_not_accumulate_binary_float_error(self):
        self.data['items']=[{'description':'A','quantity':3,'unit_price':'0.10'}];self.data['expected_total']='0.30'
        self.assertEqual(m.compile_quote(self.data)['total'],'0.30')
    def test_mismatch_negative_nan_float_and_bool_rejected(self):
        for price in ['-1','NaN','Infinity','1.001',0.1]:
            data=copy.deepcopy(self.data);data['items'][0]['unit_price']=price
            with self.subTest(price=price),self.assertRaises(ValueError):m.compile_quote(data)
        self.data['expected_total']='1.00'
        with self.assertRaisesRegex(ValueError,'不一致'):m.compile_quote(self.data)
        del self.data['expected_total'];self.data['items'][0]['quantity']=True
        with self.assertRaises(ValueError):m.compile_quote(self.data)
    def test_table_delimiters_and_unknown_fields_rejected(self):
        self.data['items'][0]['description']='A\tB'
        with self.assertRaises(ValueError):m.compile_quote(self.data)
        self.data['extra']='invented'
        with self.assertRaises(ValueError):m.compile_quote(self.data)
    def test_invalid_input_creates_no_output_and_never_needs_cli(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);source=root/'input.json';self.data['expected_total']='0.00';source.write_text(json.dumps(self.data));out=root/'steps.json'
            result=subprocess.run([sys.executable,str(HOME/'scripts/quotation.py'),'--input',str(source),'--output',str(out),'--save',str(root/'result.docx'),'--cli','nonexistent'],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0);self.assertFalse(out.exists());self.assertFalse((root/'result.docx').exists())
    def test_every_row_has_explicit_break_protection_and_numeric_alignment(self):
        p=m.compile_quote(self.data)
        protected=[s for s in p['steps'] if s['command']=='table.properties' and s['params'].get('allowBreak') is False]
        self.assertEqual(len(protected),4)
        widths=[s['params']['width'] for s in p['steps'] if s['command']=='table.columnWidth']
        self.assertEqual(widths,[250,45,75,81])
        self.assertEqual(sum(s['command']=='para.align' and s['params'].get('value')=='right' for s in p['steps']),3)
if __name__=='__main__':unittest.main()
