# 插件 dev.6 显式中文 OCR 验收

从已发布技能源 v0.1.0-dev.6 / d0085f028232ba27112ad65cd967be150d705bf7 下载官方发行归档，校验 GitHub 资产摘要、远端 tag/commit、suite 摘要及 78 项技能文件；保护旧快照后同步，保留本地 Harness。来源实证见 remote-source-dev6.json，离线 validate_package 不代替该远端证据。

插件新增薄 Harness `ocr diagnose/run` 与 `ocr` 路由，委托包内公开 ocr.py；show 消费独立 printcraft.ocr/1，禁止 VERIFIED/completeAcceptance。更新检查保留原核心 execution/verification，接受已知可选 OCR 协议，未知/不兼容仍拒绝。未知 OCR 回执只读查看及检查实际产物，不传给原生计划 reconcile。

18/18 插件单元回归通过，包括新增适配/协议兼容红绿测试。另通过插件内独立 ocr.py 实际执行简繁各两页扫描，原件为空文本，TXT 12 行目标正确、新原生重开、图像像素一致、输入及资源/后端不变。真实 Harness 委托繁体并 show 的状态/协议/不重放/不升级验收断言通过。实际命令、当前资源摘要、回执和产物见 external-ocr/collection.json 与对应归档。

完整技能源专项证据与独立使用验证：[源报告](https://github.com/full-aigc-skills/printcraft-skills/blob/d0085f028232ba27112ad65cd967be150d705bf7/docs/verification/external-ocr-2026-10-08.md)。固定原生 0.2.1 仍不支持中文。当前外部组合仅 macOS arm64 / Tesseract 5.5.3 / tessdata_fast 4.1.0。

**PDF 字序错误与长句搜索不可靠仍存在。** 繁体“合同金額”原生提取成“合金同額”，短词“驗收”可命中两页，金额整句等不命中；TXT 正确不等于 PDF 全文搜索正确。GUI 阅读器搜索/选择未验收。结果保持 REVIEW_REQUIRED，视觉图像审阅与文字/搜索结论独立。栅格化不保留表单、签名等原语义。该受控预发布不承诺任意识别质量、可靠长句搜索或生产通过。

技能源 7.2 按语言/模型矩阵与独立真实证据完成；手机/平板真机仍 NOT_RUN。插件 5.6、技能源 7.4/7.5 保持开放，未同步主规格或归档。宿主公开安装/模型证据按发行版本单独记录，dev.5 历史不用于宣称 dev.6 实际路由通过。
