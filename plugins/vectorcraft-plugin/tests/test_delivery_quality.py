"""技术解码不能由高视觉评分替代；未执行的原生重开保持独立状态。"""
import hashlib
import base64
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
import unittest
import zlib

ROOT=Path(__file__).resolve().parents[1]


def checker():
    spec=importlib.util.spec_from_file_location('delivery_quality',ROOT/'src/evaluation/delivery_quality.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def png():
    def chunk(name,value):return struct.pack('>I',len(value))+name+value+struct.pack('>I',zlib.crc32(name+value)&0xffffffff)
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',1,1,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(b'\0\xff\0\0\xff'))+chunk(b'IEND',b'')


class DeliveryQualityTests(unittest.TestCase):
    def test_embedded_png_svg_can_be_decoded_without_external_fetch(self):
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary)/'graphic.svg'
            path.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"><image width="10" height="10" href="data:image/png;base64,'+base64.b64encode(png()).decode()+'"/></svg>')
            result=checker().decode_output(path)
            self.assertIn(result['status'],('PASS','NOT_RUN'))
            self.assertNotEqual(result.get('reason'),'svg_external_resource')

    def test_undisclosed_svg_image_blocks_even_passing_decoder(self):
        module=checker()
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);manifest=self.fixture(root,png())
            path=root/'graphic.svg';path.write_text('<svg><image href="data:image/png;base64,'+base64.b64encode(png()).decode()+'"/></svg>')
            manifest['files'][path.name]=hashlib.sha256(path.read_bytes()).hexdigest();manifest['outputs']=[{'path':path.name}]
            (root/'manifest.json').write_text(json.dumps(manifest))
            result=module.check_delivery(root,'a'*64,manifest['files']['project.vectorcraft'],decoder=lambda path:{'status':'PASS'})
            self.assertEqual(result['technicalStatus'],'FAIL');self.assertIn('raster_disclosure',result['error'])

    def test_remote_or_vector_data_svg_remains_blocked(self):
        for uri in ['https://invalid.example/image.png','data:image/svg+xml;base64,PHN2Zy8+','data:image/png;base64,%%%']:
            with tempfile.TemporaryDirectory() as temporary:
                path=Path(temporary)/'graphic.svg';path.write_text('<svg><image href="'+uri+'"/></svg>')
                self.assertEqual(checker().decode_output(path)['status'],'FAIL')

    def test_unknown_status_cannot_be_accepted(self):
        module=checker()
        report={'artifactIntegrityStatus':'PASS','engineeringStatus':'PASS','technicalStatus':'unverified'}
        with self.assertRaisesRegex(ValueError,'invalid_quality_state'):module.quality_state(report,'PASS',True)

    def fixture(self,root,preview):
        (root/'project.vectorcraft').write_bytes(b'native-identity-only');(root/'preview.png').write_bytes(preview)
        digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
        manifest={'schema':'vectorcraft-delivery/v1','runtimeSha256':'a'*64,'files':{name:digest(root/name) for name in ('project.vectorcraft','preview.png')},'outputs':[{'path':'preview.png'}],'fontDependencies':[]}
        (root/'manifest.json').write_text(json.dumps(manifest));return manifest

    def test_corrupt_image_with_matching_manifest_hash_cannot_pass(self):
        module=checker()
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);manifest=self.fixture(root,b'\x89PNG\r\n\x1a\ncorrupt')
            report=module.check_delivery(root,'a'*64,manifest['files']['project.vectorcraft'])
            self.assertEqual(report['technicalStatus'],'FAIL')
            state=module.quality_state(report,'PASS',True)
            self.assertEqual(state['acceptanceStatus'],'blocked')

    def test_missing_decoder_is_not_a_technical_pass(self):
        module=checker()
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);manifest=self.fixture(root,png())
            report=module.check_delivery(root,'a'*64,manifest['files']['project.vectorcraft'],decoder=lambda path:{'status':'NOT_RUN','reason':'missing_decoder'})
            self.assertEqual(report['technicalStatus'],'NOT_RUN');self.assertEqual(module.quality_state(report,'PASS',True)['acceptanceStatus'],'pending')

    def test_manifest_integrity_does_not_claim_native_reopening(self):
        module=checker()
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);manifest=self.fixture(root,png())
            report=module.check_delivery(root,'a'*64,manifest['files']['project.vectorcraft'],decoder=lambda path:{'status':'PASS','scope':'unit decoder fixture only'})
            self.assertEqual(report['artifactIntegrityStatus'],'PASS');self.assertEqual(report['engineeringStatus'],'NOT_RUN')
            self.assertEqual(module.quality_state(report,'PASS',True)['acceptanceStatus'],'pending')

    def test_declared_file_or_runtime_drift_blocks_before_decode(self):
        module=checker()
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);manifest=self.fixture(root,png())
            def decode(path):self.fail('must not decode after identity mismatch')
            report=module.check_delivery(root,'b'*64,manifest['files']['project.vectorcraft'],decoder=decode)
            self.assertEqual(report['artifactIntegrityStatus'],'FAIL')
            (root/'preview.png').write_bytes(b'replaced')
            report=module.check_delivery(root,'a'*64,manifest['files']['project.vectorcraft'],decoder=decode)
            self.assertEqual(report['artifactIntegrityStatus'],'FAIL')
