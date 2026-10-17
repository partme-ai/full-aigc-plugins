# DeckCraft main：模板和品牌页复用

固定main `1dc69720db64323370dda061226becb09ad79fd4`的实际原生命令目录为321个唯一标识，较稳定版观察目录新增89个。[差异](main-command-delta.json)保留旧目录的歧义：旧234条中text.delete/text.move各有两份不同参数，唯一标识232个；只对其余标识比较契约，不静默选择其中一份。完整main参数见[目录](main-command-catalog.json)。已有8条业务手册通过main回归，下面模板与复用流程已通过专项Windows原生业务回归，未替代宿主验收。

## 先选择真实模板，再制作演示稿

1. 通过当前宿主`list_commands {"filter":"file.templates"}`检查方法；`run_command {"command":"file.templates","params":{}}`列出真实starter名称、用途、主题和页数。main帮助写成数组，但实际返回`{templates:[...]}`，读取templates成员，不把外层对象当模板数组。按用户目标选择返回的名称，不编造模板ID。
2. 新建任务可用`run_command {"command":"file.new","params":{"template":"实际返回的模板名称"}}`。已有未保存文稿先保存；不能在既有编辑任务中直接照抄新建。
3. 逐页替换目标文字、数据和图片，保持用户要求的版式，检查溢出、可编辑对象、页码和原生图表。模板名不等于用户内容已经填完。
4. 保存新的`.deckcraft`母版和`.pptx`交付文件，重开检查；不能把渲染成一张图片的页面算作可编辑演示稿。外部PowerPoint字体、动画和媒体兼容另验。

## 从品牌资料库复用指定页面

适用：把批准的封面、公司介绍、团队或结束页插入当前演示，避免每次从空白搭版。只使用有本任务使用权的源文件。

1. 先确认来源文件页数、标题、字号/字体和页面尺寸，及目标文稿当前页序。保留源文件，现有目标另存副本。
2. 来源至少3页时，插入第1和第3页的例子为：

```json
{"command":"slide.reuse","params":{"path":"input/brand-library.pptx","slides":[0,2],"keepFormatting":true,"at":1}}
```

这是当前MCP `run_command`的参数。slides/at使用0基索引；at=1插到目标第2页位置。Web前端若只允许字节输入，可按实际schema改用`data:base64`和`name`，不能把本机绝对路径交给浏览器自己读取。

3. keepFormatting默认false，会采用目标主题；品牌复用先明确true，并核对实际字体、填色和背景。不同页面尺寸、缺字体和复杂对象需实际检查，不能只看返回成功。
4. 检查总页数、两页顺序与目标其他页不变，保存并重开，确认源文件摘要未改变。不得用slide.reuse替代用户明确要求的整稿重排。

模板与复用流程通过Windows main专项CI [39010982169](https://github.com/partme-ai/full-aigc-plugins/actions/runs/39010982169)：使用真实返回的starter创建文稿；从品牌PPTX选择A/C两页按顺序插入目标第2页位置，保存原生格式重开、PPTX活文字与非目标内容保留、源文件摘要不变均通过。外部PowerPoint渲染、复杂主题格式逐属性保持和真实宿主画面同步尚未验收。SmartArt、图片去背景、形状点编辑等其他新增方法也只在索引中，不据名称推断效果。

## CLI目录变化

main的`deckcraft-cli commands`与`describe`输出人类可读帮助，不是JSON；`commands --json`不是此版本的结构化接口。需要程序读取时连接原生stdio MCP，调用`list_commands {}`或按filter查询。实际main Windows回归已使用这一路径，然后执行原生CLI业务；不把它当成宿主安装验证。

同会话编辑始终复用当前内嵌编辑器的MCP。另起headless CLI操作其他工程不会自动回显到当前画面。
