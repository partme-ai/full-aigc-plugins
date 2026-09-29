# candidate-plugin-governance Specification

## Purpose
集中登记发布候选（release candidate），使其在获得明确晋级之前既可审计又不可被任何宿主安装；晋级为正式插件必须是一次显式的、有证据的发布动作。

## Requirements
### Requirement: Blocked candidates are centrally tracked without becoming installable

市场 MUST 在中央 catalog 中记录每个发布候选的仓库、精确候选版本、状态与发布门禁证据路径。状态为 `release_candidate_blocked` 时，市场 MUST NOT 将该候选写入任何宿主安装清单。状态为 `release_candidate_installable` 时，市场 MUST 将其以明确标注的 RC/preview 条目写入 Codex、ZCode 与 Kimi 安装清单，并固定到其不可变预发布 tag，同时 MUST NOT 将其提升进正式 `plugins` 集合，也 MUST NOT 改动其正式发布门禁。

#### Scenario: Content Factory remains blocked

- **GIVEN** Content Factory 的状态为 `release_candidate_blocked`
- **WHEN** 市场 catalog 被同步
- **THEN** 该候选仍出现在 `catalog.json` 中
- **AND** 它不出现在 Codex、ZCode 与 Kimi 的可安装清单中

#### Scenario: Approved RC is visible and test-installable

- **GIVEN** Content Factory 版本 `1.0.0-rc.2` 已有不可变 tag 并已发布 GitHub 预发布
- **AND** 其候选状态为 `release_candidate_installable`
- **WHEN** 市场 catalog 被同步
- **THEN** 它出现在 Codex、ZCode 与 Kimi 的可安装清单中
- **AND** 每个条目都标明其为 RC/preview 并将安装固定到 `v1.0.0-rc.2`
- **AND** 该候选仍留在正式 `plugins` 集合之外，其最终发布门禁保持不变

#### Scenario: Candidate identity overlaps a released plugin

- **GIVEN** 某个候选 ID 同时存在于正式 `plugins` 集合中
- **WHEN** 市场被校验
- **THEN** 校验失败，而不是发布重复条目

#### Scenario: Installable candidate uses a stable version

- **GIVEN** 某个候选状态为 `release_candidate_installable`
- **AND** 其版本不是语义化预发布版本
- **WHEN** 市场被校验
- **THEN** 校验失败，而不是通过 preview 路径暴露一个看起来已正式发布的候选

#### Scenario: Candidate gate no longer reports blocked

- **GIVEN** 某个候选登记项指向的发布门禁不再是 `BLOCKED`
- **WHEN** 市场被校验
- **THEN** 校验失败，并要求显式晋级到正式 `plugins` 集合
