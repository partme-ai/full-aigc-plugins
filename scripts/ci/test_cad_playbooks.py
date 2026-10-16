import unittest
from cad_playbook_smoke import verify_dxf


def fixture(body):
    return '\n'.join(map(str,[0,'SECTION',2,'HEADER',9,'$INSUNITS',70,4,0,'ENDSEC',0,'SECTION',2,'ENTITIES']+body+[0,'ENDSEC',0,'EOF']))+'\n'


class GeometryTests(unittest.TestCase):
    def test_hole_center_and_radius(self):
        d=fixture([0,'CIRCLE',10,10,20,15,40,2])
        verify_dxf(d,{'circles':[[10,15,2]]})
        with self.assertRaisesRegex(AssertionError,'center/radius'):verify_dxf(d,{'circles':[[10,15,4]]})
    def test_missing_native_dimension(self):
        with self.assertRaisesRegex(AssertionError,'dimension count'):verify_dxf(fixture([]),{'dimensions':1})
    def test_doorway_wall_crossing(self):
        with self.assertRaisesRegex(AssertionError,'crosses doorway'):
            verify_dxf(fixture([0,'LINE',10,0,20,0,11,5000,21,0]),{'doorGap':[2000,3000],'arc':[2000,0,1000,0,90]})
    def test_route_uses_segment_length(self):
        d=fixture([0,'LWPOLYLINE',70,0,10,0,20,0,10,3,20,0,10,3,20,4])
        verify_dxf(d,{'openPolyline':[[0,0],[3,0],[3,4]],'length':7})
        with self.assertRaisesRegex(AssertionError,'length'):verify_dxf(d,{'openPolyline':[[0,0],[3,0],[3,4]],'length':5})
    def test_unit_must_survive(self):
        with self.assertRaisesRegex(AssertionError,'unit lost'):verify_dxf(fixture([]).replace('$INSUNITS\n70\n4','$INSUNITS\n70\n0'),{})


if __name__=='__main__':unittest.main()
