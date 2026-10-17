# Codex 视觉 Judge 适配 / Codex visual Judge adapter

此适配由当前宿主智能体执行，不调用独立付费模型，不以脚本生成随机评分。技术解码和模型实际观察是两类证据。

1. 通过当前技能公开 `review` 获取v2请求，检查任务、标准、工程/媒体摘要及`scope.requiredFrameIndices`；命令/桌面请求使用`scope.contexts[*].requiredFrameIndices`和`scope.requiredMediaPaths`，逐context分别核验，不混合帧覆盖。
2. 使用当前Codex实际可用的本地图像查看工具打开绑定预览。视频先用宿主已安装的媒体解码器提取请求的具体帧；序列按其描述找到相应全局编号的PNG。提取文件留在任务私有评估目录，不能写进技能或改动原交付。提取前后核对原媒体摘要；衍生帧应保留原媒体路径/摘要和对应帧索引。
3. 实际查看每个声明观察的样本，再根据请求标准记录可见对象、问题、时间/属性定位和理由。多帧观察只能证明声明样本；需要全片或更密集判断时，单独记录未解决问题，不宣称所有帧通过。
4. 写v2回执：`schema: effectcraft-judge-receipt/v2`；复制请求的`taskId/requestId/binding/criteriaHash/scopeHash`。`status`为PASS/FAIL/NOT_RUN；`capabilities`中的visual/temporal只能反映实际宿主能力。`observations`每项包括请求媒体`path/sha256`、实际查看的`frameIndices`、非空`method/description`。PASS/FAIL才提供0–1的score、布尔passed及定位issues；PASS不能含未解决issues。`temporalReviewed`只在确实比较对应样本后为true。
5. 缺工具、解码器或时序观察时提交NOT_RUN（score可为null、passed为false），保留原因，不能代签PASS。通过公开`review --judge RECEIPT`导入；同一已结算请求的冲突响应不会覆盖原报告。
6. 仅在创作FAIL、工程/技术通过且已有revisionScope与预算时，通过公开revise局部修改，再重复实际观察。用户接受始终独立。

This adapter runs in the current Codex agent using its actual visual tools. It adds no independent paid model API. Read the v2 request, verify bound artifact digests, and inspect the requested preview/video/sequence samples. For video, extract the exact requested frame indices using an available decoder and keep derived images outside the skill and original delivery. Record only samples actually inspected, along with source-media path/digest, indices, method and observations. Return the explicit v2 receipt bound to task/request, criteria and scope. Missing tools or temporal coverage produce NOT_RUN; a sampled PASS does not assert all-frame acceptance. Import the receipt via public review, then revise only within the existing authorization and shared budget. User acceptance remains independent.

命令／桌面修订需要原plan/run通过独立 `--revision-scope` 预先绑定范围；其内部请求使用 `effectcraft-command-revision/v1` 和当前Judge binding，不能沿用workflow的manifest或expectedProjectSha256字段。参见本技能 `managed-execution.md`。仅在新子版本完成原生保全复检后实际观察，不能把旧PNG或旧评分用于新版本。

Command/desktop revision requires a scope bound separately before the original run. Its internal request uses the current Judge binding, not workflow manifest fields. Reopen/preservation checks and actual observation apply to the new child version; old media/scores do not prove it.
