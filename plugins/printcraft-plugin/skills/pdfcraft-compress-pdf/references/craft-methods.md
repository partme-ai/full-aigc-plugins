# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 核对原件页数与结构 | `doc_info` | `{"doc":1}` |
| 2. 清除冗余缩略图并优化到新文件 | `doc_optimize` | `{"doc":1,"path":"output/optimized.pdf","discard_thumbnails":true,"flate_unencoded":true}` |
| 3. 打开优化后的新输出，取得该文档新ID | `doc_open` | `{"path":"output/optimized.pdf"}` |
| 4. 在新输出上渲染代表页，不检查原件冒充结果 | `page_render` | `{"doc":2,"page":1,"dpi":144}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

MCP 直接调用 `doc_info`，参数 `{"doc": 1}`。先 `doc_open` 得到真实doc编号，页码1起，页面坐标为左上角PDF点；直接工具与command_run的内部命令表不能混用。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

pdfcraft-cli run --script steps.json --root WORKSPACE。steps.json 是 [{"tool":"doc_open","args":{"path":"input.pdf"}}, {"tool":"doc_info","args":{"doc":1}}]。doc编号必须取同会话返回值，后续保存与编辑在同一脚本。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

新进程重开优化结果，比较页数、文本可提取性、图片细节与文件大小。

边界：page_render例子仍指当前doc；检查新输出时必须重新doc_open取得新ID，不能看原件冒充输出。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。

## 本轮运行边界

本例仅适用于全新CLI会话：首个doc_open为1、优化输出的第二个doc_open为2。宿主会话必须逐次读取真实返回doc，替换示例ID。优化并非保证缩小，需同时检查字数、页数、渲染与文件大小。
