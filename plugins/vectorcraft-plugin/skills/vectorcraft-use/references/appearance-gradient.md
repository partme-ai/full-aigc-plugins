# 原生渐变与多重外观 / Native gradients and appearance

本场景通过完整命令网关组织全局色板、渐变停靠点、三项外观及定点品牌色修订。当前为源码候选；固定发布和每个命令的完整上下文验收单独记录。

目录为宿主实际加载本技能的 SKILL_DIR；任意 Vector 单技能均自带本示例与所有脚本。安装范围是锁定 macOS arm64 CLI，首次执行自动下载并核对摘要；不读取兄弟技能目录。

```bash
python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe paint.setFill
python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe appearance.setItem
python3 -I -B "$HARNESS_DIR/scripts/workflow.py" "$SKILL_DIR/examples/appearance-gradient-create.json" --output /absolute/new-original --runtime-home /absolute/empty-runtime
```

创建128×64工程：左侧渐变标记关联 Brand start/Brand end 全局色板，底部渐变填色＋空描边＋顶部20%白色填色形成三项外观；右侧绿色矩形是未绑定品牌色的控制对象。导出 `.vectorcraft`、SVG、PNG、PDF、原生重开记录、参数记录及交换损失。

外观项目 index 是原生 paint-order 索引，不是图层索引。本例先 select.set 明确目标，再 appearance.setActiveItem index=0 定位底部填色；paint.setGradientGeom 同时提供 start 与 end 文档坐标，paint.editGradient reverse=true 反转停靠点。gradient.selectStop 要求当前活动填色确实为渐变。使用 ids 不会自动为每个菜单命令建立正确选择与活动行。

不要复制 stop 的色值冒充全局色板联动。stops 的 swatch 绑定真实 swatch.new 返回名称；原生 link_stops 解析颜色及链接，后续 swatch.edit 只改变与其相连的填色／停靠点。示例的控制对象使用普通实色，返工后应保持对象JSON和像素不变。

返工计划保留 source manifest 中的绑定，并使用 expectedProjectSha256 防止编辑错版本。先将新计划中的 expectedProjectSha256 设置为原交付 manifest.json 的 files["project.vectorcraft"]，再运行：

```bash
python3 -I -B "$HARNESS_DIR/scripts/workflow.py" /absolute/revision-plan.json --source /absolute/new-original --output /absolute/new-revision --runtime-home /absolute/empty-runtime
```

revision-plan.json 从本技能 examples/appearance-gradient-revise.json 复制；不修改已安装技能中的示例。重开后重新选中 badge、定位底部渐变填色、选择停靠点，再把 Brand end 改为紫色。原工程、路径几何、对象ID、顶部白色填色及右侧控制对象都必须保持不变。新的原生工程须重开检查渐变链接与色板，PNG须出现预期目标变化，SVG须仍包含实际渐变结构。

PDF文件头或SVG渐变元素不证明其他编辑器中的外观一致或完整可编辑。exchange-loss.json 保留未知／已知损失；不以栅格预览替代矢量工程。只给 start、未建立活动填色状态等错误会失败，且不得发布成功 manifest 或覆盖原工程。

English: Create with appearance-gradient-create.json through this skill's public workflow.py. The active fill uses native paint-order item0; selection and activity are established explicitly before gradient commands. Global swatch names come from actual results. Copy appearance-gradient-revise.json to a new plan and bind the original project SHA256; never edit installed resources. Changing only Brand end must persist after native reopening, change target pixels, retain SVG gradient structure and preserve geometry, IDs, the top white fill, the unlinked control node/pixels and all original delivery files. PNG/PDF/SVG derivatives do not replace the editable native project or prove cross-editor visual equivalence. This sample is distinct from exhaustive command and fixed-installed acceptance.
