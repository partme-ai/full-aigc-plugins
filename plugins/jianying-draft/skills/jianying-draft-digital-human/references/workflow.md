# 数字人操作动线

## 功能动线

| 语义动作 | 剪映入口 | 前置事实 | 执行路由 | 验证 | 恢复 |
|---|---|---|---|---|---|
| `digital_human.catalog.search` | 数字人 → 选择数字人 | 类别、性别/风格、用途、版型、权益 | Harness 搜索库存 persona/voice 目录 | 候选、排序和拒绝理由 | 只读 |
| `digital_human.persona.select` | 数字人 → 形象 | 稳定 persona ID 或获批自定义素材 | 选择写入请求，不提交 | 资源/素材摘要与授权绑定 | 重新选择 |
| `digital_human.voice.select` | 数字人 → 配音 | 稳定 voice ID 或声音权批准 | 选择写入请求，必要时 TTS 计划 | 音色、语言、情绪和权益 | 重新选择 |
| `digital_human.custom.authorize` | 定制形象/声音 → 上传 | 精确素材、肖像/声音权、用途、Provider | 独立上传批准，凭据只引用环境变量 | 批准范围和文件摘要一致 | 撤销批准，不上传 |
| `digital_human.preview.request` | 数字人 → 预览 | 脚本、背景、形象、声音、预算 | `jianying-digital-human-preview-plan/v1` + Adapter | 预览绑定 request digest | 丢弃预览 |
| `digital_human.task.submit` | 数字人 → 生成 | Provider 握手、费用上限、有效批准 | Harness 幂等提交，保存 request/task ID | 供应商 request ID、费用和状态 | 明确失败后新批准重试 |
| `digital_human.task.resume` | 任务 → 继续/查询 | 稳定 task ID、账本 | 查询原任务 | 远端与本地账本一致 | ambiguous 保持阻断 |
| `digital_human.artifact.verify` | 生成结果 → 验证 | 产物、预期身份/声音/脚本摘要 | Harness 验证哈希、时长、音画与账单 | `jianying-digital-human-evidence/v1` | 拒绝产物，不删除证据 |
| `digital_human.timeline.apply` | 结果 → 添加到草稿 | 已验证产物、隔离草稿、时间范围 | Rust 素材/音频命令；需要原生动作时 Adapter | 冷重开、播放、原生导出 | 删除新增段或恢复快照 |

## 费用与隐私

预算、上传范围、Provider、模型、脚本摘要和目标必须进入批准绑定。日志只保存摘要、任务 ID 和费用回执，不保存账号秘密或无关个人数据。
