"""核心刊物配方必须显式绑定续文对象，并覆盖全文选择。"""
import json
import os
from pathlib import Path
import unittest
from design_core_smoke import verify_newsletter,verify_catalog_links,verify_toc_entries,verify_brochure
import copy
from design_preflight_smoke import verify_repaired

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


class LongDocumentContract(unittest.TestCase):
    def test_long_document_has_real_toc_and_scoped_chapter_styles(self):
        steps=json.loads((ROOT.parent/'designcraft-long-document/references/craft-steps.json').read_text(encoding='utf-8'))['steps']
        commands=[s['command'] for s in steps]
        self.assertIn('toc.generate',commands,'Long document has no native table of contents')
        entry=next(s for s in steps if s['command']=='style.paragraph.create' and s['params']['name']=='Contents Entry')
        self.assertEqual(entry['params'].get('para',{}).get('tabs'),[{'position':480,'align':'right','leader':'.'}],'TOC page numbers require explicit right-aligned tabs')
        self.assertIn('toc.update',commands,'Changed pagination must update contents')
        self.assertIn('text.thread',commands,'Chapter continuation is missing')
        self.assertGreaterEqual(commands.count('style.paragraph.apply'),4)
        for i,step in enumerate(steps):
            if step['command']=='style.paragraph.apply':self.assertEqual(steps[i-1]['command'],'text.select')
            if step['command']=='story.get':self.assertTrue(step['params'].get('story') or step['params'].get('frame'))

    def test_toc_rejects_stale_page_numbers_and_body_entries(self):
        chapters=[{'heading':'Chapter One'},{'heading':'Chapter Two'}]
        entries=[{'text':'Chapter One','page':'2'},{'text':'Chapter Two','page':'5'}]
        verify_toc_entries(entries,chapters,[2,5])
        with self.assertRaisesRegex(AssertionError,'stale'):verify_toc_entries(entries,chapters,[2,4])
        with self.assertRaisesRegex(AssertionError,'entry count'):verify_toc_entries(entries+[{'text':'Body copy','page':'3'}],chapters,[2,5])


class PrintPreflightContract(unittest.TestCase):
    def test_preflight_has_inspect_repair_recheck_before_export(self):
        steps=json.loads((ROOT.parent/'designcraft-print-preflight/references/craft-steps.json').read_text(encoding='utf-8'))['steps']
        commands=[s['command'] for s in steps]
        self.assertEqual(commands.count('preflight.run'),2,'Need actual before/after preflight')
        self.assertIn('links.relink',commands)
        self.assertIn('transform.resize',commands)
        self.assertLess(max(i for i,s in enumerate(steps) if s['command']=='preflight.run'),commands.index('file.exportPdf'))
        self.assertNotIn('file.new',commands,'Existing print source must not be cleared')

    def test_resolution_warning_stops_export(self):
        before={'issues':[{'kind':kind,'severity':'error' if kind!='lowResolution' else 'warning'} for kind in ['overset','missingLink','lowResolution']]}
        verify_repaired(before,{'issues':[]})
        legacy={'issues':[i for i in before['issues'] if i['kind']!='missingLink']}
        verify_repaired(legacy,{'issues':[]},[{'status':'missing'}])
        with self.assertRaisesRegex(AssertionError,'all target defects'):verify_repaired(legacy,{'issues':[]})
        with self.assertRaisesRegex(AssertionError,'export must stop'):verify_repaired(before,{'issues':[{'kind':'lowResolution','severity':'warning'}]})
        with self.assertRaisesRegex(AssertionError,'all target defects'):verify_repaired({'issues':[]},{'issues':[]})



class BrochureContract(unittest.TestCase):
    def test_brochure_has_four_distinct_pages_and_bound_product_images(self):
        recipe=json.loads((ROOT.parent/'designcraft-brochure/references/craft-steps.json').read_text(encoding='utf-8'))
        steps=recipe['steps'];new=next((s for s in steps if s['command']=='file.new'),None)
        self.assertIsNotNone(new,'Brochure needs a real multipage document')
        self.assertEqual(new['params']['pages'],4)
        self.assertEqual({s['params']['spread'] for s in steps if s['command']=='frame.create'},set(range(4)))
        placements=[s for s in steps if s['command']=='file.place']
        self.assertEqual(len(placements),2)
        self.assertTrue(all(s['params'].get('frame') and s['params'].get('link') for s in placements))
        for i,s in enumerate(steps):
            if s['command']=='style.paragraph.apply':self.assertEqual(steps[i-1]['command'],'text.select')
        self.assertGreaterEqual(sum(s['command']=='style.paragraph.apply' for s in steps),8)
        self.assertNotIn('file.package',[s['command'] for s in steps])
        self.assertEqual([s['command'] for s in recipe['deliverySteps']],['file.package'])

    def test_brochure_rejects_wrong_page_truncation_and_zero_offset_overset(self):
        recipe=json.loads((ROOT.parent/'designcraft-brochure/references/craft-steps.json').read_text(encoding='utf-8'))
        frames=[step for step in recipe['steps'] if step['command']=='frame.create']
        bindings={step['capture']:{'id':i+1} for i,step in enumerate(frames)}
        spreads=[{'items':[]} for _ in range(4)];stories=[]
        for step in frames:
            item={'id':bindings[step['capture']]['id']};spreads[step['params']['spread']]['items'].append(item)
            if step['params']['content']=='text':stories.append({'frames':[item['id']],'text':step['params']['text'],'overset':None})
        info={'pageCount':4,'settings':{'pageWidth':420,'pageHeight':595},'spreads':spreads,'stories':stories}
        verify_brochure(info,stories,bindings,recipe)
        wrong=copy.deepcopy(info);wrong['spreads'][1]['items'].append(wrong['spreads'][0]['items'].pop(0))
        with self.assertRaisesRegex(AssertionError,'wrong page'):verify_brochure(wrong,stories,bindings,recipe)
        wrong=copy.deepcopy(stories);wrong[0]['text']='truncated'
        with self.assertRaisesRegex(AssertionError,'full text'):verify_brochure(info,wrong,bindings,recipe)
        wrong=copy.deepcopy(stories);wrong[0]['overset']=0
        with self.assertRaisesRegex(AssertionError,'remains overset'):verify_brochure(info,wrong,bindings,recipe)


class PosterContract(unittest.TestCase):
    def test_poster_has_a3_size_native_qr_and_matching_visible_link(self):
        recipe=json.loads((ROOT.parent/'designcraft-poster-layout/references/craft-steps.json').read_text(encoding='utf-8'))
        steps=recipe['steps'];new=next((s for s in steps if s['command']=='file.new'),None)
        self.assertIsNotNone(new,'Poster must set the confirmed final dimensions')
        self.assertAlmostEqual(new['params']['width'],297*72/25.4)
        self.assertAlmostEqual(new['params']['height'],420*72/25.4)
        qr=next((s for s in steps if s['command']=='object.qrCode'),None)
        self.assertIsNotNone(qr,'Do not replace a scannable registration code with an empty square')
        link=next(s for s in steps if s['command']=='hyperlink.create')
        self.assertEqual(qr['params']['content'],link['params']['url'])
        copy=next(s for s in steps if s.get('capture')=='registration')
        self.assertIn(qr['params']['content'],copy['params']['text'])
        self.assertGreaterEqual(sum(s['command']=='style.paragraph.apply' for s in steps),5)
        self.assertNotIn('file.package',[s['command'] for s in steps])


    def test_qr_bounds_keep_native_ink_and_reserved_white_border_separate(self):
        from design_poster_smoke import verify_qr_bounds
        verify_qr_bounds([10,10,90,90],[0,0,100,100])
        for bounds in [[0,0,100,100],[10,10,90,80],[0,10,80,90]]:
            with self.assertRaises(AssertionError):verify_qr_bounds(bounds,[0,0,100,100])


    def test_registration_checks_destination_and_actual_source_not_link_name(self):
        from design_poster_smoke import verify_registration
        url='https://example.org/workshop';link={'dest':{'kind':'url','value':url},'source':{'id':13,'kind':'item'}}
        verify_registration(url,url,'Register: '+url,13,[link])
        wrong=copy.deepcopy(link);wrong['name']=url;wrong['dest']['value']='https://example.org/other'
        with self.assertRaisesRegex(AssertionError,'lost or changed'):verify_registration(url,url,url,13,[wrong])
        wrong=copy.deepcopy(link);wrong['source']['id']=99
        with self.assertRaisesRegex(AssertionError,'wrong frame'):verify_registration(url,url,url,13,[wrong])
        with self.assertRaisesRegex(AssertionError,'Visible'):verify_registration(url,url,'An unrelated address',13,[link])
        with self.assertRaisesRegex(AssertionError,'different destination'):verify_registration(url,'https://example.org/other',url,13,[link])

if __name__=='__main__':unittest.main()
