---
description: MiniMax 能力预检：鉴权链、网关、模型、mmx CLI 状态
---

运行能力预检并向用户汇报，不做任何付费操作：

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/minimax_video.py" check
```

逐行解读输出：密钥来源（环境变量/项目 .env/插件 .env/用户配置）、网关区域、模型、mmx CLI 状态。
若密钥缺失，按输出中的分平台指引（macOS/Linux/Windows/免改 shell 的 auth 子命令）指导用户配置；
配置完成后重跑 check 确认。不回显完整密钥。
