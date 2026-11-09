# 素材操作动线

## 功能动线

| 语义动作 | 剪映入口 | 前置事实 | 执行路由 | 验证 | 恢复 |
|---|---|---|---|---|---|
| `media.import.asset` | 素材 → 导入 → 素材 | 文件存在、`media probe`、目标起点/时长 | `jianying media add-video <draft> <source> <start> [duration] --json` | `timeline segments` + `project verify` + 冷重开 | `timeline remove` 或快照恢复 |
| `media.import.subdraft` | 素材 → 导入 → 子草稿 | 两个草稿均通过 `project verify`、画布/版本已知 | 整草稿 `project concat`；指定轨道 `template inspect` 后 `template import-track` | `project diff`、ID 无冲突、冷重开 | 恢复合并前快照 |
| `media.import.official` | 素材 → 官方素材 → 搜索/筛选/下载 | 关键词、风格、画幅、用途、渠道、版型和权益 | Harness 查询候选 → 预览 → 下载 Adapter → `media official register/preflight` → 已批准应用 | 收据、素材哈希、草稿材料与片段范围一致 | 删除新增片段；下载 ambiguous 时仅查询状态 |
| `media.library.inspect` | 素材 → 我的/素材库 | 草稿路径或资源库范围 | `media materials`、`media material`、`media official list/show` | 返回稳定资源/材料 ID | 只读，无恢复动作 |
| `media.replace.asset` | 时间线片段 → 替换素材 | 目标 segment ID、新媒体探测与时长适配 | `media replace` | 材料路径、片段时长和引用完整 | 恢复快照或换回原素材 |
| `media.relink.asset` | 素材丢失 → 重链 | 候选路径唯一、媒体类型匹配 | `media relink`，必要时先 plan | 丢失路径归零、哈希/类型匹配 | 保持原路径并撤销候选 |
| `media.remove.segment` | 时间线 → 删除素材 | 精确 segment ID、材料共享关系 | `timeline remove`，按需保留轨道/材料 | 片段消失且无悬空引用 | 快照恢复 |
| `media.analyze.scenes` | 素材 → 场景分析 | ffmpeg 可用、真实时长 | `media scenes` / `media retakes` | 切点位于素材范围，保留分析参数 | 只读，无恢复动作 |

## 筛选顺序

官方素材按“用途与渠道许可 → 基础/专业版权益 → 画幅/时长 → 主题与风格 → 成本 → 排名”筛选。没有授权证据的候选只能预览，不能写入生产草稿。

## 路由原则

固定 Rust argv 优先于原生控制；原生控制优先于可访问性 Adapter。仅能识别视觉位置且无法回读资源 ID 时停止，要求当前剪映版本 Canary。
