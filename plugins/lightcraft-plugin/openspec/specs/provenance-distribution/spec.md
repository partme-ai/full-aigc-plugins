# provenance-distribution Specification

## Purpose
定义插件从本地候选到正式发行的来源与快照完整性约束，让用户和宿主能够识别实际技能源及版本，并保证更新不会静默覆盖用户修改或将未发布内容伪装为发行制品。
## Requirements
### Requirement: PVD-1 候选来源一致性

候选校验 SHALL 核对插件身份、sourceProject、sourceVersion、sourceStatus、空 releaseTag、明确技能清单及逐文件摘要；任一冲突 MUST 拒绝，不能只检查目录数量与前缀。

#### Scenario: 来源项目被替换
- **WHEN** candidate-source 声称其他技能源项目但文件摘要未变
- **THEN** 校验失败并指出来源身份不匹配

#### Scenario: 候选标签或版本错配
- **WHEN** 本地候选的 releaseTag 非空，或 sourceVersion 不对应被记录的来源版本
- **THEN** 不返回来源有效结论，保留真实候选状态

### Requirement: PVD-2 正式发行锁与受管归属

正式来源锁 SHALL 绑定仓库、发行 tag、解析后的 commit 和文件摘要，并验证 tag 与 commit 关系；上游六技能与插件本地扩展 SHALL 分开登记，未声明额外文件 MUST 被拒绝。未发布来源 MUST NOT 被登记为已发布市场制品。

#### Scenario: tag 解析为其他提交
- **WHEN** 请求的发行 tag 与预期 commit 不一致
- **THEN** 停止升级并报告来源不一致，不继续生成成功发布回执

### Requirement: PVD-3 快照更新保护与材料完整性

同步 SHALL 预检旧快照、报告漂移及删除，保护用户修改；文档 SHALL 明确维护端同步器的真实位置，许可证和分发引用 SHALL 存在。正式升级 MUST 有明确来源迁移记录，不能通过重写摘要掩盖漂移。

#### Scenario: 用户修改插件缓存技能
- **WHEN** 旧快照与锁不一致
- **THEN** 普通同步拒绝覆盖并保留修改及旧锁，指出冲突文件

#### Scenario: 发行包引用缺失许可证
- **WHEN** 许可证或文档声明的必需文件不存在
- **THEN** 分发校验失败，即使技能摘要全部匹配也不能发布

