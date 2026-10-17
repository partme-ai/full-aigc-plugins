"""把本次商业报价数据编译为WordCraft原生命令；不自动添加税费。"""
import argparse
from datetime import date
from decimal import Decimal
import importlib.util
import json
from pathlib import Path
import re
import subprocess

HOME=Path(__file__).resolve().parents[1]

def money(value, maximum_digits=8):
    if not isinstance(value,str) or not re.fullmatch(r'(?:0|[1-9][0-9]{0,'+str(maximum_digits-1)+r'})(?:\.[0-9]{1,2})?',value):
        raise ValueError('单价和期望总额须为非负十进制字符串，最多两位小数')
    return Decimal(value)

def text(value, name, maximum=500):
    if not isinstance(value,str) or not value.strip() or len(value)>maximum or any(c in value for c in '\x00\t\r\n'):
        raise ValueError('字段须为非空单行文本：'+name)
    return value

def compile_quote(data):
    required={'quote_number','quote_date','issuer','customer','currency','pricing_basis','valid_until','terms','items'}
    if not isinstance(data,dict) or set(data)-required-{'expected_total'} or required-set(data):
        raise ValueError('报价字段缺失或包含未知字段')
    for name in required-{'items'}:text(data[name],name)
    if not re.fullmatch('[A-Z]{3}',data['currency']):raise ValueError('币种须明确提供三个大写字母代码')
    if date.fromisoformat(data['valid_until'])<date.fromisoformat(data['quote_date']):raise ValueError('有效期早于报价日期')
    items=data['items']
    if not isinstance(items,list) or not 1<=len(items)<=40:raise ValueError('报价须包含1到40个明细项目')
    rows=[];total=Decimal('0.00')
    for item in items:
        if not isinstance(item,dict) or set(item)!={'description','quantity','unit_price'}:raise ValueError('明细字段错误')
        description=text(item['description'],'description',80);quantity=item['quantity']
        if isinstance(quantity,bool) or not isinstance(quantity,int) or not 1<=quantity<=1000000:raise ValueError('数量须为1到1000000的整数')
        price=money(item['unit_price']);amount=price*quantity;total+=amount
        rows.append([description,str(quantity),format(price,'.2f'),format(amount,'.2f')])
    if 'expected_total' in data and money(data['expected_total'],16)!=total:raise ValueError('期望总额与逐项计算不一致')
    rows.append(['合计（'+data['currency']+'）','','',format(total,'.2f')])
    values={'title':'商业报价单 '+data['quote_number'],'document_date':data['quote_date'],'author':data['issuer'],
            'parties':'报价方：'+data['issuer']+'；客户：'+data['customer'],
            'basis':data['currency']+'；'+data['pricing_basis'],
            'terms':'有效期至：'+data['valid_until']+'；'+data['terms'],'records':rows}
    spec=importlib.util.spec_from_file_location('quote_template',HOME/'scripts/render_document_template.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    plan=module.compile_template(json.loads((HOME/'assets/template.json').read_text(encoding='utf-8')),values)
    steps=plan['steps']
    # 只用于本脚本新建的空文档；表格位置由转换前的真实段落数量推导。
    first_table_line=next(i for i,step in enumerate(steps) if step['command']=='text.insert' and '\t' in step['params']['text'])
    table_block=sum(step['command']=='text.newParagraph' for step in steps[:first_table_line])
    for step in steps:
        if step['command'] in ('para.alignLeft','para.alignCenter'):
            step['params']={'value':'left' if step['command']=='para.alignLeft' else 'center'}
            step['command']='para.align'
    def select_cell(row,column):
        pos={'story':'body','path':[table_block,row,column,0],'off':0}
        steps.append({'command':'select.range','params':{'anchor':pos,'focus':pos}})
    for row in range(len(rows)+1):
        select_cell(row,0)
        steps.append({'command':'table.properties','params':{'allowBreak':False}})
    for column,width in enumerate([250,45,75,81]):
        select_cell(0,column)
        steps.append({'command':'table.columnWidth','params':{'width':width}})
        if column:
            steps.extend([{'command':'table.selectColumn','params':{}},{'command':'para.align','params':{'value':'right'}}])
    plan.update(total=format(total,'.2f'),currency=data['currency'],itemCount=len(items),taxOrDiscountAutomaticallyAdded=False)
    return plan

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--save',type=Path);parser.add_argument('--pdf',type=Path);parser.add_argument('--cli',default='wordcraft-cli')
    args=parser.parse_args()
    try:
        source=args.input.resolve(strict=True);plan=compile_quote(json.loads(source.read_text(encoding='utf-8')))
        outputs=[p.resolve() for p in [args.output,args.save,args.pdf] if p is not None]
        if args.pdf and not args.save:raise ValueError('--pdf需要--save')
        if source in outputs or len(set(outputs))!=len(outputs) or any(p.exists() for p in outputs):raise ValueError('输出须为不同且不存在的新路径')
        argv=[args.cli,'run']
        for step in plan['steps']:argv+=['--cmd',step['command']+'='+json.dumps(step['params'],ensure_ascii=False,separators=(',',':'))]
        if args.save:argv+=['--save',str(args.save.resolve())]
        # 保持Windows单进程命令行可容纳；不静默截断明细或分批改变选择状态。
        if len(subprocess.list2cmdline(argv).encode('utf-16-le'))//2>28000:raise ValueError('当前数据超过可移植单进程命令长度，请缩短文本或拆分报价单')
    except (ValueError,TypeError,OSError) as error:parser.error(str(error))
    with args.output.open('x',encoding='utf-8') as stream:json.dump(plan,stream,ensure_ascii=False,indent=2);stream.write('\n')
    if args.save:
        subprocess.run(argv,check=True)
        if args.pdf:subprocess.run([args.cli,'convert',str(args.save.resolve()),str(args.pdf.resolve())],check=True)
    print(json.dumps({'state':plan['state'],'itemCount':plan['itemCount'],'total':plan['total'],'currency':plan['currency'],'scope':'compiled fields; inspect saved documents and pages separately'},ensure_ascii=False))

if __name__=='__main__':main()
