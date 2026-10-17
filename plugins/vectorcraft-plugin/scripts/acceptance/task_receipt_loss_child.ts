/** 在真实交付校验后、账本回执写入前终止自己的协调进程。 */
import {readFileSync,writeFileSync} from 'node:fs';
import {pathToFileURL} from 'node:url';
const config=JSON.parse(readFileSync(process.argv[2],'utf8'));
const {Controller}=await import(pathToFileURL(config.implementationRoot+'/src/harness/controller.ts').href);
const controller=new Controller(config.database);
// 仅注入协调进程丢失故障；保存、导出、摘要校验和原生进程停止仍走真实实现。
const receipt=controller.ledger.receipt.bind(controller.ledger);
controller.ledger.receipt=(task:string,epoch:number,step:number,result:any)=>{
 if(config.persistReceipt)receipt(task,epoch,step,result);
 writeFileSync(config.lossMarker,JSON.stringify({task,epoch,step,result,point:config.persistReceipt?'after-ledger-receipt':'before-ledger-receipt'}),{flag:'wx'});
 process.kill(process.pid,'SIGKILL');
 throw new Error('coordinator_sigkill_did_not_terminate');
};
try{await controller.run(config.request);throw new Error('receipt_loss_not_injected');}
finally{controller.close();}
