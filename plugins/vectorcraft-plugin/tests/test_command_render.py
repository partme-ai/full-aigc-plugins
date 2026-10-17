"""渲染变化证据不能以不同文件名或摘要替代实际像素变化。"""
import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class CommandRenderTests(unittest.TestCase):
 def setUp(self):
  p=ROOT/'scripts/qa/command_render.py';self.assertTrue(p.is_file(),'native_render_verifier_missing')
  spec=importlib.util.spec_from_file_location('command_render',p);self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
 def test_count_changed_rgb_pixels(self):self.assertEqual(self.m.changed_pixels(bytes([0,1,2,3,4,5]),bytes([0,1,2,3,4,9]),2,1),1)
 def test_identical_pixels_are_rejected(self):
  with self.assertRaisesRegex(ValueError,'command_render_unchanged'):self.m.changed_pixels(bytes(6),bytes(6),2,1)
 def test_wrong_buffer_shape_is_rejected(self):
  with self.assertRaisesRegex(ValueError,'command_render_shape'):self.m.changed_pixels(bytes(3),bytes(3),2,1)
