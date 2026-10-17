import unittest
from light_core_fixtures import with_synthetic_gps, has_gps
from light_core_smoke import resolve, verify_group


class LightCoreTests(unittest.TestCase):
    def test_array_binding_keeps_flat_numeric_ids(self):
        result = resolve({'ids': '$group.photoIds'}, {'group.photoIds': [12, 13]})
        self.assertEqual(result, {'ids': [12, 13]})
        with self.assertRaises(AssertionError):
            resolve({'ids': ['$group.photoIds']}, {'group.photoIds': [12, 13]})

    def test_non_light_or_unselected_changes_are_rejected(self):
        sample = {'light': {'exposure': .25}}
        before = {'light': {'exposure': 1}, 'color': {'saturation': 35}, 'crop': {'angle': .5}}
        guard = {'light': {'exposure': -.7}}
        for after, guard_after in [({'light': sample['light'], 'color': {'saturation': 0}, 'crop': before['crop']}, guard),
                                   ({**before, 'light': sample['light']}, {'light': {'exposure': .25}})]:
            with self.assertRaises(AssertionError):
                verify_group(sample, before, after, guard, guard_after)

    def test_real_exif_gps_is_distinguished_from_text(self):
        self.assertFalse(has_gps(b'\xff\xd8\xff\xd9GPS'))
        self.assertTrue(has_gps(with_synthetic_gps(b'\xff\xd8\xff\xd9')))
