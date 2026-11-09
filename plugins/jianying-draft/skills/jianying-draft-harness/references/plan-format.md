# 作业格式 `jianying-job/v2`（字段手册）

这是 Rust `jianying` CLI、插件 Runtime Adapter 与 Codex/ZCode/Kimi 共用的稳定作业信封。
权威结构来自当前 CLI 的 `schema.job_v2` capability 与 JSON Schema；运行前必须读取实际安装
制品的 capability manifest。旧版外部 headless plan、fork schema 和私有草稿 wire
字段都不是本技能的执行契约。

## 顶层信封

| 字段 | 类型 | 何时需要 | 约束 |
|---|---|---|---|
| `schema` | string | 始终 | 精确为 `jianying-job/v2`；未知主版本 fail closed |
| `operation` | string | 始终 | `create/edit/inspect/verify/publish/export/batch` |
| `project` | object | 除 `batch` 外 | `new` 或 `existing`，形状见下文 |
| `compatibility` | object | 仅 v1 转换结果 | 保存 `jianying-cli-plan/v1` 与完整规范化 payload；不得手工伪造 |
| `export` | object | `operation=export` | 声明导出种类、绝对输出路径和覆盖策略 |
| `jobs` | array | `operation=batch` | 非空；子 Job 不得再次为 batch |

Schema 只证明输入可解析。执行前还要逐项检查对应 capability 为 `supported`；`partial`、
`external_dependency`、缺失或版本不兼容都必须停止，不得切回 Python 或外部 headless。

## 项目目标

新项目：

```json
{
  "type": "new",
  "project": {
    "name": "demo",
    "width": 1920,
    "height": 1080,
    "frame_rate": {"numerator": 30, "denominator": 1},
    "timeline": {"tracks": []},
    "materials": []
  }
}
```

已有项目：

```json
{
  "type": "existing",
  "source": "/absolute/path/to/source-draft",
  "output": "/absolute/path/to/isolated-copy"
}
```

- `create` 使用 `type=new`。
- `edit` 必须使用 `type=existing`，并且 `source` 与 `output` 不同；禁止原地覆盖。
- `inspect`、`verify`、`publish` 使用 `type=existing`，通常只需 `source`。
- 所有素材和草稿路径来自 inventory/probe；不得用相对路径、猜测路径或未验证 URL。

## 领域项目

- 画布宽高为 `16..8192` 的整数。
- 帧率使用 `{numerator, denominator}`，两项均为正整数；执行器可能对尚未支持的有理帧率
  返回结构化 capability 错误。
- 时间统一使用整数微秒：`{"start_us": 0, "duration_us": 1000000}`，持续时间必须大于零。
- 轨道 `kind`：`video/audio/text/sticker/filter/effect/composite`。
- 片段必须有稳定 `id`、时间范围及与轨道兼容的类型；同轨重叠、缺失素材引用和类型不匹配
  由领域校验拒绝。
- 视频/音频片段引用 `material_id` 与 `source_range`，`speed` 为 `0.1..8`，`volume` 为
  `0..4`。文字片段包含非空 `text`；贴纸、滤镜和特效使用经过目录验证的 `resource_id`。
- 素材类型为 `video/audio/image/font` 时使用绝对 `path`；编辑器资源使用经过目录验证的
  `resource_id`。禁止猜测资源 ID。

## 导出与批处理

导出对象：

```json
{
  "kind": "proxy",
  "output": "/absolute/path/to/preview.mp4",
  "overwrite": false
}
```

- `kind` 为 `proxy/native/draft_archive`。
- `native` 是外部原生应用动作，必须先有支持该产品版本的 Runtime Profile 与精确批准。
- `proxy` 结果不能描述成剪映原生最终 MP4。
- `overwrite=true` 是目标级高风险写入，必须重新确认。
- batch 子任务按只读事实、可逆写入、外部动作排序；任一子任务失败时按任务审计判断是否有
  已发生副作用，不能假定整批未执行。

## 执行与恢复

```bash
jianying job run /absolute/path/job.json --out /absolute/path/output --json
```

- JSON 模式 stdout 只能有一个结构化信封，诊断写 stderr；非零退出码不得忽略。
- 保存返回的 `task_id`、输入摘要、素材哈希、CLI identity、批准绑定和输出路径。
- 通过 `job show`、`job audit`、`job cancel`、`job retry` 管理任务；`ambiguous` 外部操作不得
  自动重提。
- `incompatible_capability` 是停止信号，不是自动换引擎或静默降级条件。
- 完成状态只证明对应 handler 成功；最终仍按目标补充结构、冷重开、播放或原生导出证据。
