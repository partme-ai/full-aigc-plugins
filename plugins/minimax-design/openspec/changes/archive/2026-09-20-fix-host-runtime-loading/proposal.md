## Why

ZCode 会自动发现标准 `hooks/hooks.json`，manifest 再显式声明同一路径会重复注册 hooks。

## What Changes

- 删除 ZCode manifest 的重复 hooks 指针。
- 保留标准 hooks 文件供宿主自动发现，并增加回归测试。

## Capabilities

### New Capabilities

- `host-runtime-loading`: 每个宿主只加载一次 MiniMax hooks。

### Modified Capabilities

None.

## Impact

影响 ZCode manifest、README 与分发测试，不改变 hook 实现。
