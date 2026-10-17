"""基础技能发行身份独立于后续宿主插件版本，保留来源与摘要校验。"""
import copy
import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('print_source_identity',ROOT/'scripts/validate_package.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class SourceIdentityTests(unittest.TestCase):
    def test_historical_plugin_version_does_not_invalidate_identical_frozen_source(self):
        provenance={'sourceVersion':'0.1.0-dev.6','skillFileSha256':{'printcraft-use/SKILL.md':'fixed'}}
        lock={'protocol':'printcraft.source-release/1','pluginVersion':'0.1.0-dev.6','source':provenance}
        m.validate_source_release_identity(lock,provenance)
        changed=copy.deepcopy(provenance);changed['skillFileSha256']['printcraft-use/SKILL.md']='changed'
        with self.assertRaisesRegex(ValueError,'identity'):m.validate_source_release_identity(lock,changed)
        lock['pluginVersion']=''
        with self.assertRaisesRegex(ValueError,'identity'):m.validate_source_release_identity(lock,provenance)
