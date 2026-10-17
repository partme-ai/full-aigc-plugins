# 上游跨机器交付验收补充

上游 [运行 37773443950](https://github.com/full-aigc-skills/printcraft-skills/actions/runs/37773443950) 绑定源提交 cb90b21920e04fbe0f65be3d0fe8619cbe33e1da。macOS arm64 发送包含 59 个文件的完整项目交付包，独立 Linux x64 和 macOS Intel 接收；三个作业均成功。

两个接收机使用固定 ArtCraft 消费者提交 4ff30a88 校验两个完整项目包、源工程与 portable plan 引用；PrintCraft 公共 handoff 校验明确允许的原 producerVersion 0.1.0-dev.113-runtime.1 和 PDF 摘要。固定原生 0.2.1 在新机器重开交付 PDF，渲染两页；单页裁剪返工后再次保存/重开，另一页像素和全部传入材料摘要保持不变。

本项目 cross-machine-collection.json 保存摘要；完整官方 Actions ZIP、日志、原始 PDF/PAM、14 项源文件和 165 个成员的摘要核验在上游 [专项报告](https://github.com/full-aigc-skills/printcraft-skills/blob/main/docs/verification/cross-machine-2026-10-08.md) 归档。原始 ArtCraft 工作流没有在接收机重新执行，任意复杂工程、手机/平板和这些平台的技能安装器/宿主路由不由该结果证明。

现有 Android USB 设备未授权，手机/平板实测 NOT_RUN，见 mobile-device-status.json；固定原生仍不支持中文 OCR。技能 7.2/7.4/7.5 和插件 5.6 保持开放。已发布 dev.5 的技能/Harness、来源锁和发行制品均未改变，本次只补作者验收与证据，不归档 OpenSpec。
