## ADDED Requirements
### Requirement: 可搬迁插件安装
插件 SHALL 提供标准、Codex 与 Claude Code 安装入口，不依赖开发者机器绝对路径；可见产品内容使用自身名称，第三方许可来源与历史记录保留。

#### Scenario: 搬迁插件包
- **WHEN** 插件目录移动到含空格的新路径并从另一工作目录启动
- **THEN** 对应宿主配置解析后可以启动包内 stdio MCP、读取编辑器资源并选择任务工作区。

#### Scenario: 插件市场分发
- **WHEN** 用户导入本地插件市场
- **THEN** 市场内各插件来源使用相对路径，包内含实际运行时与技能，不需要复制本机 WorkBuddy MCP 配置。
