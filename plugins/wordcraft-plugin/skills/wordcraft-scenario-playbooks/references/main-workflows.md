# WordCraft main开发候选新增能力

仅用于固定main `eae242176108d328c5dd81fbc10370c51ab90706` 或具备对应契约的更新候选。版本字符串仍可能显示0.7.0，必须同时检查源码提交和实际命令参数，不能把稳定版或旧内嵌引擎当成main。实际Windows命令目录观察为629条，相对稳定版617条新增12条；27条调用契约变化见[目录差异](main-command-delta.json)。目录存在不证明业务成功；下面两条流程已在Windows原生main二进制完成专项回归（运行39007814128：原生页眉页脚、筛选排序合并、新进程读取与DOCX结构均通过），不计入原有8条手册通过数。

## 业务文档的原生页眉页脚

用途：为报告、项目方案或业务函添加可继续编辑的页眉页脚。先确认文档当前节、已有页眉页脚及是否存在首页/奇偶页差异；`page`是从0开始的页号，不是节编号。不覆盖用户原有内容。

1. 用`document.inspect`与文本读取工具确认当前工程；以下示例从新空文档执行，已有文档先定位真实正文插入点。
2. `text.insert {"text":"MAIN BODY"}`填写正文示例。
3. `insert.createHeader {"page":0}`进入该页实际显示的页眉；`text.insert {"text":"MAIN HEADER"}`填入示例抬头。该命令会把光标移入页眉。
4. `insert.createFooter {"page":0}`进入页脚；`text.insert {"text":"MAIN FOOTER"}`填入示例版本说明。
5. `file.saveAs {"path":"output/report.docx"}`或宿主实际`save_document`工具另存新文件；独立CLI可将上述指令作为多个`--cmd command=JSON`参数，最后`--save output/report.docx`。
6. 重开检查正文、对应页的页眉页脚及分页。检查DOCX中原生`word/header*.xml`、`word/footer*.xml`及引用关系，不能把页眉文本写进正文当作完成。多节、首页和奇偶页分别检查。

空页眉整理可用`insert.removeEmptyHeaders {}`；先保存副本，确认不是以空内容承担节布局。不可用`layout.pageSetup {section:...}`做局部页边距更新：其新契约替换整个节，包含页眉页脚；常规边距调整使用`layout.margins`。

## 按条件和顺序生成业务函

用途：按收件人状态筛选并按业务顺序合并通知、邀请或业务函。只使用任务授权的数据。先核对字段、缺失项和目标数量，不在本流程发送邮件。

在同一会话执行：

```json
[
  {"command":"mailings.start","params":{"kind":"letters"}},
  {"command":"mailings.recipients","params":{"rows":[
    {"Name":"ACTIVE-ALICE","Status":"active","Rank":"2"},
    {"Name":"INACTIVE-BOB","Status":"inactive","Rank":"3"},
    {"Name":"ACTIVE-CAROL","Status":"active","Rank":"1"}]}},
  {"command":"mailings.insertField","params":{"field":"Name"}},
  {"command":"mailings.filterRecipients","params":{"rules":[{"field":"Status","op":"equal","value":"active"}]}},
  {"command":"mailings.sortRecipients","params":{"field":"Rank","descending":false}},
  {"command":"mailings.editRecipients","params":{}},
  {"command":"mailings.finish","params":{"path":"output/merged.docx"}}
]
```

这些是有序方法映射，不是一个MCP请求体。插件通常用`execute {"command":"…","params":{…}}`逐步调用，实际包装以宿主schema为准。独立CLI使用`wordcraft-cli run --cmd command=JSON ...`，JSON通过argv传递，避免Windows shell拼接引号。

`filterRecipients`替换原筛选；`{}`清除筛选与排序，不能误当“读取状态”。只读取时用`mailings.editRecipients {}`。规则`join`与前一规则连接，and比or优先；复杂条件先核对预览记录。读取工作簿时可能返回`chooseSheet:true`，必须选择实际sheet后再继续。

交付必须只有CAROL、ALICE且顺序如此，BOB不得出现；使用DOCX正文原生文本和新进程重开验证，不看日志总数就算成功。真实数据另检查重名、编号与空字段。

## 其余新增命令的适用条件

| 方法 | 参数与边界 |
| --- | --- |
| `arrange.copyTo` | `{x,y,page?}`，pt坐标；先选择对象，复制后选择副本，原对象和剪贴板保持；不能当整篇文档复制。 |
| `file.rename` | `{name}`不含扩展名；区分文档命名和实际交付路径，保存后检查文件。 |
| `font.loadSystem` | `{}`；主机系统字体与浏览器字体可用性不同，不能由命令存在推断WASM能加载系统字体。 |
| `insert.deleteBookmark` | `{name}`；先检查交叉引用，避免删除仍被链接的书签。 |
| `link.targets` | `{}`获取真实标题/书签目标；`insert.link`可传`{bookmark,text?}`、`{heading,text?}`或`{top:true,text?}`，不伪造block标识。 |
| `text.typeCode` | `{code:"0233",ansi:1252}`表示带前导0的小键盘字符码；普通Unicode正文使用`text.insert`，不能当Unicode码点接口。 |
| `view.fullScreen` | `{value:true}`；属于界面能力，CLI存在不等于无头进程有可见窗口。 |

同会话要求：先`editor_status`确认当前内嵌编辑器已连接，再通过该会话执行。独立CLI生成文件后需要显式打开，不能声称它自动改了当前编辑器。
