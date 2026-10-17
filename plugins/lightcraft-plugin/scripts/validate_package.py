"""校验插件来源和分发材料；不安装、不生成照片。"""
import runpy
import argparse
import importlib.util
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate(source_git=None):
    spec = importlib.util.spec_from_file_location('provenance', ROOT / 'scripts/provenance.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    # CI 显式提供只读来源检出；不自动克隆，也不以摘要代替 tag/commit 核验。
    source_git = source_git or os.environ.get('LIGHTCRAFT_SOURCE_GIT')
    result = module.validate(ROOT, source_git)
    for name in ['LICENSE', 'licenses/Apache-2.0.txt', 'THIRD_PARTY_NOTICES.md']:
        if not (ROOT / name).is_file():
            raise ValueError('distribution_material_missing: ' + name)
    adapters = json.loads((ROOT / '.codex-plugin/plugin.json').read_text())
    manifest = json.loads((ROOT / 'plugin.json').read_text())
    if any(adapters.get(key) != manifest.get(key) for key in ['name', 'version', 'description']):
        raise ValueError('host_manifest_identity_mismatch')
    spec=importlib.util.spec_from_file_location('package_checks',ROOT/'skills/lightcraft-use/scripts/package_checks.py')
    checks=importlib.util.module_from_spec(spec);spec.loader.exec_module(checks)
    # 原技能逐文件摘要已由 provenance 校验；新增 MCP 场景不要求复制 CLI 运行时资源。
    scenes=runpy.run_path(str(ROOT/'scripts/validate_editor_scenes.py'))['candidate_names'](ROOT)
    quality={'skills':len(module.EXPECTED_SKILLS)+len(scenes),'markdownReferences':checks.markdown(ROOT),'structure':'PASS'}
    return dict(result,**quality,plugin='lightcraft',hostAcceptance='NOT_RUN')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-git', type=Path, help='用于核验发行 tag/commit/blob 的本地来源 Git 根目录')
    args = parser.parse_args()
    print(json.dumps(validate(args.source_git), ensure_ascii=False))
