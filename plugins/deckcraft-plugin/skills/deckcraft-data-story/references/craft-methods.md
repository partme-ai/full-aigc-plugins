# 本场景的 Craft 方法与参数

新建示例仅用于新任务：已有演示文稿先读取页数、选择和内容；不得用file.new清空。索引为0起，仅在此新文稿示例固定；已有文稿重新查询。布局和真实内容质量、外部PowerPoint渲染、宿主同步不由命令通过证明。

| 顺序与目的 | 实际方法 | 参数模板 |
| --- | --- | --- |
| 1. 仅创建新的16:9示例；已有文稿不得清空 | `file.new` | `{"size":[960,540],"blank":true}` |
| 2. 建立结论与数据依据页 | `slide.new` | `{"layout":"titleOnly","title":"结论与数据依据","body":""}` |
| 3. 用原生柱状图保留数据和类别顺序 | `insert.chart` | `{"type":"column","rect":[80,150,800,300],"categories":["A","B"],"series":[{"name":"指标","values":[21,42]}]}` |
| 4. 给第1页写入专属备注 | `slide.notes` | `{"index":0,"text":"数据依据：A/B与21/42仅为示例；替换为真实数据并注明单位、周期、来源和缺失值处理。"}` |
| 5. 建立解释边界与下一步页 | `slide.new` | `{"layout":"titleAndContent","title":"解释边界与下一步","body":"核实指标定义、样本范围与异常点；相关关系不等于因果；下一步待确认。"}` |
| 6. 给第2页写入专属备注 | `slide.notes` | `{"index":1,"text":"解释边界：检查轴范围、标签、对比口径与样本限制；当前命令未设置轴基线，不得宣称已配置。"}` |

## 调用与动态值

先读实际运行时schema及[观察目录](craft-command-evidence.json)。`$变量`必须替换为查询到的真实值。品牌主题从`design.themes`返回列表选择；复制页所有对象ID必须来自新增副本，不能沿用源页ID。

需要编辑器同步时，等待editor_status就绪，再通过该编辑器同一会话的`run_command`调用，例如`{"command":"slide.notes","params":{"index":0,"text":"课程目标：完成标准"}}`。独立CLI文件任务使用argv调用`deckcraft-cli run --in input.deckcraft --cmd 'slide.notes={"index":0,"text":"课程目标：完成标准"}' --save output.deckcraft`；shell引号仅为展示，跨平台执行传argv。CLI新进程不会自动改变已打开Web编辑器。CLI run成功可能没有stdout；保存后重新查询或读取工程，不解析不存在的返回ID。

JSON步骤见[craft-steps.json](craft-steps.json)，是参数模板而非可直接执行的脚本；保留输入，另存可编辑原生工程和PPTX。新增页、图表和备注逐项核查，回读PPTX后再次修改图表数据验证可编辑性。

## 结果检查

两页分别陈述依据和解释边界；图表活数据回读可修改，类别顺序保留，轴和标签仍需视觉检查。

外部投影效果、字体回退、字号溢出、真实教学或商业内容有效性、安装宿主画面同步需要分别验证；当前不因结构检查通过而宣称完整场景验收。

[来源与许可](workflow-sources.json)：只借鉴工作流事实，步骤及参数原创适配。
