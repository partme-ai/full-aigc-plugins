# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 读取文档结构 | `doc_info` | `{"doc":1}` |
| 2. 检查代表页渲染 | `page_render` | `{"doc":1,"page":1,"dpi":144}` |
| 3. 抽取文本看字体映射 | `text_extract` | `{"doc":1}` |
| 4. 检查表单字段完整性 | `form_fields` | `{"doc":1}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

MCP 直接调用 `doc_info`，参数 `{"doc": 1}`。先 `doc_open` 得到真实doc编号，页码1起，页面坐标为左上角PDF点；直接工具与command_run的内部命令表不能混用。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

pdfcraft-cli run --script steps.json --root WORKSPACE。steps.json 是 [{"tool":"doc_open","args":{"path":"input.pdf"}}, {"tool":"doc_info","args":{"doc":1}}]。doc编号必须取同会话返回值，后续保存与编辑在同一脚本。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

按要求核对每页尺寸、字体、文本、图像与书签，文件可打开不代表印前合规。

边界：该流程不自动认证PDF/X、PDF/A或可访问性标准；对应标准需当前真实检测工具。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。
