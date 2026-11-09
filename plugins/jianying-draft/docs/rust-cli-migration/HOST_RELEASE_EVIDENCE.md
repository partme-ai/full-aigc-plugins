# 三宿主发布验收证据

最终 Rust-only cutover 不能只依赖静态 manifest、Node fixture 或未发布的开发 CLI。它要求
Codex、ZCode、Kimi 分别加载同一组正式发布身份，并执行同一份 `jianying-job/v2` 输入。

## 证据文件

`runtime/host-acceptance.json` 是汇总锁，初始状态为 `pending`。每个宿主完成验收后，将原始结果
保存到 `runtime/host-evidence/<host>.json`，汇总锁只记录相对路径和文件 SHA-256。

三个交换格式分别由以下 Draft 2020-12 JSON Schema 固定：

- `schemas/host-observation-v2.schema.json`
- `schemas/host-run-evidence-v2.schema.json`
- `schemas/host-release-acceptance-v1.schema.json`

已发布的 `host-observation-v1` 与 `host-run-evidence-v1` 文件只用于解释历史五项布尔记录；当前
发布门禁仅接受 v2，避免在相同 Schema ID 下改变既有语义。

每份原始证据必须绑定：

- `pluginVersion`、`cliVersion`、`skillsVersion` 和 `jianying-job/v2`；
- `evidenceLevel=real_host`，不能使用 fixture、结构测试或代理预览；
- 同一 Job 输入的 SHA-256 和规范化结果语义 SHA-256；
- fresh install、doctor、技能发现、单技能安装、13 分类发现与路由、选择解释、批准、简单 Job、
  停止、恢复、证据展示、原生导出目标级授权共十三项检查；
- 每项检查对应一个 `checkEvidence` 记录，包含证据来源类型、带时区观察时间、内嵌宿主/命令
  结果对象及其 canonical JSON SHA-256；只有 `checks.<name>=true` 的手写布尔声明无效；
- 带时区的 RFC 3339 执行时间。

三个宿主必须使用相同 Job 输入并产生相同语义摘要。真实宿主执行器把剔除 task ID、临时路径
和宿主日志后的稳定对象写入 observation 的 `semanticResult`；`record_host_acceptance.py` 使用
排序键、无空白分隔符和 UTF-8 canonical JSON 计算两个摘要，验证器会从内嵌对象重新计算，
不能只信文件中声明的 hash。
记录器和最终汇总器还会逐项重算 `checkEvidence.<name>.artifactSha256`，因此更改任何宿主命令
结果、UI 观察或授权回执都会使验收失败。

## 验证命令

每个宿主先把固定 `jianying-host-observation/v2` 输出转换为证据：

```bash
python3 scripts/record_host_acceptance.py \
  --observation /path/to/codex-observation.json \
  --output runtime/host-evidence/codex.json
```

三份证据收集完成后，先校验全部内容，再原子生成 `passed` 汇总锁：

```bash
python3 scripts/finalize_host_acceptance.py \
  --plugin-version 0.17.2 \
  --cli-version 1.6.0 \
  --skills-version 2.0.3
```

最后执行正式发布校验：

```bash
python3 scripts/host_acceptance.py \
  --plugin-version 0.17.2 \
  --cli-version 1.6.0 \
  --skills-version 2.0.3
python3 scripts/release_readiness.py
python3 scripts/validate_distribution.py --release
```

任一证据缺失、摘要被篡改、版本漂移、宿主集合不完整或结果语义分叉都会 fail-closed。
不可变 `v0.26.2` 已在三宿主完成上述检查；一次性 `rust-cutover.yml` 与
`JIANYING_HEADLESS_ROOT` 兼容诊断随后从发布面删除。

正式 CLI release index 导入器、Skills manifest 导入器和插件版本提升脚本都会先将该汇总锁
重置为 `pending`、清空 `hosts`，再激活新版本身份。即使更新中断，也只会留下需要重新验收的
fail-closed 状态，旧版本证据不会被新版本复用。

当前 `v0.26.2` 汇总锁由三份 v2 observation 生成并保持 `passed`。不得手工修改为 `passed`
来替代真实宿主运行；任何版本、CLI 或技能锁更新仍会自动重置为 `pending`。
