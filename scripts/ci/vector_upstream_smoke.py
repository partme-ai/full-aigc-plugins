"""VectorCraft 0.12：原生stdio目录检索及可编辑Legacy AI交付。"""
import hashlib
import json
from pathlib import Path

from craft_cli_windows import require
from vector_playbook_smoke import inspect, nodes


def run_checks(r):
    # 原生stdio报文往返；不把它标为宿主安装或宿主画面同步。
    messages = [
        {'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-06-18','capabilities':{},'clientInfo':{'name':'craft-release-check','version':'1'}}},
        {'jsonrpc':'2.0','method':'notifications/initialized','params':{}},
        {'jsonrpc':'2.0','id':2,'method':'tools/list','params':{}},
    ]
    for id, arguments in [(3,{'query':'graph.','brief':True}), (4,{'menu':'Object > Path','brief':True}), (5,{'filter':'graph.setType'})]:
        messages.append({'jsonrpc':'2.0','id':id,'method':'tools/call','params':{'name':'command_list','arguments':arguments}})
    output = r.run('mcp','--headless','--automation-read-root',r.work,'--automation-write-root',r.work,
                   stdin=''.join(json.dumps(m)+'\n' for m in messages))
    responses = {row['id']:row for row in map(json.loads,output.splitlines()) if 'id' in row}
    tools = responses[2]['result']['tools']
    schema = next(t['inputSchema'] for t in tools if t['name']=='command_list')
    require({'query','menu','brief'} <= schema['properties'].keys(),'New MCP discovery parameters absent')
    def rows(id):
        result=responses[id]['result'];require(not result.get('isError'),'Native MCP listing failed')
        return json.loads(next(c['text'] for c in result['content'] if c['type']=='text'))
    graph, paths, detail = rows(3),rows(4),rows(5)
    require(bool(graph) and all(x['id'].startswith('graph.') and 'params' not in x for x in graph),'Query/brief not applied')
    require(bool(paths) and all('object > path' in ' > '.join(x['menu']).lower() and 'params' not in x for x in paths),'Menu filter not applied')
    require(len(detail)==1 and bool(detail[0].get('params')),'Detailed command parameters lost')
    # 保留组、图层和活文字；Legacy AI不是渲染成一张图片的交付。
    commands = [('file.new',{'width':240,'height':180,'units':'Pixels','backgroundContents':'white'}),
                ('shape.rectangle',{'x':20,'y':20,'width':60,'height':40}),
                ('paint.setFill',{'color':'#2563eb'}),('paint.setStroke',{'none':True}),
                ('shape.ellipse',{'x':100,'y':20,'width':40,'height':40}),
                ('paint.setFill',{'color':'#16a34a'}),('paint.setStroke',{'none':True}),
                ('select.all',{}),('object.group',{}),
                ('text.create',{'x':20,'y':120,'text':'CRAFT 012','size':20,'font':'Arial','color':'#172033'})]
    args=['run']
    for name,params in commands:args+=['--cmd',name,'--params',json.dumps(params,separators=(',',':'))]
    source='release-012.vectorcraft';target='release-012-legacy.ai'
    r.run(*args,'--export',source)
    digest=hashlib.sha256((r.work/source).read_bytes()).hexdigest()
    r.run('convert',source,target,'--ai-version','7','--hidden-objects','layer','--transparent-images','flatten')
    require((r.work/target).read_bytes().startswith(b'%!PS-Adobe'),'Legacy AI is not PostScript')
    info=inspect(r,target);ns=nodes(info)
    require(any(n['kind']=='Group' for n in ns),'Legacy AI lost editable grouping')
    require(any(n['kind']=='Type' and n.get('text')=='CRAFT 012' for n in ns),'Legacy AI lost live text')
    require(sum(n['kind']=='Layer' for n in ns)>=1,'Legacy AI lost layers')
    require(sum(n['kind'] in ('Path','Rectangle','Ellipse') for n in ns)>=2,'Legacy AI lost geometry')
    require(hashlib.sha256((r.work/source).read_bytes()).hexdigest()==digest,'Legacy export changed native master')
    r.run('convert',target,'release-012-legacy.png')
    # 单独MCP会话打开同一个母版，通过真实export工具验证参数；不借CLI结果冒充MCP。
    export_messages = messages[:2] + [
        {'jsonrpc':'2.0','id':6,'method':'tools/call','params':{'name':'open_file','arguments':{'path':str(r.work/source)}}},
        {'jsonrpc':'2.0','id':7,'method':'tools/call','params':{'name':'export','arguments':{'path':str(r.work/'release-012-mcp.ai'),'format':'ai','options':{'aiVersion':'7','hiddenObjects':'layer','transparentImages':'flatten'}}}},
    ]
    raw = r.run('mcp','--headless','--automation-read-root',r.work,'--automation-write-root',r.work,
                stdin=''.join(json.dumps(m)+'\n' for m in export_messages))
    responses = {row['id']:row for row in map(json.loads,raw.splitlines()) if 'id' in row}
    require(all('result' in responses[id] and not responses[id]['result'].get('isError') for id in (6,7)),
            'Native MCP open/export failed')
    require((r.work/'release-012-mcp.ai').read_bytes().startswith(b'%!PS-Adobe'),'MCP legacy options were ignored')
    reopened = nodes(inspect(r,'release-012-mcp.ai'))
    require(any(n['kind']=='Group' for n in reopened) and any(n['kind']=='Type' and n.get('text')=='CRAFT 012' for n in reopened),
            'MCP legacy AI lost group or live text')
    require(hashlib.sha256((r.work/source).read_bytes()).hexdigest()==digest,'MCP export changed native master')
    return {'version':'0.12.0','nativeStdioDiscovery':'PASS','queryCount':len(graph),'menuCount':len(paths),
            'legacyAiEditableRoundtrip':'PASS','nativeMcpLegacyExport':'PASS','nativeMasterPreserved':'PASS',
            'hostAcceptance':'NOT_TESTED','embeddedEngineUpgrade':'NOT_INFERRED'}
