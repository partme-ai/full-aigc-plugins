/** 原生交付真实验证后、提交回执之前取消；保留原生实际回执的隔离结果。 */
import {readFileSync,writeFileSync} from 'node:fs';
import {pathToFileURL} from 'node:url';
const config=JSON.parse(readFileSync(process.argv[2],'utf8'));
const {Controller}=await import(pathToFileURL(config.implementationRoot+'/src/harness/controller.ts').href);
const controller=new Controller(config.database),receipt=controller.ledger.receipt.bind(controller.ledger);
controller.ledger.receipt=(task:string,epoch:number,step:number,result:any)=>{
 controller.requestCancel(task,epoch);const recorded=receipt(task,epoch,step,result);
 writeFileSync(config.marker,JSON.stringify({task,epoch,step,result,state:recorded.state}),{flag:'wx'});process.kill(process.pid,'SIGKILL');throw new Error('SIGKILL did not terminate coordinator');
};
try{await controller.run(config.request);throw new Error('actual late-delivery boundary missing');}finally{controller.close();}
