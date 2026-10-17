# 历史发布门禁的正向夹具

`plugin.json` 按历史报告声明的 SHA-256
`9799bbefaf90b6529ddce43aa0dfcf4e49e91e113d5c3166db061bf8ac6dd58b`
从本仓原始 Git blob `8b72ae49bda1c8b317854477c4990168fcbdc651` 恢复。

`docs/current-identity.json` 从新增场景前的基础提交恢复，其历史报告声明摘要为
`19f8d4e8313a3052232c06ab144d3392a29efe964b961c076351fdf6e8d63757`。

它仅供旧快照的正向单元测试使用，不表示当前候选沿用旧资格，也不改写原报告或摘要。
真实工作树发布门禁仍读取当前 manifest；已有漂移拒绝测试保持生效。
