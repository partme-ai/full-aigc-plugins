"""画板导出的稳定身份合同；索引只描述当前顺序，ID描述原生画板身份。"""
import math


def validate_exports(exports):
    """在运行时安装前核验输出列表、格式与显式定位参数。"""
    if not isinstance(exports,list):raise ValueError('invalid_export')
    seen=set()
    for item in exports:
        if not isinstance(item,dict) or set(item)-{'format','artboard','artboardId'} or item.get('format') not in ('svg','png','pdf'):raise ValueError('invalid_export')
        if 'artboard' in item and (type(item['artboard']) is not int or item['artboard']<0):raise ValueError('invalid_export')
        if 'artboardId' in item:
            value=item['artboardId']
            if not ((type(value) is int and value>0) or (isinstance(value,dict) and set(value)=={'$ref'} and isinstance(value['$ref'],str) and value['$ref'])):raise ValueError('invalid_export')
        key=(item['format'],item.get('artboard',0),str(item.get('artboardId')))
        if key in seen:raise ValueError('duplicate_export')
        seen.add(key)


def snapshot(native):
    """返回实际原生画板顺序、ID、名称、矩形与文档单位尺寸；不从像素推断。"""
    boards=native.get('artboards') if isinstance(native,dict) else None
    if not isinstance(boards,list):raise ValueError('invalid_native_artboard')
    result=[];seen=set()
    for index,board in enumerate(boards):
        if not isinstance(board,dict) or type(board.get('id')) is not int or board['id']<=0 or board['id'] in seen or not isinstance(board.get('name'),str):raise ValueError('invalid_native_artboard')
        rect=board.get('rect')
        if not isinstance(rect,dict) or any(type(rect.get(k)) not in (int,float) or not math.isfinite(rect[k]) for k in ('x0','y0','x1','y1')) or rect['x1']<=rect['x0'] or rect['y1']<=rect['y0']:raise ValueError('invalid_native_artboard')
        if not math.isfinite(rect['x1']-rect['x0']) or not math.isfinite(rect['y1']-rect['y0']):raise ValueError('invalid_native_artboard')
        seen.add(board['id']);result.append({'id':board['id'],'index':index,'name':board['name'],'rect':dict(rect),'width':rect['x1']-rect['x0'],'height':rect['y1']-rect['y0']})
    return result


def resolve_exports(exports,native,bindings,source_native=None):
    """一次解析全部导出；返工旧索引绑定操作前实际源ID，显式ID可跟随新顺序。"""
    validate_exports(exports);boards=snapshot(native);prior=snapshot(source_native) if source_native is not None else [];by_id={b['id']:b for b in boards};result=[];seen=set()
    for item in exports:
        target=item.get('artboardId')
        if isinstance(target,dict):
            value=bindings
            try:
                for part in target['$ref'].split('.'):value=value[int(part)] if isinstance(value,list) else value[part]
            except (KeyError,IndexError,TypeError,ValueError):raise ValueError('invalid_artboard_reference') from None
            target=value
            if type(target) is not int or target<=0:raise ValueError('invalid_artboard_reference')
        index=item.get('artboard',0)
        if target is not None:
            if target not in by_id:raise ValueError('artboard_id_not_found: '+str(target))
            board=by_id[target]
            if 'artboard' in item and board['index']!=index:raise ValueError(f'artboard_mapping_conflict: expectedId={target} actualId={boards[index]["id"] if index<len(boards) else None} resolvedIndex={board["index"]}')
        else:
            if index>=len(boards):raise ValueError('artboard_out_of_range')
            board=boards[index]
            if index<len(prior) and prior[index]['id']!=board['id']:
                expected=prior[index]['id'];raise ValueError(f'artboard_mapping_conflict: expectedId={expected} actualId={board["id"]} resolvedIndex={by_id.get(expected,{}).get("index")}')
        key=(item['format'],board['id'])
        if key in seen:raise ValueError('duplicate_export')
        seen.add(key);result.append({'format':item['format'],'artboardIndex':board['index'],'artboardId':board['id'],'artboardName':board['name'],'artboardRect':board['rect']})
    return result


def bind_created(reply,native):
    """将artboard.new原生索引回执绑定同会话查得的稳定ID；不把索引冒充ID。"""
    boards=snapshot(native)
    if not isinstance(reply,dict) or type(reply.get('index')) is not int or not 0<=reply['index']<len(boards):raise ValueError('invalid_artboard_reply')
    board=boards[reply['index']]
    if 'id' in reply and (type(reply['id']) is not int or reply['id']!=board['id']):raise ValueError('invalid_artboard_reply')
    return {**reply,'id':board['id']}
