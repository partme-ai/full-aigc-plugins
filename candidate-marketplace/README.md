# Craft 开发候选插件库

仅包含13个固定版本 `0.1.0-dev.20261017.4` 的开发候选，市场名 `full-aigc-craft-candidates`，可与原有 `full-aigc-plugins` 主库并存。Node.js 24；Git安装首次启动下载并核验编辑器资源。完整ZIP可从每个固定发行标签获取。

当前候选按授权经test分支合入main；它与主库固定到相同开发标签。完整创作质量、所有main新能力及三宿主内嵌同步仍待验收。

克隆候选分支后：

```sh
codex plugin marketplace add ./full-aigc-plugins/candidate-marketplace
codex plugin add photocraft@full-aigc-craft-candidates
```

安装其他应用时把photocraft替换为对应插件ID。PdfCraft的插件ID为printcraft。Codex清单在`.agents/plugins/marketplace.json`，ZCode清单为`marketplace.json`，Kimi清单为`kimi-marketplace.json`。候选市场使用独立名称，不替换主库的来源或版本。本轮仅在隔离目录验收，没有自动修改你的全局插件配置。
