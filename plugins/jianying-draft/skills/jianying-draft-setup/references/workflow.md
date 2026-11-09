# 环境诊断参考

## 就绪层级

1. CLI 存在且版本可解析。
2. capability manifest schema 可识别，所需 ID 为 `supported`。
3. ffprobe/ffmpeg 和目标草稿根可用。
4. 配置 profile 通过 schema 校验。
5. `runtime discover` 只读识别安装、executable 身份和草稿根；`drafts_without_editor` 表示只有
   历史草稿而没有可用应用，发现结果一律 `unverified/automatic_routing=false`。
6. Runtime Profile 精确识别产品、版本、平台和文件身份。
7. 真实剪映 canary 通过后，才能报告 app-open/playback/native-export 证据。

## 常见恢复建议

- CLI 缺失或哈希错误：停止，要求从已验证制品重新安装。
- 版本过旧：报告最低版本；不要在诊断中自动升级。
- 剪映正在运行：涉及草稿写入时停止；只读命令仍可继续。
- Runtime Profile 未支持：保持 fail-closed，允许代理预览，不伪装成原生导出。
- 仅发现草稿根：报告 `drafts_without_editor`；不猜测应用路径、不自动下载安装编辑器。
- 配置损坏：先展示 `config file` 和 `config validate` 诊断；修改需要单独批准。
