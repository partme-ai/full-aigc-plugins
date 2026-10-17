"""失败诊断只能证明已记录的失败，不能提升命令通过数。"""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AppearanceDiagnosticTests(unittest.TestCase):
    def setUp(self):
        self.report = json.loads((ROOT / 'docs/evidence/vectorcraft-appearance-diagnostic-fixed64-20261009.json').read_text())

    def test_failure_cannot_close_tasks_or_promote_appearance(self):
        self.assertEqual(self.report['result'], 'FAIL')
        self.assertEqual(self.report['tasksClosed'], [])
        self.assertEqual(self.report['acceptedAppearanceCommands'], 0)
        self.assertEqual(self.report['acceptedCatalogCommands'], 110)

    def test_reopen_loses_target_despite_in_memory_probe_restore(self):
        stage = self.report['runs'][0]['stage']
        self.assertTrue(stage['observed']['activeProbe']['restored'])
        ids = lambda model: [n['id'] for n in model['layers'][0]['kind']['children']]
        self.assertEqual(ids(stage['after']), [2, 3])
        self.assertEqual(ids(stage['reopened']), [3])
        self.assertNotEqual(stage['after'], stage['reopened'])

    def test_unknown_request_is_preserved_without_replay(self):
        self.assertEqual(self.report['runs'][1]['lastRequest']['state'], 'submitted')
        self.assertEqual(self.report['runs'][1]['lastRequest']['command'], 'effect.apply')
        for run in self.report['runs']:
            self.assertTrue(run['failure']['noAutomaticReplay'])
            self.assertTrue(run['failure']['allOwnedProcessesStopped'])

    def test_candidate_identity_is_not_an_execution_identity(self):
        self.assertTrue(self.report['executionDriverIdentity'].startswith('NOT_RECORDED'))
        candidate = ROOT / 'docs/evidence/pre-appearance-diagnostic-identity/scripts/qa/command_appearance.py'
        self.assertEqual(self.report['candidateDriverSha256'], hashlib.sha256(candidate.read_bytes()).hexdigest())

    def test_acceptance_task_remains_open(self):
        tasks = (ROOT / 'openspec/changes/establish-v1-plugin/tasks.md').read_text()
        self.assertIn('- [ ] 8.3', tasks)
        self.assertEqual(len(self.report['openTasks']), 6)
