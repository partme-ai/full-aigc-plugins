## Context

MiniMax 插件包含 12 个公共技能和 2 个只服务插件运行时的本地技能。现有双来源锁包含移动分支，且测试仍假设旧 manifest 结构。

## Goals / Non-Goals

**Goals:**

- 技能同步可复现、可拒绝漂移、可审查。
- 插件专属技能边界被机器校验。
- Codex、ZCode、Kimi、tag 与 Release 形成一致证据链。

**Non-Goals:**

- 不把 `minimax-design-use` 或 `minimax-video-generation` 迁入公共技能仓。
- 不修改 MiniMax 生成模型、请求参数或授权边界。
- 不移动任何已发布 tag。

## Decisions

1. 12 个公共技能统一由 `full-aigc-skills/minimax-skills` 发布，避免移动分支和双来源碰撞。
2. 锁文件保存 release tag、peeled SHA 和目录摘要，在线与离线检查分别验证来源和树内内容。
3. `plugin-local-skills.json` 是两个插件专属技能的唯一允许清单。
4. producer 只在 `release.published` 后 dispatch；consumer 必须同时收到 tag 与 SHA，并在写入前验证。
5. 三端版本比较使用基础 SemVer，允许 Codex 在相同版本后附构建元数据。

## Risks / Trade-offs

- [dispatch token 缺少跨仓权限] → 工作流明确失败，保留携带 tag/SHA 的手工 dispatch 路径。
- [上游 release 与锁不一致] → vendor 在任何写入前失败，不留下部分更新。
- [插件目录出现未声明技能] → CI 阻断并要求明确归属。

## Migration Plan

1. 引入 vendor v2、本地技能清单和 mutation tests。
2. 从 `minimax-skills v1.1.1` 重新同步 12 个技能并删除移动来源。
3. 修复分发验证并运行单测、在线/离线 vendor 检查。
4. 推送并等待 CI，通过后创建不可变插件 tag/Release，再更新市场目录。
