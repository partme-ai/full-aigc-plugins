# 本场景的 Craft 方法与参数

新建示例仅用于新任务：已有演示文稿先读取页数、选择和内容；不得用file.new清空。索引为0起，仅在此新文稿示例固定；已有文稿重新查询。布局和真实内容质量、外部PowerPoint渲染、宿主同步不由命令通过证明。

| 顺序与目的 | 实际方法 | 参数模板 |
| --- | --- | --- |
| 1. 仅创建新的16:9示例；已有文稿不得清空 | `file.new` | `{"size":[960,540],"blank":true}` |
| 2. 按目标、练习、回顾建立三页 | `slide.fromOutline` | `{"text":"课程目标\n\t完成标准\n练习\n\t操作步骤\n回顾\n\t常见错误"}` |
| 3. 给第1页写入专属备注 | `slide.notes` | `{"index":0,"text":"课程目标：说明受众、先备知识与完成标准；例子应有来源，不能编造答案。"}` |
| 4. 给第2页写入专属备注 | `slide.notes` | `{"index":1,"text":"练习：提供输入材料、操作步骤和可检查的输出；演示后留时间独立完成。"}` |
| 5. 给第3页写入专属备注 | `slide.notes` | `{"index":2,"text":"回顾：对照练习答案解释常见错误，并注明课后资料和待确认问题。"}` |

## 调用与动态值

先读实际运行时schema及[观察目录](craft-command-evidence.json)。`$变量`必须替换为查询到的真实值。品牌主题从`design.themes`返回列表选择；复制页所有对象ID必须来自新增副本，不能沿用源页ID。

需要编辑器同步时，等待editor_status就绪，再通过该编辑器同一会话的`run_command`调用，例如`{"command":"slide.notes","params":{"index":0,"text":"课程目标：完成标准"}}`。独立CLI文件任务使用argv调用`deckcraft-cli run --in input.deckcraft --cmd 'slide.notes={"index":0,"text":"课程目标：完成标准"}' --save output.deckcraft`；shell引号仅为展示，跨平台执行传argv。CLI新进程不会自动改变已打开Web编辑器。CLI run成功可能没有stdout；保存后重新查询或读取工程，不解析不存在的返回ID。

JSON步骤见[craft-steps.json](craft-steps.json)，是参数模板而非可直接执行的脚本；保留输入，另存可编辑原生工程和PPTX。新增页、图表和备注逐项核查，回读PPTX后再次修改图表数据验证可编辑性。

## 结果检查

三页分别具有目标、练习、回顾正文和专属备注；PPTX回读保留活文字和备注。

外部投影效果、字体回退、字号溢出、真实教学或商业内容有效性、安装宿主画面同步需要分别验证；当前不因结构检查通过而宣称完整场景验收。

[来源与许可](workflow-sources.json)：只借鉴工作流事实，步骤及参数原创适配。
