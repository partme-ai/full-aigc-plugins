# 本场景的 Craft 方法与参数

新建示例仅用于新任务：已有演示文稿先读取页数、选择和内容；不得用file.new清空。索引为0起，仅在此新文稿示例固定；已有文稿重新查询。布局和真实内容质量、外部PowerPoint渲染、宿主同步不由命令通过证明。

| 顺序与目的 | 实际方法 | 参数模板 |
| --- | --- | --- |
| 1. 仅创建新的16:9示例；已有文稿不得清空 | `file.new` | `{"size":[960,540],"blank":true}` |
| 2. 建立本周结论页 | `slide.new` | `{"layout":"titleAndContent","title":"本周结论","body":"完成事项、证据与风险；以下数值仅是待替换示例。"}` |
| 3. 给第1页写入专属备注 | `slide.notes` | `{"index":0,"text":"本周结论：确认报告周期、完成量定义、单位和数据来源；21与42是示例，不能当成真实业务结果。"}` |
| 4. 建立完成量趋势页 | `slide.new` | `{"layout":"titleOnly","title":"完成量趋势","body":""}` |
| 5. 插入原生可编辑折线图 | `insert.chart` | `{"type":"line","rect":[80,150,800,300],"categories":["上周","本周"],"series":[{"name":"完成量","values":[21,42]}]}` |
| 6. 给第2页写入专属备注 | `slide.notes` | `{"index":1,"text":"趋势：相同口径下比较上周和本周；说明缺失值和样本限制，不据两点预测未来。"}` |
| 7. 建立行动与风险页 | `slide.new` | `{"layout":"titleOnly","title":"行动与风险","body":""}` |
| 8. 建立行动、负责人、截止日期表 | `insert.table` | `{"rows":3,"cols":3,"rect":[48,150,864,260]}` |
| 9. 填入行动表单元格 | `text.set` | `{"cell":[0,0],"text":"行动"}` |
| 10. 填入行动表单元格 | `text.set` | `{"cell":[0,1],"text":"负责人"}` |
| 11. 填入行动表单元格 | `text.set` | `{"cell":[0,2],"text":"截止"}` |
| 12. 填入行动表单元格 | `text.set` | `{"cell":[1,0],"text":"复核风险"}` |
| 13. 填入行动表单元格 | `text.set` | `{"cell":[1,1],"text":"待确认"}` |
| 14. 填入行动表单元格 | `text.set` | `{"cell":[1,2],"text":"待确认"}` |
| 15. 填入行动表单元格 | `text.set` | `{"cell":[2,0],"text":"推进试点"}` |
| 16. 填入行动表单元格 | `text.set` | `{"cell":[2,1],"text":"待确认"}` |
| 17. 填入行动表单元格 | `text.set` | `{"cell":[2,2],"text":"待确认"}` |
| 18. 标明表头 | `table.options` | `{"headerRow":true}` |
| 19. 给第3页写入专属备注 | `slide.notes` | `{"index":2,"text":"行动：负责人和截止日期须由真实计划填充，未给定项保留待确认；逐项检查风险与下一步关联。"}` |

## 调用与动态值

先读实际运行时schema及[观察目录](craft-command-evidence.json)。`$变量`必须替换为查询到的真实值。品牌主题从`design.themes`返回列表选择；复制页所有对象ID必须来自新增副本，不能沿用源页ID。

需要编辑器同步时，等待editor_status就绪，再通过该编辑器同一会话的`run_command`调用，例如`{"command":"slide.notes","params":{"index":0,"text":"课程目标：完成标准"}}`。独立CLI文件任务使用argv调用`deckcraft-cli run --in input.deckcraft --cmd 'slide.notes={"index":0,"text":"课程目标：完成标准"}' --save output.deckcraft`；shell引号仅为展示，跨平台执行传argv。CLI新进程不会自动改变已打开Web编辑器。CLI run成功可能没有stdout；保存后重新查询或读取工程，不解析不存在的返回ID。

JSON步骤见[craft-steps.json](craft-steps.json)，是参数模板而非可直接执行的脚本；保留输入，另存可编辑原生工程和PPTX。新增页、图表和备注逐项核查，回读PPTX后再次修改图表数据验证可编辑性。

## 结果检查

三页结论、趋势、行动；图表类别和数值顺序正确，表格可编辑，逐页备注正确，回读后修改图表数据。

外部投影效果、字体回退、字号溢出、真实教学或商业内容有效性、安装宿主画面同步需要分别验证；当前不因结构检查通过而宣称完整场景验收。

[来源与许可](workflow-sources.json)：只借鉴工作流事实，步骤及参数原创适配。
