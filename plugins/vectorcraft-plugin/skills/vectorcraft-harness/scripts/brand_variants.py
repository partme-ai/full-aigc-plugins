"""从原生对象而非 RGB 相等性核验色板依赖更新。"""
import hashlib
import json
import math
import re


def snapshot(document):
    """提取对象自身属性；容器子对象独立编号，保留原有子对象顺序。"""
    if not isinstance(document, dict) or not isinstance(document.get('layers'), list) or not isinstance(document.get('artboards'), list):
        raise ValueError('invalid_brand_snapshot')
    result = {}

    def visit(obj):
        if not isinstance(obj, dict) or type(obj.get('id')) is not int or obj['id'] <= 0 or not isinstance(obj.get('kind'), dict) or obj['id'] in result:
            raise ValueError('invalid_brand_snapshot')
        kind = obj['kind']
        own = {**obj, 'kind': {key: value for key, value in kind.items() if key != 'children'}}
        if 'children' in kind:
            if not isinstance(kind['children'], list):
                raise ValueError('invalid_brand_snapshot')
            own['kind']['children'] = [child.get('id') if isinstance(child, dict) else None for child in kind['children']]
        result[obj['id']] = own
        for child in kind.get('children', []):
            visit(child)

    for obj in document['layers']:
        visit(obj)
    return result


def uses_token(value, token):
    """仅原生显式 swatch 引用构成消费关系，颜色相同不构成依赖。"""
    if isinstance(value, dict):
        return value.get('swatch') == token or any(uses_token(child, token) for child in value.values())
    if isinstance(value, list):
        return any(uses_token(child, token) for child in value)
    return False


def color_channels(value):
    """保留固定运行时的 RGB／CMYK／Gray／Lab 作者模型，不以跨模型近似伪造相等。"""
    if isinstance(value, str) and re.fullmatch(r'#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?', value):
        return 'rgb', tuple(int(value[i:i+2], 16)/255 for i in (1, 3, 5))
    if isinstance(value, dict):
        model = value.get('model') or ('lab' if {'l', 'a', 'b'} <= value.keys() else
                'cmyk' if {'c', 'm', 'y', 'k'} <= value.keys() else 'gray' if 'k' in value else 'rgb')
        names = {'rgb': ('r', 'g', 'b'), 'cmyk': ('c', 'm', 'y', 'k'), 'gray': ('k',), 'lab': ('l', 'a', 'b')}.get(model)
        if names and set(names) <= value.keys():
            channels = tuple(value[k] for k in names)
            if all(type(v) in (int, float) and math.isfinite(v) for v in channels):
                return model, channels
    raise ValueError('unsupported_brand_color_model')


def matches_color(value, target, tint=1.):
    """按原生 Color.tinted 语义检查消费者；浮点容差仅用于 f32 序列化。"""
    model, channels = color_channels(value)
    expected_model, expected = target
    if model != expected_model:
        return False
    if model == 'rgb':
        desired = tuple(1 - tint + tint * c for c in expected)
    elif model == 'lab':
        desired = (100 - (100 - expected[0]) * tint, expected[1] * tint, expected[2] * tint)
    else:
        desired = tuple(tint * c for c in expected)
    return len(channels) == len(desired) and all(abs(a-b) < 1e-5 for a, b in zip(channels, desired))


def bound_fields(value, token, path=()):
    """返回实际含 swatch 的颜色字段，不能把整个消费者视为修改豁免。"""
    result = {}
    if isinstance(value, dict):
        if value.get('swatch') == token and 'color' in value:
            result[path + ('color',)] = (value['color'], value.get('tint', 1.))
        for key, child in value.items():
            result.update(bound_fields(child, token, path + (key,)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            result.update(bound_fields(child, token, path + (index,)))
    return result


def without_bound_colors(value, token, palette=False):
    """只忽略绑定颜色的值；绑定、透明度、文字和几何仍参加严格比对。"""
    if isinstance(value, dict):
        if palette and value.get('name') == token and isinstance(value.get('paint'), dict) and 'color' in value['paint']:
            value = {**value, 'paint': {**value['paint'], 'color': None}}
        return {key: None if key == 'color' and value.get('swatch') == token
                else without_bound_colors(child, token, palette) for key, child in value.items()}
    if isinstance(value, list):
        return [without_bound_colors(child, token, palette) for child in value]
    return value


def inspect_update(before, after, token, expected_color=None):
    """返回依赖检查报告；未知模型拒绝检查，不伪造成功结论。"""
    if not isinstance(token, str) or not token:
        raise ValueError('invalid_brand_token')
    original, updated = snapshot(before), snapshot(after)
    consumers = {key for key, value in original.items() if uses_token(value, token)}
    # 子对象增删会同时改变父容器的顺序引用，报告实际对象和受影响容器。
    affected = set(original) ^ set(updated)
    shared = set(original) & set(updated)
    changed = {key for key in shared - consumers if original[key] != updated[key]}
    consumer_changed = {key for key in shared & consumers
                        if without_bound_colors(original[key], token) != without_bound_colors(updated[key], token)}
    structural = {key for key in shared if original[key]['kind'].get('children') != updated[key]['kind'].get('children')}
    root_order_changed = [obj['id'] for obj in before['layers']] != [obj['id'] for obj in after['layers']]
    if root_order_changed:
        structural.update(obj['id'] for obj in before['layers'])
        structural.update(obj['id'] for obj in after['layers'])
    affected |= changed
    affected |= consumer_changed
    affected |= structural
    edges = [{'token': token, 'objectId': key,
              'reason': 'object_structure_changed' if key in structural else
                        'consumer_noncolor_changed' if key in consumer_changed else
                        'unbound_object_changed' if key in changed else 'object_identity_changed'}
             for key in sorted(affected)]
    artboards_changed = before['artboards'] != after['artboards']
    mismatches = []
    fields_changed = False
    target = color_channels(expected_color) if expected_color is not None else None
    for key in sorted(consumers & shared):
        old_fields = bound_fields(original[key], token)
        new_fields = bound_fields(updated[key], token)
        fields_changed |= old_fields != new_fields
        if target is not None:
            valid = bool(old_fields) and old_fields.keys() == new_fields.keys()
            for color, tint in new_fields.values():
                try:
                    if type(tint) not in (int, float) or not math.isfinite(tint) or not 0 <= tint <= 1:
                        valid = False
                        continue
                    valid &= matches_color(color, target, tint)
                except ValueError:
                    valid = False
            if not valid:
                mismatches.append(key)
    no_consumers = expected_color is not None and not consumers
    palette_changed = False
    token_mismatch = False
    if 'swatches' in before or 'swatch_groups' in before:
        old_palette = {k: before.get(k, []) for k in ('swatches', 'swatch_groups')}
        new_palette = {k: after.get(k, []) for k in ('swatches', 'swatch_groups')}
        palette_changed = without_bound_colors(old_palette, token, True) != without_bound_colors(new_palette, token, True)
        if target is not None:
            candidates = list(new_palette['swatches'])
            for group in new_palette['swatch_groups']:
                candidates.extend(group.get('swatches', []))
            selected = [swatch for swatch in candidates if swatch.get('name') == token]
            try:
                token_mismatch = len(selected) != 1 or not matches_color(selected[0]['paint']['color'], target)
            except (ValueError, KeyError, TypeError):
                token_mismatch = True
    digest = lambda value: hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()
    return {'schema': 'vectorcraft-brand-dependency-check/v1',
            'status': 'failed' if affected or artboards_changed or mismatches or no_consumers or palette_changed or token_mismatch else 'passed', 'token': token,
            'paletteChangedUnexpectedly': palette_changed, 'tokenTargetMismatch': token_mismatch,
            'targetMismatchObjectIds': mismatches,
            'effect': 'no_effect' if no_consumers else 'updated' if fields_changed else 'verified_noop' if target is not None and not mismatches else 'not_verified',
            'consumerIds': sorted(consumers), 'affectedObjectIds': sorted(affected),
            'unexpectedDependencies': edges, 'artboardsChanged': artboards_changed,
            'beforeSha256': digest(before), 'afterSha256': digest(after),
            'scope': 'native explicit swatch color fields; consumer noncolor fields, palette, identities, artboards and requested authoring-model target'}


def instance_bounds(inspection, ids):
    """读取实际原生检查结果中的实例联合边界；未知或非有限边界不伪造。"""
    found = {}
    def visit(nodes):
        for node in nodes:
            found[node['id']] = node.get('bounds')
            visit(node.get('children', []))
    visit(inspection['layers'])
    boxes = [found.get(i) for i in ids]
    if not boxes or not all(isinstance(box, dict) and all(type(box.get(k)) in (int, float) and math.isfinite(box[k]) for k in ('x','y','width','height')) and box['width'] >= 0 and box['height'] >= 0 for box in boxes):
        return None
    x, y = min(box['x'] for box in boxes), min(box['y'] for box in boxes)
    return {'x':x, 'y':y, 'width':max(box['x']+box['width'] for box in boxes)-x, 'height':max(box['y']+box['height'] for box in boxes)-y}


def inspect_asset_update(before, after, asset, mapping, before_inspect, after_inspect):
    """核验登记素材的真实子树替换映射、实例边界及非消费者保全。"""
    original, updated = snapshot(before), snapshot(after)
    if not isinstance(asset, str) or not asset or not isinstance(mapping, dict) or not mapping:
        raise ValueError('asset_dependency_mapping')
    def subtree(nodes, root):
        if root not in nodes:
            raise ValueError('asset_dependency_mapping')
        result = {root}
        for child in nodes[root]['kind'].get('children', []):
            result |= subtree(nodes, child)
        return result
    old_ids, new_ids = set(), set()
    for old, replacements in mapping.items():
        if type(old) is not int or not isinstance(replacements, list) or not replacements or any(type(i) is not int for i in replacements) or len(replacements) != len(set(replacements)):
            raise ValueError('asset_dependency_mapping')
        consumed = subtree(original, old)
        if consumed & old_ids:
            raise ValueError('asset_dependency_mapping')
        old_ids |= consumed
        for new in replacements:
            replaced = subtree(updated, new)
            if replaced & new_ids:
                raise ValueError('asset_dependency_mapping')
            new_ids |= replaced
    # 新消费者不能吞入原有的无关对象，哪怕对象自身字段没有变化。
    if new_ids & (original.keys() - old_ids):
        raise ValueError('asset_dependency_mapping')
    def mapped(ids):
        return [new for old in ids for new in mapping.get(old, [old])]
    unaffected = original.keys() - old_ids
    affected = set(unaffected - updated.keys()) | (updated.keys() - unaffected - new_ids)
    for object_id in unaffected & updated.keys():
        expected = original[object_id]
        if 'children' in expected['kind']:
            expected = {**expected, 'kind': {**expected['kind'], 'children': mapped(expected['kind']['children'])}}
        if expected != updated[object_id]:
            affected.add(object_id)
    if mapped([obj['id'] for obj in before['layers']]) != [obj['id'] for obj in after['layers']]:
        affected |= {obj['id'] for obj in before['layers']} | {obj['id'] for obj in after['layers']}
    mismatches = []
    for old, replacements in mapping.items():
        a = instance_bounds(before_inspect, [old])
        b = instance_bounds(after_inspect, replacements)
        if a is None or b is None or any(abs(a[k]-b[k]) > 1e-5 for k in a):
            mismatches.append(old)
    artboards_changed = before['artboards'] != after['artboards']
    edges = [{'asset':asset, 'objectId':i, 'reason':'unbound_object_or_structure_changed'} for i in sorted(affected)]
    edges += [{'asset':asset, 'objectId':i, 'reason':'instance_bounds_changed'} for i in mismatches]
    digest = lambda value: hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()
    return {'schema':'vectorcraft-brand-asset-dependency-check/v1', 'status':'failed' if affected or mismatches or artboards_changed else 'passed',
            'asset':asset, 'consumerIds':sorted(mapping), 'replacementIds':sorted(i for ids in mapping.values() for i in ids),
            'replacementMapping':{str(i):ids for i,ids in mapping.items()}, 'affectedObjectIds':sorted(affected),
            'boundsMismatchObjectIds':mismatches, 'unexpectedDependencies':edges, 'artboardsChanged':artboards_changed,
            'beforeSha256':digest(before), 'afterSha256':digest(after),
            'scope':'registered native asset consumer subtrees, explicit replacement identities, instance bounds and unrelated object/stacking/artboard preservation'}
