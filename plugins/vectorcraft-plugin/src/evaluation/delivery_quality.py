#!/usr/bin/env python3
"""只读产物身份与真实解码检查；工程重开、创作判断和接受状态分别记录。"""
import argparse
import base64
import binascii
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import re
import warnings
import xml.etree.ElementTree as ET

MAX_FILE=64*1024*1024
MAX_TOTAL=256*1024*1024

def exchange_module():
    """从不可变技能快照读取源码，不向安装目录写入Python缓存。"""
    path=Path(__file__).resolve().parents[2]/'skills/vectorcraft-harness/scripts/exchange_loss.py'
    spec=importlib.util.spec_from_file_location('quality_exchange',path)
    module=importlib.util.module_from_spec(spec)
    exec(compile(path.read_bytes(),str(path),'exec'),module.__dict__)
    return module


def embedded_svg_image(value):
    """仅放行有界PNG／JPEG内嵌数据；验证像素后才交给SVG渲染器。"""
    match=re.fullmatch(r'data:image/(png|jpeg);base64,([A-Za-z0-9+/=]+)',value,re.I)
    if not match or len(match[2])>24*1024*1024:raise ValueError('svg_external_resource')
    try:data=base64.b64decode(match[2],validate=True)
    except (binascii.Error,ValueError):raise ValueError('svg_invalid_embedded_image') from None
    try:from PIL import Image
    except (ImportError,OSError):raise ImportError('Pillow') from None
    with warnings.catch_warnings():
        warnings.simplefilter('error',Image.DecompressionBombWarning)
        with Image.open(io.BytesIO(data)) as image:
            if image.format!=('PNG' if match[1].lower()=='png' else 'JPEG') or image.width*image.height>64*1024*1024:raise ValueError('svg_invalid_embedded_image')
            image.verify()
        with Image.open(io.BytesIO(data)) as image:image.load()

def check_raster_disclosure(directory,manifest,path,file):
    """当前SVG中的图像必须与独立损失回执绑定，不能由解码PASS覆盖。"""
    xml=ET.fromstring(path.read_bytes())
    if not any(n.tag.rsplit('}',1)[-1] in ('image','feImage') for n in xml.iter()):return
    binding=manifest.get('lossReport')
    if not isinstance(binding,dict) or binding.get('path')!='exchange-loss.json':raise ValueError('raster_disclosure_missing')
    if manifest['files'].get(binding['path'])!=binding.get('sha256'):raise ValueError('raster_disclosure_unbound_report')
    loss_path=file(binding['path'])
    if hashlib.sha256(loss_path.read_bytes()).hexdigest()!=binding.get('sha256'):raise ValueError('raster_disclosure_digest_mismatch')
    loss=strict_json(loss_path.read_text())
    if not isinstance(loss,dict) or not isinstance(loss.get('outputs'),list) or any(not isinstance(row,dict) for row in loss['outputs']):raise ValueError('raster_disclosure_invalid_report')
    if not isinstance(loss.get('native'),dict) or not isinstance(loss.get('inspection'),dict):raise ValueError('raster_disclosure_invalid_report')
    matches=[row for row in loss['outputs'] if row.get('location')==path.relative_to(directory).as_posix()]
    if (len(matches)!=1 or loss['native'].get('location')!='project.vectorcraft' or loss['native'].get('sha256')!=manifest['files']['project.vectorcraft']
            or loss['inspection'].get('location')!='native.json' or 'native.json' not in manifest['files']
            or loss['inspection'].get('sha256')!=manifest['files']['native.json']):raise ValueError('raster_disclosure_identity_mismatch')
    row=matches[0]
    module=exchange_module()
    if (row.get('format')!='svg' or row.get('nativeSubstitute') is not False or not isinstance(row.get('observations'),dict)
            or row.get('sha256')!=hashlib.sha256(path.read_bytes()).hexdigest() or row['observations'].get('rasterizationScope')!=module.svg_image_scope(xml)):raise ValueError('raster_disclosure_scope_mismatch')
    changes=row.get('changes')
    if not isinstance(changes,list) or any(not isinstance(c,dict) for c in changes) or not any(change.get('code')=='lossless-vector-claim' and change.get('status')=='blocked' for change in changes):raise ValueError('raster_disclosure_claim_not_blocked')


def check_exchange_report(directory,manifest,file):
    """核对原生／检查记录及每个派生输出的损失语义，不推断保真或批准。"""
    binding=manifest.get('lossReport');declared=manifest['files']
    if binding is None and 'exchange-loss.json' not in declared and 'lineage' not in manifest:return 'NOT_RUN'
    if not isinstance(binding,dict) or binding.get('path')!='exchange-loss.json' or declared.get('exchange-loss.json')!=binding.get('sha256'):raise ValueError('exchange_report_missing_or_unbound')
    path=file('exchange-loss.json')
    if hashlib.sha256(path.read_bytes()).hexdigest()!=binding.get('sha256'):raise ValueError('exchange_report_digest_mismatch')
    loss=strict_json(path.read_text())
    if not isinstance(loss,dict) or loss.get('schema')!='craft-exchange-loss/v1' or loss.get('pluginId')!='vectorcraft' or loss.get('acceptance')!='technical-observations-only':raise ValueError('exchange_report_invalid_identity')
    for key,name in [('native','project.vectorcraft'),('inspection','native.json')]:
        if loss.get(key)!={'location':name,'sha256':declared.get(name)} or name not in declared:raise ValueError('exchange_report_'+key+'_mismatch')
    inspection=strict_json(file('native.json').read_text())
    if not isinstance(inspection,dict):raise ValueError('exchange_report_invalid_inspection')
    rows=loss.get('outputs');wanted=[r['path'] for r in manifest['outputs']]
    if not isinstance(rows,list) or len(rows)!=len(wanted) or any(not isinstance(r,dict) for r in rows) or sorted(r.get('location','') for r in rows)!=sorted(wanted):raise ValueError('exchange_report_output_coverage')
    required={
        'pdf':{'font-portability':'unknown','effect-fidelity':'unknown','vector-structure':'unknown'},
        'svg':{'font-portability':'unknown','effect-fidelity':'unknown','vector-structure':'observed','lossless-vector-claim':'blocked'},
        'png':{'editable-layers-paths-text':'lost','effect-keyframe-parameters':'lost','font-appearance':'unknown'}}
    for row in rows:
        name=row['location'];fmt=Path(name).suffix.removeprefix('.').lower()
        if fmt not in required or row.get('format')!=fmt or row.get('sha256')!=declared[name] or row.get('role')!='derivative' or row.get('nativeSubstitute') is not False:raise ValueError('exchange_report_derivative_mismatch')
        changes=row.get('changes')
        if not isinstance(changes,list) or any(not isinstance(c,dict) or not isinstance(c.get('code'),str) or c.get('status') not in ('lost','observed','unknown','blocked') or not isinstance(c.get('reason'),str) or not c['reason'] for c in changes):raise ValueError('exchange_report_invalid_changes')
        states={c['code']:c['status'] for c in changes}
        if len(states)!=len(changes) or any(states.get(code)!=state for code,state in {'native-editing-model':'lost',**required[fmt]}.items()):raise ValueError('exchange_report_loss_semantics')
        if not isinstance(row.get('observations'),dict) or not isinstance(row.get('warnings'),list) or any(not isinstance(v,str) for v in row['warnings']):raise ValueError('exchange_report_invalid_observations')
        if fmt=='svg':
            try:xml=ET.fromstring(file(name).read_bytes())
            except ET.ParseError:raise ValueError('exchange_report_invalid_svg') from None
            tags=[n.tag.rsplit('}',1)[-1] for n in xml.iter()]
            counts={tag:tags.count(tag) for tag in ['path','text','image','filter','mask','clipPath']}
            observation=row['observations'];setup=inspection.get('setup',{})
            if not isinstance(setup,dict):raise ValueError('exchange_report_invalid_setup')
            mode=setup.get('exportText')
            def text_ids(value):
                found=[]
                if isinstance(value,dict):
                    if type(value.get('id')) is int and value['id']>0 and isinstance(value.get('kind'),dict) and value['kind'].get('type')=='text':found.append(value['id'])
                    for child in value.values():found.extend(text_ids(child))
                elif isinstance(value,list):
                    for child in value:found.extend(text_ids(child))
                return found
            ids=sorted(set(text_ids(inspection.get('layers',[]))))
            if observation.get('svg')!=counts or observation.get('nativeTextObjectIds')!=ids or observation.get('svgTextExportMode')!=(mode if mode in ('editable','appearance') else None):raise ValueError('exchange_report_svg_observation_mismatch')
            text_state='lost' if mode=='appearance' and ids else 'observed' if counts['text'] else 'unknown'
            raster_state='observed' if any(tag in ('image','feImage') for tag in tags) else 'unknown'
            if states.get('live-text-editability')!=text_state or states.get('raster-content')!=raster_state:raise ValueError('exchange_report_svg_loss_mismatch')
    return 'PASS'


def strict_json(text):
    """计划及清单不接受重复键、非有限数值或溢出。"""
    def pairs(items):
        result={}
        for key,value in items:
            if key in result:raise ValueError('duplicate_key')
            result[key]=value
        return result
    def number(value):
        result=float(value)
        if not math.isfinite(result):raise ValueError('nonfinite_number')
        return result
    def constant(value):raise ValueError('nonfinite_number')
    return json.loads(text,object_pairs_hook=pairs,parse_float=number,parse_constant=constant)


def decode_output(path):
    """真实解码 PNG、PDF、SVG；解码器缺失属于未执行，不能变为通过。"""
    data=path.read_bytes();suffix=path.suffix.lower()
    try:
        if suffix=='.png':
            if len(data)<33 or not data.startswith(b'\x89PNG\r\n\x1a\n'):raise ValueError('invalid_png_header')
            try:from PIL import Image
            except (ImportError,OSError):return {'status':'NOT_RUN','reason':'decoder_unavailable','decoder':'Pillow'}
            with warnings.catch_warnings():
                warnings.simplefilter('error',Image.DecompressionBombWarning)
                with Image.open(io.BytesIO(data)) as image:
                    if image.width*image.height>64*1024*1024:raise ValueError('image_pixel_limit')
                    image.verify()
                with Image.open(io.BytesIO(data)) as image:
                    image.load();size=list(image.size)
            return {'status':'PASS','decoder':'Pillow','size':size}
        if suffix not in ('.pdf','.svg'):return {'status':'NOT_RUN','reason':'unsupported_export_format'}
        if suffix=='.svg':
            if re.search(br'<!\s*(DOCTYPE|ENTITY)',data,re.I):raise ValueError('svg_external_definition')
            tree=ET.fromstring(data)
            for node in tree.iter():
                if node.tag.rsplit('}',1)[-1] in ('script','foreignObject'):raise ValueError('svg_active_content')
                for key,value in node.attrib.items():
                    if key.rsplit('}',1)[-1]=='href' and not value.startswith('#'):
                        if node.tag.rsplit('}',1)[-1] not in ('image','feImage'):raise ValueError('svg_external_resource')
                        embedded_svg_image(value)
                for value in [*node.attrib.values(),node.text or '']:
                    if '@import' in value.lower() or any(not target.strip(' \"\'').startswith('#') for target in re.findall(r'url\((.*?)\)',value,re.I)):
                        raise ValueError('svg_external_resource')
        try:import fitz
        except (ImportError,OSError):return {'status':'NOT_RUN','reason':'decoder_unavailable','decoder':'PyMuPDF'}
        with fitz.open(stream=data,filetype=suffix.removeprefix('.')) as document:
            if not 0<len(document)<=16 or document.needs_pass:raise ValueError('document_page_limit_or_encrypted')
            for page in document:
                scale=min(1.,256/max(page.rect.width,page.rect.height,1))
                raster=page.get_pixmap(matrix=fitz.Matrix(scale,scale),alpha=True)
                if raster.width<=0 or raster.height<=0:raise ValueError('empty_render')
            count=len(document)
        return {'status':'PASS','decoder':'PyMuPDF','pages':count,'scope':'bounded raster decode; creative quality not assessed'}
    except ImportError as error:return {'status':'NOT_RUN','reason':'decoder_unavailable','decoder':error.name}
    except Exception as error:return {'status':'FAIL','reason':str(error)}


def check_delivery(directory,expected_runtime,expected_project,decoder=decode_output):
    """核对当前目录全部清单文件与导出；本函数不发起原生重开或人工接受。"""
    directory=Path(directory)
    report={'schema':'vectorcraft-technical-review/v1','artifactIntegrityStatus':'FAIL','engineeringStatus':'NOT_RUN',
        'technicalStatus':'NOT_RUN','creativeStatus':'NOT_RUN','acceptanceStatus':'pending','nativeReopenStatus':'NOT_RUN',
        'files':{},'outputs':[],'lineageStatus':'NOT_RUN','exchangeStatus':'NOT_RUN','scope':'artifact integrity and export decode only; native reopening and creative review remain separate'}
    def file(name):
        if not isinstance(name,str) or '\\' in name or Path(name).is_absolute() or any(p in ('','.','..') for p in name.split('/')):raise ValueError('invalid_artifact_path')
        path=directory/name
        if any(p.is_symlink() for p in [path,*path.parents] if p.is_relative_to(directory)) or not path.is_file() or not path.resolve().is_relative_to(directory.resolve()):raise ValueError('invalid_artifact_path')
        if path.stat().st_size>MAX_FILE:raise ValueError('artifact_size_limit')
        return path
    try:
        if directory.is_symlink() or not directory.is_dir():raise ValueError('invalid_delivery_root')
        manifest_path=file('manifest.json');manifest=strict_json(manifest_path.read_text())
        if not isinstance(manifest,dict):raise ValueError('invalid_manifest')
        if manifest.get('schema')!='vectorcraft-delivery/v1' or manifest.get('runtimeSha256')!=expected_runtime or not re.fullmatch('[a-f0-9]{64}',expected_runtime):raise ValueError('runtime_identity_mismatch')
        declared=manifest.get('files')
        if not isinstance(declared,dict) or not 1<=len(declared)<=4096 or declared.get('project.vectorcraft')!=expected_project or not re.fullmatch('[a-f0-9]{64}',expected_project):raise ValueError('project_identity_mismatch')
        total=0
        for name,expected in declared.items():
            path=file(name);total+=path.stat().st_size
            if total>MAX_TOTAL or not isinstance(expected,str) or not re.fullmatch('[a-f0-9]{64}',expected) or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:raise ValueError('artifact_identity_mismatch: '+name)
            report['files'][name]=expected
        outputs=manifest.get('outputs')
        if not isinstance(outputs,list) or any(not isinstance(row,dict) or row.get('path') not in declared for row in outputs):raise ValueError('unbound_export')
        if len({row['path'] for row in outputs})!=len(outputs):raise ValueError('duplicate_export')
        if 'lineage' in manifest:
            lineage=exchange_module()
            identity=lineage.verify_lineage(directory,manifest)
            report.update(lineageStatus='PASS',artifactLogicalId=identity['logicalId'],artifactVersion=identity['version'],sourceTask=identity['sourceTask'])
        elif 'lineage.json' in declared:
            raise ValueError('lineage_missing_binding')
        report.update(artifactIntegrityStatus='PASS',projectRevision=expected_project,runtimeIdentity=expected_runtime,
            manifestSha256=hashlib.sha256(manifest_path.read_bytes()).hexdigest())
        report['exchangeStatus']=check_exchange_report(directory,manifest,file)
        for row in outputs:
            if row['path'].endswith('.svg'):check_raster_disclosure(directory,manifest,file(row['path']),file)
            result=decoder(file(row['path']))
            if not isinstance(result,dict) or result.get('status') not in ('PASS','FAIL','NOT_RUN'):raise ValueError('invalid_decoder_result')
            report['outputs'].append({'path':row['path'],'sha256':declared[row['path']],**result})
        fonts=manifest.get('fontDependencies',[])
        if not isinstance(fonts,list) or any(not isinstance(font,dict) or font.get('missing') is not False for font in fonts):raise ValueError('missing_or_unverified_font')
        states=[row['status'] for row in report['outputs']]
        report['technicalStatus']='FAIL' if 'FAIL' in states else 'NOT_RUN' if not states or 'NOT_RUN' in states else 'PASS'
    except (ValueError,TypeError,KeyError,OSError,OverflowError) as error:
        report['technicalStatus']='FAIL';report['error']=str(error)
    report['acceptanceStatus']='blocked' if report['artifactIntegrityStatus']=='FAIL' or report['technicalStatus']=='FAIL' else 'pending'
    return report


def quality_state(report,creative_status='NOT_RUN',accepted=False):
    """技术或工程失败不可被创作判断覆盖；未执行及未明确接受保持待处理。"""
    if creative_status not in ('PASS','FAIL','NOT_RUN') or not isinstance(accepted,bool):raise ValueError('invalid_quality_state')
    states=[report['engineeringStatus'],report['technicalStatus'],creative_status]
    if report['artifactIntegrityStatus'] not in ('PASS','FAIL','NOT_RUN') or any(state not in ('PASS','FAIL','NOT_RUN') for state in states):raise ValueError('invalid_quality_state')
    status='blocked' if 'FAIL' in states or report['artifactIntegrityStatus']=='FAIL' else 'pending' if 'NOT_RUN' in states or not accepted else 'accepted'
    return {'engineeringStatus':report['engineeringStatus'],'technicalStatus':report['technicalStatus'],'creativeStatus':creative_status,'acceptanceStatus':status}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('directory',type=Path);parser.add_argument('--runtime-sha256',required=True);parser.add_argument('--project-sha256',required=True);args=parser.parse_args()
    print(json.dumps(check_delivery(args.directory,args.runtime_sha256,args.project_sha256),ensure_ascii=False,indent=2,allow_nan=False))
