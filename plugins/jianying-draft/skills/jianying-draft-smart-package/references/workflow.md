# 智能包装操作动线

## 功能动线

| 语义动作 | 剪映入口 | 前置事实 | 执行路由 | 验证 | 恢复 |
|---|---|---|---|---|---|
| `smart_package.style.select` | 智能包装 → 选择风格 | 创作简报、渠道、节奏、素材与保护项 | Harness 将风格映射为开放路由标签 | 风格、标签和请求摘要固定 | 重新选型，无副作用 |
| `smart_package.preview.request` | 智能包装 → 预览 | 精确版本、预算、允许轨道、素材事实 | 版本绑定 Adapter 请求预览 | proposal 绑定 request digest | 停止任务并查询状态 |
| `smart_package.proposal.decompose` | 预览 → 查看变更 | 完整 proposal | Harness 拆为 B-Roll/字幕/花字/音效/特效/转场 | 每项有资源、范围和理由 | 拒绝不可解释项 |
| `smart_package.proposal.approve` | 预览 → 应用 | 保护规则、权益、预算均通过 | 批准绑定 request/proposal digest、目标和有效期 | 批准字段精确匹配 | 撤销批准、重新生成 |
| `smart_package.apply.changes` | 智能包装 → 应用 | 有效批准、应用前快照 | Adapter 执行，CLI/Harness 检查草稿变更 | 草稿差分与 approved change set 一致 | 恢复快照或局部移除 |
| `smart_package.review.result` | 时间线 → 播放/审阅 | 应用后草稿、代理/原生播放 | 质量循环评估叙事、音画和保护项 | playback 证据、人工评审 | 局部返工后重验 |
| `smart_package.task.resume` | 任务 → 恢复 | 稳定 request/task ID、账本 | 查询原任务，不创建新请求 | 状态与供应商/编辑器一致 | 保持 blocked，不静默重提 |

## 执行路由

智能包装没有发布 CLI 的单一原子命令。技能调用插件 Harness 合同，由版本绑定 Adapter 取得提案；实际可解释子变更再编译为 Rust 原子步骤。无法解释的整体变更只能预览和人工批准。
