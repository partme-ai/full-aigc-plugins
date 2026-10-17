"""所有公开文字修订入口共享显式目标与首样式合同。"""
def validate_text_edit(params):
    """要求唯一id或ids及字符串text；允许计划绑定，禁止隐式选择和字体替换。"""
    valid_ref=lambda value:isinstance(value,dict) and set(value)=={'$ref'} and isinstance(value['$ref'],str) and bool(value['$ref'])
    valid_id=lambda value:(type(value) is int and value>0) or valid_ref(value)
    if (not isinstance(params,dict) or set(params)-{'id','ids','text'} or not isinstance(params.get('text'),str)
            or ('id' in params)==('ids' in params)):
        raise ValueError('invalid_text_edit: explicit id or ids and string text required')
    if 'id' in params:valid=valid_id(params['id'])
    else:
        ids=params['ids'];valid=valid_ref(ids) or (isinstance(ids,list) and bool(ids) and all(valid_id(value) for value in ids))
    if not valid:raise ValueError('invalid_text_edit: invalid target')
