# 上游原生平台专项验收补充

本插件继续消费已发布技能源 v0.1.0-dev.5 的正式来源锁；本次补充作者验收证据，没有修改 66 项上游技能文件或本地 Harness，也没有改写已发布插件制品。

上游 [原生专项报告](https://github.com/full-aigc-skills/printcraft-skills/blob/main/docs/verification/native-platforms-2026-10-08.md) 保存两轮真实运行：

- [37771440411](https://github.com/full-aigc-skills/printcraft-skills/actions/runs/37771440411)，8b43297a2f91ac3d286361ed9b1d92af820815bf：五平台各五场景，共 25 场景。
- [37772042337](https://github.com/full-aigc-skills/printcraft-skills/actions/runs/37772042337)，bad64e181e1b6b4e8d60e10cdb7623b6d2710d74：五平台各六场景，共 30 场景，增加固定上游模型的英语扫描件 OCR、保存后新进程读回与原件不变。

实际平台：Linux x64/arm64、Windows x64、macOS Intel/arm64。归档与 CLI 双摘要、作者程序/锁/夹具摘要、实时工具目录及模型许可/摘要均绑定。收集摘要见 native-platform-collection.json；原始 ZIP/日志/PDF/PAM 在上游报告目录与官方 Actions artifacts 保留，不将模型二进制纳入分发。

此证据直接执行固定原生 CLI，不经过本插件的安装器、任务包装器或模型路由。当前技能安装锁仍只支持 darwin-arm64；此前 Codex/模型入口证据也只对应已声明的本机环境。其他平台的插件安装、宿主路由和包装行为仍未验收。

中文仍缺固定原生识别能力，手机/平板仍未实测。上游 7.2、7.4、7.5 及插件 5.6 不关闭，不同步或归档 OpenSpec。
