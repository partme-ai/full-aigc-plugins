# 新旧版本差异报告的方法与参数

## 输入与步骤

本场景输入：用户提供新旧PDF需要列出文字修改并交付差异报告。结构化配方见[craft-steps.json](craft-steps.json)，参数的当前观察记录见[craft-command-evidence.json](craft-command-evidence.json)。先读取实际后端schema与doc_open返回值；文字比较不证明图像、矢量、复杂重排和扫描内容完全相同；limit可能截断，必须检查总变化数与返回列表，超限不能当作完整审阅。比较矩形为PDF左下角坐标，不直接作为link_add热点。

| 顺序与目的 | 工具 | 参数样例 |
| --- | --- | --- |
| 1. doc槽1为新版，确认标题及页数 | `doc_info` | `{"doc": 1}` |
| 2. doc槽2为旧版，确认版本身份 | `doc_info` | `{"doc": 2}` |
| 3. 新版对旧版比较文字，读取旧/新文本及页号，检查是否截断 | `doc_compare` | `{"doc": 1, "other": 2, "limit": 500, "visual": false}` |
| 4. 另写差异报告，不标注或改写任一原PDF | `doc_compare_report` | `{"doc": 1, "other": 2, "path": "output/revision-report.pdf"}` |

## CLI、MCP与文档ID

`sourceFiles`列出本次任务的输入PDF，先替换真实路径。`doc`和`other`为1起始文档槽，不是任意运行中的文档ID。附带[write_script.py](../scripts/write_script.py)仅将明确输入和槽位转换为原生工具脚本，不实现PDF业务：

```text
python <本技能目录>/scripts/write_script.py --recipe <已替换输入的craft-steps.json> --output steps.json
pdfcraft-cli run --script steps.json --root <本次输入输出根目录>
```

本批CLI观察来自官方0.8.0；不能将冻结基础技能安装的其他版本自动视为支持。先查`pdfcraft-cli tools`并逐项核对参数，缺失时使用已验证的配套后端或明确停止。

必须用全新CLI进程执行整个脚本。其首先按sourceFiles顺序打开文件，文档ID从1顺序分配；不要拆成多次`run tool`，不要向已有会话发送这里的数字。记录doc_open结果；后端行为变化时停止并改用按实际返回值逐步执行的MCP。用argv运行，避免Windows shell引号差异。

当前插件的`printcraft-editor` MCP直接暴露`doc_open`和本表工具；已将当前清单的字段/必填项与原生schema逐项核对，记录在本技能观察文件的`mcpCatalog`。先等待`editor_status`并查实际schema，再调用`doc_open {"path":"newer.pdf"}`记录返回doc。随后直接调用`doc_compare`，参数格式`{"doc": 1, "other": 2, "limit": 500, "visual": false}`，将doc替换为刚返回的实际ID；比较场景还须另开旧版并将other换成其ID。不使用其他Craft的execute包装。独立CLI不会自动更改另一个Web会话。

## 保存与结果检查

报告明确旧值与新值，差异方向正确、同页不变内容没有误报；独立提取报告文字核对。新旧两源摘要都不变。

先对照真实输入检查目标范围，再执行修改。写入使用新输出路径，不能覆盖源；处理已有水印、页脚、书签或链接时先盘点，不盲目重复叠加。PDF重开后还要用独立解释器或宿主查看器核对最终文字、页数、目标和图像；业务效果不能只由退出码或对象存在判断。

来源固定提交、许可和哈希见[workflow-sources.json](workflow-sources.json)。流程事实为参考，参数和场景正文原创适配。
