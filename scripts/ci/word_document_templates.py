"""从六类文档技能的实际模板编译回归输入；执行由官方WordCraft CLI负责。"""
import argparse
import importlib.util
import json
import os
from pathlib import Path


def prepare(source):
    source=Path(source)
    index=json.loads((source/'document-templates.json').read_text(encoding='utf-8'))
    recipes=[]
    for record in index['templates']:
        folder=source/'skills'/record['skill']
        spec=importlib.util.spec_from_file_location('document_template',folder/'scripts/render_document_template.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        template=json.loads((folder/'assets/template.json').read_text(encoding='utf-8'))
        values=json.loads((folder/'examples/input.json').read_text(encoding='utf-8'))
        recipe=module.compile_template(template,values)
        recipe['id']='template-'+recipe['id']
        scalar=[value for value in values.values() if isinstance(value,str)]
        expected_cells=[template['table']['headers'],*values[template['table']['field']]]
        recipe['assertions']={'textContains':scalar+[cell for row in expected_cells for cell in row],
                              'headingRequired':True,'heading2Minimum':len(template['sections'])+1,
                              'tableCount':1,'tableCells':expected_cells}
        recipes.append(recipe)
    if len(recipes)!=6:raise ValueError('Expected six document types')
    return {'application':'wordcraft','recipes':recipes}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    data=prepare(args.source)
    data['sourceSkills']=Path(os.path.relpath(args.source.resolve()/'skills',args.output.resolve().parent)).as_posix()
    args.output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
