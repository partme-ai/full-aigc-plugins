# 规划与执行交接

目标渠道 → 用途/场景候选 → 选择场景 → 素材盘点 → Recipe → 人工编辑判断 → 能力预检 → 用户确认 → 确定性 Job → 隔离执行 → 分级验证。

## 正常路径

用户要旅行 Vlog：读 TR01，确认发布渠道和素材路径，给出旅程主线与缺失的转折/收尾镜头。使用真实 probe 结果形成入出点后，才交接 draft/edit。

## 缺少信息

只说婚礼视频：WD01 预告、WD02 当日快剪、WD04 完整仪式的素材、时效和验收不同。先给候选，不要求用户掌握全部术语。

## 门禁

仅 plan 不因 native/TTS 缺失被拒绝。structural 检查 Recipe 原子能力与 Job 能力；proxy_preview 另需 render.proxy；native_export 另需 render.native/runtime.profile/runtime.status 及授权和真实验收。必要能力 partial 或 external_dependency 不视为 supported。

插件 read-only planner 只做选型与预检，不读取视频理解语义、不填时间码、不调用模型、也不执行 Job。其 planned 状态仅表示可继续规划。
