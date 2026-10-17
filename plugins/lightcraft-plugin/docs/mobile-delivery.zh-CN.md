# 移动文件交付

插件控制器提供显式打包及只读校验；Python 3.11+、Node 24 与现有公共协议校验器是运行依赖。它不安装移动应用，不自动连接或传输到设备，也不执行或重放三领域原生任务。

先独立核实三领域来源报告及实际输入、产物，记录报告 SHA256。输入 JSON 必须恰好包含 `report`（报告绝对路径）与 `report_sha256`（明确的预期摘要）。报告中的 `root` 指向真实产物目录；`artifacts` 必须是完整 craft-artifact/v1 集合及其输入引用。报告的 PASS 字符串本身不证明原生执行或视觉质量。

在插件根运行以下命令，替换为实际绝对路径：

```sh
python3 -I -B scripts/controller.py mobile-prepare /absolute/new-bundle --payload /absolute/prepare.json
python3 -I -B scripts/controller.py mobile-inspect /absolute/new-bundle
```

目标必须不存在且位于来源树之外。包内保留原图、产物、工程/呈现/证据引用和原始报告；清单绑定每个成员的字节数和 SHA256。拒绝来源漂移、已有目标、缺失引用、路径外逃、链接、特殊文件、多余文件及内容变化。既有 craft-artifact 校验器负责协议和文件头验证；文件头有效不等于图像或 PDF 内容解码及视觉通过。复制前后检查身份，失败清理本次新建目录；这不是抵抗其他进程同时改写文件系统的安全沙箱。

两个入口只报告文件身份，设备验收、视觉和原生工程移动重开均保持 NOT_RUN。获得设备授权后，在全新专用目录传输，设备端逐文件核对摘要并记录清单摘要；分别用实际查看器打开 PNG/PDF，保存稳定屏幕及审阅结果。用户自行确认应用条款及权限。不得用传输成功代替显示验收，也不得用合成图显示通过代替 RAW 色彩质量。

当前实机范围及限制见 [Android 证据](verification/mobile-20261009/README.md)。完整移动父任务继续 OPEN。
