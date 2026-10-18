"""通过真实原生CLI stdio会话验证字段请求辅助工具，不代替宿主验收。"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import queue
import subprocess
import sys
import threading
from craft_cli_windows import require


def fixture(path):
    objects=[b'<< /Type /Catalog /Pages 2 0 R /AcroForm << /Fields [5 0 R 6 0 R] /DA (/Helv 12 Tf 0 g) /DR << /Font << /Helv 7 0 R >> >> >> >>',
        b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
        b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 200] /Resources << /Font << /Helv 7 0 R >> >> /Annots [5 0 R 6 0 R] /Contents 4 0 R >>',
        b'<< /Length 0 >>\nstream\n\nendstream',
        b'<< /Type /Annot /Subtype /Widget /FT /Tx /T (customer.name) /V (Initial) /Rect [20 100 260 130] /P 3 0 R /DA (/Helv 12 Tf 0 g) /F 4 >>',
        b'<< /Type /Annot /Subtype /Widget /FT /Btn /T (consent) /V /Off /AS /Off /Rect [20 40 40 60] /P 3 0 R /F 4 /AP << /N << /Off 8 0 R /Yes 9 0 R >> >> >>',
        b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>']
    for data in (b'0 0 20 20 re S',b'0 0 20 20 re S 2 2 m 18 18 l 2 18 m 18 2 l S'):
        objects.append(b'<< /Type /XObject /Subtype /Form /BBox [0 0 20 20] /Length '+str(len(data)).encode()+b' >>\nstream\n'+data+b'\nendstream')
    data=b'%PDF-1.7\n';offsets=[0]
    for i,obj in enumerate(objects,1):offsets.append(len(data));data+=f'{i} 0 obj\n'.encode()+obj+b'\nendobj\n'
    start=len(data);data+=f'xref\n0 {len(offsets)}\n0000000000 65535 f \n'.encode()
    data+=b''.join(f'{n:010d} 00000 n \n'.encode() for n in offsets[1:]);data+=f'trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{start}\n%%EOF\n'.encode();path.write_bytes(data)


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    g=p.add_mutually_exclusive_group(required=True);g.add_argument('--cli',type=Path);g.add_argument('--runtime-root',type=Path);a=p.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
    exe=a.cli.resolve() if a.cli else None
    if a.runtime_root:
        matches=list(a.runtime_root.resolve().rglob('pdfcraft-cli.exe'));require(len(matches)==1,'Expected one verified runtime');exe=matches[0]
        prior=json.loads((a.runtime_root/'result.json').read_text(encoding='utf-8'));require(hashlib.sha256(exe.read_bytes()).hexdigest()==prior['exeSha256'],'Runtime changed')
    helper=a.source.resolve()/'skills/printcraft-fill-pdf-forms/scripts/form_request.py';s=importlib.util.spec_from_file_location('form_request',helper);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
    work=out/'表单 中文 workspace';work.mkdir();inp=work/'input.pdf';fixture(inp);before=inp.read_bytes();records=[];seq=0
    stderr=(out/'stderr.log').open('w',encoding='utf-8');proc=subprocess.Popen([str(exe),'mcp','--root',str(work)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=stderr,text=True,encoding='utf-8');responses=queue.Queue()
    def reader():
        for line in proc.stdout:responses.put(line)
        responses.put(None)
    threading.Thread(target=reader,daemon=True).start()
    def rpc(method,params):
        nonlocal seq
        seq+=1;proc.stdin.write(json.dumps({'jsonrpc':'2.0','id':seq,'method':method,'params':params})+'\n');proc.stdin.flush()
        while True:
            line=responses.get(timeout=60);require(line is not None,'Native CLI exited');value=json.loads(line)
            if value.get('id')==seq:
                require('error' not in value,'Native RPC error');records.append({'method':method,'params':params,'result':value['result']});return value['result']
    def tool(name,args):
        result=rpc('tools/call',{'name':name,'arguments':args});require(not result.get('isError'),'Native tool failed: '+name)
        return json.loads(next(c['text'] for c in result['content'] if c['type']=='text'))
    try:
        rpc('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'native-form-business-check','version':'1'}})
        proc.stdin.write(json.dumps({'jsonrpc':'2.0','method':'notifications/initialized'})+'\n');proc.stdin.flush();cases=[]
        for name,text,check in [('checked','Sample Customer',True),('unchecked','Other Customer',False),('chinese','真实姓名',True)]:
            opened=tool('doc_open',{'path':'input.pdf'});doc=opened['doc'];fields=tool('form_fields',{'doc':doc});request=m.build_request(fields,{'customer.name':text,'consent':check},doc);filled=tool(request['tool'],request['arguments']);tool('doc_save',{'doc':doc,'path':name+'.pdf','full':True});reopened=tool('doc_open',{'path':name+'.pdf'});saved=tool('form_fields',{'doc':reopened['doc']});actual={f['name']:f['value'] for f in saved['fields']}
            require(actual['customer.name']==text,'Text value changed');require(actual['consent']==check,'Checkbox value changed')
            cases.append({'name':name,'savedFieldValues':'PASS','appearance':'NOT_ACCEPTED' if filled.get('warnings') else 'NOT_VIEWED','warnings':filled.get('warnings',[])})
        require(inp.read_bytes()==before,'Input changed');result={'scope':'native CLI stdio business; no installed-host acceptance','platform':sys.platform,'status':'PASS','cases':cases,'inputPreserved':True};(out/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False))
    finally:
        (out/'calls.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8');proc.terminate();proc.wait(timeout=10);stderr.close()

if __name__=='__main__':main()
