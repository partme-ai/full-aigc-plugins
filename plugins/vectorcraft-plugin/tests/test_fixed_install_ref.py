"""公开不可变提交验收不得被误记为已发布标签验收。"""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('fixed_install_ref', ROOT/'scripts/acceptance/fixed_install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)
SHA = 'a'*40


class FixedInstallReferenceTests(unittest.TestCase):
    def git(self, *args):
        if args == ('rev-parse', SHA+'^{commit}'): return SHA
        if args == ('rev-parse', 'v0.1.0-dev.64^{commit}'): return SHA
        if args == ('ls-remote', 'origin', 'refs/heads/main'): return SHA+'\trefs/heads/main'
        if args[0] == 'ls-remote': return SHA+'\trefs/tags/v0.1.0-dev.64^{}'
        raise AssertionError(args)

    def test_default_remains_public_tag(self):
        self.assertEqual(installer.resolve_reference('0.1.0-dev.64', None, self.git),
            {'ref':'v0.1.0-dev.64','commit':SHA,'kind':'public-tag'})

    def test_exact_remote_commit_is_candidate_not_published_tag(self):
        self.assertEqual(installer.resolve_reference('0.1.0-dev.64', SHA, self.git),
            {'ref':SHA,'commit':SHA,'kind':'public-commit'})

    def test_branch_abbreviated_commit_and_other_tag_are_rejected_before_git(self):
        def forbidden(*args): self.fail('invalid reference reached git')
        for ref in ('main','aaaaaaa','v0.1.0-dev.63','../main','A'*40):
            with self.subTest(ref=ref), self.assertRaisesRegex(ValueError,'invalid_fixed_reference'):
                installer.resolve_reference('0.1.0-dev.64',ref,forbidden)

    def test_unpushed_commit_is_rejected(self):
        def git(*args):
            if args[0]=='ls-remote': return 'b'*40+'\trefs/heads/main'
            return self.git(*args)
        with self.assertRaisesRegex(ValueError,'remote_commit_mismatch'):
            installer.resolve_reference('0.1.0-dev.64',SHA,git)

    def test_moved_tag_or_local_commit_alias_cannot_pass(self):
        def moved(*args):
            if args[0]=='ls-remote': return 'b'*40+'\trefs/tags/v0.1.0-dev.64^{}'
            return self.git(*args)
        with self.assertRaisesRegex(ValueError,'remote_release_mismatch'):
            installer.resolve_reference('0.1.0-dev.64',None,moved)
        def alias(*args):
            if args[0]=='rev-parse': return 'b'*40
            return self.git(*args)
        with self.assertRaisesRegex(ValueError,'fixed_commit_mismatch'):
            installer.resolve_reference('0.1.0-dev.64',SHA,alias)
