# 交付血缘 / Artifact lineage

公开工作流在成功交付中自动生成 `lineage.json`，由 `manifest.json` 摘要绑定。`logicalId` 跨修订保持稳定；`version` 是除血缘文件自身之外的交付文件表内容摘要。`sourceTask` 登记本次工作流执行ID和计划摘要，不代表外部调度任务；原生工程、导出及登记素材依赖均使用包内相对路径。

移动整个交付目录后，仍须重新校验文件内容和血缘边，再重开原生工程。修订会验证来源血缘并登记父版本；历史包缺少血缘时登记 legacy 来源，不虚构其父版本。历史包可继续读取，但缺少血缘不能作为血缘验收通过。

The public workflow writes digest-bound `lineage.json`: a stable logical ID, content-addressed package version, workflow execution ID, plan hash, native project, derivatives and registered asset dependencies. Paths are package-relative. Moving a whole package preserves identity; verify every file again before reopening. Revisions verify versioned parents; old packages remain readable with an explicit legacy parent, without fabricated lineage. Integrity checks do not establish creative quality or external editor fidelity.
