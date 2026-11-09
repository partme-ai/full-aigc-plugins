# 统一路由参考

## 决策表

| 用户目标 | 首选入口 | 最低完成证据 |
|---|---|---|
| 查看环境或草稿 | `doctor`、`media probe`、`project inspect` | structural |
| 新建或编辑草稿 | `job run --json` | structural，随后按需冷重开 |
| 批量执行 | `job batch --json` | 每个子任务独立结果 |
| 代理预览 | `render proxy` / `render batch` | proxy artifact |
| 原生 MP4 | `render.native` capability + 精确批准 | native_export |
| 失败恢复 | `job show/audit/retry` 或 `store restore` | 恢复后重新验证 |

## 停止条件

- capability 不是 `supported`。
- 输入素材不存在或探测失败。
- 目标草稿可能包含用户修改而工作流准备覆盖它。
- 付费 ASR/TTS、启动编辑器或原生导出缺少精确批准。
- 只有结构测试，却被要求证明真实剪映播放或导出。

## 输出摘要

报告所用 CLI 版本、task ID、输出路径、实际证据等级、尚未完成的宿主验证；不要把
`partial` capability 改写为“基本支持”。
