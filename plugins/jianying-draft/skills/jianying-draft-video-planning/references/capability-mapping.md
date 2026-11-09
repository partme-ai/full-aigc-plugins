# 技能、原子操作与人工职责

## 分层

| 层 | 职责 | 证据 |
|---|---|---|
| 规划技能 | 场景、来源、素材、故事、剪法 | plan |
| 插件 Harness | 选择、门禁、任务状态、批准、追踪 | 审计记录 |
| Rust CLI | 公开 capability 对应的媒体/草稿原子操作 | 命令输出及产物 |
| 人工/外部服务 | 内容理解、事实、节拍、多机同步、图表 | 独立记录，不能假装 CLI 提供 |

## 已观察的二进制

[快照](cli-capability-snapshot.json) 来自 v1.6.13 真实发布二进制的 capabilities 输出。它只验证 ID 引用和当时声明，不等于108个场景实机通过。运行时必须重新握手。

## 通用公开入口

`jianying capabilities --json` 获取能力；`jianying doctor --json` 诊断环境。
已确认的 Job 交给 `jianying job run --help` 所声明参数执行，agent 不凭记忆猜参数。此库不依赖 Rust 源码，不要求用户安装 Cargo。

Recipe 的 required_capabilities 是选定结构草稿步骤的最小集合；选用的技能可能还包含本次不需要的功能，不把整个技能的所有能力做全局硬门禁。

## 可选功能

- ASR：media.asr_whisper_cpp + media.asr_ledger；另需已安装模型和运行许可。
- TTS：media.tts_local；不是所有本地/云厂商都已支持。media.tts_provider 仍不可一概称就绪。
- 转场：timeline.transition；资源 ID 与授权单独查询。
- 自动字幕验证：captions.verify；快照是 partial，人工校对不冒充机器验证。
- 原生导出：render.native 以及 runtime.profile/runtime.status；快照不满足 supported，需明确阻断。

## 非原子能力

不宣称 CLI 自动完成语义挑片、节拍检测、多机音频同步、人物/物种识别、广告效果预测、图表计算、事实核查、上网发布。人或外部工具先完成并留下证据，CLI 只接收已经确定的操作与素材。
