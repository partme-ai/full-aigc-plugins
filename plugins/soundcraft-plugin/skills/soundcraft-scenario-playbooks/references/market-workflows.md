# 从技能商店适配的场景方法

以下内容是基于已阅读技能的原创 Craft 指导。沿用现有配方的实际命令；这里补充任务判断和结果检查，不将同一配方再计为新增场景。商店提供发现入口，原技能使用的软件、服务和依赖不会随本插件安装。

示例步骤是参数模板，不能直接作为通用执行脚本。先取当前会话的文档、图层、片段或故事ID，解析所有引用，再按实际工具schema执行；尺寸、坐标、路径和文本按本次任务调整。已打开编辑器时使用同一个MCP会话；独立CLI文件编辑不能证明界面同步。

## 先处理切口再做全局音量

参考：[hkuds/cli-anything/cli-anything-audacity](https://github.com/hkuds/cli-anything/blob/34f519533bc175d2fe287ab8316b0dd99bb9cc43/skills/cli-anything-audacity/SKILL.md)。

监听片段首尾是否有切口爆音或截断音节，再对边缘施加短淡变；淡变范围按当前录音调整，不能让字头消失。

原配方：`voice-edge-fades`。输入与边界：Voice示例为单声道；实际先probe输入声道并将track.new的format设为mono或stereo，多声道超出当前手册范围时停止。切口两端无需保留尖锐瞬态；示例片段4秒，头尾各100ms。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `session.new` | `{"name":"Audio work copy","sample_rate":48000,"bit_depth":24,"template":"blank"}` |
| 2 | `track.new` | `{"name":"Voice","format":"mono","kind":"audio"}` |
| 3 | `file.import_audio` | `{"path":"input.wav","track":"Voice","new_tracks":false,"at":{"seconds":0}}` |
| 4 | `edit.select_all` | `{}` |
| 5 | `edit.fades_create` | `{"tracks":["Voice"],"start":{"seconds":0},"end":{"seconds":0.1},"shape":"linear"}` |
| 6 | `edit.fades_create` | `{"tracks":["Voice"],"start":{"seconds":3.9},"end":{"seconds":4},"shape":"linear"}` |
| 7 | `file.bounce_mix` | `{"path":"result.wav","format":"wav","bit_depth":16,"start":{"seconds":0},"end":{"seconds":4},"normalize":false,"dither":false}` |

检查：耳听切口自然，时长与声道保留，源录音未覆盖。

能力边界：峰值检查不能代替监听；不把短淡变称为背景降噪。

原配方结果检查：["头尾波形渐入渐出而非突切", "中间内容基本不变", "首辅音、呼吸和尾音未被吞掉"]

原配方限制：淡变区间必须据真实录音定位；不能把头尾时刻原样用于任意录音。

## 播客章节对应真实音频

参考：[skillhub:podcast-workflow](https://api.skillhub.cn/api/v1/download?slug=podcast-workflow)。

从已核对的章节时间定位采访摘录，截取前后保留足够上下文。输出段与章节标题对应；章节笔记使用摘录实际起点，避免把原片时间误当短片时间。

原配方：`interview-excerpt`。输入与边界：Voice示例为单声道；实际先probe输入声道并将track.new的format设为mono或stereo，多声道超出当前手册范围时停止。已确认引用的起止时间并有使用权；示例从1秒到3秒。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `session.new` | `{"name":"Audio work copy","sample_rate":48000,"bit_depth":24,"template":"blank"}` |
| 2 | `track.new` | `{"name":"Voice","format":"mono","kind":"audio"}` |
| 3 | `file.import_audio` | `{"path":"input.wav","track":"Voice","new_tracks":false,"at":{"seconds":0}}` |
| 4 | `edit.select_all` | `{}` |
| 5 | `edit.select` | `{"tracks":["Voice"],"start":{"seconds":1},"end":{"seconds":3}}` |
| 6 | `file.bounce_mix` | `{"path":"result.wav","format":"wav","bit_depth":16,"start":{"seconds":1},"end":{"seconds":3},"normalize":false,"dither":false}` |

检查：摘录时长、首尾语义和章节时间对应，回听确认无截词。

能力边界：本流程不自动下载播客、转录或发布社交内容。

原配方结果检查：["导出时长2秒", "导出的样本对应原录音1到3秒", "原会话保留完整4秒录音"]

原配方限制：切口是否落在词句边界需试听；不把2秒样例当任意任务时长。

## 保留独立人声与背景素材

参考：[hkuds/cli-anything/cli-anything-audacity](https://github.com/hkuds/cli-anything/blob/34f519533bc175d2fe287ab8316b0dd99bb9cc43/skills/cli-anything-audacity/SKILL.md)；[calesthio/generative-media-skills/talking-head-podcast-recut](https://github.com/calesthio/generative-media-skills/blob/8c85352d5d75d4dcbe58480bd138e37b9742bab1/skills/production/content-formats/talking-head-podcast-recut/SKILL.md)。

使用真实分轨来源，先核对对齐、采样率和声道，再分别导出。把分轨与混音预览分开命名；重开后再次检查导出的开始位置和持续时间。

原配方：`two-track-stems`。输入与边界：仅在专用两轨副本会话执行；示例Voice为mono，Bed为stereo。实际先probe两个输入声道，按其结果建轨，不静默降为mono。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `session.new` | `{"name":"Audio work copy","sample_rate":48000,"bit_depth":24,"template":"blank"}` |
| 2 | `track.new` | `{"name":"Voice","format":"mono","kind":"audio"}` |
| 3 | `file.import_audio` | `{"path":"input.wav","track":"Voice","new_tracks":false,"at":{"seconds":0}}` |
| 4 | `edit.select_all` | `{}` |
| 5 | `track.new` | `{"name":"Bed","format":"stereo","kind":"audio"}` |
| 6 | `file.import_audio` | `{"path":"bed.wav","track":"Bed","new_tracks":false,"at":{"seconds":0}}` |
| 7 | `file.bounce_stems` | `{"dir":"stems","format":"wav","bit_depth":16,"start":{"seconds":0},"end":{"seconds":4}}` |

检查：独立文件确实对应各自素材，混音余量合理。

能力边界：分轨导出不等于从混合音频中自动分离人声，也不等于LUFS达标。

原配方结果检查：["输出轨名集合恰为Voice与Bed，两个stem均为4秒", "Bed左右保留不同内容，不能静默变单声道", "原始输入文件哈希保持"]

原配方限制：bounce_stems导出所有未静音活动音轨，不受编辑选区限制。此例仅用于专用两轨会话；已有工程先在副本中核实所有活动轨道，不能只选择两轨就假定仅导出两轨。当前16位stem编码会抖动，样本比较需允许量化噪声。

## 版本与执行

执行包装沿用本技能主文件。先核对采样率、声道和实际片段范围；峰值归一化不等于响度标准化，分轨导出不等于从混音自动分离。 保存到未占用路径并重开，按实际产物检查；本轮文档适配未新增宿主或真实媒体验收。

本技能内的[商店来源与参数记录](market-adaptations.json)记录版本、内容哈希和观察方法；没有分发第三方脚本或正文。
