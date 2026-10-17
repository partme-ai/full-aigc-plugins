# 可调整行列的贴纸阵列的方法和参数

## 输入和目标

确认单个贴纸尺寸、行列数、水平/垂直净间距和画板范围。例子是30×30pt源图、20pt净间距、3行4列，不是自动填满纸张或印刷拼版。

保存为可编辑Grid Repeat，原稿仅有一个源图；重开可改行列、改源图颜色并同步实例，另存展开副本得到12个真实独立图形。

先查询当前版本实际命令和参数。示例画板320×240，所有几何参数以pt计算；1mm=72/25.4pt。以实际交付规格重算位置、边距、偏移或间距。

## 具体操作

| 顺序与目的 | 方法 | 参数例子 | 批次 |
| --- | --- | --- | --- |
| 1. 仅在新作品任务建立独立画板 | `file.new` | `{"width":320,"height":240,"units":"Pixels","backgroundContents":"white"}` | new |
| 2. 创建本次圆形并记录真实返回id | `shape.ellipse` | `{"x":20,"y":20,"width":30,"height":30}` | art |
| 3. 设置目标填色；无ids时仅作用于当前批次新对象 | `paint.setFill` | `{"color":"#2563eb"}` | art |
| 4. 显式去掉描边以避免继承默认黑边 | `paint.setStroke` | `{"none":true}` | art |
| 5. 以源对象真实ID建立可编辑行列阵列 | `object.repeat.grid` | `{"ids":[{"$ref":"art.id"}],"rows":3,"cols":4,"hSpacing":20,"vSpacing":20}` | grid |

## 返回ID与批次

按[步骤配方](craft-steps.json)的batch连续分批；同批原生CLI保持新对象选择，批间不能依赖选择仍在。capture保存该命令真实result，后续`{"$ref":"art.id"}`等用实际整数替换；`border.ids`是整个返回数组，不能把它再包一层。首次file.new仅用于独立新图，已有作品要先inspect并选实际对象，不能清空后重建。

CLI每批使用argv构造`vectorcraft-cli run`，各步追加`--cmd 方法 --params JSON`。首批`--export 新工程.vectorcraft`；后续`--in 上一实际工程.vectorcraft ... --export 新检查点.vectorcraft`。不能把batch/capture/$ref传给引擎，不能依赖每次重新开CLI的光标或选择，不能用固定示例ID猜测当前对象。

宿主内先open_browser_editor并使用真实editorUrl打开内置浏览器，等待editor_status.attached。通过同一VectorCraft MCP的command_list查询具体方法；读取当前command_run schema，逐条`{"id":"实际方法","params":{替换后的参数}}`。不要另开CLI声称是相同画布状态；宿主引擎缺命令时明确说明，不能把未执行写成完成。

## 保存与检查

同一MCP实例用实际save_file schema保存新路径；CLI用另一个进程`run --in 结果.vectorcraft --cmd document.inspect`重开读取。再`vectorcraft-cli convert 结果.vectorcraft 审阅.svg`和`... 审阅.png`。检查原生可编辑对象、SVG向量结构以及实际像素与层次，不仅看退出码。PNG是派生预览，不能代替原生工程。来源固定提交与许可见[来源](workflow-sources.json)，参数观察见[命令证据](craft-command-evidence.json)。

净间距20pt加30pt源图得到50pt中心步长，3×4阵列外接框为180×130pt。重开后先`select.set {"ids":[本次repeat.id]}`，同批`object.repeat.options {"rows":2,"cols":3}`可改为六格；按art.id改填色应同步全部实例。保留原生主稿，另存后选择repeat.id再`object.repeat.expand {}`交付12个独立对象。展开后不能再把它当共享源阵列。
