# 可释放的裁切蒙版插画的方法和参数

## 输入和目标

新建独立矢量插画样例；真实任务先明确保留范围、哪些对象参与蒙版和最上层遮罩路径。已有作品只选择获授权的对象，不select.all。

用圆形蒙版显示两块色面，原始矩形不被裁掉；保存重开后仍有Clip Group和完整子对象，另存副本释放蒙版后恢复外围内容。

先查询当前版本实际命令和参数。示例画板320×240，所有几何参数以pt计算；1mm=72/25.4pt。以实际交付规格重算位置、边距、偏移或间距。

## 具体操作

| 顺序与目的 | 方法 | 参数例子 | 批次 |
| --- | --- | --- | --- |
| 1. 仅在新作品任务建立独立画板 | `file.new` | `{"width":320,"height":240,"units":"Pixels","backgroundContents":"white"}` | new |
| 2. 创建本次矩形并记录真实返回id | `shape.rectangle` | `{"x":20,"y":40,"width":240,"height":160}` | art |
| 3. 设置目标填色；无ids时仅作用于当前批次新对象 | `paint.setFill` | `{"color":"#2563eb"}` | art |
| 4. 显式去掉描边以避免继承默认黑边 | `paint.setStroke` | `{"none":true}` | art |
| 5. 创建本次矩形并记录真实返回id | `shape.rectangle` | `{"x":100,"y":40,"width":40,"height":160}` | stripe |
| 6. 设置目标填色；无ids时仅作用于当前批次新对象 | `paint.setFill` | `{"color":"#f97316"}` | stripe |
| 7. 显式去掉描边以避免继承默认黑边 | `paint.setStroke` | `{"none":true}` | stripe |
| 8. 创建本次圆形并记录真实返回id | `shape.ellipse` | `{"x":80,"y":60,"width":120,"height":120}` | mask |
| 9. 以真实对象ID建立非破坏蒙版，顶层路径为遮罩 | `object.clippingMask.make` | `{"ids":[{"$ref":"art.id"},{"$ref":"stripe.id"},{"$ref":"mask.id"}]}` | clip |

## 返回ID与批次

按[步骤配方](craft-steps.json)的batch连续分批；同批原生CLI保持新对象选择，批间不能依赖选择仍在。capture保存该命令真实result，后续`{"$ref":"art.id"}`等用实际整数替换；`border.ids`是整个返回数组，不能把它再包一层。首次file.new仅用于独立新图，已有作品要先inspect并选实际对象，不能清空后重建。

CLI每批使用argv构造`vectorcraft-cli run`，各步追加`--cmd 方法 --params JSON`。首批`--export 新工程.vectorcraft`；后续`--in 上一实际工程.vectorcraft ... --export 新检查点.vectorcraft`。不能把batch/capture/$ref传给引擎，不能依赖每次重新开CLI的光标或选择，不能用固定示例ID猜测当前对象。

宿主内先open_browser_editor并使用真实editorUrl打开内置浏览器，等待editor_status.attached。通过同一VectorCraft MCP的command_list查询具体方法；读取当前command_run schema，逐条`{"id":"实际方法","params":{替换后的参数}}`。不要另开CLI声称是相同画布状态；宿主引擎缺命令时明确说明，不能把未执行写成完成。

## 保存与检查

同一MCP实例用实际save_file schema保存新路径；CLI用另一个进程`run --in 结果.vectorcraft --cmd document.inspect`重开读取。再`vectorcraft-cli convert 结果.vectorcraft 审阅.svg`和`... 审阅.png`。检查原生可编辑对象、SVG向量结构以及实际像素与层次，不仅看退出码。PNG是派生预览，不能代替原生工程。来源固定提交与许可见[来源](workflow-sources.json)，参数观察见[命令证据](craft-command-evidence.json)。

顶层圆形必须最后创建或显式置顶；make会去掉遮罩的填色和描边。保存的Clip Group应含圆和两块完整矩形。另存释放样例：`object.clippingMask.release {"ids":[本次clip.id]}`；图形周边应重新出现，遮罩路径仍在且默认无色。不得用pathfinder.crop替代可释放蒙版。
