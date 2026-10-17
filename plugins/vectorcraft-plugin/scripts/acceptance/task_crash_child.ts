/** 真实原生工作流父进程；外部验收者可在已保存检查点后终止本进程。 */
import {readFileSync,writeFileSync} from 'node:fs';
import {pathToFileURL} from 'node:url';
const config=JSON.parse(readFileSync(process.argv[2],'utf8'));
const {Controller}=await import(pathToFileURL(config.implementationRoot+'/src/harness/controller.ts').href);
const controller=new Controller(config.database);
try{const result=await controller.run(config.request);writeFileSync(config.actorResult,JSON.stringify(result));}
finally{controller.close();}
