"""任务恢复和视觉证据绑定；使用模拟回执，不构造原生验收。"""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TaskCore(unittest.TestCase):
    def core(self):
        path = ROOT / 'scripts/task_core.py'
        self.assertTrue(path.exists(), 'missing persistent task controller')
        spec = importlib.util.spec_from_file_location('core', path)
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        return module

    def test_parent_path_alias_preserves_input_identity_after_create(self):
        core = self.core()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / 'source'; source.mkdir()
            photo = source / 'original.png'; photo.write_bytes(b'unchanged original')
            alias = root / 'alias'; alias.symlink_to(source, target_is_directory=True)
            state = core.create(root / 'task', {}, {'domain': 'lightcraft', 'steps': [{'command': 'library.info', 'params': {}}]}, [str(alias / photo.name)])
            core.check_inputs(state)
            self.assertEqual(set(state['originals']), {str(photo.resolve())})

    def test_existing_or_corrupt_task_is_not_reinitialized(self):
        core = self.core()
        with tempfile.TemporaryDirectory() as temporary:
            task = Path(temporary) / 'task'
            core.create(task, {'request': 'exposure only'}, {'domain': 'lightcraft', 'steps': [{'command': 'library.info', 'params': {}}]}, [])
            (task / 'state.json').write_text('{')
            with self.assertRaises(ValueError): core.inspect(task)
            with self.assertRaises((ValueError, FileExistsError)): core.create(task, {}, {}, [])

    def test_two_controllers_cannot_take_same_lock(self):
        core = self.core()
        with tempfile.TemporaryDirectory() as temporary:
            task = Path(temporary) / 'task'
            core.create(task, {}, {'domain': 'lightcraft', 'steps': [{'command': 'library.info', 'params': {}}]}, [])
            with core.task_lock(task):
                with self.assertRaises(ValueError):
                    with core.task_lock(task): pass

    def test_old_receipt_is_read_only_and_unknown_has_no_remaining_plan(self):
        core = self.core()
        with tempfile.TemporaryDirectory() as temporary:
            task = Path(temporary) / 'task'
            core.create(task, {}, {'domain': 'lightcraft', 'steps': [{'command': 'library.info', 'params': {}}]}, [])
            before = (task / 'state.json').read_bytes()
            report = core.reconcile(task)
            self.assertTrue(report['readOnly'])
            self.assertEqual((task / 'state.json').read_bytes(), before)
            with self.assertRaises(ValueError): core.remaining(task)


if __name__ == '__main__':
    unittest.main()
