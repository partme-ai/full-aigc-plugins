# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 确认文档与页数 | `doc_info` | `{"doc":1}` |
| 2. 把指定页移到正确位置 | `page_move` | `{"doc":1,"pages":[3],"to":1}` |
| 3. 抽取独立交付页而不删除原件 | `page_extract` | `{"doc":1,"pages":[1,2],"out":"output/selected.pdf","delete":false}` |
| 4. 完整保存整理副本 | `doc_save` | `{"doc":1,"path":"output/organized.pdf","full":true}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

MCP 直接调用 `doc_info`，参数 `{"doc": 1}`。先 `doc_open` 得到真实doc编号，页码1起，页面坐标为左上角PDF点；直接工具与command_run的内部命令表不能混用。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

pdfcraft-cli run --script steps.json --root WORKSPACE。steps.json 是 [{"tool":"doc_open","args":{"path":"input.pdf"}}, {"tool":"doc_info","args":{"doc":1}}]。doc编号必须取同会话返回值，后续保存与编辑在同一脚本。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

对照页缩略图核对顺序、旋转、空白页和页数，重开两个输出。

边界：doc=1仅为示例，实际取doc_open返回值；原文少于3页时须换成有效页码。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。
