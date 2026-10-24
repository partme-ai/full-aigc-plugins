# full-aigc-plugins（国内渠道）

本目录由 `scripts/sync-cn-marketplace.mjs` 生成，是 Gitee 渠道的中文市场入口，**不要手改**。

- 语言：中文（`catalog.json` 的 `localizations.zh-CN`）
- 代码源：Gitee 全量镜像，tag 与 GitHub 一致
- 身份校验：`node scripts/verify-channel-parity.mjs`

## 安装

ZCode：把本目录作为独立市场仓添加（市场名 `full-aigc-plugins-cn`），或使用 Gitee 上的对应仓库。

Kimi Code：

```text
/plugins marketplace https://gitee.com/full-aigc-plugins/full-aigc-plugins-cn/raw/main/kimi-marketplace.json
```

Codex：

```bash
codex plugin marketplace add full-aigc-plugins/full-aigc-plugins-cn
```

生成与校验命令见仓库 `docs/channels.md`。
