# 3–2–1开场倒数：方法与参数

0–1秒3、1–2秒2、2–3秒1、3–4秒START；逐个边界帧检查没有重叠、空白或重复数，文字可编辑。

## 输入与选择

先确认批准文案/名单、分辨率、帧率、开始点、停留和交付格式。下面是新工程参数模板；不覆盖既有工程，不凭空补充人名、职务或章节事实。详情见[步骤](craft-steps.json)与[实际命令观察](craft-command-evidence.json)。

| 操作目的 | CLI命令 | 参数 |
| --- | --- | --- |
| 1. 新建专用1920×1080、25fps合成 | `comp.new` | `{"name": "CountdownIntro", "width": 1920, "height": 1080, "frameRate": 25, "duration": 4}` |
| 2. 建立独立可编辑文字层Three | `layer.newText` | `{"name": "Three", "text": "3", "position": [960, 610], "size": 180, "justify": "center", "fill": "#ffffff"}` |
| 3. 仅让该数字出现在独占的一秒区间 | `layer.timing` | `{"layers": ["Three"], "in": 0, "out": 1}` |
| 4. 建立独立可编辑文字层Two | `layer.newText` | `{"name": "Two", "text": "2", "position": [960, 610], "size": 180, "justify": "center", "fill": "#ffffff"}` |
| 5. 仅让该数字出现在独占的一秒区间 | `layer.timing` | `{"layers": ["Two"], "in": 1, "out": 2}` |
| 6. 建立独立可编辑文字层One | `layer.newText` | `{"name": "One", "text": "1", "position": [960, 610], "size": 180, "justify": "center", "fill": "#ffffff"}` |
| 7. 仅让该数字出现在独占的一秒区间 | `layer.timing` | `{"layers": ["One"], "in": 2, "out": 3}` |
| 8. 建立独立可编辑文字层Start | `layer.newText` | `{"name": "Start", "text": "START", "position": [960, 610], "size": 120, "justify": "center", "fill": "#ffffff"}` |
| 9. 仅让该数字出现在独占的一秒区间 | `layer.timing` | `{"layers": ["Start"], "in": 3, "out": 4}` |

## 同会话MCP

先读取当前`command_run` schema和`editor_status`；已打开编辑器时使用它所属的会话。逐行调用`command_run {"id":"命令ID","params":{参数}}`，例如第一步是`{"id":"comp.new","params":{"name": "CountdownIntro", "width": 1920, "height": 1080, "frameRate": 25, "duration": 4}}`。创建层后核对返回ID、当前合成和唯一名称，再执行显式layer关键帧。`layer.timing.layers`取实际名称/ID；`in/out`为合成秒，出点需检查实际相邻帧。此映射来自0.10.0原生目录；Web候选与原生不同，必须查当前目录，缺少方法时报告缺口。

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

先替换配方中的占位内容；只对本次可信技能配方使用。已存在输出改用新文件名。用`info --project output.ecproj --json`核对保存；再用`get <合成> <层> transform/position --time <秒> --project output.ecproj --json`或opacity核对采样。渲染：`effectcraft-cli render-frame --project output.ecproj --comp CountdownIntro --time <有效合成秒> --max-side 480 --transparent --out preview.png`。完整PNG序列：`render --project output.ecproj --comp CountdownIntro --start 0 --end 4 --fps 25 --format png --channels rgba --resolution quarter --out frames.png`，核对实际帧数、首中末及重新解码，不能只看静帧。CLI文件任务不会自动更新另一个Web会话。

## 检查与边界

0–1秒3、1–2秒2、2–3秒1、3–4秒START；逐个边界帧检查没有重叠、空白或重复数，文字可编辑。

这是视觉倒数，不是现实世界准确计时器。无自动音效或圆环进度；用户要求音效另行对齐，不假称已音画同步。

时间参数是秒；25fps时最后有效帧为duration−0.04。对输出工程重开后检查所有文字、图层时长和关键帧；实际成片必须播放检查截字、阅读时长、滚动闪烁和拼接点。保存可编辑EC工程与约定导出，两者分开验证；PNG有透明通道不代表每个宿主混合正确。

[固定来源与许可](workflow-sources.json)仅证明阅读来源。技术合成样本、真实媒体质量、MCP实际业务和编辑器同步分别报告，不互相代替。
