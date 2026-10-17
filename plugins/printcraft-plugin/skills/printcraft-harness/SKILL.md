---
name: printcraft-harness
description: 用户在 PrintCraft 插件内需要多阶段 PDF 编排、任务状态与产物展示、UNKNOWN 对账或定向修订时使用；薄适配上游六项技能和版本化协议，不重写原生执行器。
license: Apache-2.0
---

# PrintCraft 插件编排

将 PLUGIN_ROOT 设为宿主实际加载的插件目录；不要使用开发工作区路径。
一般任务使用 **printcraft-use**，环境使用 **printcraft-cli-setup**，检查使用 **printcraft-cli-inspect**，页面处理使用 **printcraft-cli-pages**，批处理和恢复使用 **printcraft-cli-automation**，专项工具使用 **printcraft-cli**。用户显式指定时直接进入该技能，不强制经过 Harness。

```bash
python3 -I -B "$PLUGIN_ROOT/skills/printcraft-harness/scripts/harness.py" route pages
python3 -I -B "$PLUGIN_ROOT/skills/printcraft-harness/scripts/harness.py" delegate status "$TASK_DIR/receipt.json"
python3 -I -B "$PLUGIN_ROOT/skills/printcraft-harness/scripts/harness.py" show "$TASK_DIR/receipt.json"
```

公开 delegate 支持 list/describe/check/run/status/reconcile/verify，参数原样按 argv 交给包内上游公开入口。执行由上游负责，本 Harness 不直接调用二进制或实现重试。

消费 printcraft.execution/1、printcraft.verification/1 和独立 printcraft.ocr/1；未知/缺失协议拒绝。STARTED、UNKNOWN、部分失败只能只读对账；零退出仍待产物与视觉验收。不用换 runId 绕过恢复约束，doc ID 不能跨进程复用。

复用既有授权；仅新增原件覆盖、真实打印或外部范围才确定新授权。候选摘要或规则变化使旧审阅失效。定向修订创建独立候选和验收请求，不自动重放整条链、不无限循环。

单个上游技能独立安装：`npx skills add full-aigc-skills/printcraft-skills --skill <技能名>`。本插件已带完整快照，安装后不需要技能源仓库。

跨插件文件先经 `harness.py delegate handoff "$HANDOFF_JSON" --producer-version "$EXPECTED_ARTCRAFT_VERSION"` 只读核验，再按已授权范围登记 PDF 输入；兼容版本从已确认生产者配置取得。核验不会自动运行 PDF 编辑。


显式中文 OCR：意图 `ocr` 路由 printcraft-use，契约见包内该技能 references/ocr.md。使用下列薄入口，参数与上游 ocr.py 相同，不经 commands.py：

```bash
python3 -I -B "$PLUGIN_ROOT/skills/printcraft-harness/scripts/harness.py" ocr diagnose --backend tesseract --language chi_sim --tesseract "$TESSERACT" --tessdata-dir "$TESSDATA_DIR" > "$BACKEND_LOCK"
python3 -I -B "$PLUGIN_ROOT/skills/printcraft-harness/scripts/harness.py" ocr run --backend tesseract --language chi_sim --backend-lock "$BACKEND_LOCK" --input "$ORIGINAL_PDF" --output-dir "$NEW_TASK_DIR" --runtime-home "$RUNTIME_DIR" --rasterize
python3 -I -B "$PLUGIN_ROOT/skills/printcraft-harness/scripts/harness.py" show "$NEW_TASK_DIR/receipt.json"
```

该路径须显式授权栅格化新副本；不保留原签名/表单等语义，不安装外部依赖。外部 OCR 回执只读查看与检查实际产物，不交给 commands.py reconcile。show 永不把外部 OCR 提升为 VERIFIED/completeAcceptance。原生中文仍不支持；简繁 TXT 识别与图像检查不代表 PDF 阅读顺序、长句搜索或 GUI 阅读器通过。实际有原生字序/搜索限制，保持待审阅，按业务要求核对。
