"""独立技能的凭据字段与原生子进程环境边界；不解析任意正文秘密。"""
import os
SYSTEM_VARIABLES=('PATH','HOME','TMPDIR','TMP','TEMP','LANG','LC_ALL','LC_CTYPE','LC_MESSAGES','SystemRoot','SYSTEMROOT','WINDIR','COMSPEC','PATHEXT','USERPROFILE','LOCALAPPDATA')
CREDENTIAL_FIELDS=frozenset(('apikey','accesstoken','refreshtoken','clientsecret','password','privatekey','secretvalue','credentials'))

def native_environment(source=None):
    """只传系统执行所需环境；未知产品变量、代理及动态加载器配置不透传。"""
    source=os.environ if source is None else source
    return {name:source[name] for name in SYSTEM_VARIABLES if isinstance(source.get(name),str)}

def assert_no_literal_secrets(value, depth=0):
    """凭据字段必须由宿主引用传递，拒绝时不回显字段名或内容。"""
    if depth>64:raise ValueError('invalid_input_depth')
    if isinstance(value,dict):
        for key,child in value.items():
            if isinstance(key,str) and key.replace('_','').replace('-','').lower() in CREDENTIAL_FIELDS:raise ValueError('literal_secret_forbidden')
            assert_no_literal_secrets(child,depth+1)
    elif isinstance(value,list):
        for child in value:assert_no_literal_secrets(child,depth+1)
