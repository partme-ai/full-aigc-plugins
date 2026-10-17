# VectorCraft 技术评审接入

`node src/cli.ts review-checked DATABASE REQUEST.json` 读取与旧评审请求相同的身份、原生工程、候选、目标、rubric、交换损失和授权字段。授权还须包含 `readRoots`、`writeRoots`；候选必须属于同目录 `manifest.json` 声明的导出。数据库目录下 `.technical-checks/` 保存只读副本和结果，须位于允许写入的根目录。运行环境使用 Python 3、Pillow 和 PyMuPDF；缺少解码器时返回 NOT_RUN。

共享预算在复制与启动进程前持久化，字节预留包含副本和1 MiB报告上限；超时停止已确认身份的自建进程组。相同请求复用记录，不重置预算；未知结果返回 reconcile_required，保留记录供人工核验，尚无自动恢复重放。检查完成及回执导入时重新核对全部清单文件、brief、rubric、交换损失和检查器摘要。

技术失败返回 technical_failed／blocked；未执行返回 technical_pending／pending。工程重开仍为 NOT_RUN，健康解码加视觉接受也只能 pending。旧 `review-request` 兼容但标记 caller_unverified，不能注入 checked-decoder 证据；回执独立性仍需真实宿主证据。`revision` 只返回经授权的问题修订建议，不自动执行下一轮。

```mermaid
flowchart LR
  A[请求与全部源文件] --> B[持久化共享预算]
  B --> C[不可变副本真实解码]
  C --> D{进程与结果确定}
  D -->|未知或超时| E[停止自建进程组并保留待核验记录]
  D -->|已核验| F[绑定技术证据的评审请求]
  F --> G[当前文件指纹复核]
  G --> H[人工或宿主回执]
  H --> I[技术失败阻断 或 待接受与修订建议]
```

6.1已有5项检查器测试。6.2接入通过4项新增测试及两条入口各健康／损坏共4项持久检查，复用此前固定38／源35生成的导出副本；高评分回执为自动注入的测试数据，不代表真实创作判断。本轮没有重新生成原生工程，6.3完整原生工程／创作验收及最大轮数、停滞和最佳版本合同继续开放。[接入证据](evidence/vectorcraft-checked-review-candidate-20261008.json)，[此前独立检查器证据](evidence/vectorcraft-technical-quality-candidate-20261008.json)。


公开提交固定副本验收：从远端main的完整不可变提交`11a49e9d1d5f471d1c4cbf93551bdb1c87abe3d1`安装dev.64/source46到独立、含空格的Codex0.153.4配置；13技能发现与身份匹配，13次独立HTTPS空缓存启动、12组原生创建／返工通过，setup-only单独标记，不计作跳过。实际安装Harness完成原生返工、三格式重新解码、4次共享额度停止及源／文本保全；回执评分为显式QA夹具。5项引用守卫及161项Python回归通过。新脚本默认仍要求公开版本标签；显式候选只允许与远端main相同的完整SHA，并记录publicTagVerified=false。旧脚本原字节已归档，旧报告不重签。此证据推进9.9／9.18的安装与冷启动部分，不关闭模型默认路由、公开标签复验、六层发行门禁、全命令GUI或秘密边界；121/127完成、6项开放。 [Evidence](evidence/vectorcraft-public-commit64-install-20261009.json).


当前固定副本四场景复验：dev.64/source46公开提交安装上，6次原生修订、15项守卫及拥有签名桌面的源工程修改／保存／重开后陈旧建议拒绝通过；最佳候选、轮数、停滞、额度与文本保全按VC-QA-002核验。桌面初次夹具越界被正确拒绝，调整为测试拥有的GUI根内工程后通过，产品权限未放宽。证据v2解析已绑定checker_bundle.ts的完整10文件身份；发布门禁核验所选当前报告，旧v1三文件证据与原脚本归档保留。当前六层开发发行门禁通过，市场资格仍为false；公开标签后的安装复验、模型路由、权限／秘密完整边界及逐命令GUI仍开放，121/127完成、6项开放。回执评分为QA夹具，不代表真实创意评审。 [Evidence](evidence/vectorcraft-revision-commit64-20261009.json).


公开标签发布后复验：插件v0.1.0-dev.64已发布，标签指向6763caa1f0e6596fc01d298304794d0e9c139dc3，固定独立技能源v0.1.0-dev.46。从公开标签安装到全新Codex0.153.4隔离配置，13技能身份一致；13次独立HTTPS空缓存启动、12组原生创建／返工通过，setup-only单列，零跳过。安装产品源码与发行前四场景副本逐文件一致，main／tag共4个CI运行通过。已完成且无句柄的13个测试运行时缓存被清理，原生工程和执行记录保留。此结果补齐9.18的公开发行及实际安装／冷启动部分；其9.9真实模型默认路由等前置仍未完成，不关闭9.18。权限／秘密完整边界、全命令GUI、其他平台与完整V1不提升；121/127完成、6项开放。 [Evidence](evidence/vectorcraft-public-tag64-install-20261009.json).
