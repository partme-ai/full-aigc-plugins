/** 原生本地工具只接收运行所需的系统变量；宿主模型秘密不得透传。 */
export function nativeEnvironment(source:NodeJS.ProcessEnv=process.env):NodeJS.ProcessEnv {
 const result:NodeJS.ProcessEnv=Object.create(null);
 // 不包含代理、令牌、加载器注入、Python/Node 启动配置或任意产品变量。
 const allowed=['PATH','HOME','TMPDIR','TMP','TEMP','LANG','LC_ALL','LC_CTYPE','LC_MESSAGES',
  'SystemRoot','SYSTEMROOT','WINDIR','COMSPEC','PATHEXT','USERPROFILE','LOCALAPPDATA'];
 for(const name of allowed)if(typeof source[name]==='string')result[name]=source[name];
 return result;
}
