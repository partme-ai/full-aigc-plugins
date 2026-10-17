# soundcraft 场景步骤

按当前输入先测量声道、时长或完整源图坐标。每条为独立任务；不要对已有工程无条件初始化或导入示例。

## voice-headroom：配音剪辑保留混音余量

输入：Voice示例为单声道；实际先probe输入声道并将track.new的format设为mono或stereo，多声道超出当前手册范围时停止。有合法源录音；先probe采样率、声道和时长，示例为4秒。

| 顺序与目的 | 命令 | 参数 |
| --- | --- | --- |
| 1. 仅在新建副本任务中创建48kHz空会话 | `session.new` | `{"name":"Audio work copy","sample_rate":48000,"bit_depth":24,"template":"blank"}` |
| 2. 建立已知名称的单声道人声轨 | `track.new` | `{"name":"Voice","format":"mono","kind":"audio"}` |
| 3. 把源音频放到指定轨道零点，保持原文件 | `file.import_audio` | `{"path":"input.wav","track":"Voice","new_tracks":false,"at":{"seconds":0}}` |
| 4. 选择导入的整段片段与轨道 | `edit.select_all` | `{}` |
| 5. 以绝对片段增益降低6dB，保持可编辑而非重复叠加 | `clip.gain` | `{"db":-6}` |
| 6. 导出新文件，不覆盖源音频；区间秒数按实际片段重算 | `file.bounce_mix` | `{"path":"result.wav","format":"wav","bit_depth":16,"start":{"seconds":0},"end":{"seconds":4},"normalize":false,"dither":false}` |

检查：时长、内容与原始剪辑一致；相对未处理混音的峰值约下降6dB；重新打开工程后增益仍在。

边界：这是电平整理，不是压缩、降噪或LUFS归一；真实语音必须试听尾音。

## peak-normalized-preview：单片段峰值标准化预览

输入：Voice示例为单声道；实际先probe输入声道并将track.new的format设为mono或stereo，多声道超出当前手册范围时停止。输入未剪切，峰值目标由用途提供；不要把峰值等同感知响度。

| 顺序与目的 | 命令 | 参数 |
| --- | --- | --- |
| 1. 仅在新建副本任务中创建48kHz空会话 | `session.new` | `{"name":"Audio work copy","sample_rate":48000,"bit_depth":24,"template":"blank"}` |
| 2. 建立已知名称的单声道人声轨 | `track.new` | `{"name":"Voice","format":"mono","kind":"audio"}` |
| 3. 把源音频放到指定轨道零点，保持原文件 | `file.import_audio` | `{"path":"input.wav","track":"Voice","new_tracks":false,"at":{"seconds":0}}` |
| 4. 选择导入的整段片段与轨道 | `edit.select_all` | `{}` |
| 5. 将选中片段峰值对齐到-3dBFS，生成可回退的新音源 | `audiosuite.process` | `{"process":"normalize","params":{"target_db":-3}}` |
| 6. 导出新文件，不覆盖源音频；区间秒数按实际片段重算 | `file.bounce_mix` | `{"path":"result.wav","format":"wav","bit_depth":16,"start":{"seconds":0},"end":{"seconds":4},"normalize":false,"dither":false}` |

检查：片段输出相对原峰值达到目标增益；时长不变且无削波；源文件哈希不变。

边界：主总线声像定律会影响每个输出声道的峰值；此例不是ITU/EBU响度达标流程。

## voice-edge-fades：配音切口的短淡入淡出

输入：Voice示例为单声道；实际先probe输入声道并将track.new的format设为mono或stereo，多声道超出当前手册范围时停止。切口两端无需保留尖锐瞬态；示例片段4秒，头尾各100ms。

| 顺序与目的 | 命令 | 参数 |
| --- | --- | --- |
| 1. 仅在新建副本任务中创建48kHz空会话 | `session.new` | `{"name":"Audio work copy","sample_rate":48000,"bit_depth":24,"template":"blank"}` |
| 2. 建立已知名称的单声道人声轨 | `track.new` | `{"name":"Voice","format":"mono","kind":"audio"}` |
| 3. 把源音频放到指定轨道零点，保持原文件 | `file.import_audio` | `{"path":"input.wav","track":"Voice","new_tracks":false,"at":{"seconds":0}}` |
| 4. 选择导入的整段片段与轨道 | `edit.select_all` | `{}` |
| 5. 仅在片段起点建立100ms线性淡入 | `edit.fades_create` | `{"tracks":["Voice"],"start":{"seconds":0},"end":{"seconds":0.1},"shape":"linear"}` |
| 6. 在片段尾部建立100ms线性淡出 | `edit.fades_create` | `{"tracks":["Voice"],"start":{"seconds":3.9},"end":{"seconds":4},"shape":"linear"}` |
| 7. 导出新文件，不覆盖源音频；区间秒数按实际片段重算 | `file.bounce_mix` | `{"path":"result.wav","format":"wav","bit_depth":16,"start":{"seconds":0},"end":{"seconds":4},"normalize":false,"dither":false}` |

检查：头尾波形渐入渐出而非突切；中间内容基本不变；首辅音、呼吸和尾音未被吞掉。

边界：淡变区间必须据真实录音定位；不能把头尾时刻原样用于任意录音。

## interview-excerpt：从长采访导出指定引用段

输入：Voice示例为单声道；实际先probe输入声道并将track.new的format设为mono或stereo，多声道超出当前手册范围时停止。已确认引用的起止时间并有使用权；示例从1秒到3秒。

| 顺序与目的 | 命令 | 参数 |
| --- | --- | --- |
| 1. 仅在新建副本任务中创建48kHz空会话 | `session.new` | `{"name":"Audio work copy","sample_rate":48000,"bit_depth":24,"template":"blank"}` |
| 2. 建立已知名称的单声道人声轨 | `track.new` | `{"name":"Voice","format":"mono","kind":"audio"}` |
| 3. 把源音频放到指定轨道零点，保持原文件 | `file.import_audio` | `{"path":"input.wav","track":"Voice","new_tracks":false,"at":{"seconds":0}}` |
| 4. 选择导入的整段片段与轨道 | `edit.select_all` | `{}` |
| 5. 明确引用选区，保留源工程完整片段 | `edit.select` | `{"tracks":["Voice"],"start":{"seconds":1},"end":{"seconds":3}}` |
| 6. 导出新文件，不覆盖源音频；区间秒数按实际片段重算 | `file.bounce_mix` | `{"path":"result.wav","format":"wav","bit_depth":16,"start":{"seconds":1},"end":{"seconds":3},"normalize":false,"dither":false}` |

检查：导出时长2秒；导出的样本对应原录音1到3秒；原会话保留完整4秒录音。

边界：切口是否落在词句边界需试听；不把2秒样例当任意任务时长。

## two-track-stems：人声与背景素材分轨交付

输入：仅在专用两轨副本会话执行；示例Voice为mono，Bed为stereo。实际先probe两个输入声道，按其结果建轨，不静默降为mono。

| 顺序与目的 | 命令 | 参数 |
| --- | --- | --- |
| 1. 仅在新建副本任务中创建48kHz空会话 | `session.new` | `{"name":"Audio work copy","sample_rate":48000,"bit_depth":24,"template":"blank"}` |
| 2. 建立已知名称的单声道人声轨 | `track.new` | `{"name":"Voice","format":"mono","kind":"audio"}` |
| 3. 把源音频放到指定轨道零点，保持原文件 | `file.import_audio` | `{"path":"input.wav","track":"Voice","new_tracks":false,"at":{"seconds":0}}` |
| 4. 选择导入的整段片段与轨道 | `edit.select_all` | `{}` |
| 5. 建立独立背景轨 | `track.new` | `{"name":"Bed","format":"stereo","kind":"audio"}` |
| 6. 将背景素材放在零点，不改变人声轨 | `file.import_audio` | `{"path":"bed.wav","track":"Bed","new_tracks":false,"at":{"seconds":0}}` |
| 7. 导出两个音频轨的独立文件，统一起止区间 | `file.bounce_stems` | `{"dir":"stems","format":"wav","bit_depth":16,"start":{"seconds":0},"end":{"seconds":4}}` |

检查：输出轨名集合恰为Voice与Bed，两个stem均为4秒；Bed左右保留不同内容，不能静默变单声道；原始输入文件哈希保持。

边界：bounce_stems导出所有未静音活动音轨，不受编辑选区限制。此例仅用于专用两轨会话；已有工程先在副本中核实所有活动轨道，不能只选择两轨就假定仅导出两轨。当前16位stem编码会抖动，样本比较需允许量化噪声。

## reverse-transition：环境声倒放转场素材

输入：Voice示例为单声道；实际先probe输入声道并将track.new的format设为mono或stereo，多声道超出当前手册范围时停止。有授权的环境声素材；创建独立效果版，不覆盖原录音。

| 顺序与目的 | 命令 | 参数 |
| --- | --- | --- |
| 1. 仅在新建副本任务中创建48kHz空会话 | `session.new` | `{"name":"Audio work copy","sample_rate":48000,"bit_depth":24,"template":"blank"}` |
| 2. 建立已知名称的单声道人声轨 | `track.new` | `{"name":"Voice","format":"mono","kind":"audio"}` |
| 3. 把源音频放到指定轨道零点，保持原文件 | `file.import_audio` | `{"path":"input.wav","track":"Voice","new_tracks":false,"at":{"seconds":0}}` |
| 4. 选择导入的整段片段与轨道 | `edit.select_all` | `{}` |
| 5. 倒放选中片段，保持其可追溯来源 | `audiosuite.process` | `{"process":"reverse"}` |
| 6. 导出新文件，不覆盖源音频；区间秒数按实际片段重算 | `file.bounce_mix` | `{"path":"result.wav","format":"wav","bit_depth":16,"start":{"seconds":0},"end":{"seconds":4},"normalize":false,"dither":false}` |

检查：片段时长不变；导出样本时间顺序与基准相反；试听接入点是否需要淡变。

边界：不要用倒放掩盖未经确认的语音内容；需要过渡淡变时另用切口流程。

## dc-offset-cleanup：录音直流偏置清理副本

输入：Voice示例为单声道；实际先probe输入声道并将track.new的format设为mono或stereo，多声道超出当前手册范围时停止。测量发现波形基线偏移；不能把低频乐器声音误当直流偏置。

| 顺序与目的 | 命令 | 参数 |
| --- | --- | --- |
| 1. 仅在新建副本任务中创建48kHz空会话 | `session.new` | `{"name":"Audio work copy","sample_rate":48000,"bit_depth":24,"template":"blank"}` |
| 2. 建立已知名称的单声道人声轨 | `track.new` | `{"name":"Voice","format":"mono","kind":"audio"}` |
| 3. 把源音频放到指定轨道零点，保持原文件 | `file.import_audio` | `{"path":"input.wav","track":"Voice","new_tracks":false,"at":{"seconds":0}}` |
| 4. 选择导入的整段片段与轨道 | `edit.select_all` | `{}` |
| 5. 运行已核实的直流偏置移除处理 | `audiosuite.process` | `{"process":"dc_offset_removal"}` |
| 6. 导出新文件，不覆盖源音频；区间秒数按实际片段重算 | `file.bounce_mix` | `{"path":"result.wav","format":"wav","bit_depth":16,"start":{"seconds":0},"end":{"seconds":4},"normalize":false,"dither":false}` |

检查：稳定段样本均值更接近0；保留音高与时长；没有误称底噪已被移除。

边界：高通/去直流的启动瞬态需试听；不等于降噪、去嗡声或修复削波。

## polarity-diagnostic-copy：制作极性反转诊断副本

输入：Voice示例为单声道；实际先probe输入声道并将track.new的format设为mono或stereo，多声道超出当前手册范围时停止。用于与同源等时信号作相消诊断；不自动改变正式混音。

| 顺序与目的 | 命令 | 参数 |
| --- | --- | --- |
| 1. 仅在新建副本任务中创建48kHz空会话 | `session.new` | `{"name":"Audio work copy","sample_rate":48000,"bit_depth":24,"template":"blank"}` |
| 2. 建立已知名称的单声道人声轨 | `track.new` | `{"name":"Voice","format":"mono","kind":"audio"}` |
| 3. 把源音频放到指定轨道零点，保持原文件 | `file.import_audio` | `{"path":"input.wav","track":"Voice","new_tracks":false,"at":{"seconds":0}}` |
| 4. 选择导入的整段片段与轨道 | `edit.select_all` | `{}` |
| 5. 仅在副本中反转样本正负极性 | `audiosuite.process` | `{"process":"invert"}` |
| 6. 导出新文件，不覆盖源音频；区间秒数按实际片段重算 | `file.bounce_mix` | `{"path":"result.wav","format":"wav","bit_depth":16,"start":{"seconds":0},"end":{"seconds":4},"normalize":false,"dither":false}` |

检查：输出样本约等于基准样本取负；时长和峰值绝对值保持；文件名注明诊断用途。

边界：极性反转不是时间对齐；若信号有延迟或处理差异，不能期待完全相消。

