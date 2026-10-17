## Purpose

定义插件本地薄 Harness 对宿主任务、执行状态和 PDF 验收的呈现与交接，消费独立技能源的版本化契约，避免在插件中复制参数、运行时和文件修改逻辑。

## ADDED Requirements

### Requirement: HO-01 薄 Harness 与契约消费

系统 SHALL 提供声明为插件本地的 printcraft-harness，路由六项上游技能、调用其公开执行/验收入口，验证消费协议版本；公共执行和 PDF 规则以技能源变更为唯一事实源。

#### Scenario: 缺失或不兼容执行能力
- **WHEN** 对应上游资源或协议版本不可用
- **THEN** 报告依赖/兼容缺口，不复制私有函数或借工作区兄弟目录绕过。

#### Scenario: 常规 PDF 请求
- **WHEN** 宿主收到页面编排任务
- **THEN** Harness 选择对应技能并展示任务身份、状态与产物证据，不新增另一套页码或保存规则。

### Requirement: HO-02 状态呈现和恢复边界

系统 SHALL 分别展示执行、产物、重开、内容审阅状态；继续任务时消费同一 runId 的对账结果，保留 UNKNOWN/部分成功，不自动创建新任务重放。

#### Scenario: 恢复未知任务
- **WHEN** 用户要求继续且上游回执为 UNKNOWN
- **THEN** 先展示并调用只读对账，未核实副作用前不重新提交。

#### Scenario: 零退出未验收
- **WHEN** 执行结果为零退出但没有有效 PDF 验收记录
- **THEN** 显示待验收，不能宣称任务完成。

### Requirement: HO-03 授权复用和修订交接

系统 SHALL 保留已确认输入、目标、修改范围及授权；只有新增覆盖/打印/安装等超范围影响才询问。定向返工关联失败项及新候选身份，不复制 Dreamina 积分审批或远端 submitId 机制。

#### Scenario: 已有授权内继续
- **WHEN** 用户已授权同一工作副本的页面修订
- **THEN** 在范围内继续，不逐步重复确认；新文件仍须通过上游验收。

#### Scenario: 新增外部副作用
- **WHEN** 输出 PDF 任务变为真实打印或覆盖受保护原件
- **THEN** 执行前说明新增影响并取得授权，不将先前导出授权视为通用授权。

### Requirement: HO-04 显式外部 OCR 薄适配

系统 SHALL 将 ocr 意图路由至 printcraft-use，公开 `harness.py ocr diagnose/run` 原样委托包内 ocr.py，不复制身份或识别逻辑；show 支持 printcraft.ocr/1 的合法状态、runId、后端身份及产物。该协议不能声称 VERIFIED 或 completeAcceptance=true。

#### Scenario: 外部 OCR 未知结果
- **WHEN** show 消费外部 OCR 的 UNKNOWN/FAILED_OR_PARTIAL 回执
- **THEN** 展示只读查看与产物对账，不调用不兼容的 commands.py reconcile，不自动重放。

#### Scenario: 兼容升级
- **WHEN** dev.5 的核心 execution/verification 契约升级到带已知可选 ocr/ocrBackend 契约的 dev.6
- **THEN** 保持旧任务数据，已知可选协议允许增量扩展；未知字段/协议或核心版本变化拒绝升级，不自动迁移。
