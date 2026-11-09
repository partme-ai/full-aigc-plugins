# 开放路由：第一批可运行增量

本页描述开放路由合同，不是生产验收或自动成片证明。
插件 `0.27.8` 正式锁定 Skills `v2.3.0`；`workflow-plan` 可读取 v2 目录。
真实剪映、Windows 和三宿主验收仍需分别完成，不能由路由成功推断。

## 运行 Vlog 路由

在插件仓执行，开发目录参数必须显式指定到规划技能根：

```bash
node scripts/harness.mjs workflow-plan examples/workflows/vlog_brief.json \
  --development-skill-root \
  /Users/wandl/workspaces/workspace-agent-skills/full-aigc-skills-repositories/jianying-skills/skills/jianying-draft-video-planning
```

预期：`route=known`、`readiness=needs_input`，VG01 映射为 `scene.d01.vg01`，选择 R01。
例子没有真实媒体，所以要求补素材；不生成草稿、不读取视频、不调用模型。
有路径声明也不代表已分析媒体。输出始终为 `executable=false`、`evidence_level=plan`。
结果使用 `jianying-open-route/v1`，不是已编译的 WorkflowPlan 或 Job。
开发目录输出 `provenance.kind=development_candidate`，不能作为正式安装证明。

## 开放路由输入

输入遵循插件 `schemas/creative-brief.v1.schema.json`：

- `scene_ids` 可以使用新版 ID 或旧 ID；多选表示需要组合，冲突策略要求人工确认。
- 无 `scene_ids` 时按 `intent` 与目录描述检索，多个候选不擅自选择第一项。
- `dimensions` 表示偏好；`constraints.tags`、`domain_ids`、`exclude_domain_ids` 是硬约束。
- 未登记的维度/取值要求复核；缺少标签不能被当作满足硬约束。
- 首页最多三个候选，用 `next_cursor` 传给 `--cursor`；更换简报或目录后游标失效。
- `output_intents` 分别声明用途、形式和交付；普通视频以外的形式明确阻塞。
  原生交付能形成方法方案，也不表示已通过能力、授权或实机检查。

没有精确案例时返回 `proposed` 和待审核策略，不新增伪造场景。
当前是确定性的结构化/文本匹配，不是语义向量检索，也没有自动观看视频。

## 兼容与资源边界

旧 `plan-video`、v1 资源及 108 篇例文保持不变；v2 不要求固定场景、家族或 Recipe 数量。
默认索引 16 MiB/10000 场景、单例文 256 KiB，技能整体 64 MiB/20000 项。
这些是安全限额，不是视频类型上限，目录不能自行提高限额。
拒绝重复键、身份冲突、缺失引用、非法路径、链接、超限及正式目录中的 test_fixture。
目录 Schema 由 Skills 持有，插件固定所支持合同摘要，不能附带宽松 Schema 绕过校验。

## 回滚与未完成门禁

设置 `JIANYING_OPEN_WORKFLOW_DISABLED=1` 可停止新工作流的规划、编译、启动、批准、执行和恢复；
旧 `plan-video` 保持可用。先保留运行状态与副作用账本，再回退到上一兼容 Skills 锁；
旧锁缺 v2 时，新入口返回 `catalog_v2_unavailable`，不能静默改走 v1。
清除开关属于单独的重新启用决策，不得借回滚重跑未知结果的导出或付费动作。

WorkflowPlan、Job 编译及受控执行已有离线与发布 CLI 证据，但 Vlog 叙事/音画验收、
课程专业审校、婚礼用途审核、Windows 与三宿主安装尚未完成；原生导出不得降级为代理成功。
