## Why

插件当前同时从 `minimax-skills` 的固定 tag 和 `MiniMax-H3` 的移动 `main` 分支 vendoring 技能，旧同步工具也不能消费 release 事件中的精确 tag/commit，导致安装内容无法完整复现。

## What Changes

- 将 12 个公共技能统一锁定到 `minimax-skills` 的正式 release tag、peeled commit SHA 和逐技能摘要。
- 使用声明式清单区分外部受管技能与两个插件专属技能。
- 让同步工作流校验 release 事件中的 tag 与 commit 后创建升级 PR。
- 修复 Codex 构建元数据、ZCode `userConfig` 对象结构和技能数量的分发验证。

## Capabilities

### New Capabilities

- `immutable-minimax-skill-supply-chain`: 定义 MiniMax 技能来源、插件本地技能边界和事件驱动升级契约。

### Modified Capabilities

无。

## Impact

影响 `skills.lock.json`、`plugin-local-skills.json`、vendor 工具、同步与检查工作流、三端 manifest 和分发测试；不改变 MiniMax API 调用和付费生成行为。
