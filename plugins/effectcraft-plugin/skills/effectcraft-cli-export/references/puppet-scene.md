# 木偶与局部变形动画 / Puppet deformation

## 输入与前置状态 / Input and state

输入为目标图层、变形区域、锚定区域、动画时间与交付范围。先建立或打开合成，导入真实素材或建立可渲染图层；Puppet支持素材、纯色、文字、形状、预合成图层。显式 layer.select 后查询 puppet.info，不把控制用空对象当作可变形素材。position 是图层空间[x,y]，不是合成空间；time为秒，frame为帧，按合成帧率对齐，图层时间还受其时间变换影响。不要猜测图层、网格或针脚ID。

Use an actual renderable layer and its returned ID. Pin coordinates are in layer space. Time in seconds and frame numbers are distinct; composition and layer timing must be checked.

## 场景与命令 / Tasks and commands

| 场景 | 命令 | 步骤与核验 |
| --- | --- | --- |
| 建立锚定和可动针脚 | `puppet.addPin` | 指定目标layer、kind及position；记录返回fx、mesh、pin。第一次建针会创建Puppet效果，后续针是否加入原网格需核对，不直接用newMesh制造重复网格 |
| 制作位置动画 | `puppet.movePin` | 使用实际pin与图层；在不同time/frame设置位置，检查关键帧和变形结果。固定针与移动针分别记录 |
| 高级形变与刚度 | `puppet.setPin` | scale为百分比、rotation为角度、extent为像素；支持的字段取决于针脚kind，查询后设置。starch/overlap与position/advanced/bend不是同一种动画能力 |
| 网格密度与覆盖 | `puppet.mesh` | 指定实际mesh并调整density、expansion、triangles；检查透明边界、覆盖区域和变形质量。showMesh仅控制显示，不证明导出成功 |
| 选择与检查 | `puppet.selectPins`、`puppet.info` | 提供实际pins，[]取消选择，add/toggle改变选择集合；info检查针脚、网格和指定时间。操作前后分别核对，不依赖未知旧选择 |
| 录制手动运动 | `puppet.recordOptions`、`puppet.recordPin` | samples中的t为拖动开始后的秒，start是合成起点；speed百分比和smoothing影响结果。先设置并记录选项，再提交samples，验收实际关键帧和运动时长 |
| 延迟跟随 | `puppet.follow` | 明确leader、跟随pins、delay秒、amount百分比和cascade；只修改授权针脚，检查延迟、位移和其他针脚未变 |
| 删除针脚 | `puppet.removePin` | 指定pin/pins，先另存工程；检查删除范围和剩余网格、针脚及关键帧，不把默认选中集合当成目标范围 |

Describe each command before constructing a plan. Returned IDs identify created objects. Mesh display, keyframe presence and rendered deformation are separate acceptance checks.

## 查询、执行与交付 / Query, execute and deliver

```bash
python3 -I -B "$HARNESS_DIR/scripts/commands.py" list --filter puppet.
python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe puppet.addPin
python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe puppet.recordPin
python3 -I -B "$HARNESS_DIR/scripts/commands.py" check /absolute/puppet-plan.json
python3 -I -B "$HARNESS_DIR/scripts/commands.py" run /absolute/puppet-plan.json --output /absolute/new-puppet-result
```

使用本技能command-usage.md的计划合同；创建针脚返回值通过$ref连接下一步，同会话保存.ecproj。交付原生工程、素材、参数记录和需要的透明或视频渲染。重开后检查原始针脚ID、关键帧及目标时刻的实际渲染；局部返工保留锚定针与其他动画。禁用项先核对活动合成、选择和针脚状态；未知结果先检查原任务，不重复录制或删除。

## 验收边界 / Acceptance boundary

本指南将10条命令组织为场景操作；原生实现参考commands/puppet.rs的图层验证、网格和针脚属性变更。目录与计划检查不等于网格质量或全部针脚类型及交付验收。

All10 commands have task guidance; full deformation quality, pin kinds and delivery acceptance remain separate runtime checks.

## 已执行代表实例 / Executed representative example

`examples/puppet-create.json` 不需要外部素材，建立96×64、12fps合成和64×48红色纯色图层，在图层空间[16,24]、[48,24]建立position针脚，通过返回moving.pin在0.5秒移动第二针到[48,8]。创建后渲染0和0.5秒，保存project.ecproj。`examples/puppet-reopen.json` 接收 `--input project=/absolute/project.ecproj`，查询Deform subject图层在0.5秒的木偶状态并渲染。两个计划均使用本技能commands.py run和新输出目录。真实工程必须适配图层名称、尺寸、坐标、动画范围和稳定锚点。

实例已核验一网格两针脚、帧像素变化、原生重开后木偶状态相同且渲染像素一致；不代表变形质量、全部针脚类型、录制和跟随命令已验收。

This self-contained fixture proves a rendered change and native reopening identity for two position pins. Adapt layer geometry and anchors for real artwork; production deformation quality remains a separate review.


## 录制、跟随与局部返工 / Recording, follow and revision

本技能自带三个无需外部素材的命令计划。创建实例建立 96×64、12 fps、2 秒合成，蓝色可变形主体和绿色非目标控制图层；建立 Position 锚点与运动针、Advanced 跟随针和临时 Starch 针。所有创建后操作用实际返回的 layer、mesh、pin ID。删除临时针前保存 rigged.ecproj；位置编辑后保存 moved.ecproj。

```bash
python3 -I -B "$HARNESS_DIR/scripts/commands.py" check "$SKILL_DIR/examples/puppet-record-follow-create.json"
python3 -I -B "$HARNESS_DIR/scripts/commands.py" run "$SKILL_DIR/examples/puppet-record-follow-create.json" --output /absolute/new-puppet-create
python3 -I -B "$HARNESS_DIR/scripts/commands.py" run "$SKILL_DIR/examples/puppet-record-follow-reopen.json" --input project=/absolute/new-puppet-create/project.ecproj --output /absolute/new-puppet-reopen
python3 -I -B "$HARNESS_DIR/scripts/commands.py" run "$SKILL_DIR/examples/puppet-record-follow-revise.json" --input project=/absolute/new-puppet-create/project.ecproj --output /absolute/new-puppet-revision
```

创建实例的 samples 为 [[0,48,24],[0.25,48,12],[0.5,48,24]]；时间为录制相对秒，start=0 为合成起点。speed=100%、smoothing=0，0.5 秒按 12 fps 生成含两端的 7 个关键帧，间隔 1/12 秒。跟随配置 delay=1/12 秒、amount=50%、cascade=false。在 1/3 秒，运动针位于 [48,16]，跟随针位于 [32,18]，锚点保持 [16,24]。验收原生 info 的表达式求值、属性关键帧和实际渲染，不能只看回执成功。

选择与 recordOptions 是会话状态；原生工程保存动画和跟随表达式，并不保存这些录制会话选项。每次新录制会话显式设置选项。修订计划只降低运动针幅度，将中间样本改为 [0.25,48,18]；跟随针在 1/3 秒变为 [32,21]，其自身属性与表达式、锚点和控制图层保持。另存新工程，保留输入摘要，随后用 reopen 计划核验新工程。

修订实例依赖该实例的唯一图层名 Deform subject，以及 puppet.info 返回的一网格三针脚布局；original.meshes.0.pins.1.pin 只适用于此固定实例。真实工程先查询并确认目标身份，将引用改为目标实际 ID，不能将数组下标视作通用对象契约。尺寸、图层空间坐标、时间范围、运动样本与跟随参数须按素材调整。

禁用命令先核对合成与目标状态。无合成、对 Starch 针录制、删除不存在的针会失败并停止后续保存；原输入保持。超时或 unknown 时检查原任务回执，禁止自动重放编辑。PNG 预览用于像素变化与重开一致性；本实例不验证透明导出、视频编码或创作质量。

The three bundled plans create, reopen and revise a self-contained rig. Samples use relative seconds; start is composition time. Seven frame-aligned keys span 0–0.5 s at 12 fps. Follow uses a 1/12 s delay and 50% displacement. Recording options and selection are transient: set options explicitly in each session. Revision preserves the anchor, follower properties/expression and control layer. Adapt returned identities and geometry for real projects; the fixed fixture's array index is not a general identity contract. Rendered pixel identity after reopening is checked separately from parameter receipts. The candidate test exercises ten representative puppet commands and three real rejection paths; exhaustive pin/context, GUI and creative acceptance remain open.
