# 辅助媒体 Provider 边界

## 步骤责任

| 步骤类型 | 执行者 | 允许副作用 | 必要门禁 |
|---|---|---|---|
| `screen_capture.prepare` | Harness | 无 | 捕获范围、隐私、音频/点击选择 |
| `screen_capture.execute` | 本地录屏 Provider | 创建录屏 | 精确批准、超时、原始制品摘要 |
| `interaction_events.ingest` | Harness | 创建事件账本 | 录屏摘要、坐标映射、禁止按键内容 |
| `smart_zoom.plan` | 确定性规划器 | 无草稿写入 | 事件 Schema、FPS、黑边、可访问性 |
| `web_vfx.render` | 沙箱浏览器 Provider | 创建媒体 | Origin allowlist、网络、字体/脚本、超时 |
| `media.preflight_normalize` | 受控媒体 Provider | 创建派生媒体 | 源/派生摘要、参数、质量、回滚、批准 |
| `native_asset.discover` | Runtime Adapter | 只读查询或下载候选 | 版本、基础/专业权益、用途、收据 |
| `exposure.analyze` | 本地或获准分析 Provider | 创建评估 | 代理摘要、Provider identity、上传/费用 |
| `commentary.storyboard` | 规划器 | 创建计划 | 来源、版权、事实与人工审校 |

每一步还必须声明输入/输出 artifact schema、执行者版本、capability、风险、超时、幂等键、重试/对账、隐私、成本、验证与回滚。缺字段时不生成自由命令作为 fallback。

## 权限链

Provider 产物先进入 Harness 账本，再编译为 WorkflowPlan。只有审批与 capability 均满足时才能生成 `jianying-job/v2`，并交给不可变发布的 Rust CLI。Provider、模型输出和 Skills 文件都不能直接修改草稿。

## 故障语义

- `failed`：确认没有目标副作用后，可在新批准下重试。
- `ambiguous`：先查询录屏、浏览器、转码、下载或远程 Provider 的制品/request-id；不得普通重提。
- `cancelled`：只证明请求停止，不证明外部副作用撤销；必须对账。
- 草稿阶段失败：使用 CLI 审计与快照恢复，不让 Provider修补草稿 JSON。
