"""把有来源的分类数据转换为新建演示文稿的原生命令计划。"""
import argparse
import json
import math
from pathlib import Path


def text(value, field, limit=240):
    if not isinstance(value,str) or not value.strip() or len(value)>limit or any(ord(c)<32 or c in '\u2028\u2029' for c in value):
        raise ValueError(f'{field}: required single-line text, maximum {limit} characters')
    return value.strip()


def compile_story(data):
    if not isinstance(data,dict):
        raise ValueError('input must be an object')
    fields={k:text(data.get(k),k,60 if k=='title' else 240) for k in ('title','unit','period','source','definition','limitations','action')}
    categories=data.get('categories')
    if not isinstance(categories,list) or not 2<=len(categories)<=12:
        raise ValueError('categories:2..12 ordered categories required')
    categories=[text(c,'category',24) for c in categories]
    if len(set(categories))!=len(categories):
        raise ValueError('categories must be unique')
    rows=data.get('series')
    if not isinstance(rows,list) or not 1<=len(rows)<=3:
        raise ValueError('series:1..3 required with the same unit and definition')
    series=[]
    for row in rows:
        if not isinstance(row,dict):
            raise ValueError('series must contain objects')
        name=text(row.get('name'),'series name',32)
        values=row.get('values')
        if not isinstance(values,list) or len(values)!=len(categories):
            raise ValueError('each series must match categories exactly')
        if any(type(v) not in (int,float) or not math.isfinite(v) or abs(v)>1e12 for v in values):
            raise ValueError('finite numeric values required; missing values are not zero')
        series.append({'name':name,'values':values[:]})
    if len({s['name'] for s in series})!=len(series):
        raise ValueError('series names must be unique')
    def command(name,params):
        return {'command':name,'params':params}
    notes='；'.join(f'{k}：{fields[k]}' for k in ('unit','period','source','definition','limitations'))
    commands=[command('file.new',{'size':[960,540],'blank':True}),
        command('slide.new',{'layout':'titleOnly','title':fields['title']+'（'+fields['unit']+'）','body':''}),
        command('insert.chart',{'type':'column','rect':[80,150,800,300],'categories':categories,'series':series}),
        command('chart.options',{'title':fields['period'],'dataLabels':True,'gridlines':True,'legend':'r'}),
        command('slide.notes',{'index':0,'text':notes}),
        command('slide.new',{'layout':'titleAndContent','title':'解释边界与下一步','body':fields['limitations']+'\n下一步：'+fields['action']}),
        command('slide.notes',{'index':1,'text':notes+'；行动：'+fields['action']})]
    return {'schema':'deckcraft-data-story-plan/v1','newDocumentOnly':True,'status':'PLAN_REQUIRES_REVIEW','commands':commands,
        'checks':['核对原始数据、类别顺序、期间及单位','确认标题结论由数据支持；编译器不推断因果','预览图表轴、数值标签和标题溢出','保存新原生工程和PPTX，回读检查图表数据可编辑']}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    plan=compile_story(json.loads(args.input.read_text(encoding='utf-8')))
    with args.output.open('x',encoding='utf-8') as stream:
        json.dump(plan,stream,ensure_ascii=False,indent=2,allow_nan=False)
        stream.write('\n')

if __name__=='__main__':main()
