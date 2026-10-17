# 摄像机、灯光与三维图形 / Cameras, lights and 3D graphics

## 首次使用与输入 / First use and inputs

从当前宿主加载的 SKILL.md 确定 SKILL_DIR，使用 effectcraft-harness 技能（HARNESS_DIR）的 scripts/bootstrap.py 安装固定官方 CLI。输入包括合成、目标图形或模型、摄像机、灯光、时间范围和允许修改对象。三维坐标用 [x,y,z] 合成像素，旋转用度，时间用秒。先查询实际参数及 enabled；连续创建在同会话中使用返回 layer ID，不猜 ID。

## 分类与使用场景 / Command families

本技能完整归属 46 条命令，逐条参数在 command-reference.md 和 commands.py describe 中；下表按实际场景组织。命令可查询和执行不等于全部参数上下文已验收。

| 场景 | 命令 | 使用与核验 |
| --- | --- | --- |
| 建立可渲染图形 | layer.setSwitch、layer.new3dPrimitive、material.set | 二维图层先核对 threeD 开关；primitive 须设置 comp.renderer=advanced3d，否则创建成功不证明渲染。明确几何尺寸、材质及接受光照状态 |
| 材质复用与复位 | material.revealSource、material.reset、material.duplicateAssign | 先观察实际图层材质；duplicateAssign 的首图层是来源，后续是目标，复位或赋值前保存检查点并检查非目标材质 |
| 建立镜头和灯光 | layer.newCamera、layer.cameraSettings、layer.newLight | 明确 oneNode/twoNode、position、poi、zoom；灯类型与强度按场景决定，景深和阴影另作像素验收 |
| 摄像机视角 | view.set3DView、view.get3D、view.set3DViewCamera、view.reset3DView、camera.fromView | activeCamera 下 orbit/pan/dolly 修改真实摄像机；其他视角下修改会话视图，即使提供 layer 也不替代视角前置。fromView 需有效三维视角，不适用于默认二维会话 |
| 预设与自定义视角 | view.3d.activeCamera、view.3d.default、view.3d.front、view.3d.left、view.3d.top、view.3d.back、view.3d.right、view.3d.bottom、view.3d.custom1、view.3d.custom2、view.3d.custom3、view.3d.last | 用于检查空间结构；视图状态是会话状态，重开后重新设置。视角变化不等于导出的摄像机变化 |
| 调整镜头 | camera.orbit、camera.pan、camera.dolly | orbit 为角度，pan 为像素，dolly 的 amount>0 表示向前。twoNode dolly 同时平移位置与兴趣点；查询两者及实际画面，不能只检查位置 |
| 对焦 | camera.linkFocusToPoi、camera.linkFocusToLayer、camera.setFocusToLayer | link 保存表达式，set 设置当前距离。目标图层身份须明确；关联表达式保存与启用景深后实际模糊效果分别验收 |
| 镜头和灯光绑定 | camera.stereoRig、camera.orbitNull、camera.fromModel、light.fromModel、light.controlWithCamera、light.environmentBackground | stereoRig 创建多个子合成与依赖；模型输入需包含真实摄像机／灯光；环境背景需环境灯，不把 Ambient 当环境灯。交付依赖和原生工程，检查绑定后的属性及实际输出 |
| 视频摄像机解算 | camera.analyze、camera.cancel、camera.solveStatus、camera.points、camera.selectPoints、camera.createFromSolve、camera.create、camera.setGroundPlane、camera.deletePoints | 先用 track.camera 为真实视频建立跟踪器，观察求解状态和实际返回 points；未求解不得伪造点云或创建镜头。索引与 ID 以实时输出为准，取消只在分析确实运行时执行。未知结果检查原任务，禁止重放 |

These families cover all 46 owned commands. Use describe for exact parameters. Active Camera tools edit a real camera; custom views edit transient viewer state. Primitive creation needs the Advanced 3D renderer. Camera solving requires an actual footage tracker, completed solve and observed points; static camera creation does not prove solving, stereo rigs or GUI acceptance.

## 自包含实例 / Self-contained example

```bash
python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe layer.newCamera
python3 -I -B "$HARNESS_DIR/scripts/commands.py" check "$SKILL_DIR/examples/camera-scene-create.json"
python3 -I -B "$HARNESS_DIR/scripts/commands.py" run "$SKILL_DIR/examples/camera-scene-create.json" --output /absolute/new-camera-create
python3 -I -B "$HARNESS_DIR/scripts/commands.py" run "$SKILL_DIR/examples/camera-scene-reopen.json" --input project=/absolute/new-camera-create/project.ecproj --output /absolute/new-camera-reopen
python3 -I -B "$HARNESS_DIR/scripts/commands.py" run "$SKILL_DIR/examples/camera-scene-revise.json" --input project=/absolute/new-camera-create/project.ecproj --output /absolute/new-camera-revision
```

实例建立 128×96、12 fps、一秒合成，Advanced 3D 渲染器，36 像素立方体、Ambient 灯、twoNode 摄像机和二维绿色对照图层。先执行 orbit 与 pan，再显式重置镜头；保留 focus-to-POI 表达式，dof=false。摄像机从 [64,48,-250] 前进 50 到 [64,48,-200]，兴趣点从 [64,48,0] 到 [64,48,50]；实际红色投影由 40×40 变成 50×50。

修订只执行 amount=-25，摄像机位于 [64,48,-225]、兴趣点 [64,48,25]；图形材质、灯光、控制图层与输入工程保持。重开后逐项检查保存属性与预览像素。图层名只属于固定实例；真实工程应先确认目标唯一身份，适配坐标、镜头、尺寸和光照。视图与属性当前查询时间不算持久化工程属性。

The create/reopen/revise plans are self-contained and live in this skill. Dolly changes position and point of interest together. Reopening must preserve native layer properties and rendered pixels. Revise only the intended camera and compare the source checksum plus full non-target properties. Adapt fixture names, identities and geometry for real tasks.

## 错误与交付 / Errors and delivery

无活动合成、activeCamera 下将纯色图层作为摄像机、对非摄像机执行 cameraSettings，均需停止后续保存并保全输入。独立安装失败与原生前置条件失败分别报告。超时或 unknown 先检查回执，不自动重放修改。

交付 .ecproj、依赖、逐步参数回执与实际渲染。实例只覆盖无外部依赖的静态三维镜头；不证明景深、阴影、模型格式保真、全部 46 命令上下文、视频解算、立体绑定、透明输出、GUI或创作质量。
