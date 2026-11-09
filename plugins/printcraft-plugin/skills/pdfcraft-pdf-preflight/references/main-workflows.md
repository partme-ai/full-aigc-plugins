# PrintCraft main交付检查补充

仅用于PdfCraft固定main `924c4da4ac2879ac9107c6c82e20ac6be5570f0a`或明确具备相同schema的新候选。实际原生工具目录为170项，相对稳定版163项新增7项，16处契约变化见[完整差异](main-command-delta.json)。这里的名称是MCP工具名，其JSON采用`input_schema`中的snake_case参数，不把它们当原始引擎command ID。新增统计/定向检查已通过Windows main专项39008588714：3个英文词测试、重复页去重、未标记正文检出与输入摘要不变通过；不是完整无障碍认证。

## 指定页统计与未标记内容检查

适用：交付前核对所选页的文字量，并找出未标记的正文、批注或表单字段。输入保留原文件，所有统计为只读；此步骤不自动修复标签，也不等于完整无障碍认证。

1. `doc_open {"path":"input/report.pdf"}`取得真实`doc`，使用`doc_info`确认页数、复制权限及页面是否已有文本；不能假定doc=1。下列`doc`占位使用实际返回的正整数。
2. `text_word_count {"doc":实际句柄,"pages":[1,2],"exclude_tables":false,"exclude_code":false,"exclude_images":false}`，核对`total`与逐页结果，页号从1开始。重复页不应重复累计；无法读取的页面应报错，不能把不完整结果称为全本总数。
3. 若需要排除表格/代码/图像相关文字，明确相应布尔值并保留未分类结构提示。表格、代码由PDF结构标签判断，不能靠视觉猜测；缺标签或无法分类的文字可能保留。排除images会排除Figure标签和不可见/OCR文字，不会执行OCR。
4. `accessibility_find_untagged {"doc":实际句柄,"pages":[1,2]}`，读取逐规则`status`、`findings`及页面位置；只针对tagged-content、tagged-annotations、tagged-form-fields。不能因其他规则skipped就宣称没有语言、阅读顺序、替代文本等问题。
5. 保存检查报告，抽取一页独立核对文字；必要时进入已有OCR技能处理扫描件，再重新统计。对图片型PDF返回0字不能推断没有正文。

独立CLI对应方法是`pdfcraft-cli run --script steps.json --root workspace`：步骤使用`{"tool":"doc_open","args":{"path":"input/report.pdf"}}`等对象。doc句柄依该会话实际打开顺序返回，不能把别的脚本或编辑器句柄带进来。内嵌工作流优先调用同会话原生工具；其工具目录未暴露这些名称时，不另起CLI并声称结果已同步到页面。

## 标签和交互交付的新工具边界

| 新工具 | 参数与处理方式 |
| --- | --- |
| `accessibility_autotag_form_fields` | `{doc}`，给表单字段补结构标签；另存副本、重开核对字段关联和阅读顺序，不代表修复字段中文显示。 |
| `accessibility_tag_content` | `{doc,object,generation}`；使用审计返回的真实PDF对象引用，不把页码/数组下标当object。修改后重新检查。 |
| `accessibility_mark_tag_artifact` | `{doc,object,generation}`；只将确定为装饰的内容标成Artifact，不能为通过检查而隐藏正文语义。 |
| `page_transition_set` | `{doc,pages:[1],style:"Fade",duration:0.5}`；动画显示取决于PDF阅读器，纸面打印不会呈现；页号从1开始。 |
| `xfa_to_static` | `{doc}`；转换为静态表示会改变交互能力，先保留原件并核对表单内容/外观。目录存在不代表任意动态XFA都兼容。 |

上述五项当前仅有main真实工具契约，尚未完成本技能的业务交付验收。已有中文表单外观限制仍保留，不能由新增标签工具推断其已解决。
