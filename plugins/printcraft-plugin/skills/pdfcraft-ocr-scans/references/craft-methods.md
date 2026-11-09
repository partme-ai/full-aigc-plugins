# 本场景的 Craft 方法与参数

先读取输入与当前选择。数值、路径、名称和对象编号仅为格式示例；用当前输入、实际返回ID和目标尺寸替换后执行。

| 顺序与目的 | 实际方法 | 参数例子 |
| --- | --- | --- |
| 1. 查看OCR引擎与模型状态 | `ocr_status` | `{}` |
| 2. 识别英文扫描页 | `ocr_recognize` | `{"doc":1,"language":"en","pages":[1],"dpi":300,"skip_text_pages":true}` |
| 3. 抽取识别文字核对 | `text_extract` | `{"doc":1,"pages":[1]}` |
| 4. 保存新副本 | `doc_save` | `{"doc":1,"path":"output/searchable.pdf","full":true}` |

## 如何调用

宿主内已打开编辑器时使用该同会话MCP；先等待editor_status就绪，读取实际工具schema和当前命令参数。独立CLI可用于文件任务，但新进程与已打开Web编辑器不是同一状态。

MCP 直接调用 `ocr_status`，参数 `{}`。先 `doc_open` 得到真实doc编号，页码1起，页面坐标为左上角PDF点；直接工具与command_run的内部命令表不能混用。

CLI 语法（下面是展示用写法，实际跨平台执行用argv避免shell引号差异）：

pdfcraft-cli run --script steps.json --root WORKSPACE。steps.json 是 [{"tool":"doc_open","args":{"path":"input.pdf"}}, {"tool":"doc_info","args":{"doc":1}}]。doc编号必须取同会话返回值，后续保存与编辑在同一脚本。

## 参数核对与完成标准

先查 [当前版本观察目录](craft-command-evidence.json) 中对应方法的完整参数，再按实际运行时查询更新。结构化步骤见 [craft-steps.json](craft-steps.json)。

抽查姓名、数字和表格顺序，检查识别文字与图像位置。

边界：当前官方0.8.0 schema语言枚举仅en；中文不能用en假装已支持，需另接实际可用中文后端。

保存可编辑工程后由新进程或重新打开的同一宿主会话核对；导出格式单独解码/查看。方法存在和零退出不代表本场景已经完成。

工作流来源与许可见 [workflow-sources.json](workflow-sources.json)。仅借鉴事实与方法，本文与参数例子原创编写。

## 本轮运行边界

当前官方0.8.0 schema语言枚举仅en；中文不能用en假装已支持，需另接实际可用中文后端。 先检查ocr_status.available；缺模型时仅在已授权范围配置PDFCRAFT_MODELS到模型目录，再复查状态；不得把原有可选文字页的skip结果当作OCR成功。模型来源与SHA256见方法手册。

模型地址、哈希和CC-BY-SA-4.0许可信息见[官方模型来源](ocr-models.json)。使用运行时配置的模型目录，不改全局环境；模型存在后仍应由当前ocr_status及图像页识别结果确认。
