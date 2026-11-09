# Harness 参考

## 生命周期

`queued → running → succeeded|failed|cancelled|ambiguous`。恢复必须从最后已验证检查点继续；
`ambiguous` 外部操作先对账，不能自动重提。

## 调用面

```bash
jianying job run job.json --out /absolute/output --state-root /absolute/state --json
jianying job list --state-root /absolute/state --json
jianying job show <task-id> --state-root /absolute/state --json
jianying job audit <task-id> --state-root /absolute/state --json
jianying mcp tools --json
jianying mcp serve --transport stdio
```

具体 flag 以当前 `--help` 和 machine-readable command catalogue为准，不从文档猜测。
MCP 客户端使用 `jianying_job_list`、`jianying_job_show`、`jianying_job_cancel`、
`jianying_job_retry` 和 `jianying_job_audit` 管理同一 SQLite JobStore 中的业务任务。

## 远程 MCP 门禁

- 默认只监听 loopback。
- 非 loopback 要求显式 token、Host allowlist、Origin allowlist 和 TLS 前置层。
- stdio 的 stdout 只能承载协议消息；诊断写 stderr。
- JSON-RPC 请求取消、通知、初始化和关闭由 SDK 生命周期处理，不自行发明消息格式。
- 连接断开或 `notifications/cancelled` 只表示协议请求停止等待，不能据此声称任务副作用已撤销；
  业务取消必须调用 `jianying_job_cancel` 并复核任务终态。

## 恢复

- failed：查看审计，修复输入后使用显式 retry。
- ambiguous：先查询外部系统或制品哈希，再决定采用结果或新审批重试。
- 草稿写入失败：使用审计中记录的快照恢复命令，并重新运行 verify。
