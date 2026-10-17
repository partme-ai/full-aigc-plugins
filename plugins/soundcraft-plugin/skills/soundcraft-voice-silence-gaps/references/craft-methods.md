# 实际方法与参数

先查询 `commands` / `describe`，或同会话MCP的实际schema。输入为已打开并检查的会话；新文件任务才使用 `session.new`、`track.new`、`file.import_audio` 准备源轨。先保存工作副本。

`$source.track` 来自目标轨真实ID，`$source.clip` 来自该轨实际活动playlist的目标片段ID。`capture` 不是命令字段。已有会话先确认目标轨ID和活动playlist，重名时不靠猜名称。

| 顺序与目的 | 方法 | 参数模板 |
| --- | --- | --- |
| 1. 检查会话采样率及目标轨道 | `session.inspect` | `{"detail":"full"}` |
| 2. 显式选择需要检查的0至4秒；替换实际范围 | `edit.select` | `{"tracks":["$source.track"],"start":{"seconds":0},"end":{"seconds":4}}` |
| 3. 以阈值检测长低电平区并保留呼吸边缘余量 | `edit.strip_silence` | `{"threshold_db":-40,"min_length_ms":100,"pad_before_ms":10,"pad_after_ms":20}` |
| 4. 核对保留片段的start与source offset，不应将对白向前挪动 | `session.inspect` | `{"detail":"full"}` |
| 5. 输出明确时长的24位审核混音 | `file.bounce_mix` | `{"path":"gaps-review.wav","format":"wav","bit_depth":24,"start":{"seconds":0},"end":{"seconds":4},"normalize":false,"dither":false}` |

## CLI与MCP

CLI以argv传参：`soundcraft-cli run --in input.scraft --cmd 方法ID=JSON … --save output.scraft`。每个方法ID和JSON组成一个argv，不拼接用户文本为shell代码。需要重新查询ID时先保存阶段文件，再读取实际会话并绑定后续参数。

可见编辑器ready后使用该服务的 `execute`，例如：

```json
{"command":"session.inspect","params":{"detail":"full"}}
```

所有编辑和保存都保持同一MCP实例。保存用实际schema中的 `save_session`，新输出相对工作区；独立CLI进程不会同步改动现有页面。不要把JSON模板中的变量、capture或用途字段送给原生方法。

保存后重新打开工程，解码审核WAV，核对通道、帧数、目标区及非目标区；原会话与源音频摘要应不变。样例使用48kHz/24位PCM、关闭normalize与dither以便比较，不能当作所有平台的音频交付标准。任何处理后都要听实际词首尾、接缝和呼吸声。

## 宿主实际保存路径

当前内嵌运行时请求save_session的.scraft路径，实际written回执可能返回.scraftz打包工程（内含会话和Audio Files）。以实际回执路径核对交付，重开调用open_session传实际.scraftz路径；不要声称请求的.scraft文件已单独写入。CLI文件任务仍可保存.scraft并保留其关联音频目录。当前这两种路径已分别回读；不把纯JSON会话当成自包含音频包。
