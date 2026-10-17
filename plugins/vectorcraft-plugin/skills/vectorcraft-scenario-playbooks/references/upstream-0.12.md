# VectorCraft 0.12.0 能力补充

官方发布：[v0.12.0](https://github.com/storytold/vectorcraft/releases/tag/v0.12.0)，提交 `8bc65329286dc1b84aa392997bb205613c3e96cb`。以下为独立原生CLI 0.12.0实测；插件dev.65内嵌引擎也已从同一0.12提交独立构建，保留中文字体，并在实际浏览器中执行标注、交织与CSV三条场景。此为本地候选工具桥验证，不冒充已安装宿主MCP验收。官方源码保持只读。

## 大目录按需发现

真实0.11与0.12原生CLI目录为749→770：新增21个命令，72个参数描述变化。新版MCP还扩展了目录查询参数。先读取实际工具schema，再调用：

```json
{"name":"command_list","arguments":{"query":"graph.","brief":true}}
```

按菜单查路径工具：`command_list {"menu":"Object > Path","brief":true}`。`brief`省略每条的params；选定目标后用 `command_list {"filter":"graph.setType"}`取得完整参数。`filter`与`query`同传时非空filter优先；保留返回的enabled/disabled_reason，不把目录命中当作授权或当前可执行证明。`list_commands`提供相同的query/menu/brief用法，enabledOnly与command_list的enabled_only按各自schema填写。

插件适配层也提供这三个参数，兼容当前内嵌引擎；只过滤目录结果，不模拟新编辑算法。已有宿主会话继续使用原会话，不能另起headless进程冒充同画面修改。

## 向旧版Illustrator流程交付AI 7

仅当接收方明确要求旧版AI，使用单独派生文件；默认现代PDF兼容AI与原生工程分别保留。先保存原生母版，再运行：

```text
vectorcraft-cli convert master.vectorcraft delivery.ai --ai-version 7 --hidden-objects layer --transparent-images flatten
```

以上每个token是独立argv参数；不要用shell拼接用户路径。对应MCP可用 `export {"path":"delivery.ai","format":"ai","options":{"aiVersion":"7","hiddenObjects":"layer","transparentImages":"flatten"}}`，先核实当前后端支持这些选项；插件dev.65也已通过实际内嵌工具桥验证：适配器将path留在宿主，浏览器返回dataBase64，宿主在当前工作区写入新文件；没有扩展引擎文件系统权限。目标必须是未占用的新路径。多文件返回需指定单个画板或走无path的字节导出，不静默丢弃其他文件。`run_command document.export`的参数目录不一定列尽所有格式选项，先查询document.formats并检查返回warnings。

多画板旧AI按画板分别输出，使用返回的真实文件列表，不假定只有delivery.ai。隐藏对象默认形成隐藏图层；omit会删除派生文件中的隐藏对象，visible会显示它们，按交付要求选择。透明图片flatten会结合其下方内容，不能声称仍保留原透明图片编辑性。文字可选outline以摆脱字体依赖，但需另保留活文字母版。

保存后由新原生进程重开：检查组、图层和活文字，再渲染查看；输入母版摘要保持不变。0.12技术样例实际验证两种几何组成的组、一个活文字对象保存到PostScript AI后仍可编辑；不代表复杂透明、渐变、置入图、专色或跨Illustrator版本保真。

## 既有命令的行为修复

0.12发布还包含Transform Again/Transform Each、Reflect轴向、画板复制与导出隔离、SVG文字控制字符等修复。不能因命令ID与0.11相同就认为行为已对齐。涉及这些任务时先核对实际运行时版本和对象、另存测试副本，按相应业务检查几何、画板边界与输出warnings；本补充没有把这些全部标为验收通过。

## 三条新增场景的实际命令

以下步骤完整参数见[结构化场景](recipes.json)，0.12原生和本地内嵌工具桥均已执行三个场景；真实宿主MCP安装调用另行验收。

| 场景ID | 命令顺序与关键参数 | 检查 |
| --- | --- | --- |
| dimension-unit-delivery | dimension.create：mode linear，a [20,50]、b [164,50]，options {units:in,precision:2,scale:"1:1"}；dimension.update：options {units:mm,precision:1} | 2.00 in→50.8 mm；scale是字符串，传数值1会失败 |
| intertwine-overlap-order | 创建两条色带并以实际ID选择；object.intertwine.make；object.intertwine.arrange：at [100,80]，order toggle；副本上object.intertwine.release | 只交换重叠区，保留两条对象；释放后恢复原顺序 |
| csv-text-variants | variable.define：name offer、kind text；variable.bind：variable offer、ids为实际文字；dataset.import：csv含name,offer；dataset.select：name B；dataset.export | 活文字BETA，重开切A为ALPHA；导出含两套数据 |

其他新增命令还包括dimension.applyToAll、action.batch、数据集导入导出、图表/图像动态变量、批量导出预设、交织编辑/释放、选区更新、符号选项与文字步进。它们在0.12目录中存在，不代表这些场景均已验收。批量动作的saveAndClose会覆盖源文件，不能把发现能力当作覆盖授权；先使用destination folder并保留母版。

完整[21个新增命令与72项参数描述变化](upstream-0.12-commands.json)来自两个官方原生二进制的实测目录。按任务搜索具体command ID，读取其参数后再对照当前会话schema；清单记录方法存在，不代表每个方法已完成业务验收。

旧AI交付的格式损失必须随结果返回：实际内嵌交织样例导出后重开为普通组、裁切组与路径，旧AI不保留Intertwine编辑能力；原生.vectorcraft母版仍保留。不能把“能重开AI”当成全部新对象类型保持原生编辑性。
