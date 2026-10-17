#!/usr/bin/env python3
"""将文档字段编译为原生WordCraft命令，不管理编辑器会话。"""
import argparse
import json
from pathlib import Path
import subprocess


def compile_template(template, values, allow_incomplete=False):
    if not isinstance(values, dict):
        raise ValueError('输入须为JSON对象')
    fields = template['fields']
    unknown = set(values) - set(fields)
    if unknown:
        raise ValueError('未知字段：' + ', '.join(sorted(unknown)))
    resolved = dict(values)
    missing = []
    for name, field in fields.items():
        value = resolved.get(name)
        absent = value is None or (isinstance(value, str) and not value.strip()) or value == []
        if absent:
            if field.get('required'):
                missing.append(name)
            resolved[name] = [['待确认'] * len(template['table']['headers'])] if field['type'] == 'rows' else '待确认'
        elif field['type'] == 'rows':
            if not isinstance(value, list) or any(not isinstance(row, list) or len(row) != len(template['table']['headers']) for row in value):
                raise ValueError('表格行列数错误：' + name)
            if any(not isinstance(cell, str) or any(c in cell for c in '\t\r\n') for row in value for cell in row):
                raise ValueError('表格单元格须为不含制表符或换行的字符串：' + name)
        elif not isinstance(value, str):
            raise ValueError('字段须为字符串：' + name)
    if missing and not allow_incomplete:
        raise ValueError('缺少必填字段：' + ', '.join(missing))
    steps = []
    def add(command, **params):
        steps.append({'command': command, 'params': params})
    def paragraph(text, style='para.normal', centered=False):
        add(style)
        add('para.alignCenter' if centered else 'para.alignLeft')
        add('text.insert', text=text)
        add('text.newParagraph')
    add('layout.size', name='A4')
    add('layout.margins', preset='normal')
    paragraph(resolved['title'], 'para.heading1', True)
    paragraph('日期：' + resolved['document_date'] + '    编写：' + resolved['author'])
    if missing:
        paragraph('资料不完整草稿；待确认：' + '、'.join(fields[name].get('label',name) for name in missing))
    for section in template['sections']:
        paragraph(section['title'], 'para.heading2')
        paragraph(resolved[section['field']])
    paragraph(template['table']['title'], 'para.heading2')
    table_rows = [template['table']['headers'], *resolved[template['table']['field']]]
    add('para.normal')
    # text.insert中的换行是软换行；表格转换需要真实段落作为行边界。
    for index, row in enumerate(table_rows):
        add('text.insert', text='\t'.join(row))
        if index < len(table_rows)-1:
            add('text.newParagraph')
    # select.text只在单个段落内查找，不能选择多行表格。
    add('caret.docEnd', extend=False)
    for _ in table_rows:
        add('caret.paraUp', extend=True)
    add('table.fromText', separator='tab')
    add('table.autofit', mode='window')
    add('table.repeatHeader')
    add('table.selectTable')
    add('table.borders', kind='all', width=0.5, color='D5DBE5')
    add('table.look', headerRow=True, bandedRows=True)
    return {'application': 'wordcraft', 'id': template['id'], 'steps': steps,
            'missingFields': missing, 'state': 'DRAFT_INCOMPLETE' if missing else 'READY_FOR_REVIEW'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--template', type=Path, default=Path(__file__).resolve().parents[1] / 'assets/template.json')
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True, help='填好字段后的命令JSON，新文件')
    parser.add_argument('--allow-incomplete', action='store_true')
    parser.add_argument('--save', type=Path, help='独立CLI新建DOCX；已有编辑器会话不使用此选项')
    parser.add_argument('--pdf', type=Path)
    parser.add_argument('--cli', default='wordcraft-cli')
    args = parser.parse_args()
    if args.pdf and not args.save:
        parser.error('--pdf需要--save')
    paths = [p.resolve() for p in [args.output, args.save, args.pdf] if p is not None]
    if len(set(paths)) != len(paths) or any(p.exists() for p in paths):
        parser.error('所有输出必须是不同且未占用的新路径')
    try:
        template = json.loads(args.template.read_text(encoding='utf-8'))
        values = json.loads(args.input.read_text(encoding='utf-8'))
        result = compile_template(template, values, args.allow_incomplete)
    except (ValueError, TypeError) as error:
        parser.error(str(error))
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    if args.save:
        argv = [args.cli, 'run']
        for step in result['steps']:
            argv += ['--cmd', step['command'] + '=' + json.dumps(step['params'], ensure_ascii=False, separators=(',', ':'))]
        subprocess.run([*argv, '--save', str(args.save)], check=True)
        if args.pdf:
            subprocess.run([args.cli, 'convert', str(args.save), str(args.pdf)], check=True)
    print(json.dumps({'state': result['state'], 'missingFields': result['missingFields'], 'steps': len(result['steps'])}, ensure_ascii=False))

if __name__ == '__main__':
    main()
