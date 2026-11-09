# Rust Runtime 与草稿快照回滚演练

- 日期：2026-09-20
- 关联 OpenSpec：`route-all-execution-to-rust-cli` 9.5
- 边界：本地合成制品与合成草稿；不启动剪映，不执行真实原生导出

## 场景一：CLI 制品回滚

`tests/runtime_adapter.test.mjs` 执行以下顺序：

1. 安装带 manifest 和逐文件 SHA-256 的 Rust CLI 1.6.0 bundle。
2. 升级到另一份经过相同校验的 Rust CLI 1.6.0 bundle。
3. 使用旧二进制 SHA-256 选择 rollback slot，原子交换 active 与 rollback 目录。
4. 重新执行 version/capability handshake，确认 active 版本回到 1.6.0。
5. 扫描恢复后的安装目录，拒绝 `.py`、pyJianYingDraft 或 headless 制品。

中断升级测试同时证明：新 bundle 缺文件时，旧 active runtime 保持原位，不能通过
Python 或外部 checkout 补偿安装失败。

## 场景二：草稿快照恢复

插件通过共享 Runtime Adapter 暴露：

```text
jianying store restore-snapshot --snapshot <snapshot> --target <draft>
```

`tests/workflow_e2e.test.mjs` 验证该路径要求 `store.restore` capability，并与 create、
edit、caption、audio、batch、retry 和 proxy 一样只经过 `runJsonCommand`。真正的文件
事务、验证失败不改源草稿、快照恢复和原子提交由 CLI workspace 的
`crates/jianying-store/tests/mutation_plan.rs` 验证。

## 结论与未覆盖项

- 插件版本和 CLI 制品可以回滚，但不会恢复已删除的 Python/fork 自动回退。
- 草稿恢复使用 CLI 快照事务，不从插件复制或覆盖草稿目录。
- 本演练不提升真实宿主证据等级；冷重开、播放和原生导出仍受 9.2 独立门禁约束。
