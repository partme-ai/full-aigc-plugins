# 分段透明动画：生产、恢复与交接

`scripts/segmented_sequence.py` 与公开 `workflow.py` 均随 effectcraft-harness 技能分发。先从本技能 runtime.lock.json 和实际安装回执读取固定 CLI 身份；不要套用历史候选版本。公开工作流支持 `png-segmented`，Film 的 `--segmented-sequence-asset` 与 Art 的类型化素材绑定可消费其已验证检查点。单段仍受 512 MiB 解码预算约束；普通 v1 序列与分段检查点不可混用。

已有原生工程与从 native.json 提取的 composition.json 时：

```bash
python3 -I -B "$HARNESS_DIR/scripts/segmented_sequence.py" --project /absolute/project.ecproj --composition /absolute/composition.json --output /absolute/segments --chunk-frames 60
```

以实际加载的技能目录设置 SKILL_DIR。入口自动安装及核验固定 CLI。相同参数再次调用会重新核验已有段，仅重跑坏段；原生版本、工程或设置改变时用新目录。不要改动 checkpoint.json、verified.json 或完成段。失败不是交付完成；segments.json 必须通过分段专用入口交接，不能传给 --sequence-asset。

分段生产核验透明 RGBA、精确帧范围、像素与文件摘要、源工程及安装技能保全；技术通过不自动判断创作质量。当前固定发行的实际能力与验收版本见包内 README 和发行证据，不能把历史候选记录当作本次执行证明。

## 首次公开工作流

以本技能 examples/brand-intro.json 为基础，计划内把 document 的 width、height、frameRate、duration 分别设为1920、1080、24、5，并设置：

```json
{"exports":[{"format":"png-segmented","chunkFrames":32}]}
```

其他图层和关键帧操作仍取原模板或实际命令参数。执行时以实际加载的 SKILL.md 目录设置 SKILL_DIR：

```bash
python3 -I -B "$HARNESS_DIR/scripts/workflow.py" /absolute/intro-plan.json --output /absolute/intro --runtime-home /absolute/craft-runtime
```

交付包含 project.ecproj、native.json、manifest.json、rgba-segments/segments.json、checkpoint.json、verified.json 及完整段内PNG和清单。1920×1080／24fps／5秒生成120帧；chunkFrames32生成全局起点0、32、64、96的四段。不要按段丢失全局时刻或将首帧当作完整动画。单帧超限、绑定冲突或并行占用须先排除原因；不要删除锁以抢占仍运行的任务。

文字返工传 --source /absolute/intro 与 expectedProjectSha256，仅修改绑定的 title.layer，保留其他动画，使用新输出目录及同样 png-segmented 导出。直接生产器的同绑定重复调用先复验已完成段，仅重跑坏段；新工程或设置使用新目录。

交给 **filmcraft-cli-media** 技能。安装：`npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。交给 Art 时使用 image-sequence MIME、rgba-segments/segments.json 与完整产物摘要，不把它标成普通JSON或MP4。保留未知色彩空间说明、全部依赖、原生工程和独立成片核验。
