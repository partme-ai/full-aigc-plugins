# DeckCraft Plugin 需求与验收

> 2026-10-09；最小本地包已创建。静态、宿主和原生运行分层验收；后续格式质量不阻塞基础包结构通过。

| ID | 优先级 | 可观察行为 | 验收证据 | 状态 |
|---|---|---|---|---|
| P-01 | P0 | 根 `plugin.json` 符合 Agent Plugins 1.0.0 | Schema、字段、真实路径校验 | 字段与路径 PASS；官方 Schema NOT_RUN |
| P-02 | P0 | 包内 Skill 可被发现，单独安装仍完整 | frontmatter、隔离安装与触发回归 | frontmatter 与隔离安装 PASS；宿主触发 NOT_RUN |
| P-03 | P0 | `mcp.json` 连接已安装的 DeckCraft MCP | 实际客户端握手、工具列表和只读调用 | 直接 MCP PASS；客户端 NOT_RUN |
| P-04 | P0 | 授权范围内建稿、inspect、render、导出 | 当前 DeckCraft 版本的真实文稿与回读 | 两页建稿、保存重开、PNG PASS；完整场景 OPEN |
| P-05 | P0 | 缺 CLI、MCP 失败、损坏文稿、导出失败准确报告 | 故障场景；原件不被误覆盖 | PLANNED |
| P-06 | P1 | 来源固定，manifest、Skills、文档一致 | 来源 SHA、摘要与隔离安装 | PLANNED |
| P-07 | P1 | 客户端命令或 Hook 只在实际需求下添加 | 特定客户端加载与事件测试 | OPTIONAL |
| P-08 | P1 | 回读与重开检查区分格式损失和视觉差异 | PPTX 真实语料、PDF/PNG 样本 | PLANNED |

## 代码增加门槛

插件首先复用宿主与 DeckCraft。新增脚本须具备真实场景、可复现缺口、现成能力调查、最小行为实现和回归。远程回复丢失的风险保持显式限制；没有去重证据前，不承诺恰好执行一次。
多轮修订、计费、预算账本和独立控制器不属于本次基础交付范围。未来若任务明确需要，另建独立需求与验收，不提前写空框架。[架构](DeckCraft-Plugin-Architecture.zh_CN.md)
