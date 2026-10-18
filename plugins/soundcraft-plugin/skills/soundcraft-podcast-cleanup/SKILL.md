---
name: soundcraft-podcast-cleanup
description: 当用户需要用 soundcraft 完成播客人声整理，涉及口播剪辑、停顿和响度时使用；适用于从素材诊断到可编辑交付的完整任务。
license: Apache-2.0
---

# 播客人声整理


执行具体方法前读取 [Craft 场景命令与参数](references/craft-methods.md)，按其中的对象选择、会话、输入替换和结果检查执行。

## 任务起点

先读取素材，确认交付用途、目标尺寸或时长、修改范围与必要格式。能从任务和素材确定的细节直接采用合理默认值；只询问会改变结果的缺失条件。

需要可见编辑器时交给 **soundcraft-editor** 技能。独立安装：`npx skills add full-aigc-skills/soundcraft-skills --skill soundcraft-editor`。当前新增技能为本地候选，发布前使用本地配套插件，不把此安装命令当作已发布证明。

## 执行步骤

1. 确认轨道与采样率，试听开头、中段和结尾。
2. 移除明确错误段落，保留自然换气，用短交叉淡化消除剪切爆音。
3. 温和均衡和动态处理，先解决低频噪声再调整清晰度。
4. 按发布目标检查响度和峰值，导出试听版。

## 实际单片段的快速执行

1. 调用 `open_session` 后检查返回的 `missing` 必须为空，再用 `inspect_session` 核对音源 loaded、真实轨道名、采样率和片段边界。`.scraft` 的 `Audio Files` 是工程组成部分，不能只搬一个JSON文件；交付自包含工程时使用宿主支持的 `.scraftz`。
2. 从 [片段输入示例](assets/clip-input.json) 填写本次参数，范围必须恰好对应一个已确认片段。例子中的中文轨道、时间和增益不作为默认处理目标。
3. 使用本技能 [输入助手](scripts/podcast_input.py)：`python /mnt/skills/user/soundcraft-podcast-cleanup/scripts/podcast_input.py --input clip-input.json --output recipe.json`。宿主安装在其他位置时，Agent用当前加载技能的实际安装路径替换，不要求用户维护绝对路径。
4. 读取输出 `steps`。同画面编辑时，逐项通过同一会话的 MCP `execute` 传入 `command` 和 `params`；独立CLI则拼成一个进程的独立 argv `--cmd`、`方法ID=JSON`。不要另开CLI进程并声称Web画面已同步。
5. 核对片段 gain_db、fade_in/out 与未选中片段，再另存新工程，解码导出检查采样率/位深/时长，最后试听。当前助手只做选中整片段增益、两端淡变和指定区间混音，不执行剪除、EQ、降噪或LUFS归一化。

输出配方拒绝覆盖，但原生混音器仍可能覆盖同名WAV；执行前确认导出目标不存在。效果目录查询仅是查询，不能在报告中列作已处理效果。

## 工具落地

用 open_session/new_session 管理会话；import_audio 导入、inspect_session 检查，其他编辑查实时工具；save_session 保存工程，bounce_mix 输出音频。

先读取实际工具 schema，再填写参数；对象或文档 ID 使用返回值。查询到的命令必须在当前后端可用。保存前选择新输出路径，保留输入。需要的算法、格式或命令不存在时说明缺口，不能用相近名称冒充。

## 结果检查

- 不把底噪处理成金属水声。
- 剪辑后语义连贯，无突然静音和削波。
- 交付会话工程、混音与处理说明。

对照用户目标检查实际内容，而不只检查进程退出码。局部编辑查看局部细节，版式任务查看整页，时间媒体查看起止与关键段。异常结果先检查当前工程，避免重复执行不可逆操作。

## 交付

返回可编辑工程、实际派生文件和简短说明：做了哪些修改、哪些步骤因当前能力未执行、需要用户判断的内容。只列真实存在且已经检查的文件。若用户随后返工，读取本次源工程并局部修改，保留已接受的内容。
