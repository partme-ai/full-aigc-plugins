# 前言与正文分别编号的方法与参数

## 输入与步骤

本场景输入：用户需要前言使用单独标识而正文从第一页开始显示阅读页码。结构化配方见[craft-steps.json](craft-steps.json)，参数的当前观察记录见[craft-command-evidence.json](craft-command-evidence.json)。先读取实际后端schema与doc_open返回值；此处添加可见页脚，不修改PDF阅读器PageLabels，也不是书签页码或Bates连续编号。实际正文页数变化后重新生成映射；replace=false不会清理旧页脚，不能对已有编号盲目重复执行。

| 顺序与目的 | 工具 | 参数样例 |
| --- | --- | --- |
| 1. 核对前言/正文的实际页区间及页脚留白 | `doc_info` | `{"doc": 1}` |
| 2. 确认只有一页前言，显示i | `doc_header_footer` | `{"doc": 1, "pages": [1], "footer_center": "i", "margins": [12, 12, 20, 20], "font_size": 9, "replace": false}` |
| 3. 正文第1页对应PDF物理第2页 | `doc_header_footer` | `{"doc": 1, "pages": [2], "footer_center": "Page 1 of 3", "margins": [12, 12, 20, 20], "font_size": 9, "replace": false}` |
| 4. 正文第2页对应PDF物理第3页 | `doc_header_footer` | `{"doc": 1, "pages": [3], "footer_center": "Page 2 of 3", "margins": [12, 12, 20, 20], "font_size": 9, "replace": false}` |
| 5. 正文第3页对应PDF物理第4页 | `doc_header_footer` | `{"doc": 1, "pages": [4], "footer_center": "Page 3 of 3", "margins": [12, 12, 20, 20], "font_size": 9, "replace": false}` |
| 6. 完整另存交付副本，不覆盖源PDF | `doc_save` | `{"doc": 1, "path": "output/numbered-report.pdf", "full": true}` |

## CLI、MCP与文档ID

`sourceFiles`列出本次任务的输入PDF，先替换真实路径。`doc`和`other`为1起始文档槽，不是任意运行中的文档ID。附带[write_script.py](../scripts/write_script.py)仅将明确输入和槽位转换为原生工具脚本，不实现PDF业务：

```text
python <本技能目录>/scripts/write_script.py --recipe <已替换输入的craft-steps.json> --output steps.json
pdfcraft-cli run --script steps.json --root <本次输入输出根目录>
```

本批CLI观察来自官方0.8.0；不能将冻结基础技能安装的其他版本自动视为支持。先查`pdfcraft-cli tools`并逐项核对参数，缺失时使用已验证的配套后端或明确停止。

必须用全新CLI进程执行整个脚本。其首先按sourceFiles顺序打开文件，文档ID从1顺序分配；不要拆成多次`run tool`，不要向已有会话发送这里的数字。记录doc_open结果；后端行为变化时停止并改用按实际返回值逐步执行的MCP。用argv运行，避免Windows shell引号差异。

当前插件的`pdfcraft-editor` MCP直接暴露`doc_open`和本表工具；已将当前清单的字段/必填项与原生schema逐项核对，记录在本技能观察文件的`mcpCatalog`。先等待`editor_status`并查实际schema，再调用`doc_open {"path":"input.pdf"}`记录返回doc。随后直接调用`doc_header_footer`，参数格式`{"doc": 1, "pages": [1], "footer_center": "i", "margins": [12, 12, 20, 20], "font_size": 9, "replace": false}`，将doc替换为刚返回的实际ID；比较场景还须另开旧版并将other换成其ID。不使用其他Craft的execute包装。独立CLI不会自动更改另一个Web会话。

## 保存与结果检查

重开输出检查前言i及正文1/3、2/3、3/3仅出现在对应页，页脚不遮挡正文；四页原文字与源摘要保持。

先对照真实输入检查目标范围，再执行修改。写入使用新输出路径，不能覆盖源；处理已有水印、页脚、书签或链接时先盘点，不盲目重复叠加。PDF重开后还要用独立解释器或宿主查看器核对最终文字、页数、目标和图像；业务效果不能只由退出码或对象存在判断。

来源固定提交、许可和哈希见[workflow-sources.json](workflow-sources.json)。流程事实为参考，参数和场景正文原创适配。
