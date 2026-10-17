# 只比较规范写入的顶层身份字节；不求值JSON或任务中任何命令。
# 完整JSON语义随后仍由当前只读Python派发器重读检查。
NR==1 { expected=$0; next }
NR!=2 { invalid=1; next }
{
  text=$0; depth=0; quoted=0; escaped=0;
  for(i=1;i<=length(text);i++) {
    c=substr(text,i,1);
    if(!quoted && depth==1) {
      if(substr(text,i,11)=="\"identity\":") {
        identities++;
        if(substr(text,i+11,length(expected))!=expected || substr(text,i+11+length(expected),1)!=",") invalid=1;
      }
      token="\"identityHash\":\""sha"\"";
      if(substr(text,i,15)=="\"identityHash\":") { hashes++; if(substr(text,i,length(token))!=token) invalid=1 }
    }
    if(quoted) {
      if(escaped) escaped=0;
      else if(c=="\\") escaped=1;
      else if(c=="\"") quoted=0;
    } else {
      if(c=="\"") quoted=1;
      else if(c=="{" || c=="[") depth++;
      else if(c=="}" || c=="]") depth--;
      if(depth<0) invalid=1;
    }
  }
  if(depth!=0 || quoted || substr(text,1,1)!="{" || substr(text,length(text),1)!="}") invalid=1;
}
END { exit invalid || NR!=2 || identities!=1 || hashes!=1 }
