# Craft 场景技能重建进展

## 目标与当前交付

目标仍是从对标软件的实际经验构建覆盖13应用、规模为数百条的可用场景技能，方法与参数对应真实CLI/MCP。当前166条命令映射：PhotoCraft50条，GridCraft18条，WordCraft/DeckCraft/SoundCraft/LightCraft各14条，其余7应用各6条。不是166条都已通过完整效果验收。

| 内容 | 当前事实 |
| --- | --- |
| GitHub来源 | 16个仓，固定commit、实际阅读文件和许可状态见 craft-scenario-sources.json |
| 原生命令参数 | 13个官方Windows x64 CLI实际采集；全部目录采集与业务矩阵通过运行38921194883 |
| 场景分发 | 78个技能中落地166条，独立引用、方法ID、PDF参数和源/插件副本检查通过 |
| PhotoCraft实际操作 | 18条场景由技能原始步骤在Windows CLI执行，保存重开导出通过运行38926679341；其中6条检查RGB变化，4条检查局部效果及保护区域不变，1条检查非删除裁切保存后的原像素恢复 |
| Office实际操作 | Grid12条、Word8条、Deck8条及1条组合用例通过运行38928803118 |
| 视听实际操作 | Sound8条、Light8条通过运行38931238554；包含重开后再导出检查 |
| 画质与完整场景 | 合成输入证明技术链；真实损伤照片审阅和其余104条场景逐项业务验收尚未完成 |

## 用法

PhotoCraft从 `photocraft-scenario-playbooks` 选择修复、影调、人像、商品、版式或交付手册。其他应用的既有场景技能增加 `references/craft-methods.md`，列出步骤、参数、MCP包装及CLI会话方式，所需文件都在单个技能内。

数字、采样坐标、路径和返回ID是任务相关值，不能照抄例子。CLI版本与Web增强运行时可能不同，进入真实会话后仍查当前schema。LightCraft Web库与原生库、PdfCraft直接工具与内部命令表、FilmCraft ticks/秒/帧，都有明确边界。

来源仅借鉴工作流事实，场景正文与参数例子原创编写。未声明许可的来源不复制正文、代码或素材。当前没有将外部Photoshop脚本拿来当Craft脚本执行。

## 验证链接

- [13应用命令目录与原生业务](https://github.com/partme-ai/full-aigc-plugins/actions/runs/38921194883)
- [PhotoCraft 18场景技术往返及局部像素](https://github.com/partme-ai/full-aigc-plugins/actions/runs/38926679341)
- 静态检查：`python3 scripts/validate-craft-playbooks.py`，覆盖166条；新技能格式检查通过；28项回归与OpenSpec严格检查通过。

## 继续工作

继续扩展13应用的场景深度与数量，接下来补足CADCraft、DesignCraft、VectorCraft、FigCraft、EffectCraft、FilmCraft、PrintCraft等场景，并逐项验证尚未运行的既有流程。每条新增场景须有实际命令与参数、前置选择/对象ID和结果检查，不能靠参数排列组合凑数。随后逐批做真实文件/媒体运行和视觉/听觉审阅。当前OpenSpec保持实施中，不归档、不把剩余验收写成通过。

## 本轮局部操作扩展

PhotoCraft增加20条流程，含局部蒙版、硬边商品保色、背景柔化、渐变曝光、定区修补、透明画布及非删除裁切。源为GNOME/gimp-help固定提交的操作事实，原创适配到Craft命令。独立复核纠正了羽化跨边界、渐变抖动与保存后裁切恢复检查；Windows运行38926679341已通过18条场景，其中4条局部操作验证目标区变化、保护区逐像素不变；裁切保存后恢复并比较全图RGB通过。初次运行38926297765暴露无选区取消命令被拒绝的问题，已删除无条件调用后重跑通过。此结论不包含真实照片画质、全部122条场景或宿主同步显示验收。

## 办公场景扩展

本轮新增GridCraft12条、WordCraft8条、DeckCraft8条。GitHub来源仍使用固定提交，补充阅读XlsxWriter验证/表格案例、python-docx页眉页脚与段落手册、python-pptx图表与备注手册。手册明确新建任务边界、同进程步骤、公式/数值分开读取以及多场景只新建一次。

原生Windows首轮运行38928398377中，Word8条与Deck8条及1条组合用例通过；Grid在百分比显示值解析处失败。测试已改为通过sheet.read读取未格式化数值；运行38928803118的13应用业务矩阵通过，包含Grid12条、Word8条、Deck8条及1条组合用例。详细步骤摘要、技能源提交与参数检查见craft-office-playbook-validation.json。Word业务函和编号SOP的实际PDF已渲染查看，中文、页眉页脚和编号在这两份示例中正常；不将此视为全部文档版式验收。

办公批次完成时共有150条映射，其中46条完成技术检查；后续视听批次见下节。

## 视听场景扩展

新增SoundCraft8条、LightCraft8条并集成到插件。借鉴Audacity和darktable官方手册的工作流事实；新手册明确声道、时间单位、完整源图坐标、专用会话、Web/原生导出边界。

Windows运行38931238554的13应用业务矩阵通过，新增16条均通过样本/像素/结构检查；Sound保存重开再导出包含分轨，Light逐像素比较重开后的渲染。首次Sound测试误把分轨文件名前缀当轨名，已按实际命名规则修正后重跑。详细源提交、步骤摘要和检查范围见craft-media-playbook-validation.json。

累计166条映射中62条已经执行对应步骤并检查技术结果，另有Deck组合用例1条。其余104条仍待逐项运行；真实音质、相机RAW画质和复杂版式没有用合成输入替代验收。现有目标继续推进，OpenSpec不归档。
