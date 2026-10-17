"""分组／Pathfinder事务：固定原生ID、持久检查点与明确失败后的恢复。"""
import copy
import hashlib
import json
import os
import subprocess
from pathlib import Path


COMMANDS = {'object.group', 'object.ungroup'} | {
    'object.pathfinder.'+name for name in (
        'unite', 'minusFront', 'intersect', 'exclude', 'divide', 'trim',
        'merge', 'crop', 'outline', 'minusBack')}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def nodes(document):
    """收集真实对象及父节点；拒绝重复身份或畸形对象树。"""
    result = {}
    def walk(items):
        if not isinstance(items, list):
            raise ValueError('invalid_boolean_native_tree')
        for item in items:
            if (not isinstance(item, dict) or type(item.get('id')) is not int or item['id'] <= 0
                    or item['id'] in result or not isinstance(item.get('kind'), dict)):
                raise ValueError('invalid_boolean_native_tree')
            result[item['id']] = item
            if 'children' in item['kind']:
                walk(item['kind']['children'])
    walk(document.get('layers'))
    return result


def normalized(document):
    value = copy.deepcopy(document)
    if isinstance(value.get('metadata'), dict):
        value['metadata'].pop('modified', None)
    return value


def pruned(document, excluded):
    """比较目标子树以外的完整对象、祖先属性与顺序。"""
    value = normalized(document)
    value.pop('next_id', None)
    def walk(items):
        kept = []
        for item in items:
            if item['id'] in excluded:
                continue
            if 'children' in item['kind']:
                item['kind']['children'] = walk(item['kind']['children'])
            kept.append(item)
        return kept
    value['layers'] = walk(value['layers'])
    return value


def write_report(path, data):
    temporary = path.with_suffix('.writing')
    with temporary.open('w', encoding='utf-8') as stream:
        json.dump(data, stream, ensure_ascii=False, allow_nan=False, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def verify_result(before, after, identifier, ids, result, selection=None):
    """独立复核结构结果与未选对象；供事务和受控执行复用同一规则。"""
    objects = nodes(before)
    current = nodes(after)
    if identifier == 'object.ungroup':
        result_ids = selection
    else:
        result_ids = ([result['id']] if isinstance(result, dict) and 'id' in result else
                      result.get('ids') if isinstance(result, dict) else None)
    if (not isinstance(result_ids, list)
            or any(type(i) is not int or i not in current for i in result_ids) or len(set(result_ids)) != len(result_ids)):
        raise RuntimeError('boolean_result_identity_mismatch')
    if identifier == 'object.group':
        if len(result_ids) != 1 or current[result_ids[0]]['kind'].get('type') != 'group':
            raise RuntimeError('boolean_group_identity_mismatch')
        group_nodes = nodes({'layers':current[result_ids[0]]['kind'].get('children')})
        if any(i not in group_nodes or group_nodes[i] != objects[i] for i in ids):
            raise RuntimeError('boolean_group_source_violation')
    elif identifier == 'object.ungroup':
        expected = []
        for i in ids:
            if objects[i]['kind'].get('type') != 'group':
                raise RuntimeError('boolean_ungroup_source_violation')
            expected.extend(objects[i]['kind'].get('children', []))
        if set(result_ids) != {v['id'] for v in expected} or any(current.get(v['id']) != v for v in expected):
            raise RuntimeError('boolean_ungroup_result_violation')
    else:
        if any(i in objects and i not in ids for i in result_ids):
            raise RuntimeError('boolean_result_identity_reused')
        result_tree = nodes({'layers':[current[i] for i in result_ids]})
        if any(i in current and i not in result_tree for i in ids):
            raise RuntimeError('boolean_sources_not_consumed')
    if pruned(before, set(ids)) != pruned(after, set(result_ids)):
        raise RuntimeError('boolean_unselected_violation')
    return result_ids


def execute(session, identifier, params, invoke, stage):
    """执行一次已分类操作；不明确回复不恢复、不重放，保留原位置检查点。"""
    if identifier not in COMMANDS:
        return invoke()
    if params != {}:
        raise ValueError('boolean_operation_requires_live_selection')
    stage = Path(stage)
    report_path = stage/'boolean-transactions.json'
    report = (json.loads(report_path.read_text()) if report_path.exists()
              else {'schema':'vectorcraft-boolean-transactions/v1', 'operations':[]})
    if report.get('schema') != 'vectorcraft-boolean-transactions/v1' or not isinstance(report.get('operations'), list):
        raise ValueError('invalid_boolean_transaction_report')
    before = session.command('document.json', {})
    objects = nodes(before)
    inspection = session.command('document.inspect', {})
    ids = inspection.get('selection') if isinstance(inspection, dict) else None
    if (not isinstance(ids, list) or not ids
            or any(type(i) is not int or i not in objects for i in ids) or len(set(ids)) != len(ids)):
        raise ValueError('boolean_selection_identity_mismatch')
    checkpoint = stage/('boolean-checkpoint-'+str(len(report['operations']))+'.vectorcraft')
    if checkpoint.exists() or checkpoint.is_symlink():
        raise ValueError('boolean_checkpoint_exists')
    session.command('document.save', {'path':str(checkpoint)})
    if not checkpoint.is_file() or checkpoint.is_symlink():
        raise RuntimeError('boolean_checkpoint_missing')
    with checkpoint.open('rb') as stream:
        os.fsync(stream.fileno())
    entry = {'command':identifier, 'participantIds':ids, 'resultIds':None,
             'checkpoint':checkpoint.name, 'checkpointSha256':digest(checkpoint),
             'status':'submitted', 'replayAllowed':False}
    report['operations'].append(entry)
    write_report(report_path, report)
    try:
        result = invoke()
        after = session.command('document.json', {})
        selection = session.command('document.inspect', {}).get('selection') if identifier == 'object.ungroup' else None
        result_ids = verify_result(before, after, identifier, ids, result, selection)
        if digest(checkpoint) != entry['checkpointSha256']:
            raise RuntimeError('boolean_checkpoint_changed')
        entry.update(status='verified', resultIds=result_ids)
        write_report(report_path, report)
        return result
    except (ValueError, RuntimeError, OSError, TimeoutError, subprocess.SubprocessError) as error:
        entry['error'] = str(error)
        uncertain = isinstance(error, (TimeoutError, subprocess.SubprocessError)) or any(value in str(error) for value in (
            'outcome_unknown', 'mcp_disconnected', 'mcp_response_too_large', 'cancel_requested',
            'deadline_exceeded', 'stale_epoch', 'revision_conflict', 'output_budget_exceeded'))
        if uncertain:
            entry['status'] = 'unknown'
            write_report(report_path, report)
            raise
        # 只恢复明确失败且仍可查询的同一个会话，不发起第二次有副作用操作。
        try:
            damaged = normalized(session.command('document.json', {})) != normalized(before)
            if damaged:
                if checkpoint.is_symlink() or digest(checkpoint) != entry['checkpointSha256']:
                    raise RuntimeError('boolean_checkpoint_changed')
                session.command('document.open', {'path':str(checkpoint)})
                if normalized(session.command('document.json', {})) != normalized(before):
                    raise RuntimeError('boolean_restore_identity_mismatch')
                session.command('select.set', {'ids':ids})
                entry['status'] = 'restored_after_failure'
            else:
                entry['status'] = 'failed_without_mutation'
        except (ValueError, RuntimeError, OSError, TimeoutError, subprocess.SubprocessError) as restore_error:
            entry.update(status='restore_unconfirmed', restoreError=str(restore_error))
            write_report(report_path, report)
            raise RuntimeError('outcome_unknown: boolean_restore_unconfirmed; '+str(error)) from restore_error
        write_report(report_path, report)
        if damaged:
            raise RuntimeError('non_atomic_operation_defect: restored checkpoint; '+str(error)) from error
        raise



def checkpoint_model(document, project):
    """收集前后比较完整模型；仅以实际文件摘要替代链接路径及复制后的mtime。"""
    value = normalized(document)
    for node in nodes(value).values():
        kind = node['kind']
        if kind.get('type') == 'image' and isinstance(kind.get('link'), dict):
            link = kind['link']
            path = Path(link['path'])
            if not path.is_absolute():
                path = Path(project).parent/path
            if path.is_symlink() or not path.is_file():
                raise RuntimeError('boolean_checkpoint_link_missing')
            link['contentSha256'] = digest(path)
            for key in ('path', 'relative', 'modified'):
                link.pop(key, None)
    return value


def collect_checkpoints(original, destination, session_factory):
    """素材收集改变交付根时独立打包检查点，避免遗失或保留已失效的绝对链接。"""
    original, destination = Path(original), Path(destination)
    report_path = original/'boolean-transactions.json'
    if original == destination or not report_path.is_file():
        return
    report = json.loads(report_path.read_text())
    for index, entry in enumerate(report['operations']):
        source = original/entry['checkpoint']
        if source.is_symlink() or digest(source) != entry['checkpointSha256']:
            raise RuntimeError('boolean_checkpoint_changed')
        bundle = destination/('boolean-checkpoint-'+str(index)+'-bundle')
        if bundle.exists() or bundle.is_symlink():
            raise ValueError('boolean_checkpoint_exists')
        with session_factory() as session:
            session.command('document.open', {'path':str(source)})
            before = checkpoint_model(session.command('document.json', {}), source)
            packaged = session.command('file.package', {'folder':str(bundle),'name':'checkpoint','report':False})
            if packaged.get('missingLinks'):
                raise RuntimeError('boolean_checkpoint_missing_links')
            checkpoint = bundle/'checkpoint'/source.name
            if not checkpoint.is_file() or checkpoint.is_symlink():
                raise RuntimeError('boolean_checkpoint_package_missing')
            session.command('document.open', {'path':str(checkpoint)})
            if before != checkpoint_model(session.command('document.json', {}), checkpoint):
                raise RuntimeError('boolean_checkpoint_package_identity_mismatch')
            links = session.command('links.check', {})
            if links.get('missing') or links.get('modified'):
                raise RuntimeError('boolean_checkpoint_package_links_invalid')
        entry.update(originalCheckpointSha256=entry['checkpointSha256'],
                     checkpoint=str(checkpoint.relative_to(destination)),checkpointSha256=digest(checkpoint),
                     checkpointCollection='native-package; linked dependencies included')
    write_report(destination/'boolean-transactions.json', report)
