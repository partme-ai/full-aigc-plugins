/** 故障只注入协调器检查点，运行时探测、任务登记和启动器均走真实实现。 */
import {readFileSync,writeFileSync} from 'node:fs';
import {pathToFileURL} from 'node:url';
const config=JSON.parse(readFileSync(process.argv[2],'utf8'));
const {Controller}=await import(pathToFileURL(config.implementationRoot+'/src/harness/controller.ts').href);
const controller=new Controller(config.database);
const crash=(task:string,epoch:number)=>{writeFileSync(config.marker,JSON.stringify({point:config.point,task,epoch}),{flag:'wx'});process.kill(process.pid,'SIGKILL');throw new Error('SIGKILL did not terminate coordinator');};
const claim=controller.ledger.claim.bind(controller.ledger);
controller.ledger.claim=(...args:any[])=>{const task=claim(...args);if(config.point==='ready')crash(task.id,task.epoch);return task;};
const intent=controller.ledger.intent.bind(controller.ledger);
controller.ledger.intent=(...args:any[])=>{if(config.point==='prepared')crash(args[0],args[1]);const task=intent(...args);if(config.point==='intent')crash(args[0],args[1]);return task;};
const register=controller.processes.register.bind(controller.processes);
controller.processes.register=(...args:any[])=>{register(...args);if(config.point==='registered')crash(args[0],args[1]);};
const authorize=controller.ledger.authorizeLaunch.bind(controller.ledger);
controller.ledger.authorizeLaunch=(...args:any[])=>{authorize(...args);if(config.point==='authorized')crash(args[0],args[1]);};
try{await controller.run(config.request);throw new Error('launch_crash_not_injected');}finally{controller.close();}
