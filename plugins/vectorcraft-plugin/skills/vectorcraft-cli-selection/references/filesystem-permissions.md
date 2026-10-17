# 文件权限边界 / Filesystem permissions

macOS arm64 固定原生进程由 `filesystem_scope.py` 生成系统策略并执行。完整命令入口只读登记并复制到输出目录的输入，写入限定新的输出目录；主工作流只读可信调用层指定的源交付目录，写入限定暂存目录，保存及独立重开使用相同边界。模型计划及素材元数据不能扩展原生进程的根目录。已知文件命令在 RPC 发送前核对真实路径，内核策略继续约束实际文件读取、写入及链接目标。GUI 的 `file.save` 可先返回后台受理，因此受理回执不能证明已落盘；交付应使用经过验证的保存、重开与文件摘要。

原始 CLI 默认没有用户工程读取或写入权限。可信调用层可显式绑定已授权的根目录，不能从模型计划直接抄入：

```bash
python3 -I -B "$HARNESS_DIR/scripts/cli.py" \
  --read-root /absolute/authorized-input \
  --write-root /absolute/authorized-output \
  -- convert /absolute/authorized-input/project.vectorcraft /absolute/authorized-output/preview.svg
```

`--read-root` 和 `--write-root` 可重复；路径必须为绝对路径，链接按真实目标校验。原生运行时、系统库及字体是独立只读资源，不能以允许 `/System` 或 `/usr` 整棵树代替。GUI 额外允许固定 Metal 窗口资源及本次拥有的回环端口，应用与桥接 CLI 共享工程根目录。

该适配不等于 Python 宿主自身的全进程沙箱；显式低层 `Session` 调用者仍须提供可信 `filesystem` 策略。新素材的原生放置／继承返工与冷安装、实际宿主秘密引用、所有585条命令的适用上下文与固定插件安装权限验收仍需各自证据。未适配平台拒绝受限原生启动，不静默回退无约束执行。

English: The macOS arm64 native gateways enforce explicit file roots using a kernel policy. Registered command inputs are copied into the output root; revision workflows read the trusted source delivery and write their staging root. Known filesystem commands are checked before RPC submission; the kernel also constrains actual file access and symlink targets. Raw CLI calls require repeatable trusted `--read-root` and `--write-root` options for user files. GUI and bridge CLI share project roots, with explicit Metal resources and an owned loopback port. A GUI background-save acknowledgement is not persistence evidence. This does not sandbox the Python host, qualify every native command, resolve host secret references, or establish fixed-plugin acceptance. Low-level Session callers must supply their own trusted filesystem policy.


## Python素材读取 / Python asset reads

素材计划中的路径、摘要及额外 `readRoots` 元数据不能授权读取。独立 `workflow.execute(..., read_roots=[absolute_root])` 或 `workflow.py --read-root /absolute/authorized-assets` 由可信调用层绑定；`--asset logo=/absolute/authorized-assets/logo.svg` 仅显式授权该文件并登记其摘要。受管模式以控制配置冻结的 `authorization.readRoots` 为准，调用参数不能扩大授权，CLI在计算素材摘要前核对控制状态与计划快照。继承素材仅在可信指定的源交付目录内读取。

安全读取按目录描述符逐级打开，不跟随打开过程中的链接替换；只接受普通文件，素材保留64MiB限制，记录文件设备与inode，在格式检查、复制及最终核验时复查身份和摘要。完整命令入口的显式登记输入同样安全复制，保留流式读取与原有大小合同。私有授权根及文件身份不写入公共素材记录。它不替代原生进程的权限策略，也不是Python宿主全进程沙箱。

English: Plan paths, digests and metadata never grant read authority. Standalone workflow callers explicitly bind trusted roots or an individual `--asset` file; managed CLI uses frozen `authorization.readRoots` before hashing. Inherited assets are confined to the trusted source delivery. Descriptor traversal refuses link replacement and nonregular files, retains the64MiB asset limit, and rechecks device/inode and digest during validation and copying. Registered command inputs use the same safe streaming copy without imposing a new size contract. Private roots and identities are omitted from public asset records. Native placement/rework, cold-install and host-secret qualification remain pending for source46.
