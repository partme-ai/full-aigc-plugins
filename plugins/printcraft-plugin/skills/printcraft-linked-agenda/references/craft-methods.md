# 会议议程双向跳转的方法与参数

## 输入与步骤

本场景输入：用户需要让会议议程和附录在PDF内双向跳转。结构化配方见[craft-steps.json](craft-steps.json)，参数的当前观察记录见[craft-command-evidence.json](craft-command-evidence.json)。先读取实际后端schema与doc_open返回值；rect为显示页面左上角起点的pt，不是比较报告的左下角坐标；必须用当前text_find结果或渲染图重算。示例坐标不能原样套真实议程，目标是PDF物理页不是印刷页码。

| 顺序与目的 | 工具 | 参数样例 |
| --- | --- | --- |
| 1. 核对议程和附录的物理页码 | `doc_info` | `{"doc": 1}` |
| 2. 定位可点击文字，检查唯一命中并确认当前显示坐标 | `text_find` | `{"doc": 1, "query": "Open appendix", "limit": 10}` |
| 3. 样本已确认框包住Open appendix文字，添加内跳至附录 | `link_add` | `{"doc": 1, "page": 1, "rect": [18, 45, 180, 70], "to_page": 3, "visible": true, "width": 1, "color": "#2457cc"}` |
| 4. 定位附录的返回文字 | `text_find` | `{"doc": 1, "query": "Back to agenda", "limit": 10}` |
| 5. 按已确认文字框建立返回议程入口 | `link_add` | `{"doc": 1, "page": 3, "rect": [18, 75, 180, 100], "to_page": 1, "visible": true, "width": 1, "color": "#2457cc"}` |
| 6. 核对议程跳转目标 | `link_list` | `{"doc": 1}` |
| 8. 完整另存交付副本，不覆盖源PDF | `doc_save` | `{"doc": 1, "path": "output/linked-agenda.pdf", "full": true}` |

## CLI、MCP与文档ID

`sourceFiles`列出本次任务的输入PDF，先替换真实路径。`doc`和`other`为1起始文档槽，不是任意运行中的文档ID。附带[write_script.py](../scripts/write_script.py)仅将明确输入和槽位转换为原生工具脚本，不实现PDF业务：

```text
python <本技能目录>/scripts/write_script.py --recipe <已替换输入的craft-steps.json> --output steps.json
pdfcraft-cli run --script steps.json --root <本次输入输出根目录>
```

本批CLI观察来自官方0.8.0；不能将冻结基础技能安装的其他版本自动视为支持。先查`pdfcraft-cli tools`并逐项核对参数，缺失时使用已验证的配套后端或明确停止。

必须用全新CLI进程执行整个脚本。其首先按sourceFiles顺序打开文件，文档ID从1顺序分配；不要拆成多次`run tool`，不要向已有会话发送这里的数字。记录doc_open结果；后端行为变化时停止并改用按实际返回值逐步执行的MCP。用argv运行，避免Windows shell引号差异。

当前插件的`printcraft-editor` MCP直接暴露`doc_open`和本表工具；已将当前清单的字段/必填项与原生schema逐项核对，记录在本技能观察文件的`mcpCatalog`。先等待`editor_status`并查实际schema，再调用`doc_open {"path":"input.pdf"}`记录返回doc。随后直接调用`text_find`，参数格式`{"doc": 1, "query": "Open appendix", "limit": 10}`，将doc替换为刚返回的实际ID；比较场景还须另开旧版并将other换成其ID。不使用其他Craft的execute包装。独立CLI不会自动更改另一个Web会话。

## 保存与结果检查

另开输出检查第1页到第3页和第3页到第1页的内部链接；独立解释器读目标并确认热点覆盖指定文字；原文本与源摘要保持。

先对照真实输入检查目标范围，再执行修改。写入使用新输出路径，不能覆盖源；处理已有水印、页脚、书签或链接时先盘点，不盲目重复叠加。PDF重开后还要用独立解释器或宿主查看器核对最终文字、页数、目标和图像；业务效果不能只由退出码或对象存在判断。

来源固定提交、许可和哈希见[workflow-sources.json](workflow-sources.json)。流程事实为参考，参数和场景正文原创适配。
