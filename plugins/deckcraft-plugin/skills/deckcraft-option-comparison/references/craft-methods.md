# 方法与执行

先读 [实际命令目录](craft-command-evidence.json)。新建时依次调用 `file.new`、`slide.new`、`insert.table`。随后 `slide.inspect {"index":0}`，从当前页 shapes 查找唯一新建的 table 类型形状，绑定真实ID；已有多张表时比较插入前后ID并核对矩形，不取“第一个表”。

模板中的 `capture` / `$table.id` 不是原生命令字段。后续每条操作都显式传此ID，避免依赖选择漂移：

```json
{"id":259,"cell":[1,1],"text":"1200 USD/year"}
```

这里259仅为演示，必须替换。对应命令 `text.set`；cell为0起行列。`table.columnWidth` 依次设置0/1/2列为220/310/310，`table.style` 为medium2-accent1，`table.options` 开启headerRow及bandedRows、关闭totalRow。最后 `slide.notes` 指定真实页索引。

## CLI

用参数数组调用，避免Windows/macOS引号差异：

```python
subprocess.run([cli, "run", "--in", "input.deckcraft",
    "--cmd", "text.set=" + json.dumps({"id": actual_table_id,
        "cell": [1, 1], "text": actual_cost}),
    "--save", "comparison.deckcraft"], check=True)
```

CLI可能无stdout；保存后用 `info` 或读取原生工程核查真实内容。`convert comparison.deckcraft comparison.pptx` 另存PPTX，`render comparison.deckcraft --slide 0 comparison.png` 检查实际页面。先确认输出不存在或允许覆盖，输入另行保留。

## 同会话MCP

内嵌编辑器ready后，在该编辑器服务调用实际schema中的 `run_command`：

```json
{"command":"text.set","params":{"id":259,"cell":[1,1],"text":"1200 USD/year"}}
```

插表后用同服务查询 `slide.inspect` 或其实际检查工具得到ID。整轮修改、保存都用同一服务；独立CLI进程不自动改变已打开页面。宿主不同可能有不同外层工具名称，先读实际schema，不把CLI的 `--cmd` 字符串填入MCP参数。

## 交付检查

表格必须是4行3列且文字逐格匹配，不把费用单位或周期丢掉；列宽总和840pt，左60pt加总宽不超960pt画布。检查PPTX含原生 `a:tbl`、行列及活文字；在副本修改一格并回读，确认原输入摘要不变。备注必须跟随目标页。检查渲染可读性；不由结构通过推导真实采购判断或全宿主同步通过。
