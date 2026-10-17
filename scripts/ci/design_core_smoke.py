"""验证核心刊物的原生故事链、完整内容、栏数和可编辑样式。"""
import importlib.util
import json
from pathlib import Path
from design_playbook_smoke import run_script,require,verify,idml_check


def verify_newsletter(info,story,bindings,expected,assertions):
    verify(info,[story],bindings,assertions)
    require(story['text']==expected,'Newsletter full text changed')
    expected_ids=[bindings['body']['id'],bindings['continuation']['id']]
    require(story['frames']==expected_ids,'Newsletter story order changed')
    items={i['id']:i for spread in info['spreads'] for i in spread['items']}
    require(all(items[i]['columns']==3 for i in expected_ids),'Newsletter three-column settings lost')


def run_newsletter(r,skills):
    root=Path(skills)/'designcraft-newsletter'
    recipe=json.loads((root/'references/craft-steps.json').read_text(encoding='utf-8'))
    spec=importlib.util.spec_from_file_location('newsletter_compiler',root/'scripts/write_script.py')
    compiler=importlib.util.module_from_spec(spec);spec.loader.exec_module(compiler)
    steps,names=compiler.compile_steps(recipe)
    target='core-newsletter.designcraft';pdf='core-newsletter.pdf';idml='core-newsletter.idml'
    results=run_script(r,steps,save=target,exports=[pdf,idml]);bindings={n:results[i] for n,i in names.items()}
    require(bindings['before_thread']['overset'],'Fixture did not exercise continuation')
    info=json.loads(r.run('run','--in',target,'--cmd','document.inspect'))
    story=run_script(r,[{'command':'story.get','params':{'frame':bindings['body']['id']}}],source=target)[0]
    expected=next(s['params']['text'] for s in recipe['steps'] if s.get('capture')=='body')
    verify_newsletter(info,story,bindings,expected,recipe['assertions'])
    preflight=run_script(r,[{'command':'preflight.run','params':{'minPpi':150}}],source=target)[0]
    require(not any(i['severity']=='error' for i in preflight['issues']),'Newsletter preflight errors: '+str(preflight))
    idml_check(r.work/idml,recipe['assertions'])
    require((r.work/pdf).read_bytes().startswith(b'%PDF'),'Newsletter PDF invalid')
    (r.work/'core-newsletter-inspection.json').write_text(json.dumps({'info':info,'story':story,'bindings':bindings,'preflight':preflight},ensure_ascii=False,indent=2),encoding='utf-8')
    return {'id':'newsletter','coreSkill':'designcraft-newsletter','technicalRoundtrip':'PASS','fullStory':'PASS','threadOrder':'PASS','threeColumns':'PASS','editableParagraphStyle':'PASS','finalPreflight':'PASS','layoutReview':'NOT_TESTED','hostSameCanvas':'NOT_TESTED'}
