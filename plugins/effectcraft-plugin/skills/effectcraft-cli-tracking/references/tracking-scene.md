# 镜头跟踪与图形附着 / Shot tracking and graphic attachment

适用于将标题或品牌图形附着到运动主体，或稳定镜头。先提供真实视频、合成、跟踪源图层、目标图层、分析时间段和需要跟随的属性。稳定源画面与驱动目标图形是不同任务；不默认同时改变两者。

Use for attaching graphics to moving footage or stabilizing a shot. Establish source and target layers, the analysis interval and the properties to track. Stabilization and driving a graphic have different targets.

## 参数选择 / Parameter choices

| 阶段 / Stage | 命令 / Command | 决策 / Decision |
| --- | --- | --- |
| 建立跟踪器 | `track.new` | 核对 `layer`、`target` 和 `kind`；按任务选择 transform、stabilize、affine、perspective 或 raw |
| 选择已有跟踪器 | `track.select` | 使用实际 uid、名称或 #n；不要将其他工程的编号套入当前工程 |
| 特征区域 | `track.setPoint` | `point` 从 1 开始；记录中心、特征区和搜索区，`time` 是秒 |
| 分析策略 | `track.options` | 按素材选择 rgb/luminance/saturation；确认低置信度时 continue/stop/extrapolate/adapt 的实际意图 |
| 分析范围 | `track.analyze` | `start`、`end` 是秒；核对 forward/backward/frameForward/frameBackward 和 `wait`，等待分析完成后再应用 |
| 目标绑定 | `track.setTarget` | 确认实际 target 图层；null 的含义按原生合同处理 |
| 应用结果 | `track.apply` | 明确 xy/x/y；检查实际目标关键帧与运动，不把分析成功当成应用成功 |

Exact parameters are in `command-reference.md`. Point indices are 1-based and analysis times use seconds. Check the chosen low-confidence policy before analysis; wait for completion before applying the track.

## 使用顺序 / Workflow

打开合成并检查源素材 → 保存检查点 → 查询 `track.*` 参数与当前 enabled → 建立/选择跟踪器 → 设置特征和搜索区域 → 运行限定时间段的分析 → 检查漂移和遮挡 → 绑定目标并应用 → 保存新 `.ecproj` → 重开并渲染目标时间段。

按本技能 `command-usage.md` 构造计划，先 check 再 run。分析超时或连接中断时先检查原任务状态；不能直接重放分析或 apply。没有活动合成时先打开正确工程，不能把禁用解释成 CLI 安装失败。

Open the correct composition, preserve a checkpoint, inspect live availability and analyze the bounded interval. Review drift before applying. Reconcile running analysis after a timeout rather than replaying it.

## 返工与交付 / Revision and delivery

修改文字内容时保留已确认的跟踪关键帧；修改跟踪区间或特征点时重新核验受影响帧。交付 `.ecproj`、源视频/图形依赖、参数记录和渲染结果；检查开始、中间、遮挡及结尾帧的附着误差，确认非目标图层与动画未变。透明输出需另核验 alpha，不用黑底预览替代透明验收。

Preserve tracking keys when changing text. Revalidate affected frames when changing tracking settings. Deliver the native project, dependencies, parameter records and render; inspect attachment at occlusion and interval boundaries. Full tracking-command execution acceptance remains open.

## 已执行实例 / Executed example

`examples/tracking-create.json` 通过 `--input shot=/absolute/shot.mp4` 导入源视频。创建目标空对象后必须显式 layer.select 选择源视频，再建立跟踪器；传 layer 参数不能替代当前选择前置。样例是128×96、12fps、一秒，需要适配真实素材。`examples/tracking-reopen.json` 使用 `--input project=/absolute/project.ecproj` 重开并渲染，通过本技能 commands.py run 执行，使用新输出目录。已核验11个分析帧、12个应用关键帧及重开关键帧一致；播放头不同会改变属性当前求值，不应误报关键帧损坏。

Explicitly select source footage after creating the target. Adapt the local create/reopen fixtures and input paths. Compare saved keyframes separately from properties evaluated at different playhead times.
