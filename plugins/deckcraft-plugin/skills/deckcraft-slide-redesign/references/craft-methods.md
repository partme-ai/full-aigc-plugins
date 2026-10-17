# 本场景的 Craft 方法与参数

先绑定source.index；复制后用slide.inspect查询副本，并按对象类型/文本唯一定位copy.titleId/bodyId/metricId。示例边框适用960×540页；真实尺寸按当前页重算。图片、图表不得按文字框规则拉伸。新建示例仅用于新任务：已有演示文稿先读取页数、选择和内容；不得用file.new清空。索引为0起，仅在此新文稿示例固定；已有文稿重新查询。布局和真实内容质量、外部PowerPoint渲染、宿主同步不由命令通过证明。

| 顺序与目的 | 实际方法 | 参数模板 |
| --- | --- | --- |
| 1. 明确源页并复制；读取实际新增页与对象编号 | `slide.duplicate` | `{"index":"$source.index"}` |
| 2. 查询副本的对象类型、文本、边框并绑定新ID | `slide.inspect` | `{"index":"$copy.index"}` |
| 3. 进入副本，保持后续命令属于此页 | `slide.go` | `{"index":"$copy.index"}` |
| 4. 为副本选择标题正文布局 | `slide.layout` | `{"index":"$copy.index","layout":"titleAndContent"}` |
| 5. 定位副本titleId | `shape.move` | `{"ids":["$copy.titleId"],"x":48,"y":36}` |
| 6. 调整副本可编辑文字框，不拉伸图像 | `shape.resize` | `{"ids":["$copy.titleId"],"w":864,"h":80,"lockAspect":false}` |
| 7. 定位副本bodyId | `shape.move` | `{"ids":["$copy.bodyId"],"x":48,"y":150}` |
| 8. 调整副本可编辑文字框，不拉伸图像 | `shape.resize` | `{"ids":["$copy.bodyId"],"w":540,"h":300,"lockAspect":false}` |
| 9. 定位副本metricId | `shape.move` | `{"ids":["$copy.metricId"],"x":630,"y":150}` |
| 10. 调整副本可编辑文字框，不拉伸图像 | `shape.resize` | `{"ids":["$copy.metricId"],"w":280,"h":120,"lockAspect":false}` |

## 调用与动态值

先读实际运行时schema及[观察目录](craft-command-evidence.json)。`$变量`必须替换为查询到的真实值。品牌主题从`design.themes`返回列表选择；复制页所有对象ID必须来自新增副本，不能沿用源页ID。

需要编辑器同步时，等待editor_status就绪，再通过该编辑器同一会话的`run_command`调用，例如`{"command":"slide.notes","params":{"index":0,"text":"课程目标：完成标准"}}`。独立CLI文件任务使用argv调用`deckcraft-cli run --in input.deckcraft --cmd 'slide.notes={"index":0,"text":"课程目标：完成标准"}' --save output.deckcraft`；shell引号仅为展示，跨平台执行传argv。CLI新进程不会自动改变已打开Web编辑器。CLI run成功可能没有stdout；保存后重新查询或读取工程，不解析不存在的返回ID。

JSON步骤见[craft-steps.json](craft-steps.json)，是参数模板而非可直接执行的脚本；保留输入，另存可编辑原生工程和PPTX。新增页、图表和备注逐项核查，回读PPTX后再次修改图表数据验证可编辑性。

## 结果检查

源页及无关页保持一致；只修改新增副本，所有对象使用副本新ID，保留文字及目标边框。

外部投影效果、字体回退、字号溢出、真实教学或商业内容有效性、安装宿主画面同步需要分别验证；当前不因结构检查通过而宣称完整场景验收。

[来源与许可](workflow-sources.json)：只借鉴工作流事实，步骤及参数原创适配。
