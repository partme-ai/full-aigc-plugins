## Purpose

为视频场景规划提供来源可追溯、能力可验证、按需加载的契约，使用户提供目标与素材后能获得具体剪法与明确缺口，并将方法建议同实际剪映执行证据区分。

## ADDED Requirements

### Requirement: 每个场景独立且可追溯
系统 SHALL 提供 18 家族的 108 个唯一场景，每场景一个独立 Markdown example，并记录至少一个实际检索到的实操或创作者案例来源、查阅日期、检索词及适用范围。

#### Scenario: 查找婚礼全程
- **WHEN** 用户选择 WD04
- **THEN** 系统返回独立 example、完整仪式策略、来源及对应 Recipe，不能用婚礼精选代替

### Requirement: 热度与方法证据分开
系统 SHALL 将可见播放量、点赞或模板使用量绑定对应来源与查阅日期；没有可靠数值时标记未核验，不以搜索排名声称热门，不声称已观看只有摘要的完整视频。

#### Scenario: 教程未显示播放量
- **WHEN** 来源有教程内容但无热度指标
- **THEN** 记录方法参考和 popularity_unverified，不虚构热度

### Requirement: 可组合规划与能力门禁
系统 SHALL 通过版本化 Recipe 将场景步骤映射到已存在技能和公开 CLI capability，并区分 required、optional 与人工/模型规划。缺素材、歧义或未 supported 的必要能力必须返回明确未就绪状态。

#### Scenario: 需要原生输出但无原生能力
- **WHEN** 用户要求 native_export 且 render.native 未 supported
- **THEN** 返回 blocked_capability，不能用预览冒充最终输出

#### Scenario: 仅计划不需要配音
- **WHEN** 用户只要求无配音场景规划
- **THEN** 不因云 TTS 不可用而阻断计划，也不调用剪映或付费服务

### Requirement: 规划产物可验证且不覆盖执行契约
系统 SHALL 保持既有 job/v2 与技能入口兼容，规划输出只声称选型或预检完成。注册表、example 路径、Recipe 引用和能力 ID 必须可自动校验。

#### Scenario: 注册表引用不存在场景
- **WHEN** 数据含重复 ID、缺少 example 或未知 Recipe
- **THEN** 内容或加载验证失败，不返回成功路由

