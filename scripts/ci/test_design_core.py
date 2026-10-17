"""核心刊物配方必须显式绑定续文对象，并覆盖全文选择。"""
import json
import os
from pathlib import Path
import unittest
from design_core_smoke import verify_newsletter,verify_catalog_links
import copy

ROOT=Path(os.environ.get('CRAFT_DESIGN_SKILLS_ROOT',str(Path(__file__).resolve().parents[3]/'full-aigc-skills-repositories/designcraft-skills/skills')))/'designcraft-newsletter'


class NewsletterContract(unittest.TestCase):
    def test_recipe_has_explicit_thread_and_style_scope(self):
        recipe=json.loads((ROOT/'references/craft-steps.json').read_text(encoding='utf-8'))
        steps=recipe['steps']
        thread=next((s for s in steps if s['command']=='text.thread'),None)
        self.assertIsNotNone(thread,'Newsletter promises continuation but has no text.thread')
        self.assertEqual(thread['params'],{'from':{'$ref':'body.id'},'to':{'$ref':'continuation.id'}})
        body=next(s for s in steps if s.get('capture')=='body')['params']['text']
        selection=next(s for s in steps if s['command']=='text.select' and s['params']['story']=={'$ref':'body.story'})
        self.assertEqual(selection['params']['focus'],len(body.encode('utf-8')))
        applied=next(i for i,s in enumerate(steps) if s['command']=='style.paragraph.apply')
        self.assertEqual(steps[applied-1],selection)
        for s in steps:
            if s['command']=='object.textFrameOptions':self.assertTrue(s['params'].get('ids'))
            if s['command']=='story.get':self.assertTrue(s['params'].get('frame') or s['params'].get('story'))

    def test_reopened_model_rejects_wrong_columns_and_truncated_text(self):
        bindings={'body':{'id':10},'continuation':{'id':11}}
        info={'pageCount':2,'settings':{'pageWidth':595,'pageHeight':842},'spreads':[{'items':[{'id':10,'columns':3},{'id':12,'columns':1}]},{'items':[{'id':11,'columns':3}]}],'stories':[{'frames':[10,11],'overset':False}]}
        story={'frames':[10,11],'overset':None,'text':'Article end'}
        a={'pages':2,'size':[595,842],'frameCount':3,'thread':['body','continuation']}
        verify_newsletter(info,story,bindings,'Article end',a)
        overflow=dict(story,overset=0)
        with self.assertRaisesRegex(AssertionError,'remains overset'):verify_newsletter(info,overflow,bindings,'Article end',a)
        wrong=copy.deepcopy(info);wrong['spreads'][1]['items'][0]['columns']=1
        with self.assertRaisesRegex(AssertionError,'three-column'):verify_newsletter(wrong,story,bindings,'Article end',a)
        with self.assertRaisesRegex(AssertionError,'full text'):verify_newsletter(info,story,bindings,'Article end missing',a)


class CatalogContract(unittest.TestCase):
    def test_catalog_places_real_files_into_explicit_sku_frames(self):
        root=ROOT.parent/'designcraft-catalog'
        steps=json.loads((root/'references/craft-steps.json').read_text(encoding='utf-8'))['steps']
        placements=[s for s in steps if s['command']=='file.place']
        self.assertEqual(len(placements),2,'Catalog has empty frames instead of product assets')
        self.assertEqual({s['params']['path'] for s in placements},{'catalog-input/sku-101.png','catalog-input/sku-205.png'})
        self.assertTrue(all(s['params'].get('frame') and s['params'].get('link') is True for s in placements))
        for index,s in enumerate(steps):
            if s['command']=='style.paragraph.apply':self.assertEqual(steps[index-1]['command'],'text.select')
        self.assertTrue(any(s['command']=='links.list' for s in steps))
        self.assertTrue(any(s['command']=='file.package' for s in steps))

    def test_wrong_sku_image_and_low_ppi_are_rejected(self):
        products=[{'sku':'A','key':'a','image':'input/a.png'},{'sku':'B','key':'b','image':'input/b.png'}]
        bindings={'a_image':{'id':10},'b_image':{'id':20}}
        links=[{'path':'input/a.png','status':'ok','uses':[{'id':10,'ppi':177}]},{'path':'input/b.png','status':'ok','uses':[{'id':20,'ppi':177}]}]
        verify_catalog_links(links,products,bindings)
        wrong=copy.deepcopy(links);wrong[0]['uses'][0]['id']=20
        with self.assertRaisesRegex(AssertionError,'wrong SKU'):verify_catalog_links(wrong,products,bindings)
        wrong=copy.deepcopy(links);wrong[0]['uses'][0]['ppi']=72
        with self.assertRaisesRegex(AssertionError,'PPI'):verify_catalog_links(wrong,products,bindings)
        wrong=copy.deepcopy(links);wrong[0]['status']='embedded'
        with self.assertRaisesRegex(AssertionError,'not linked'):verify_catalog_links(wrong,products,bindings)


if __name__=='__main__':unittest.main()
