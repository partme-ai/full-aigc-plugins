"""核心刊物配方必须显式绑定续文对象，并覆盖全文选择。"""
import json
from pathlib import Path
import unittest
from design_core_smoke import verify_newsletter
import copy

ROOT=Path(__file__).resolve().parents[3]/'full-aigc-skills-repositories/designcraft-skills/skills/designcraft-newsletter'


class NewsletterContract(unittest.TestCase):
    def test_recipe_has_explicit_thread_and_style_scope(self):
        recipe=json.loads((ROOT/'references/craft-steps.json').read_text())
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
        story={'frames':[10,11],'overset':False,'text':'Article end'}
        a={'pages':2,'size':[595,842],'frameCount':3,'thread':['body','continuation']}
        verify_newsletter(info,story,bindings,'Article end',a)
        wrong=copy.deepcopy(info);wrong['spreads'][1]['items'][0]['columns']=1
        with self.assertRaisesRegex(AssertionError,'three-column'):verify_newsletter(wrong,story,bindings,'Article end',a)
        with self.assertRaisesRegex(AssertionError,'full text'):verify_newsletter(info,story,bindings,'Article end missing',a)


if __name__=='__main__':unittest.main()
