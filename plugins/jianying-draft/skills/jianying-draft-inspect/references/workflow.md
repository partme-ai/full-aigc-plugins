# 检查与证据参考

## 素材事实

记录绝对路径、内容哈希、duration_us、视频尺寸/FPS、音视频流、图片类型和探测器身份。探测失败时不猜测。

## 草稿事实

- metadata 和 timeline 可解析。
- material/segment 引用完整。
- 主轨时序符合目标。
- 未知字段在只读操作中原样保留。
- 素材路径存在只说明可访问，不说明剪映可播放。

## 证据等级

- structural：CLI 解析和引用校验。
- cold_reopen：目标剪映版本关闭后重新打开草稿。
- playback：真实播放检查画面、声音和同步。
- native_export：真实编辑器产出并验证最终制品。
