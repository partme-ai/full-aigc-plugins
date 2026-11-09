# Job/Plan 参考

## 操作选择

| operation | 用途 | 关键字段 |
|---|---|---|
| create | 新建草稿 | `project.type=new`、`project.project` |
| edit | 隔离编辑已有草稿 | `project.type=existing`、`source`、`output` |
| inspect / verify | 只读检查 | `project.type=existing`、`source` |
| publish | 登记草稿 | 已验证的工作副本和精确批准 |
| export | proxy/native/archive | `export.kind/output/overwrite` |
| batch | 多任务 | `jobs[]`，每项仍是完整 v2 Job |

## 时间与引用不变量

- `start_us`、`duration_us` 非负，duration 大于零。
- 片段 `material_id` 必须解析到同类型素材。
- 主视频轨按目标时间有序且不产生意外间隙或重叠。
- source range 不得超过探测到的素材时长。
- 帧量化有不安全偏移时停止，不静默舍入。

## 验证顺序

Schema → capability → 素材事实 → Job dry reasoning → `job run --json` → `project verify --json` → 按目标执行 cold-reopen/playback/native-export。
