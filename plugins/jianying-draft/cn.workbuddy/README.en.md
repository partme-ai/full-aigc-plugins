# JianYing Edit — WorkBuddy candidate

Use `adapter.json` with the shared exporter described in `full-aigc-plugins-repositories/.github/docs/workbuddy.md`. Run the exact check/build commands in [the local guide](README.md) from the workspace root. Output must be a new directory. Each selected MCP server produces a separate connector ZIP.

This adapter reuses the original skills and execution tools. Skill-only routes provide workflows, not additional model tools or MCP servers. Source skills and their locks are not edited; multilingual WorkBuddy metadata is added only to exported copies.

See the connector profile and generated WORKBUDDY.md for concrete prerequisites and scope. Local Python MCP requires an installed Python 3.11–3.13 interpreter; no tool or dependency is installed by the exporter. Existing authorization, budgets, native confirmations, credentials and artifact checks remain authoritative.

Lifecycle Hooks, Slash Commands, Codex imagegen and other host-specific tools are not automatically provided. WorkBuddy installation, authentication, routing and real business acceptance remain NOT_RUN. Original development/RC release gates remain in force. Initial connector candidate version is `0.27.9`; normal release tooling owns future version updates and immutable market refs.

Cross-repository specification: `full-aigc-plugins/openspec/changes/add-workbuddy-connectors/`. [Official connector documentation](https://open.workbuddy.cn/docs/connector), [skill documentation](https://open.workbuddy.cn/docs/skill).


## Authentication audit / 认证核对 (2026-10-16)

- `partme-jianying-edit`: `workflow-delegated` / `EXTERNAL_DEPENDENCY`. 仅提供技能与资源；本包没有 WorkBuddy 托管的认证生命周期。实际 CLI、宿主模型、渠道或外部服务由各自执行器负责登录；使用前逐项检查，不代表无需认证或已获授权。
