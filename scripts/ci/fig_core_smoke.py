"""六项Fig核心的真实CLI检查；原型连线检查不冒充浏览器点击。"""
import copy
import hashlib
import json
from pathlib import Path
import struct
import urllib.request
import xml.etree.ElementTree as ET
from fig_playbook_smoke import read_nodes, near


def verify_wireframe(nodes):
    assert 'frame' in nodes, 'Missing returned frame binding'
    frame = nodes['frame']
    assert [frame['width'], frame['height']] == [1280, 1024], 'Desktop frame size wrong'
    children = {n['name']: n for n in frame['children']}
    for name in ['Navigation', 'PageTitle', 'ContentCard', 'PrimaryAction']:
        assert name in children, 'Wireframe region missing: ' + name
    assert children['PageTitle']['characters'] == '页面目标', 'Editable title missing'
    assert children['PrimaryAction']['width'] >= 120, 'Primary action too narrow'


def verify_responsive(nodes, width, height):
    root = nodes['root']
    assert near(root['width'], width) and near(root['height'], height), 'Requested viewport not applied'
    assert root['layout']['mode'].lower() == 'vertical', 'No vertical auto layout'
    for key in ['heading', 'card', 'button']:
        node = nodes[key]
        assert near(node['x'], 24) and near(node['width'], width-48), 'Child did not fill resized parent: ' + key
        assert node['y'] >= 24 and node['y'] + node['height'] <= height-24, 'Child overflow: ' + key
    for first, last in [('heading', 'card'), ('card', 'button')]:
        assert near(nodes[last]['y']-nodes[first]['y']-nodes[first]['height'], 24), 'Responsive gap wrong'


def bind_strings(value):
    if isinstance(value, str) and value.startswith('$'):
        return {'$ref': value[1:]}
    if isinstance(value, dict):
        return {k: bind_strings(v) for k, v in value.items()}
    if isinstance(value, list):
        return [bind_strings(v) for v in value]
    return value


def run_core(r, helper, skill_root):
    original = r.work
    records = []
    try:
        for name in ['wireframe', 'responsive-layout', 'design-system', 'dev-handoff', 'prototype-flow', 'import-fig']:
            r.work = original / ('core-' + name)
            r.work.mkdir()
            path = Path(skill_root) / ('figcraft-' + name) / 'references/craft-steps.json'
            recipe = json.loads(path.read_text(encoding='utf-8'))
            # Native CLI receives only resolved real IDs. The skill's $strings are explanatory bindings.
            recipe['steps'] = bind_strings(recipe['steps'])
            source = None
            source_hash = None
            if name == 'import-fig':
                lock = json.loads(Path(__file__).with_name('fig_import_fixture.lock.json').read_text())
                raw = urllib.request.urlopen(lock['url'], timeout=60).read(lock['bytes']+1)
                assert len(raw) == lock['bytes'] and hashlib.sha256(raw).hexdigest() == lock['sha256'], 'Figma fixture digest mismatch'
                source = r.work / 'corners.fig'
                source.write_bytes(raw)
                recipe['steps'][0]['params']['path'] = str(source)
                source_hash = lock['sha256']
            target = r.work / 'result.figcraft'
            receipt = helper.execute_recipe(recipe, r.run, r.work, target)
            (r.work/'receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
            bindings = {k: v for k, v in receipt['bindings'].items() if isinstance(v, dict) and 'id' in v}
            nodes = read_nodes(r, str(target), bindings) if bindings else {}
            def commands(steps, output=None, input_file=target):
                script = r.work/'query.json'
                script.write_text(json.dumps(steps, ensure_ascii=False), encoding='utf-8')
                args = ['run', script, '--in', input_file] + (['--out', output] if output else [])
                rows = [json.loads(line) for line in r.run(*args).splitlines() if line.strip()]
                assert len(rows)==len(steps) and all(v['ok'] for v in rows), 'Core follow-up failed'
                return [v['result'] for v in rows]
            record = {'id': name, 'technicalRoundtrip': 'PASS', 'returnedIdBinding': 'PASS', 'designReview': 'NOT_TESTED', 'installedHostSync': 'NOT_TESTED'}
            if name == 'wireframe':
                verify_wireframe(nodes)
                root_id = bindings['frame']['id']
            elif name == 'responsive-layout':
                root_id = bindings['root']['id']
                for width, height in [(390,884), (768,1024), (1280,1024)]:
                    out = r.work/f'viewport-{width}.figcraft'
                    commands([{'command':'node.set','params':{'id':root_id,'props':{'width':width,'height':height}}}], out)
                    resized = read_nodes(r,str(out),bindings)
                    verify_responsive(resized,width,height)
                    r.run('export',out,'--node',str(root_id),'-o',f'viewport-{width}.png','--format','png')
                record['actualThreeViewportLayouts'] = 'PASS'
            elif name == 'design-system':
                root_id = bindings['root']['id']
                assert nodes['root']['type']=='COMPONENT', 'Main component missing'
                assert nodes['instance']['mainComponent']==root_id, 'Instance detached from main'
                assert any(c.get('characters')=='Proceed' for c in nodes['instance'].get('children',[])), 'Instance text property not applied'
                assert nodes['label']['characters']=='Continue', 'Instance override changed main label'
                revised = r.work/'revised.figcraft'
                commands([{'command':'node.set','params':{'id':root_id,'props':{'width':280}}}], revised)
                after=read_nodes(r,str(revised),bindings)
                assert near(after['instance']['width'],280), 'Main size change did not propagate'
                assert any(c.get('characters')=='Proceed' for c in after['instance'].get('children',[])), 'Text override lost after main edit'
                record['instanceOverrideAndMainPropagation']='PASS'
            elif name == 'dev-handoff':
                root_id=bindings['root']['id']
                code=receipt['bindings'].get('code',{})
                assert code.get('language')=='css' and '24px' in code.get('code',''), 'Actual CSS dimensions missing'
                assets=receipt['bindings'].get('exports',{}).get('files',[])
                assert len(assets)==2, 'Not two configured export variants'
                sizes=[]
                for row in assets:
                    p=Path(row['path']); p=p if p.is_absolute() else r.work/p
                    sizes.append(list(struct.unpack('>II',p.read_bytes()[16:24])))
                assert sorted(sizes)==[[24,24],[48,48]], '1x/2x exported icon pixel sizes wrong'
                record['actualCssAndTwoScaleAssets']='PASS'
            elif name == 'prototype-flow':
                root_id=bindings['start']['id']
                for key in ['button','back']:
                    interactions=nodes[key].get('interactions',[])
                    assert len(interactions)==1, 'Prototype hotspot missing'
                assert str(bindings['result']['id']) in json.dumps(nodes['button']['interactions']), 'Forward target missing'
                record['technicalRoundtrip']='PARTIAL'
                record['prototypeLinksPersisted']='PASS'
                record['actualBrowserClick']='NOT_TESTED'
            else:
                assert source_hash==hashlib.sha256(source.read_bytes()).hexdigest(), 'Original Figma file changed'
                info=json.loads(r.run('info',target,'--json'));page=info['pages'][0]['id']
                page_node=commands([{'command':'node.get','params':{'id':page}}])[0]
                imported={n['name']:n for n in page_node['children']}
                assert len(imported)==10, 'Real Figma fixture did not preserve ten layers'
                for key in ['rect radius=4:8:12:16','frame radius=4:8:12:16','shape radius=4:8:12:16']:
                    assert key in imported, 'Imported Figma layer missing: '+key
                # Mixed corner ordering differs by Figma shape kind; verify the concrete rect in native orientation.
                assert imported['rect radius=4:8:12:16'].get('cornerRadius')==[4.0,8.0,12.0,16.0], 'Mixed rectangle corner radii lost'
                root_id=imported['frame radius=4:8:12:16']['id']
                (r.work/'imported-page.json').write_text(json.dumps(page_node,ensure_ascii=False,indent=2),encoding='utf-8')
                record['actualBinaryFigFixture']='PASS'
                record['broadImportFidelity']='NOT_TESTED'
                record['importWarnings']=receipt['bindings'].get('imported',{}).get('warnings')
            r.run('export',target,'--node',str(root_id),'-o','proof.png','--format','png')
            r.run('export',target,'--node',str(root_id),'-o','proof.svg','--format','svg')
            ET.fromstring((r.work/'proof.svg').read_bytes())
            (r.work/'nodes.json').write_text(json.dumps(nodes,ensure_ascii=False,indent=2),encoding='utf-8')
            records.append(record)
        return records
    finally:
        r.work=original
