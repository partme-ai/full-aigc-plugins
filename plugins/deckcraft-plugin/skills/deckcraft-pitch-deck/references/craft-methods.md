# 本场景的 Craft 方法与参数

新建示例仅用于新任务：已有演示文稿先读取页数、选择和内容；不得用file.new清空。索引为0起，仅在此新文稿示例固定；已有文稿重新查询。布局和真实内容质量、外部PowerPoint渲染、宿主同步不由命令通过证明。

| 顺序与目的 | 实际方法 | 参数模板 |
| --- | --- | --- |
| 1. 仅创建新的16:9示例；已有文稿不得清空 | `file.new` | `{"size":[960,540],"blank":true}` |
| 2. 建立用户问题页 | `slide.new` | `{"layout":"titleAndContent","title":"用户问题","body":"目标用户、真实痛点与证据来源；规模待确认。"}` |
| 3. 给第1页写入专属备注 | `slide.notes` | `{"index":0,"text":"问题证据：区分已验证访谈、观察与假设，注明来源和日期。"}` |
| 4. 建立解决方案页 | `slide.new` | `{"layout":"titleAndContent","title":"解决方案","body":"价值、关键能力、适用范围和实施约束。"}` |
| 5. 给第2页写入专属备注 | `slide.notes` | `{"index":1,"text":"方案约束：用证据解释方案与问题的关系，说明尚未具备的能力。"}` |
| 6. 建立验证计划页 | `slide.new` | `{"layout":"titleAndContent","title":"验证计划","body":"关键假设、试点方法与成功指标待确认。"}` |
| 7. 给第3页写入专属备注 | `slide.notes` | `{"index":2,"text":"验证计划：明确输入、样本、比较方法和失败标准；不伪造验证结果。"}` |
| 8. 建立交付路径页 | `slide.new` | `{"layout":"titleAndContent","title":"交付路径","body":"阶段、依赖、里程碑；负责人和日期待确认。"}` |
| 9. 给第4页写入专属备注 | `slide.notes` | `{"index":3,"text":"里程碑：用可交付结果定义阶段，核实资源依赖与风险。"}` |
| 10. 建立资源与风险页 | `slide.new` | `{"layout":"titleAndContent","title":"资源与风险","body":"资源请求、决策事项、主要风险；预算待确认。"}` |
| 11. 给第5页写入专属备注 | `slide.notes` | `{"index":4,"text":"资源请求：说明资金或人员用途；预测、估计和已发生事实分别标记。"}` |

## 调用与动态值

先读实际运行时schema及[观察目录](craft-command-evidence.json)。`$变量`必须替换为查询到的真实值。品牌主题从`design.themes`返回列表选择；复制页所有对象ID必须来自新增副本，不能沿用源页ID。

需要编辑器同步时，等待editor_status就绪，再通过该编辑器同一会话的`run_command`调用，例如`{"command":"slide.notes","params":{"index":0,"text":"课程目标：完成标准"}}`。独立CLI文件任务使用argv调用`deckcraft-cli run --in input.deckcraft --cmd 'slide.notes={"index":0,"text":"课程目标：完成标准"}' --save output.deckcraft`；shell引号仅为展示，跨平台执行传argv。CLI新进程不会自动改变已打开Web编辑器。CLI run成功可能没有stdout；保存后重新查询或读取工程，不解析不存在的返回ID。

JSON步骤见[craft-steps.json](craft-steps.json)，是参数模板而非可直接执行的脚本；保留输入，另存可编辑原生工程和PPTX。新增页、图表和备注逐项核查，回读PPTX后再次修改图表数据验证可编辑性。

## 结果检查

五页从问题到资源请求，逐页备注保留；证据和假设明确区分，未知业务数据不捏造。

外部投影效果、字体回退、字号溢出、真实教学或商业内容有效性、安装宿主画面同步需要分别验证；当前不因结构检查通过而宣称完整场景验收。

[来源与许可](workflow-sources.json)：只借鉴工作流事实，步骤及参数原创适配。
