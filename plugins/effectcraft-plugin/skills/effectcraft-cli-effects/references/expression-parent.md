# 父级与表达式用法 / Parenting and expressions

当前技能包含独立的 `examples/expression-parent-create.json` 与 `examples/expression-parent-revise.json`，从实际 `.agents/skills` 或插件缓存目录使用本技能脚本，首次会安装摘要锁定的原生CLI。

```bash
python3 -I -B "$HARNESS_DIR/scripts/workflow.py" "$SKILL_DIR/examples/expression-parent-create.json" --output "$DELIVERY_DIR" --runtime-home "$RUNTIME_HOME"
```

设置SKILL_DIR为当前实际技能目录，DELIVERY_DIR和RUNTIME_HOME为用户自己的输出及运行时目录。创建合成128×64、12fps、一秒；两个预览时间为0和0.5**秒**，不是帧号。绿色控制图层与红色目标分离，目标挂在零位置Null父级下，透明度表达式50+time*50。Native gateway保持原生参数，先选择目标图层再执行依赖选择的命令。

| 命令 | 参数和前置上下文 |
| --- | --- |
| layer.newNull | 当前活动合成；保存返回的layer引用 |
| prop.set | 明确layer与transform/position；二维位置[0,0] |
| layer.setParent | layers为子图层列表，parent为父级layer引用或null；默认补偿变换保持位置，禁止父级循环 |
| prop.setExpression | 明确layer、path或prop；expression为原生表达式字符串，enabled为布尔值 |
| layer.expressions | layers和enabled；切换指定图层表达式，不能把切换结果当作渲染验收 |

返工：复制revision示例到自己的计划文件，用源manifest.files[project.ecproj]替换expectedProjectSha256，然后公开workflow.py传`--source`源交付、`--output`新目录。只修改目标transform/opacity表达式为25+time*50；继承目标、父级和控制对象绑定。交付保留可编辑.ecproj、native.json、参数回执、两时间点预览、依赖清单和交换损失。其他媒体或视频输出根据真实任务另行指定。

English: time samples are seconds. Create the active comp, retain actual Null/target layer references, select the target and then parent it. Parenting compensates transforms by default and rejects cycles. Set expressions on explicit native property paths; use a boolean enabled switch. Copy the revision plan to a user-owned path, fill the saved native project digest, reopen via --source and write a new output. Native alpha at both times must be checked; command success alone does not prove animation. The sample does not establish all expressions, all640 commands, GUI or fullV1 acceptance.

循环父级的错误路径也必须先显式选择拟设为子级的图层，再调用layer.setParent；否则实时门禁会先拒绝缺失选择，尚未进入循环校验。For a cycle-rejection test, select the prospective child first; live selection rejection and native cycle rejection are different results.
