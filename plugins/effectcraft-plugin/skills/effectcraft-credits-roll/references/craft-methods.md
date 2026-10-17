# 片尾滚动署名：方法与参数

独立角色/姓名层以相同速度向上滚动；确认名单、角色对应与顺序，首帧和最后有效帧为空，文本中段可读且完整离场。

## 输入与选择

先确认批准文案/名单、分辨率、帧率、开始点、停留和交付格式。下面是新工程参数模板；不覆盖既有工程，不凭空补充人名、职务或章节事实。详情见[步骤](craft-steps.json)与[实际命令观察](craft-command-evidence.json)。

| 操作目的 | CLI命令 | 参数 |
| --- | --- | --- |
| 1. 新建专用1920×1080、25fps合成 | `comp.new` | `{"name": "CreditsRoll", "width": 1920, "height": 1080, "frameRate": 25, "duration": 12}` |
| 2. 建立独立可编辑文字层Credit1 | `layer.newText` | `{"name": "Credit1", "text": "Direction", "position": [960, 1180], "size": 48, "justify": "center", "fill": "#ffffff"}` |
| 3. 按合成秒设置Credit1的transform/position | `prop.addKey` | `{"layer": "Credit1", "path": "transform/position", "time": 0, "timeBase": "comp", "value": [960, 1180, 0]}` |
| 4. 按合成秒设置Credit1的transform/position | `prop.addKey` | `{"layer": "Credit1", "path": "transform/position", "time": 12, "timeBase": "comp", "value": [960, -850, 0]}` |
| 5. 建立独立可编辑文字层Credit2 | `layer.newText` | `{"name": "Credit2", "text": "Approved Director", "position": [960, 1310], "size": 60, "justify": "center", "fill": "#ffffff"}` |
| 6. 按合成秒设置Credit2的transform/position | `prop.addKey` | `{"layer": "Credit2", "path": "transform/position", "time": 0, "timeBase": "comp", "value": [960, 1310, 0]}` |
| 7. 按合成秒设置Credit2的transform/position | `prop.addKey` | `{"layer": "Credit2", "path": "transform/position", "time": 12, "timeBase": "comp", "value": [960, -720, 0]}` |
| 8. 建立独立可编辑文字层Credit3 | `layer.newText` | `{"name": "Credit3", "text": "Camera", "position": [960, 1440], "size": 48, "justify": "center", "fill": "#ffffff"}` |
| 9. 按合成秒设置Credit3的transform/position | `prop.addKey` | `{"layer": "Credit3", "path": "transform/position", "time": 0, "timeBase": "comp", "value": [960, 1440, 0]}` |
| 10. 按合成秒设置Credit3的transform/position | `prop.addKey` | `{"layer": "Credit3", "path": "transform/position", "time": 12, "timeBase": "comp", "value": [960, -590, 0]}` |
| 11. 建立独立可编辑文字层Credit4 | `layer.newText` | `{"name": "Credit4", "text": "Approved Camera", "position": [960, 1570], "size": 60, "justify": "center", "fill": "#ffffff"}` |
| 12. 按合成秒设置Credit4的transform/position | `prop.addKey` | `{"layer": "Credit4", "path": "transform/position", "time": 0, "timeBase": "comp", "value": [960, 1570, 0]}` |
| 13. 按合成秒设置Credit4的transform/position | `prop.addKey` | `{"layer": "Credit4", "path": "transform/position", "time": 12, "timeBase": "comp", "value": [960, -460, 0]}` |
| 14. 建立独立可编辑文字层Credit5 | `layer.newText` | `{"name": "Credit5", "text": "Sound", "position": [960, 1700], "size": 48, "justify": "center", "fill": "#ffffff"}` |
| 15. 按合成秒设置Credit5的transform/position | `prop.addKey` | `{"layer": "Credit5", "path": "transform/position", "time": 0, "timeBase": "comp", "value": [960, 1700, 0]}` |
| 16. 按合成秒设置Credit5的transform/position | `prop.addKey` | `{"layer": "Credit5", "path": "transform/position", "time": 12, "timeBase": "comp", "value": [960, -330, 0]}` |
| 17. 建立独立可编辑文字层Credit6 | `layer.newText` | `{"name": "Credit6", "text": "Approved Sound", "position": [960, 1830], "size": 60, "justify": "center", "fill": "#ffffff"}` |
| 18. 按合成秒设置Credit6的transform/position | `prop.addKey` | `{"layer": "Credit6", "path": "transform/position", "time": 0, "timeBase": "comp", "value": [960, 1830, 0]}` |
| 19. 按合成秒设置Credit6的transform/position | `prop.addKey` | `{"layer": "Credit6", "path": "transform/position", "time": 12, "timeBase": "comp", "value": [960, -200, 0]}` |

## 同会话MCP

先读取当前`command_run` schema和`editor_status`；已打开编辑器时使用它所属的会话。逐行调用`command_run {"id":"命令ID","params":{参数}}`，例如第一步是`{"id":"comp.new","params":{"name": "CreditsRoll", "width": 1920, "height": 1080, "frameRate": 25, "duration": 12}}`。创建层后核对返回ID、当前合成和唯一名称，再执行显式layer关键帧。`layer.timing.layers`取实际名称/ID；`in/out`为合成秒，出点需检查实际相邻帧。此映射来自0.10.0原生目录；Web候选与原生不同，必须查当前目录，缺少方法时报告缺口。

## 原生CLI

将本技能recipe中的全部步骤保存在同一次`run --empty`调用，不拆为多个新进程。可用下面Python组织argv（只传递原生命令，不执行额外业务）：

```python
import json, subprocess
from pathlib import Path
recipe = json.loads(Path("<本技能目录>/references/craft-steps.json").read_text(encoding="utf-8"))
argv = ["<已验证的effectcraft-cli路径>", "run", "--empty"]
for item in recipe["steps"]:
    argv.extend([item["command"], json.dumps(item["params"], ensure_ascii=False)])
subprocess.run(argv + ["--save-as", "output.ecproj"], check=True)
```

先替换配方中的占位内容；只对本次可信技能配方使用。已存在输出改用新文件名。用`info --project output.ecproj --json`核对保存；再用`get <合成> <层> transform/position --time <秒> --project output.ecproj --json`或opacity核对采样。渲染：`effectcraft-cli render-frame --project output.ecproj --comp CreditsRoll --time <有效合成秒> --max-side 480 --transparent --out preview.png`。完整PNG序列：`render --project output.ecproj --comp CreditsRoll --start 0 --end 12 --fps 25 --format png --channels rgba --resolution quarter --out frames.png`，核对实际帧数、首中末及重新解码，不能只看静帧。CLI文件任务不会自动更新另一个Web会话。

## 检查与边界

独立角色/姓名层以相同速度向上滚动；确认名单、角色对应与顺序，首帧和最后有效帧为空，文本中段可读且完整离场。

Direction/Camera/Sound及Approved字段全是占位例子，必须替换为确认名单。六行12秒只是演示；名单加长或改变分辨率后重新按总高度/可读速度计算时长和离场坐标，不能只复用12秒。

时间参数是秒；25fps时最后有效帧为duration−0.04。对输出工程重开后检查所有文字、图层时长和关键帧；实际成片必须播放检查截字、阅读时长、滚动闪烁和拼接点。保存可编辑EC工程与约定导出，两者分开验证；PNG有透明通道不代表每个宿主混合正确。

[固定来源与许可](workflow-sources.json)仅证明阅读来源。技术合成样本、真实媒体质量、MCP实际业务和编辑器同步分别报告，不互相代替。
