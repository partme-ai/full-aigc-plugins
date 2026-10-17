# Windows Craft CLI 业务回归

入口：`.github/workflows/craft-cli-windows.yml`。Windows Server 2022 x64 上直接调用真实 `*-cli.exe`，不使用 MCP、浏览器、模拟 CLI 或 macOS 结果替代。每个操作通过独立 subprocess 执行；中文与空格运行目录、中文输出文件名、Unicode 参数均进入测试。

## 固定运行时与范围

`scripts/ci/craft_cli_windows.lock.json` 记录官方 Windows x64 portable ZIP 的版本、URL 和 SHA-256。ZIP 内包含原生 CLI；并非只有独立命名的 CLI ZIP 才能提供 Windows CLI。保留 portable 包相邻运行资源，不单独搬走 exe，不修改官方代码。

| 插件 | 官方 CLI 版本 | 业务操作与断言 |
| --- | --- | --- |
| CADCraft | 0.7.0 | 创建圆、保存 DXF、新进程检查实体数量、导出 SVG |
| DesignCraft | 0.8.0 | 创建中文文字框、保存工程、新进程导出 IDML 并检查 Story 文字 |
| EffectCraft | 0.10.0 | 创建合成与纯色层、修改透明度、保存后新进程读取透明度 25 |
| PhotoCraft | 0.9.0 | 创建画布、中文图层与笔画、重开检查图层及几何、导出 PNG 尺寸 |
| FigCraft | 0.6.0 | SVG 图形导入原生工程、重开导出 SVG、检查填色保留 |
| FilmCraft | 0.8.0 | 添加中文素材箱、保存重开、第二次编辑后再重开核对 |
| LightCraft | 0.8.0 | 导入测试图、调整曝光、导出 JPEG、新进程读取持久照片库曝光 |
| PrintCraft | PdfCraft 0.8.0 | 修改 PDF 标题与旋转、重开检查标题、提取页面 |
| VectorCraft | 0.12.0 | 创建画板与椭圆填色、保存重开检查画板、SVG 检查填色 |
| DeckCraft | 0.7.0 | 创建带中文标题幻灯片、保存重开、导出 PPTX 并检查 slide XML |
| SoundCraft | 0.7.0 | WAV 重采样与归一化、新进程检查采样率、独立解析 WAV 样本幅度 |
| GridCraft | 0.7.0 | 设置数值与公式、保存 XLSX、新进程检查值 42 和公式、CSV 中文保留 |
| WordCraft | 0.7.0 | 插入中文文本、保存 DOCX、新进程读取文本、导出 PDF |

每个作业保存 `calls.json`（实际 argv、退出码、stdout/stderr）、`result.json`（运行平台、归档/二进制摘要、结果）及测试工程/导出文件。所有断言必须通过才报告 PASS，退出码 0 不单独代表业务通过。

## PhotoCraft 保存名称契约

首次 Windows 执行发现旧断言不适用于官方 0.9.0：Save As 将文档名更新为输出文件名，图层和笔画并未丢失。依据[该版本官方 files.rs](https://github.com/storytold/photocraft/blob/v0.9.0/crates/automation/src/files.rs) 的 `named_for_output` 修正名称断言，同时检查中文图层、尺寸和笔画边界；图层缺失或空笔画仍失败。未改写官方程序。

## 验证边界

这组测试覆盖表中 13 条业务路径，不表示全部命令、所有导出格式、Windows ARM64/x86 或真实桌面 UI 都已通过。既有插件包的旧版技能 bootstrap/harness 锁与本次官方 CLI 锁是不同入口；本矩阵不自动升级那些旧锁，也不能证明旧技能安装器已经支持 Windows。宿主内嵌编辑同步仍由独立宿主验收负责。

## 实测结果（2026-10-16）

- [业务矩阵 38919319402](https://github.com/partme-ai/full-aigc-plugins/actions/runs/38919319402)：13/13 通过，共 52 次原生 CLI 进程调用（其中 13 次为版本检查）。
- 同提交 [安装与原生 MCP 矩阵 38919319215](https://github.com/partme-ai/full-aigc-plugins/actions/runs/38919319215)：12 项回归测试与 13/13 安装调用通过。
- 执行代码提交：`a898152`；各官方运行时版本与摘要见固定锁文件。失败首轮保留于 [38918983837](https://github.com/partme-ai/full-aigc-plugins/actions/runs/38918983837)。
