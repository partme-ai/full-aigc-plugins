## Why

用户需要根据真实素材选择剪辑类型，并明确要求 108 个场景各有一个网上实操来源支持的独立 example。现有技能只有通用操作指导，缺少场景差异与可查询的能力映射。

## What Changes

- 新增读取锁定规划技能数据的路由与能力预检入口，落盘 Harness 架构。
- 每个场景记录检索词、真实来源、查阅日期、可见热度或未核验状态、素材要求、步骤、验收及技能/CLI 映射。
- 数据与例文单一来源，保留现有技能及执行契约；计划结果不表示成片完成。

## Capabilities

### New Capabilities

- `video-recipe-routing`: 版本化场景选择、依赖预检和结构化规划结果。

### Modified Capabilities

无；既有 Rust Runtime 迁移继续独立验收。

## Impact

插件 docs、schemas、Harness 规划入口、路由测试与技能版本消费；不实现第二套草稿引擎。

108 个例文是方法迁移，素材不下载、不再分发；搜索排名不作为热门证明。现有 CLI 未 supported 的能力保持门禁。

