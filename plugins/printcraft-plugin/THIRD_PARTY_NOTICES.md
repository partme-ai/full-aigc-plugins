# 第三方归属与隐私边界

插件本身 Apache-2.0。六项上游技能源来自 full-aigc-skills/printcraft-skills 的 v0.1.0-dev.5 预发布；真实仓库、tag、commit、66 项文件摘要与 suite 身份记录在 source-release.lock.json / candidate-source.json / upstream。原始本机路径出现在合成夹具的历史验收日志中，不作为安装路径。

原生 printcraft-cli 0.2.1 从 storytold/pdfcraft 官方 GitHub release 获取，归档和二进制 SHA-256 固定。运行时不捆入插件；bootstrap 安装时复制制品随附 LICENSE 文件，保留原生许可证，不将插件 Apache-2.0 套用于全部原生依赖。

验收 PDF 夹具为本项目原创 CC0，使用 PDF Base-14 Helvetica 名称，不分发字体文件。未捆入 OCR 模型、商业字体、ArtCraft 品牌图标或他人商标素材。PrintCraft 名称用于说明兼容工具；本候选没有声称由原生作者背书。

运行时获取访问 GitHub；本地 PDF 操作可能触发原生网络/系统能力（打印、签名信任、JavaScript、外链等），按实际工具与授权范围使用。插件/包装器不主动上传 PDF，也不将原生程序描述为绝不联网。宿主模型的工具日志可能包含文件内容或路径，遵循宿主数据策略；密码等已知秘密字段会在公开回执中脱敏。

私有执行计划/通道权限 0600，正常及可捕获失败后清理；硬崩溃可能留下受限材料，需要人工核对再清理。任务目录、PDF 产物和 `.printcraft-runs` 身份记录在包缓存外保留，更新不会主动删除。自签名验收私钥只用于隔离测试，测试完成删除，不随插件分发。
