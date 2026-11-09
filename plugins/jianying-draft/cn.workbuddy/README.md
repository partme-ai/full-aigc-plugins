# JianYing Edit — WorkBuddy 接入候选

本包适配配置为 `adapter.json`；完整构建由组织共享工具完成，原 Skills、来源锁、MCP、Hooks 和市场状态保持原有归属。

在 `workspace-agent-skills` 工作区根执行：

```powershell
python -B full-aigc-plugins-repositories/.github/scripts/workbuddy.py check --plugin full-aigc-plugins-repositories/jianying-edit-plugin
python -B full-aigc-plugins-repositories/.github/scripts/workbuddy.py build --plugin full-aigc-plugins-repositories/jianying-edit-plugin --output .validation/workbuddy-partme-jianying-edit
```

输出目录必须不存在。每个连接器子目录含元信息、图标、完整技能和所需运行资源，同级 ZIP 为审核候选。多个 MCP 分别打包。

## 运行前置条件

- 按原 README 准备校验和固定的 Rust jianying-cli >= 1.6.13、Node 和原宿主软件依赖；包不提供未验证的安装命令。

## 能力边界

- NOT_RUN: WorkBuddy 安装、技能发现、认证和真实业务执行均待实机验收。
- 原宿主 Hooks、Slash Commands 和专有工具不随连接器自动接入；所有实际执行仍需原授权与校验。

原插件版本 `0.27.9` 用于首份 WorkBuddy 候选身份，不修改现有安装源或未发布 tag。正式发布时使用原版本工具同步各清单，再重新构建本包；开发版不得提升为稳定版。

`workbuddy-build.json` 分别记录静态、协议、宿主、认证和业务证据；ZIP 成功不等于 WorkBuddy 已验收。真实客户端接入和服务调用须由对应环境完成。

跨仓库规格：`full-aigc-plugins/openspec/changes/add-workbuddy-connectors/`。共享指南：`full-aigc-plugins-repositories/.github/docs/workbuddy.md`。
官方文档：https://open.workbuddy.cn/docs/connector 和 https://open.workbuddy.cn/docs/skill 。


## Authentication audit / 认证核对 (2026-10-16)

- `partme-jianying-edit`: `workflow-delegated` / `EXTERNAL_DEPENDENCY`. 仅提供技能与资源；本包没有 WorkBuddy 托管的认证生命周期。实际 CLI、宿主模型、渠道或外部服务由各自执行器负责登录；使用前逐项检查，不代表无需认证或已获授权。
