# 可编辑采访人物条：底板、姓名职位与透明入退场

这是既有lower-thirds场景的具体制作流程，不新增场景计数。示例姓名、职位、颜色只是排版样稿；实际执行替换为用户提供内容。先完成最长姓名样稿，再做系列变体。

## 操作顺序与参数

完整可执行参数顺序见[独立计划](animated-lower-third.json)。创建1920×1080、25fps、6秒的新合成，不在未知工程中直接重用Name、Role、Plate名称。

| 步骤 | 方法与关键参数 | 目的 |
| --- | --- | --- |
| 新建合成 | `comp.new {name,width:1920,height:1080,frameRate:25,duration:6}` | 确定像素、秒和帧率 |
| 新建背景条 | `layer.newShape {name:"Plate",kind:"rect",size:[1000,190],fill:"#16324f",strokeWidth:0,position:[600,915]}` | 底板范围约为x=100..1100、y=820..1010 |
| 姓名段落框 | `layer.newText {name:"Name",text:"<姓名>",box:[180,830,840,75],size:48,fill:"#ffffff",justify:"left"}` | 给出真实左边缘与文字范围 |
| 职位段落框 | `layer.newText {name:"Role",text:"<职位>",box:[180,915,840,55],size:28,fill:"#ffffff",justify:"left"}` | 姓名与职位左对齐、分行可编辑 |
| 选择对象 | `layer.select {layers:["Plate"]}`，再依次Name、Role | 新合成内名称唯一；已有工程应使用实际返回ID，不能照抄测试ID |
| 设置透明度 | 每层依次`prop.addKey {path:"transform/opacity",time:0,value:0}`、`0.4→100`、`5.4→100`、`5.96→0` | 0.4秒渐入、5秒停留、最后14帧渐退 |

不要把点文本的position当作其左边缘：在实测默认锚点下文字会伸到底板以外。明确的box使用合成坐标，适合固定采访版式。长姓名样例将字号降至36，并重新看最终画面；不能将字符数或保存后的全文当作“文字没有溢出”的证明。中文、特殊字体、连字和很长职位都应独立试排，缺字、截断或重叠时先修版式。

时间单位为秒。25fps的6秒合成含150帧，最后有效帧时间为149/25=5.96秒；不要用第150帧或time=6秒代替最后有效帧。上述采样的渐变是线性透明度，不能称作缓动或滑入动画。

## 原生CLI执行

先用[本次实际命令目录](animated-command-evidence.json)核对结构，再用当前实际CLI的commands目录复核；空工程中enabled=false不代表创建合成后仍不可执行。下例把本技能内计划作为同一run进程内的有序命令，不需要启动另一个Agent，也不依赖同级技能文件：

```python
import json, subprocess
from pathlib import Path
plan = json.loads(Path("<本技能目录>/references/animated-lower-third.json").read_text(encoding="utf-8"))
cli = "<effectcraft-cli实际路径>"
args = [cli, "run", "--empty"]
for step in plan["steps"]:
    args += [step["command"], json.dumps(step["params"], ensure_ascii=False)]
subprocess.run(args + ["--save-as", "<新的工程路径>.ecproj", "--json"], check=True)
```

已有目标路径时先选新名字；不覆盖用户工程。工程保存后用新进程`info --project <工程> --json`核对合成参数和三层名称；再用`get "Interview lower third" Name transform/opacity --time 0.2 --project <工程> --json`检查值为50，另查Role、Plate和其余时刻。姓名原文由`get <合成> Name text/sourceText`读取，不能从图层名推断。

## 同画面MCP

交给 **effectcraft-editor** 技能打开当前任务工作区并等待editor_status就绪；独立安装：`npx skills add full-aigc-skills/effectcraft-skills --skill effectcraft-editor`。在实际command_run schema中传`{"id":"<方法>","params":{…}}`，按计划逐条执行。comp.new的返回合成与各新图层返回ID属于本次会话；执行后inspect检查画面及当前选择，save_project另存工程。独立CLI生成的工程不自动改变已打开的编辑器，不能由CLI通过推断同画面验收。

## 渲染与检查

分别执行`render-frame --project <工程> --time <秒> --max-side 960 --transparent --out <新PNG路径>`，采样0、0.2、0.4、5.4、5.96秒。检查首尾alpha为0，中间态可见但未全显，停留画面一致；背景以外应保留透明，不是烘焙黑底。PNG查看器以黑色显示透明背景不代表文件没有alpha。

停留帧逐字检查姓名职位，文字应位于底板内且左右留白。图像像素检查可以发现越界和缺失，但不能证明未知语言的字形正确。透明叠加交付优先PNG序列：`render --project <工程> --out <新前缀>.png --format png --start 0 --end 6 --fps 25 --resolution half --channels rgba`，然后核对实际文件数与解码alpha；H.264不是透明交付格式。标准样稿已实际导出150帧序列，逐个核对文件编号及RGBA编码，并对0/5/10/135/149帧核对alpha与单帧采样一致；不据此推断任意文字或其他格式。

已验证原生EffectCraft0.10.0 macOS的标准及长姓名两版，49次CLI调用覆盖保存重开、三层文字分配、关键帧与五个采样帧。Windows业务运行39072031958也验证了标准/长姓名及150帧序列。Codex原生宿主在同一内嵌页面逐步创建三层及关键帧，0/10/149帧显示消失/可见/退场；保存重开后仍保持三层，独立CLI读取15个属性时间值及透明采样通过。尚未验证实际人物视频叠加、任意字体语言或其他宿主。本计划保持独立开发候选身份。

GitHub工作流事实及许可记录见[来源](animated-workflow-sources.json)。代码、JSX和模板素材未复制，参数计划与本文原创适配。
