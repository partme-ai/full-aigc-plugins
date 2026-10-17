## Purpose

定义插件内上游技能和本地编排入口的来源与清单规则，使未发布候选、正式来源锁和宿主 manifest 可以互相验证，并在同步或更新时保护用户修改而不伪造发行身份。

## ADDED Requirements

### Requirement: PP-01 候选与正式来源身份

系统 SHALL 分别验证候选与正式锁：候选 sourceProject 必须为 printcraft-skills、sourceVersion 与对应来源一致、releaseTag 必须为空；正式来源须有可核验仓库、版本/tag、commit 与文件摘要，版本映射策略显式声明。

#### Scenario: 伪造候选身份

- **WHEN** 候选携带非空 releaseTag、外来 sourceProject 或不匹配 sourceVersion
- **THEN** 校验失败，不继续输出 UNPUBLISHED/PASS。

#### Scenario: 正式来源不可解析

- **WHEN** 正式锁的 tag/commit 或技能版本不能与发布内容对应
- **THEN** 拒绝正式发行验收；离线摘要校验不冒充在线发行验证。

### Requirement: PP-02 完整清单与本地白名单

系统 SHALL 验证 manifest 的字段类型、必填及宿主映射，精确比较上游技能名/文件摘要，并独立声明插件本地技能白名单；不得仅凭前缀和数量接受清单。

#### Scenario: 非法版本

- **WHEN** manifest.version 为数字或不满足已声明版本规则
- **THEN** 报 schema/版本错误，不能只比较 $schema 字符串。

#### Scenario: 合法 Harness 或未知文件

- **WHEN** 加入声明的 printcraft-harness 或未声明技能
- **THEN** 白名单 Harness 与上游快照分别校验；未声明项、缺失项、链接及摘要漂移均拒绝。

### Requirement: PP-03 源码优先的保护性同步

系统 SHALL 从技能源更新上游快照，先核对旧来源和当前文件；用户漂移、源删除、跨域或正式身份被本地候选替换须拒绝，不进行强制覆盖。文档明确同步工具所在项目。

#### Scenario: 用户改动快照

- **WHEN** 上游同步前插件技能文件被人工修改
- **THEN** 保留修改和旧锁，报告冲突；不能以修复摘要为名接受未审查内容。

#### Scenario: 正常增量同步

- **WHEN** 未发布候选无漂移且来源身份满足约束
- **THEN** 只更新变化的受管文件与锁，保留插件本地 Harness，事后验证完整快照。
