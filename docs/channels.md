# 双渠道（GitHub 英文 / AtomGit 中文）

## 产物

| 路径 | 渠道 | 语言 | 代码源 |
|---|---|---|---|
| `marketplace.json`、`kimi-marketplace.json`、`.agents/plugins/marketplace.json` | 全球 | 英文 | GitHub |
| `cn-marketplace/` 下同名三文件 | 国内（Gitee） | 中文 | Gitee |
| `atomgit-marketplace/` 下同名三文件 | 国内（AtomGit） | 中文 | AtomGit |
| 各插件仓的 `.codex-plugin` / `.zcode-plugin` / `kimi.plugin.json` | 全球 | 英文 | GitHub |
| 同上（AtomGit 检出） | 国内 | 中文 | AtomGit |
| `channels/global.json` / `channels/cn.json` | 渠道配置 | — | — |

两个渠道共用同一份 `catalog.json` 与同一批 tag；只有展示文案和代码托管地址不同。

## 生成与校验

```bash
node scripts/sync-marketplaces.mjs --write          # 全球市场（英文）
node scripts/sync-plugin-configs.mjs --locale=en    # GitHub 插件清单（英文）
node scripts/sync-cn-marketplace.mjs --channel=atomgit --write  # AtomGit 市场（中文）
node scripts/sync-cn-marketplace.mjs --channel=cn --write      # Gitee 市场（中文）
node scripts/sync-plugin-configs.mjs --locale=zh-CN --workspace=<AtomGit checkout>  # AtomGit 插件清单（中文）
node scripts/verify-channel-parity.mjs              # id、version、ref 必须一致
node --test scripts/plugin-naming.test.mjs
```

## AtomGit / Gitee 全量镜像流程

1. 在 AtomGit（或 Gitee）建同名组织与各插件仓，或使用平台的 GitHub 同步功能做全量镜像。
2. 推送全部 tag：`git push --mirror gitee:<org>/<repo>.git`。
3. 校验 tag 存在：`git ls-remote https://gitee.com/<org>/<repo>.git refs/tags/<tag>`。
4. 运行 `sync-cn-marketplace.mjs --write` 生成中文产物。
5. 运行 `verify-channel-parity.mjs`，通过后才允许发布。

> 当前 `channels/cn.json` 的 `repositoryOrg` 与 GitHub 组织同名（`full-aigc-plugins`）。若 Gitee 组织名不同，只改这一处并重新生成。

## 冲突防线

1. **单一事实源**：语言只写在 `catalog.json`，marketplace 文件是生成物。
2. **身份不变**：`id`、`version`、`source.ref`、产物哈希跨渠道一致，parity 校验强制。
3. **单一 tag**：canonical 打 tag → 镜像 → 生成两渠道 → 校验 → 发布。
4. **市场名区分**：`full-aigc-plugins`（全球）与 `full-aigc-plugins-cn`（国内），文档要求二选一。
5. **不手改生成物**：CI 以 `--check` 模式拦截手改。
6. **插件仓不写死语言**：四份宿主清单由 `sync-plugin-configs.mjs --locale` 写入；GitHub 检出用 `en`，AtomGit 检出用 `zh-CN`。
   - `scripts/atomgit/sync.mjs` 默认在推送后按 catalog 对插件仓自动执行 `--locale=zh-CN`；`--no-localize` 可关闭，`--only=<org/repo>` 可单仓调试。
   - UI 插件的 `ui.surfaces.title` 是唯一例外：同时保留 `en-US` / `zh-CN`，供宿主按界面语言切换；`displayName` / `description` 仍严格单语。

## 已知限制

- 同一份安装包不能同时承载两种语言的清单；AtomGit 镜像需要在检出后重新生成中文清单，并提交一个只改 metadata 的 commit（或走 `atomgit` 分支）。
- Gitee Release 的下载地址格式需在镜像建成后实测一次；`channels/cn.json` 的 `releaseTagPath` 可单独调整。
