# Connect/MCP 插件增量验收

Python 3.12、3.13：34 项测试通过。session-inspect 可核对上游只读探测身份和状态，所有结果均禁止任务执行、产物交付与自动重放。

headless-current-inspection.json 和 disconnected-current-inspection.json 来源于固定原生 CLI 0.2.1 的实际探测，不是单元测试夹具。前者记录 Headless 查询成功，后者记录 Connect 后端失联。sourceSnapshotMatches=false 正确表明当前上游资源尚未进入插件的受摘要保护公开快照。

插件仍使用公开技能源 v0.1.0-dev.1 / 87fe7ce；未直接改写 managed skills。新增观察器不代表宿主已加载新增技能或桌面 Connect 已通过。历史宿主、视觉、发行和 CI 通过记录只适用于其原始源码身份。

真实桌面、NotSaved、重启恢复、MCP 宿主、不可变来源升级和配套验收尚未完成，四项扩展任务保持 OPEN。

发布准备：版本元数据已递增，仅创建 GitHub 草稿；发行门禁尚未满足，不公开发布、不移动旧标签。原生回执所绑定的运行资源和输入没有因版本元数据调整而改变；本轮重新执行离线测试和分发校验。插件来源仍锁定已公开 v0.1.0-dev.1，不能把待发布技能库版本登记为公开来源。
