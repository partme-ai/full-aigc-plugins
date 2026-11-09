# 媒体预检与显式标准化

## 顺序

1. 对源文件计算内容 SHA-256，并用 `media probe` 记录容器、编解码器、尺寸、FPS、Alpha、音频流和时长。
2. 用当前发布 capability、剪映版本和目标平台判断 `compatible`、`conversion_required` 或 `blocked`。
3. 需要转换时生成 `media-preflight/v1` 计划，绑定完整参数摘要、成本/空间预算和精确批准。
4. 受控 Provider 只创建派生媒体，不修改草稿；转换后重新计算内容 SHA-256 并 probe。
5. 比较帧数、时长、Alpha、音频和可见质量；通过后才暂存到隔离输出并交给 Rust CLI 导入。
6. 保留原文件；失败时删除派生文件并撤销暂存，不覆盖源素材。

合同见 [Schema](media-preflight-v1.schema.json) 与 [有效示例](../examples/media-preflight-v1.json)。

## 禁止静默行为

- 不因扩展名是 WebM 就自动转码；不因 MP4/MOV 可解析就假定当前剪映版本兼容。
- 不使用路径 MD5、文件名或“尺寸相同”代替内容身份。
- 不在技能中内嵌 ffmpeg 命令；Harness 选择受控 Provider，并记录 executor identity、参数摘要、超时和制品摘要。
- 不把转码成功当成草稿导入、冷重开或播放成功。

## Web VFX 特别门禁

浏览器产物还需记录本地 HTML 或允许的 Origin、网络策略、浏览器/字体/脚本版本、完成信号、超时、分辨率、FPS、Alpha 和渲染摘要。未知远程脚本或任意 CDN 必须在渲染前阻塞。
