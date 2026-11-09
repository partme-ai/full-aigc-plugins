# Clone-first 批量制作

## 原则

母模板永远只读。每个输出从固定模板摘要创建独立副本，再在副本中按稳定语义槽位替换文字和媒体；任何一个输出失败都不能回写母模板或其他输出。

## 批次流程

1. `template inspect` 固定模板摘要、画幅、FPS、字体、轨道、材料和可替换槽位。
2. 为每个输出分配唯一目标、幂等键和用途/许可记录。
3. `template duplicate/apply` 创建独立草稿，验证 ID 已重建且材料路径自包含。
4. 只对唯一语义 ID 或明确的 track/index 执行替换；同名歧义必须阻塞。
5. 每个输出分别执行结构验证、冷重开和目标证据，不用一个样片结果代表整个批次。
6. 失败只删除或恢复对应副本；保留批次账本、模板摘要和成功制品。

## Compound Clip 边界

Compound Clip 在发布 Rust CLI 的黑盒 capability 出现并为 `supported` 前保持 `plan_only`。不得用直接编辑草稿 JSON、Python 包装器或 GUI 宏模拟支持。
