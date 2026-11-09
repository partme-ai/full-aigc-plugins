# Verification

## Scope

本记录只证明 Dream Loop 启发的比较式质量合同和插件运行面已实现；不提升真实剪映、Windows、三宿主或正式发布状态，这些仍由既有 OpenSpec 变更跟踪。

## TDD baseline

新增 `tests/comparative_quality_loop.test.mjs` 后首次运行失败：Node 报告缺少 `scripts/comparative_quality_loop.mjs`。这证明测试从缺失行为出发，而不是在实现后补写成功断言。

## Implemented evidence

- 四个严格合同和机器 Schema：
  - `jianying-visual-reference-set/v1`
  - `jianying-comparative-evaluation-context/v1`
  - `jianying-macro-revision-request/v1`
  - `jianying-retarget-proposal/v1`
- `quality_contracts.mjs` 对所有新合同执行 unknown-field 拒绝、语义校验、执行字段拒绝和 canonical digest。
- `comparative_quality_loop.mjs` 实现目标绑定、三方比较、Critic 会话去重、只读工具白名单、单次宏观重规划和精确 Retarget 审批。
- `quality_iteration.mjs` 公开新能力；`quality_evaluator.mjs` 在评估前复核比较上下文与 EvaluationInput 摘要。
- `harness.mjs` 新增 `quality-reference-set`、`quality-comparison-context`、`quality-macro-revision`、`quality-retarget-propose` 和 `quality-retarget-apply` 命令。
- `THIRD_PARTY_NOTICES.md` 登记 Dream Loop 固定 commit、MIT 许可和无运行时依赖边界。

## Verification commands and results

```text
node --test tests/comparative_quality_loop.test.mjs \
  tests/quality_contracts.test.mjs tests/quality_iteration.test.mjs \
  tests/quality_evaluator.test.mjs tests/quality_workflow_steps.test.mjs \
  tests/quality_runtime_binding.test.mjs
```

结果：38 tests，38 pass，0 fail，0 skip。

```text
node --test tests/*.test.mjs
```

结果：323 tests，314 pass，0 fail，9 skip。9 项均为既有发布二进制、真实资源或三宿主外部门禁；本变更未新增 skip。

```text
python3 -m unittest discover -s tests -p 'test_*.py'
```

结果：77 tests，77 pass。

```text
node --check scripts/comparative_quality_loop.mjs
node --check scripts/quality_contracts.mjs
node --check scripts/quality_iteration.mjs
node --check scripts/quality_evaluator.mjs
node --check scripts/harness.mjs
git diff --check
openspec validate enhance-quality-loop-with-visual-targets --strict
```

结果：全部退出码 0；OpenSpec strict 报告 change valid。

## Negative gates

- Critic 会话复用、`write_access=true`、shell/CLI 工具和非 fresh context 被拒绝。
- 目标、参考集、当前输入、上一输入或上一 verdict 摘要错绑被拒绝。
- 未停滞时请求 Macro Revision 被拒绝；已有宏观请求后第二次请求返回 `quality_macro_revision_exhausted`。
- Retarget 缺审批、审批过期或 proposal digest 不匹配均被拒绝。
- 发行脚本扫描证明不存在 Dream Loop checkout、FAL、Python helper 或 research 路径运行时依赖。

## Remaining production boundary

本变更达到本地实现和验证 100%。插件整体仍需完成真实剪映 Vlog/课程/婚礼、Windows GUI、发布二进制黑盒、正式不可变插件 Release 和真实三宿主安装验收，不能据此设置 `production_ready=true`。

## 2026-09-23 — downstream production release evidence

- The comparison and retarget contracts shipped in immutable `jianying-draft v0.26.2`.
- The release attestation, three-platform no-Cargo canaries, isolated Codex/ZCode/Kimi fresh installs and shared released-CLI Job v2 equivalence all passed.
- Repository release readiness now reports `production_ready=true`; this changes the repository release boundary but does not manufacture the real Vlog/course/wedding or Windows GUI evidence tracked by other changes.

The scoped Dream Loop enhancement remains fully implemented and verified and is ready for specification sync and archive.
