import unittest
from vector_playbook_smoke import verify


def doc(children):return {'artboards':[{'width':240,'height':240}],'layers':[{'kind':'Layer','children':children}]}


class VectorChecks(unittest.TestCase):
    def test_editable_chart_bounds(self):
        info=doc([{'kind':'Rectangle','bounds':dict(x=60,y=155,width=48,height=45)}]);a={'artboard':[240,240],'rectangles':[[60,155,48,45]]};verify(info,a)
        info['layers'][0]['children'][0]['bounds']['height']=30
        with self.assertRaisesRegex(AssertionError,'Bar geometry'):verify(info,a)
    def test_white_cover_circle_is_not_ring(self):
        with self.assertRaisesRegex(AssertionError,'compound hole'):verify(doc([{'kind':'Ellipse'},{'kind':'Ellipse'}]),{'artboard':[240,240],'compoundRequired':True})
    def test_live_text_cannot_be_outlined_delivery(self):
        with self.assertRaisesRegex(AssertionError,'retains live text'):verify(doc([{'kind':'Type','text':'CRAFT'}]),{'artboard':[240,240],'textCount':0})
    def test_cropping_must_change_real_bounds(self):
        n={'kind':'Ellipse','bounds':dict(x=40,y=40,width=160,height=160),'closed':True}
        with self.assertRaisesRegex(AssertionError,'crop bounds'):verify(doc([n]),{'artboard':[240,240],'cropBounds':[40,40,80,160]})
    def test_arrow_direction_options_preserved(self):
        n={'kind':'Path','strokeWidth':8,'strokeOptions':{'cap':'round','endArrow':'Triangle','arrowAlign':'tip'}};a={'artboard':[240,240],'stroke':{'width':8,'cap':'round','endArrow':'Triangle','arrowAlign':'tip'}};verify(doc([n]),a)
        n['strokeOptions']['endArrow']=None
        with self.assertRaisesRegex(AssertionError,'endArrow'):verify(doc([n]),a)


if __name__=='__main__':unittest.main()
