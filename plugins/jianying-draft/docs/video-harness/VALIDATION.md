# 规划 Harness 验证记录

2026-09-21，插件候选0.18.0，新增变更 add-video-planning-harness（6/7）。

## 内容与真实分发

技能唯一源 jianying-skills；正式 immutable v2.1.0，commit 686e5e0b68e7b8cc31b853bc43b759d2c6e29ddc。
从 GitHub 全新克隆并下载 manifest，验证资产 attestation，重新生成清单与发布资产逐字节一致。
既有导入器完成14技能原子导入，包含108独立例子；不是手改托管技能副本。
默认 plan-video 入口已返回 locked_release/v2.1.0；技能完整性门禁 ready。
原子操作能力依据发布二进制1.6.13；最低版本随技能提升至1.6.13，旧版mock同步更新，版本不足拒绝测试保留。

## 执行的验证

- Python：68通过。
- Node回归：175项，171通过、4个需要额外真实环境的测试跳过；随后追加安装内容篡改测试，规划测试114项全部通过。
- 内容：108路径/来源/Recipe/能力引用校验、孤立复制技能资源自包含验证通过。
- 默认入口旅行场景TR01返回R01，evidence_level=plan、executable=false。
- 已发布二进制1.6.13握手后，108场景要求native_export均被render.native未supported正确阻断；未执行GUI或导出。
- OpenSpec严格校验、普通分发校验、git diff --check通过。

## 未通过的发布门禁

release_readiness仍为false：

- hosts.release_acceptance：新版本三宿主验收未完成。
- runtime.release_surface_rust_only：既有扫描仍报harness.mjs与validate_plugin_archive.py中的旧引擎名称；未在本次绕过或削弱门禁。

未创建插件0.18.0 tag/Release，未把候选市场清单发布给用户。市场仓原有未提交修改保留，未夹带提交。
规划测试不是108条实机剪辑验收；热度只有18个来源具备可见指标，其余90个明确未核验。
