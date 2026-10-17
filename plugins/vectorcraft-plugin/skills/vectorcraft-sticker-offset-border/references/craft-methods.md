# 保留原稿的白边轮廓的方法和参数

## 输入和目标

输入为已确认的闭合矢量图形，先明确向外偏移距离与连接样式。图像、文字、复杂自交轮廓不能直接套用此单矩形样例。

为100×60pt原稿生成向外8pt白边，保留原稿几何和颜色，轮廓位于原稿之后、底色之前，保存重开后可分别编辑。

先查询当前版本实际命令和参数。示例画板320×240，所有几何参数以pt计算；1mm=72/25.4pt。以实际交付规格重算位置、边距、偏移或间距。

## 具体操作

| 顺序与目的 | 方法 | 参数例子 | 批次 |
| --- | --- | --- | --- |
| 1. 仅在新作品任务建立独立画板 | `file.new` | `{"width":320,"height":240,"units":"Pixels","backgroundContents":"white"}` | new |
| 2. 创建本次矩形并记录真实返回id | `shape.rectangle` | `{"x":0,"y":0,"width":320,"height":240}` | background |
| 3. 设置目标填色；无ids时仅作用于当前批次新对象 | `paint.setFill` | `{"color":"#64748b"}` | background |
| 4. 显式去掉描边以避免继承默认黑边 | `paint.setStroke` | `{"none":true}` | background |
| 5. 创建本次矩形并记录真实返回id | `shape.rectangle` | `{"x":100,"y":80,"width":100,"height":60}` | art |
| 6. 设置目标填色；无ids时仅作用于当前批次新对象 | `paint.setFill` | `{"color":"#2563eb"}` | art |
| 7. 显式去掉描边以避免继承默认黑边 | `paint.setStroke` | `{"none":true}` | art |
| 8. 只选择本任务授权的实际对象 | `select.set` | `{"ids":[{"$ref":"art.id"}]}` | offset |
| 9. 按pt向外生成新偏移路径并记录返回ids | `object.path.offsetPath` | `{"offset":8,"joins":"round","miterLimit":4}` | offset |
| 10. 设置目标填色；无ids时仅作用于当前批次新对象 | `paint.setFill` | `{"ids":{"$ref":"border.ids"},"color":"#ffffff"}` | paint-border |
| 11. 显式去掉描边以避免继承默认黑边 | `paint.setStroke` | `{"ids":{"$ref":"border.ids"},"none":true}` | paint-border |
| 12. 将原稿置于白边之上，避免白边盖住图形 | `object.arrange.bringToFront` | `{"ids":[{"$ref":"art.id"}]}` | front |

## 返回ID与批次

按[步骤配方](craft-steps.json)的batch连续分批；同批原生CLI保持新对象选择，批间不能依赖选择仍在。capture保存该命令真实result，后续`{"$ref":"art.id"}`等用实际整数替换；`border.ids`是整个返回数组，不能把它再包一层。首次file.new仅用于独立新图，已有作品要先inspect并选实际对象，不能清空后重建。

CLI每批使用argv构造`vectorcraft-cli run`，各步追加`--cmd 方法 --params JSON`。首批`--export 新工程.vectorcraft`；后续`--in 上一实际工程.vectorcraft ... --export 新检查点.vectorcraft`。不能把batch/capture/$ref传给引擎，不能依赖每次重新开CLI的光标或选择，不能用固定示例ID猜测当前对象。

宿主内先open_browser_editor并使用真实editorUrl打开内置浏览器，等待editor_status.attached。通过同一VectorCraft MCP的command_list查询具体方法；读取当前command_run schema，逐条`{"id":"实际方法","params":{替换后的参数}}`。不要另开CLI声称是相同画布状态；宿主引擎缺命令时明确说明，不能把未执行写成完成。

## 保存与检查

同一MCP实例用实际save_file schema保存新路径；CLI用另一个进程`run --in 结果.vectorcraft --cmd document.inspect`重开读取。再`vectorcraft-cli convert 结果.vectorcraft 审阅.svg`和`... 审阅.png`。检查原生可编辑对象、SVG向量结构以及实际像素与层次，不仅看退出码。PNG是派生预览，不能代替原生工程。来源固定提交与许可见[来源](workflow-sources.json)，参数观察见[命令证据](craft-command-evidence.json)。

向外8pt≈2.82mm，不能误用为8mm。示例外框应为[92,72,116,76]，原稿仍是[100,80,100,60]。偏移结果画白色并去掉描边，再只将原稿bringToFront；不要sendToBack让白边落到灰色底板之后。本技能是可编辑视觉白边，刀模专色、设备切割和印厂规范需要另行确认。
