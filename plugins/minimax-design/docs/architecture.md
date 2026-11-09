# 架构与约定

## 分层

```text
skills/                     技能层（LLM 决策面）
  minimax-design-use          路由 + 第 0 步能力预检（鉴权缺失 → 可操作指引）
  minimax-video-generation    t2v / i2v / 白模首尾帧工作流（调 scripts/minimax_video.py）
  minimax-multimodal-toolkit  vendor 自 full-aigc-skills/minimax-skills（mmx CLI）
  minimax-music-gen           vendor 同上
  minimax-music-playlist      vendor 同上
scripts/minimax_video.py    确定性客户端：check / t2v / i2v / query（异步任务+断点续查）
scripts/vendor/             vendor 机器（update/check，内容 SHA-256 固定）
hooks/                      门禁层：SessionStart 环境检查、UserPromptSubmit 意图提示（advisory）
.codex-plugin / .zcode-plugin / kimi.plugin.json / .agents  三平台适配清单
```

## 鉴权模型（环境变量优先）

- 主通道：`MINIMAX_API_KEY`（必填）+ `MINIMAX_BASE`（国内默认 api.minimaxi.com，
  国际账号覆盖为对应网关）+ `MINIMAX_MODEL`（默认 MiniMax-Hailuo-02）。
- 辅通道：`mmx` CLI（vendored toolkit 技能使用），凭据在其自身 `~/.mmx/credentials.json`。
- 第 0 步预检（`minimax_video.py check` / `hooks/env_check.py`）永远 advisory：
  缺鉴权时输出「去哪申请、怎么配置」的可操作指引，不阻塞会话、不回显完整密钥。

## vendor 铁律

`skills/` 下四个 upstream 技能逐字来自两个源：`full-aigc-skills/minimax-skills`
（3 个，main @ 0b72343a…）与 `MiniMax-AI/MiniMax-H3`（h3-prompt-writing，
main @ d21241f0…）；两源均待上游打 tag 后收紧 ref，
由 `skills.lock.json` 的逐技能 SHA-256 固定；改上游 → 跑
`python3 scripts/vendor/skill_vendor.py update` → `check` 过 CI。
`skills/minimax-design-use` 与 `skills/minimax-video-generation` 是本仓原生技能，
不进 lock。执行层双轨：**mmx-cli（Token Plan 订阅 CLI）** 供通用生成，
**v2 API 客户端** 供白模首尾帧（FL2VA）精确锚定。

## 生成纪律

- 付费生成前必过第 0 步预检；任务轮询超时是「续查状态」不是失败——用
  `query --task-id` 恢复，永不重复提交付费任务。
- 白模首尾帧锚定是默认工作流（构图/运镜起止由帧锁定，prompt 只做风格化）；
  灰块风格泄漏需先做单镜 A/B 再批量。
