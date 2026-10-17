# DeckCraft diagram 场景

默认从新建空文件执行。按实际输入替换示例，已有文件先定位目标；不要清空或全选已有文稿。组合演示场景只新建一次，后续跳过带newDocumentOnly标记的步骤。

## approval-flow-diagram：审批步骤流程图

输入：流程与责任角色已由输入确认，异常路径需在备注中保留。

| 操作目的 | 命令 | 参数例子 |
| --- | --- | --- |
| 1. 新建960×540点空演示文稿，仅在新建任务中使用 | `file.new` | `{"size":[960,540],"blank":true}` |
| 2. 建立流程图空白页 | `slide.new` | `{"layout":"blank"}` |
| 3. 插入指定版心位置的可编辑文本图形 | `shape.insert` | `{"preset":"roundRect","rect":[48,180,180,90],"text":"申请"}` |
| 4. 只填充刚插入的当前图形 | `shape.fill` | `{"color":"#e8f0fe"}` |
| 5. 插入独立箭头标注下一步 | `shape.insert` | `{"preset":"rightArrow","rect":[232,208,40,32]}` |
| 6. 插入指定版心位置的可编辑文本图形 | `shape.insert` | `{"preset":"roundRect","rect":[276,180,180,90],"text":"复核"}` |
| 7. 只填充刚插入的当前图形 | `shape.fill` | `{"color":"#e8f0fe"}` |
| 8. 插入独立箭头标注下一步 | `shape.insert` | `{"preset":"rightArrow","rect":[460,208,40,32]}` |
| 9. 插入指定版心位置的可编辑文本图形 | `shape.insert` | `{"preset":"roundRect","rect":[504,180,180,90],"text":"批准"}` |
| 10. 只填充刚插入的当前图形 | `shape.fill` | `{"color":"#e8f0fe"}` |
| 11. 插入独立箭头标注下一步 | `shape.insert` | `{"preset":"rightArrow","rect":[688,208,40,32]}` |
| 12. 插入指定版心位置的可编辑文本图形 | `shape.insert` | `{"preset":"roundRect","rect":[732,180,180,90],"text":"归档"}` |
| 13. 只填充刚插入的当前图形 | `shape.fill` | `{"color":"#e8f0fe"}` |
| 14. 备注说明角色与异常流 | `slide.notes` | `{"text":"申请人提交；复核人核验；批准人确认；编号冲突则返回申请。箭头为独立图形，移动节点后需重对齐。"}` |

检查：版心内无溢出与遮挡；备注记录来源与待确认假设；保存源工程、导出PPTX后核对可编辑对象。

边界：独立箭头不是动态连接器；移动节点后重新检查对齐，未绘制的异常边必须明确说明。

