# Craft 场景技能重建进展

## 目标与当前交付

目标仍是从对标软件的实际经验构建覆盖13应用、规模为数百条的可用场景技能，方法与参数对应真实CLI/MCP。当前122条命令映射：PhotoCraft操作手册50条；其余12应用各6个既有技能补充具体步骤，共72条。不是122条都已通过创作验收。

| 内容 | 当前事实 |
| --- | --- |
| GitHub来源 | 15个仓，固定commit、实际阅读文件和许可状态见 craft-scenario-sources.json |
| 原生命令参数 | 13个官方Windows x64 CLI实际采集；全部目录采集与业务矩阵通过运行38921194883 |
| 场景分发 | 73个技能中落地122条，独立引用、方法ID、PDF参数和源/插件副本检查通过 |
| PhotoCraft实际操作 | 13条场景由技能原始步骤在Windows CLI执行，保存重开导出通过运行38924224124；其中6条另做实际RGB像素变化检查 |
| 画质与完整场景 | 合成输入证明技术链；真实损伤照片审阅和其余109条场景逐项业务验收尚未完成 |

## 用法

PhotoCraft从 `photocraft-scenario-playbooks` 选择修复、影调、人像、商品、版式或交付手册。其他应用的既有场景技能增加 `references/craft-methods.md`，列出步骤、参数、MCP包装及CLI会话方式，所需文件都在单个技能内。

数字、采样坐标、路径和返回ID是任务相关值，不能照抄例子。CLI版本与Web增强运行时可能不同，进入真实会话后仍查当前schema。LightCraft Web库与原生库、PdfCraft直接工具与内部命令表、FilmCraft ticks/秒/帧，都有明确边界。

来源仅借鉴工作流事实，场景正文与参数例子原创编写。未声明许可的来源不复制正文、代码或素材。当前没有将外部Photoshop脚本拿来当Craft脚本执行。

## 验证链接

- [13应用命令目录与原生业务](https://github.com/partme-ai/full-aigc-plugins/actions/runs/38921194883)
- [PhotoCraft 13场景技术往返](https://github.com/partme-ai/full-aigc-plugins/actions/runs/38924224124)
- 静态检查：`python3 scripts/validate-craft-playbooks.py`，覆盖122条；格式检查覆盖73技能；20项回归与OpenSpec严格检查通过。

## 继续工作

继续扩展13应用的场景深度与数量，优先补足PhotoCraft修复/人像/商品等更细分流程和每应用的多步骤复杂案例。每条新增场景须有实际命令与参数、前置选择/对象ID和结果检查，不能靠参数排列组合凑数。随后逐批做真实文件/媒体运行和视觉/听觉审阅。当前OpenSpec保持实施中，不归档、不把剩余验收写成通过。

## 本轮局部操作扩展

PhotoCraft增加20条流程，含局部蒙版、硬边商品保色、背景柔化、渐变曝光、定区修补、透明画布及非删除裁切。源为GNOME/gimp-help固定提交的操作事实，原创适配到Craft命令。独立复核纠正了羽化跨边界、渐变抖动与保存后裁切恢复检查；最新新增场景的Windows局部像素验证仍在进行，不能计为已通过。
