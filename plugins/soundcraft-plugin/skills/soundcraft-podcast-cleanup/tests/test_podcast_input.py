"""实际输入必须变成明确的轨道、时间与导出参数。"""
import copy
import importlib.util
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('podcast_input',ROOT/'scripts/podcast_input.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class InputContract(unittest.TestCase):
    def setUp(self):
        self.template=json.loads((ROOT/'references/craft-steps.json').read_text(encoding='utf-8'))
        self.data={'track':'访谈 主轨','startSeconds':12,'endSeconds':42,'fadeInSeconds':0.02,'fadeOutSeconds':0.05,'gainDb':-2.5,'output':'审核/访谈.wav'}
    def test_maps_actual_input_without_mutating_template(self):
        before=copy.deepcopy(self.template);recipe=module.build_recipe(self.data,self.template);steps=recipe['steps']
        self.assertEqual(steps[1]['params'],{'tracks':['访谈 主轨'],'start':{'seconds':12},'end':{'seconds':42}})
        self.assertEqual(steps[2]['params'],{'db':-2.5})
        self.assertEqual(steps[3]['params']['end'],{'seconds':12.02})
        self.assertEqual(steps[4]['params']['start'],{'seconds':41.95})
        self.assertEqual(steps[-1]['params']['path'],'审核/访谈.wav')
        self.assertEqual(steps[-1]['params']['start'],{'seconds':12})
        self.assertEqual(self.template,before)
        self.assertNotIn('limitedTechnicalValidation',recipe)
    def test_nonfinite_and_boolean_numbers_rejected(self):
        for key in ['startSeconds','endSeconds','fadeInSeconds','fadeOutSeconds','gainDb']:
            for value in [True,float('nan'),float('inf'),'1']:
                with self.subTest(key=key,value=value):
                    with self.assertRaises(ValueError):module.build_recipe({**self.data,key:value},self.template)
    def test_invalid_or_overlapping_fades_rejected(self):
        for changes in [{'endSeconds':12},{'startSeconds':-1},{'fadeInSeconds':-1},{'fadeOutSeconds':31},{'fadeInSeconds':20,'fadeOutSeconds':11}]:
            with self.assertRaises(ValueError):module.build_recipe({**self.data,**changes},self.template)
    def test_zero_fades_are_omitted(self):
        recipe=module.build_recipe({**self.data,'fadeInSeconds':0,'fadeOutSeconds':0},self.template)
        self.assertNotIn('edit.fades_create',[s['command'] for s in recipe['steps']])
    def test_unsafe_paths_and_empty_track_rejected(self):
        for value in ['/tmp/out.wav','C:\\out.wav','../out.wav','a/../out.wav','https://a/out.wav','a//b.wav','out.mp3']:
            with self.assertRaises(ValueError):module.build_recipe({**self.data,'output':value},self.template)
        with self.assertRaises(ValueError):module.build_recipe({**self.data,'track':'  '},self.template)
    def test_gain_bounds_and_unknown_fields_rejected(self):
        for changes in [{'gainDb':100},{'noiseReduction':True}]:
            with self.assertRaises(ValueError):module.build_recipe({**self.data,**changes},self.template)
if __name__=='__main__':unittest.main()
