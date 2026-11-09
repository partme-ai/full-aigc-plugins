"""由本次form_fields的原始返回与用户值生成同会话填写请求，不操作PDF。"""
import argparse
import json
from pathlib import Path


def build_request(snapshot, values, doc):
    if type(doc) is not int or doc<1:
        raise ValueError('doc must be the positive id returned in the current session')
    if not isinstance(snapshot,dict) or not isinstance(snapshot.get('fields'),list):
        raise ValueError('raw form_fields result with fields array required')
    if not isinstance(values,dict) or not values:
        raise ValueError('nonempty user field mapping required')
    fields={}
    for field in snapshot['fields']:
        if not isinstance(field,dict) or not isinstance(field.get('name'),str) or not field['name'] or field['name'] in fields:
            raise ValueError('field names must be present and unambiguous')
        fields[field['name']]=field
    for name,value in values.items():
        if name not in fields:
            raise ValueError('requested field is absent from the current snapshot')
        field=fields[name]
        if field.get('read_only') is not False:
            raise ValueError('field is read-only or writable status is unknown')
        if field.get('type')=='text':
            if not isinstance(value,str) or '\0' in value:
                raise ValueError('text fields require strings without NUL')
            if field.get('required') is True and not value.strip():
                raise ValueError('required text field cannot be blank')
            if field.get('multiline') is not True and any(c in value for c in '\r\n\u2028\u2029'):
                raise ValueError('single-line field cannot contain line breaks')
        elif field.get('type')=='checkbox':
            if type(value) is not bool:
                raise ValueError('checkbox requires a JSON boolean')
        else:
            raise ValueError('helper supports text and checkbox only; inspect other types using the native schema')
    return {'tool':'form_fill','arguments':{'doc':doc,'values':dict(values)},
        'scope':'current session and current field snapshot only; not an executable CLI script',
        'checks':['Inspect form_fill warnings; unsupported glyphs do not count as accepted appearance','Save a new output path, reopen and compare actual field values','Render affected pages and inspect appearance; filling is not signing']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--fields',type=Path,required=True);p.add_argument('--values',type=Path,required=True);p.add_argument('--doc',type=int,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    result=build_request(json.loads(a.fields.read_text(encoding='utf-8')),json.loads(a.values.read_text(encoding='utf-8')),a.doc)
    with a.output.open('x',encoding='utf-8') as stream:json.dump(result,stream,ensure_ascii=False,indent=2);stream.write('\n')
if __name__=='__main__':main()
