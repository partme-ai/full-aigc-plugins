# 比较式视频质量循环实施任务

只有实现和对应验证均通过后才勾选。本变更不重复真实剪映、Windows、三宿主和发布任务。

## 1. 规格与失败基线

- [x] 1.1 登记 Dream Loop 设计来源、MIT 边界和禁止运行时依赖范围。
- [x] 1.2 为四个新合同建立缺实现、未知字段、执行字段和摘要错绑失败测试。

## 2. 视觉目标与比较上下文

- [x] 2.1 实现 `jianying-visual-reference-set/v1` Schema、语义校验和规范化摘要。
- [x] 2.2 实现 `jianying-comparative-evaluation-context/v1` Schema，绑定目标、当前、上一版和上一 verdict。
- [x] 2.3 强制全新 Critic 会话、只读工具白名单和无写入权限。
- [x] 2.4 验证目标或引用变化会改变摘要并拒绝旧上下文。

## 3. 停滞重规划与 Retarget

- [x] 3.1 实现 `jianying-macro-revision-request/v1`，仅接受已验证停滞和注册策略。
- [x] 3.2 实现每个输出最多一次 Macro Revision，第二次停滞进入人工评审。
- [x] 3.3 实现 `jianying-retarget-proposal/v1` 及精确、未过期的人工批准门禁。
- [x] 3.4 Retarget 生效时返回旧批准、context、verdict 和 evidence 的确定性失效集合，不直接写草稿。

## 4. 集成与验证

- [x] 4.1 将比较上下文和宏观重规划接入现有质量迭代模块，不改变旧入口默认行为。
- [x] 4.2 运行新增测试、现有质量循环测试和完整 Node 回归。
- [x] 4.3 运行发行依赖扫描，证明无 Dream Loop/FAL/Python/research 运行时依赖。
- [x] 4.4 OpenSpec strict 通过并记录验证证据。
