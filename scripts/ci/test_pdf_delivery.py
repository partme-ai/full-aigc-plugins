import json
import os
from pathlib import Path
import unittest

ROOT=Path(os.environ.get('CRAFT_PRINT_SKILLS_ROOT',str(Path(__file__).resolve().parents[3]/'full-aigc-skills-repositories/printcraft-skills/skills')))
SCENES=['report-bookmarks','review-watermark','invoice-split','section-pagination','linked-agenda','revision-compare']

class DeliveryContract(unittest.TestCase):
    def test_each_workflow_has_its_own_commands_and_result_checks(self):
        for name in SCENES:
            with self.subTest(scene=name):
                file=ROOT/f'printcraft-{name}/references/craft-steps.json'
                self.assertTrue(file.is_file(),'Missing actual business workflow '+name)
                recipe=json.loads(file.read_text(encoding='utf-8'))
                self.assertTrue(recipe['check'] and recipe['boundary'])
                self.assertTrue(recipe['sourceFiles'])
                self.assertNotEqual([s['command'] for s in recipe['steps']],['doc_info','doc_save'])

    def test_compiler_rebinds_both_documents_without_changing_page_numbers(self):
        import importlib.util
        spec=importlib.util.spec_from_file_location('pdf_delivery_compiler',ROOT/'printcraft-revision-compare/scripts/write_script.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        recipe={'sourceFiles':['new.pdf','old.pdf'],'steps':[{'command':'doc_compare','params':{'doc':1,'other':2}},{'command':'page_extract','params':{'doc':1,'pages':[1,3],'out':'selected.pdf'}}]}
        result=m.compile_steps(recipe,preopen=['decoy.pdf'])
        self.assertEqual(result[3]['args'],{'doc':2,'other':3})
        self.assertEqual(result[4]['args']['pages'],[1,3])
        recipe['steps'][0]['params']['other']=3
        with self.assertRaisesRegex(ValueError,'slot'):m.compile_steps(recipe)

    def test_navigation_rejects_wrong_destination_even_with_correct_titles(self):
        from pdf_delivery_smoke import verify_navigation
        good=[{'title':'Report','page':1,'children':[{'title':'Findings','page':2}]},{'title':'Appendix','page':3}]
        verify_navigation(good)
        good[0]['children'][0]['page']=3
        with self.assertRaisesRegex(AssertionError,'destination'):verify_navigation(good)

    def test_agenda_rejects_wrong_target_and_displaced_hitbox(self):
        import copy
        from pdf_delivery_smoke import verify_agenda_links
        report={'count':2,'links':[{'page':1,'to_page':3,'rect':[10,10,100,40]},{'page':3,'to_page':1,'rect':[10,10,100,40]}]}
        find={'complete':True,'count':1,'matches':[{'page':1,'rects':[[20,20,90,30]]}]}
        verify_agenda_links(report,[find])
        wrong=copy.deepcopy(report);wrong['links'][0]['to_page']=2
        with self.assertRaisesRegex(AssertionError,'destination'):verify_agenda_links(wrong,[find])
        wrong=copy.deepcopy(report);wrong['links'][0]['rect']=[100,100,200,200]
        with self.assertRaisesRegex(AssertionError,'hotspot'):verify_agenda_links(wrong,[find])

    def test_revision_rejects_reversed_old_and_new_values(self):
        from pdf_delivery_smoke import verify_revision
        report={'identical':False,'replaced':1,'inserted':0,'deleted':0,'changes':[{'old':{'text':'100','page':1},'new':{'text':'120','page':1}}]}
        verify_revision(report)
        report['changes'][0]['old']['text']='120';report['changes'][0]['new']['text']='100'
        with self.assertRaisesRegex(AssertionError,'direction'):verify_revision(report)
