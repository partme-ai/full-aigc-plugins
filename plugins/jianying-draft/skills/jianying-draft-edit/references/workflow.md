# 创建与隔离编辑

## 新建

使用 `project.type=new`，项目中只放已探测素材。主视频轨应从 0 开始并保持预期连续；其他轨道可有间隙。

## 已有草稿

- 源草稿只读。
- 输出必须是新的绝对路径，不能与源路径相同或位于源目录内部。
- mutation plan 先生成快照和工作副本，验证通过后再原子提交。
- 失败时依据 task audit 恢复，不手工拼接半成品文件。

## 证据梯度

`plan < structural < cold_reopen < playback < native_export`。除非真实执行对应门禁，否则不要提升证据等级。

## 恢复

- CLI 返回结构化错误：修正输入后新建 Job；不要修改失败输出充数。
- task failed：读取 `job show` 与 `job audit`，再显式 retry。
- 剪映运行中拒写：关闭编辑器并确认目标后重试，不能强制写入。
