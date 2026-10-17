# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 读取真实字段名与类型 | `form_fields` | `{"doc":1}` |
| 2. 按字段映射填写值 | `form_fill` | `{"doc":1,"values":{"CustomerName":"Sample Customer"}}` |
| 3. 保存保留可编辑字段的副本 | `doc_save` | `{"doc":1,"path":"output/filled.pdf","full":true}` |
| 4. 渲染表单页检查显示 | `page_render` | `{"doc":1,"page":1,"dpi":144}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

MCP 直接调用 `form_fields`，参数 `{"doc": 1}`。先 `doc_open` 得到真实doc编号，页码1起，页面坐标为左上角PDF点；直接工具与command_run的内部命令表不能混用。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

pdfcraft-cli run --script steps.json --root WORKSPACE。steps.json 是 [{"tool":"doc_open","args":{"path":"input.pdf"}}, {"tool":"doc_info","args":{"doc":1}}]。doc编号必须取同会话返回值，后续保存与编辑在同一脚本。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

重开核对字段值、复选框、长文本、字体和签名区域。

边界：CustomerName必须由form_fields实际返回确认；填写不等于电子签名或身份认证。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。

## 本轮运行边界

CustomerName必须由form_fields实际返回确认；填写不等于电子签名或身份认证。 此ASCII值是虚构测试输入，实际用户值不得转拼音或替换。官方0.8.0在本轮Helvetica表单的中文外观测试中显示????，虽字段存储值正确也不能验收中文外观；无可用中文字体能力时保留原件、明确未完成，并按用户确认选择其他后端。
