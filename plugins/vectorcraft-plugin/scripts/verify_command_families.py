#!/usr/bin/env python3
"""合并固定安装命令族证据；重复、身份漂移及缺失语义禁止提升通过数。"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE='scripts/verify_command_evidence.py'
MATRIX='docs/evidence/vectorcraft-command-families140-fixed64-20261009.json'
FAMILIES={'magicWand':'docs/evidence/vectorcraft-command-magicWand-fixed64-20261009.json','swatch':'docs/evidence/vectorcraft-command-swatch-fixed64-20261009.json','stroke':'docs/evidence/vectorcraft-command-stroke-fixed64-20261009.json','transparency':'docs/evidence/vectorcraft-command-transparency-fixed64-20261009.json','shape':'docs/evidence/vectorcraft-command-shape-fixed64-20261009.json','layer':'docs/evidence/vectorcraft-command-layer-fixed64-20261009.json','graphicStyle':'docs/evidence/vectorcraft-command-graphicStyle-fixed64-20261009.json','appearance':'docs/evidence/vectorcraft-command-appearance-fixed64-20261009.json','effect':'docs/evidence/vectorcraft-command-effect-fixed64-20261009.json','guide':'docs/evidence/vectorcraft-command-guide-fixed64-20261009.json','attributes':'docs/evidence/vectorcraft-command-attributes-fixed64-20261009.json'}
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def merge_ids(accepted,commands):
    """按原生命令ID合并，绝不以重复执行或重复族增加覆盖。"""
    if len(commands)!=len(set(commands)):raise ValueError('command_family_duplicate')
    if set(accepted)&set(commands):raise ValueError('command_family_overlap')
    return set(accepted)|set(commands)

def era_identity(root,report):
    """收敛后 docs/current-identity.json 只描述当前世界；历史报告按执行时归档身份核对。"""
    def matches(identity):return identity['pluginVersion']==report['pluginVersion'] and identity['skillSource']['ref']==report['sourceRef'] and identity['skillSource']['sha']==report['sourceCommit']
    current=json.loads((root/'docs/current-identity.json').read_text())
    if matches(current):return current
    candidates={}
    for base in (root,ROOT):
        archived=base/'docs/evidence/pre-harness-convergence-identity'
        if not archived.is_dir():continue
        for path in sorted(archived.glob('*/docs/current-identity.json')):
            try:candidate=path.read_bytes()
            except OSError:continue
            if matches(json.loads(candidate)):candidates[hashlib.sha256(candidate).hexdigest()]=json.loads(candidate)
    if len(candidates)!=1:raise ValueError('family_installed_identity')
    return next(iter(candidates.values()))

def validate_family(root,family,path):
    """验证当前安装身份及每轮命令上下文、真实对象、交付解码和重开。"""
    report=json.loads((root/path).read_text());identity=era_identity(root,report)
    host=json.loads((root/'docs/evidence/vectorcraft-public-tag64-install-20261009.json').read_text());catalog=json.loads((root/'skills/vectorcraft-use/references/command-coverage.json').read_text())
    if report.get('schema')!='vectorcraft-command-family/v1' or report.get('result')!='PASS' or report.get('family')!=family:raise ValueError('family_report_identity')
    for key in ('pluginVersion','pluginCommit','sourceRef','sourceCommit','hostVersion','platform'):
        if report[key]!=host[key]:raise ValueError('family_fixed_identity')
    if report['installedSkillsBefore']!=identity['skills'] or report['installedSkillsAfter']!=identity['skills']:raise ValueError('family_installed_identity')
    if report['runtimeSha256']!=identity['runtime']['binarySha256'] or report['desktopBinarySha256']!=identity['desktop']['binarySha256']:raise ValueError('family_runtime_identity')
    driver_path='scripts/qa/command_'+family+'.py'
    runner_path='scripts/qa/command_family_window_diagnostic.py' if family in ('appearance','effect','guide','attributes','magicWand') else 'scripts/qa/command_family_window.py' if family in ('shape','layer','graphicStyle') else 'scripts/qa/command_family.py'
    if family=='guide':runner_path='scripts/qa/command_family_guide.py'
    if family in ('shape','layer','graphicStyle','appearance','effect','guide','attributes','magicWand') and report.get('runnerPath')!=runner_path:raise ValueError(family+'_window_runner')
    if report['driverSha256']!=sha(root/driver_path) or report['runnerSha256']!=sha(root/runner_path) or report['catalogSha256']!=sha(root/'skills/vectorcraft-use/references/command-coverage.json'):raise ValueError('family_execution_identity')
    if report['allOwnedProcessesStopped'] is not True or report['listenerOwnedByPID'] is not True:raise ValueError('family_owned_processes')
    driver=load('family_semantics_'+family,root/driver_path);cases=report['cases'];ids=[c['command'] for c in cases]
    expected=[row['id'] for row in catalog['commands'] if row['id'].startswith(family+'.')]
    if ids!=expected or ids!=driver.COMMANDS:raise ValueError('family_command_coverage')
    rows={row['id']:row for row in catalog['commands']}
    for case in cases:
        command=case['command']
        if case['result']!='PASS' or case['mode']!='owned-signed-desktop-bridge' or case['sourcePreserved'] is not True or case['previousDeliveryPreserved'] is not True:raise ValueError('family_context')
        if [s['round'] for s in case['stages']]!=[1,2]:raise ValueError('family_revision_stages')
        for stage in case['stages']:
            context=stage['context']
            if context['id']!=command or context['params']!=rows[command]['params'] or context['enabled'] is not True or stage['ui']['activeDocument'] is None:raise ValueError('family_live_context')
            driver.validate_transition(command,stage)
            if family=='guide':
                driver.validate_context(stage['contextProbe'])
                driver.shape.near(driver.shape.stable(stage['contextProbe']['after']),driver.shape.stable(stage['before']),'guide_lock_stage_binding')
            # 色板夹具只授权目标填充变化；描边与其他外观属性必须原样保全。
            if family=='swatch':
                before_appearance=driver.paint.objects(stage['before'])[2]['appearance']
                after_appearance=driver.paint.objects(stage['after'])[2]['appearance']
                def protected(value):return {**value,'items':[item for item in value['items'] if item['kind']!='fill']}
                if protected(before_appearance)!=protected(after_appearance):raise ValueError('family_protected_appearance')
            if family in ('shape','layer','graphicStyle','appearance','effect','guide','attributes','magicWand'):
                w=stage['window'];scale=w['pixelScale'];attempts=w['readAttempts']
                if scale not in (1,2) or (w['width'],w['height'])!=(1440*scale,900*scale) or w['window'] is not True or w['decoded'] is not True or w['mimeType']!='image/png' or w['bytes']<=0:raise ValueError(family+'_window_capture')
                if not 1<=len(attempts)<=3 or [x['attempt'] for x in attempts]!=list(range(1,len(attempts)+1)) or [x['status'] for x in attempts]!=['native-read-error']*(len(attempts)-1)+['PASS']:raise ValueError(family+'_window_read_attempts')
                digest=w['sha256']
                if len(digest)!=64 or any(c not in '0123456789abcdef' for c in digest):raise ValueError(family+'_window_digest')
            canvas=stage['canvas'];exports=stage['exports']
            if canvas['mimeType']!='image/png' or canvas['width']!=128 or canvas['height']!=96 or canvas['bytes']<=0:raise ValueError('family_canvas_decode')
            if [e['format'] for e in exports]!=['svg','png'] or any(e['decoded'] is not True for e in exports):raise ValueError('family_export_decode')
            for digest in [canvas['sha256'],stage['nativeProjectSha256'],*[e['sha256'] for e in exports]]:
                if len(digest)!=64 or any(c not in '0123456789abcdef' for c in digest):raise ValueError('family_artifact_identity')
    if family=='appearance':
        if report.get('preferenceRestartAcceptance')!='NOT_RUN':raise ValueError('appearance_preference_scope')
        for case in cases:
            if case['command'] not in ('appearance.setActiveItem','appearance.setNewArtBasic','appearance.newArt'):continue
            for stage in case['stages']:
                probe=stage['observed']['activeProbe' if case['command']=='appearance.setActiveItem' else 'newArtProbe']
                if probe.get('restoration')!='native-saved-checkpoint-reopen':raise ValueError('appearance_probe_restoration')
                for key in ('checkpointSha256','probeProjectSha256'):
                    digest=probe.get(key)
                    if not isinstance(digest,str) or len(digest)!=64 or any(c not in '0123456789abcdef' for c in digest):raise ValueError('appearance_probe_identity')
    if family in ('stroke','transparency','shape'):
        if family!='shape' and (report.get('preferenceRestartAcceptance')!='NOT_RUN' or any(s['observed'].get('preferenceRestartAcceptance')!='NOT_RUN' for c in cases for s in c['stages'])):raise ValueError(family+'_preference_scope')
        render=report['renderChanges'];checker_path='scripts/qa/command_render.py' if family=='stroke' else 'scripts/qa/command_'+family+'_render.py';checker=load(family+'_render',root/checker_path)
        if render['schema']!='vectorcraft-command-render-changes/v1' or render['result']!='PASS' or render['executionReportSha256']!=report['originalExecutionReportSha256'] or render['checkerSha256']!=sha(root/checker_path):raise ValueError(family+'_render_identity')
        if [c['command'] for c in render['cases']]!=checker.COMMANDS:raise ValueError(family+'_render_coverage')
        for measured in render['cases']:
            stages=next(c['stages'] for c in cases if c['command']==measured['command'])
            if [m['kind'] for m in measured['comparisons']]!=(['native-canvas','png-export','app-window'] if family=='shape' else ['native-canvas','png-export']):raise ValueError(family+'_render_coverage')
            for m in measured['comparisons']:
                size=(1440,900,1296000) if m['kind']=='app-window' else (128,96,12288)
                if m['kind']=='app-window' and (m.get('normalization')!='1440x900-logical-lanczos' or m['sourcePixelScales']!=[s['window']['pixelScale'] for s in stages]):raise ValueError('shape_window_normalization')
                if (m['width'],m['height'],m['totalPixels'])!=size or type(m['changedPixels']) is not int or not 1<=m['changedPixels']<=size[2]:raise ValueError(family+'_render_pixels')
                expected=[s['window']['sha256'] if m['kind']=='app-window' else s['canvas']['sha256'] if m['kind']=='native-canvas' else next(e['sha256'] for e in s['exports'] if e['format']=='png') for s in stages]
                if [m['firstSha256'],m['secondSha256']]!=expected or expected[0]==expected[1]:raise ValueError(family+'_render_binding')
    if family in ('layer','graphicStyle','appearance','effect','guide','attributes','magicWand'):validate_layer_render(root,report,cases,family)
    if family=='effect':
        load('effect_pixel_checks',root/'scripts/qa/command_effect_render.py').validate_expanded_images(cases,report['renderChanges']['expandedImageChecks'])
    if family=='guide':
        load('guide_pixel_checks',root/'scripts/qa/command_guide_render.py').validate_checks(cases,report['renderChanges']['guideLineChecks'])
    if family=='attributes':
        checker=load('attribute_pixels',root/'scripts/qa/command_attributes_render.py')
        checker.validate_links(cases,report['renderChanges']['svgLinkChecks'])
        checker.validate_checkboxes(cases,report['renderChanges']['checkboxChecks'])
    if family=='magicWand':
        load('wand_pixel_checks',root/'scripts/qa/command_magicWand_render.py').validate_checks(cases,report['renderChanges']['checkboxChecks'])
    return ids

def validate_layer_render(root,report,cases,family):
    """状态命令保全画布、可见性及剪切修改产生变化；窗口独立测量。"""
    path='scripts/qa/command_'+family+'_render.py';checker=load(family+'_render',root/path);render=report['renderChanges'];schema={'layer':'vectorcraft-command-layer-render/v1','graphicStyle':'vectorcraft-command-graphic-style-render/v1','appearance':'vectorcraft-command-appearance-render/v1','effect':'vectorcraft-command-effect-render/v1','guide':'vectorcraft-command-guide-render/v1','attributes':'vectorcraft-command-attributes-render/v1','magicWand':'vectorcraft-command-magic-wand-render/v1'}[family]
    if render['schema']!=schema or render['result']!='PASS' or render['executionReportSha256']!=report['originalExecutionReportSha256'] or render['checkerSha256']!=sha(root/path):raise ValueError('layer_render_identity')
    if [c['command'] for c in render['cases']]!=checker.COMMANDS:raise ValueError('layer_render_coverage')
    for measured in render['cases']:
        stages=next(c['stages'] for c in cases if c['command']==measured['command'])
        if [m['kind'] for m in measured['comparisons']]!=['native-canvas','png-export','app-window']:raise ValueError('layer_render_coverage')
        for m in measured['comparisons']:
            window=m['kind']=='app-window';size=(1440,900,1296000) if window else (128,96,12288)
            if (m['width'],m['height'],m['totalPixels'])!=size or m['expectation']!=checker.expectation(measured['command'],m['kind']):raise ValueError('layer_render_expectation')
            checker.validate_count(m['changedPixels'],size[2],m['expectation'])
            if window and (m.get('normalization')!='1440x900-logical-lanczos' or m['sourcePixelScales']!=[s['window']['pixelScale'] for s in stages]):raise ValueError('layer_window_normalization')
            hashes=[s['window']['sha256'] if window else s['canvas']['sha256'] if m['kind']=='native-canvas' else next(e['sha256'] for e in s['exports'] if e['format']=='png') for s in stages]
            if [m['firstSha256'],m['secondSha256']]!=hashes:raise ValueError('layer_render_binding')

def verify(root=ROOT):
    """复用已通过且原字节不变的paint证据，补充新的实际命令族。"""
    base=load('family_base',root/BASE);previous=base.verify(root);accepted={r['id'] for r in previous['commands'] if r['executionAcceptance']=='PASS'}
    reports={base.REPORT:sha(root/base.REPORT)};fingerprints={BASE:sha(root/BASE),'scripts/verify_command_families.py':sha(root/'scripts/verify_command_families.py'),'docs/current-identity.json':sha(root/'docs/current-identity.json'),'skills/vectorcraft-use/references/command-coverage.json':sha(root/base.CATALOG)}
    for family,path in FAMILIES.items():
        accepted=merge_ids(accepted,validate_family(root,family,path));reports[path]=sha(root/path)
        for name,digest in json.loads((root/path).read_text())['fingerprints'].items():
            if sha(root/name)!=digest:raise ValueError('family_dependency_drift')
            fingerprints[name]=digest
    catalog=json.loads((root/base.CATALOG).read_text());entries=base.matrix_rows(catalog,accepted)
    for name,digest in reports.items():fingerprints[name]=digest
    return {'schema':'vectorcraft-command-families/v1','result':'PASS','requirement':'VC-CM-001','tasksClosed':[],
            'pluginVersion':previous['pluginVersion'],'pluginCommit':previous['pluginCommit'],'sourceRef':previous['sourceRef'],
            'coverage':{'catalogCommands':len(entries),'passed':len(accepted),'notRun':len(entries)-len(accepted),'stages':2*len(accepted)},
            'reports':reports,'fingerprints':fingerprints,
            'scope':'Explicit paint,swatch,stroke,transparency,shape,layer,graphicStyle,appearance,effect,guide,attributes and magicWand native semantics on public fixed64/source46;incomplete exhaustive commands/GUI/creative/V1 acceptance;shape/layer/graphicStyle/appearance/effect/guide/attributes/magicWand have separate actual app-window captures;layer/style state-only commands preserve canvas pixels and use independent session readbacks;earlier native canvas images are not OS-window screenshots',
            'commands':entries}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true');args=parser.parse_args();result=verify()
    if args.write:(ROOT/MATRIX).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    elif json.loads((ROOT/MATRIX).read_text())!=result:raise SystemExit('command_family_matrix_drift')
    print(json.dumps({'result':'PASS',**result['coverage'],'tasksClosed':[]}))
