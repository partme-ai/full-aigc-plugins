---
description: 跨平台配置 MINIMAX_API_KEY（macOS/Windows/Linux 指引 + 免改 shell 的 auth 写入）
---

1. 运行 `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/minimax_video.py" check`，读出当前解析链状态。
2. 密钥申请：platform.minimax.cn（国内）/ platform.minimax.io（国际）→ 用户中心 → 接口密钥。
   网关必须与密钥同区（.cn / .minimaxi.com / .io）。
3. 按用户系统给命令：macOS 追加 ~/.zshrc；Linux 追加 ~/.bashrc；Windows setx 或 PowerShell
   SetEnvironmentVariable；**任意系统推荐** `auth --api-key sk-...`（写入
   ~/.minimax-design/credentials.json，权限 600）。
4. 也支持项目 `.env`（`MINIMAX_API_KEY=...`），优先级：环境变量 > 项目 .env > 插件 .env > 用户配置。
5. 重跑 check 确认「已设置，来源=…」。全程不回显完整密钥。
