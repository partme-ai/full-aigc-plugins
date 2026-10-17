import unittest
from fig_core_smoke import verify_wireframe, verify_responsive, verify_prototype, verify_imported_corners

class FigCoreTests(unittest.TestCase):
    def test_old_wireframe_without_content_and_action_is_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'region missing'):
            verify_wireframe({'frame': {'width':1280,'height':1024,'children':[{'name':'Navigation'}]}})

    def test_fill_children_must_really_resize(self):
        nodes={'root':{'width':390,'height':884,'layout':{'mode':'vertical'}}}
        for name in ['heading','card','button']:
            nodes[name]={'x':24,'width':720,'y':24,'height':48}
        with self.assertRaisesRegex(AssertionError, 'did not fill'):
            verify_responsive(nodes,390,884)

    def test_prototype_destination_must_not_match_duration_digits(self):
        nodes={key:{'interactions':[{'trigger':{'type':'onClick'},'actions':[{'type':'navigate','dest':99}],'duration_ms':300}]} for key in ['button','back']}
        with self.assertRaisesRegex(AssertionError,'destination wrong'):
            verify_prototype(nodes,{'result':{'id':3},'start':{'id':2}})

    def corner_document(self):
        entries={}
        for name,radii in [('rect radius=4:8:12:16',[4,8,12,16]),('shape radius=4:8:12:16',[8,12,16,4])]:
            entries[name]={'name':name,'type':'vector','network':{'vertices':[{'radius':r} for r in radii]},'corners':{'radii':[12]*4}}
        for name,radii in [('frame radius=4:8:12:16',[4,8,16,12]),('frame radius=0:12:0:0',[0,12,0,0])]:
            entries[name]={'name':name,'type':'frame','corners':{'radii':radii}}
        return {'nodes':entries}

    def test_vector_geometry_takes_priority_over_generic_radius(self):
        verify_imported_corners(self.corner_document())

    def test_original_frame_import_loss_is_rejected(self):
        doc=self.corner_document();doc['nodes']['frame radius=4:8:12:16']['corners']['radii']=[12]*4
        with self.assertRaisesRegex(AssertionError,'frame corner geometry'):
            verify_imported_corners(doc)

    def test_vector_vertex_loss_is_rejected(self):
        doc=self.corner_document();doc['nodes']['rect radius=4:8:12:16']['network']['vertices'][0]['radius']=12
        with self.assertRaisesRegex(AssertionError,'vector corner geometry'):
            verify_imported_corners(doc)
