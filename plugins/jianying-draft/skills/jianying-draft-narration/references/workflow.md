# 口播精剪参考

## ASR 账本

- 本地 whisper.cpp 路径先执行：

  ```text
  jianying --json media transcribe /abs/input.wav --out /abs/transcript.json \
    --executable /abs/whisper-cli --model /abs/model.bin --model-id reviewed-model \
    --format verbose-json --segment-timestamps --language zh \
    --task-id narration-asr --state-root /abs/asr-state --plan
  ```

- `--plan` 不启动进程、不创建账本或产物；确认 executor identity、源哈希、输出和幂等键后，
  原样去掉 `--plan` 执行。CLI 不下载/捆绑 executable 或模型权重。
- `media.asr_whisper_cpp=supported` 只证明结构化 argv、原子产物和离线黑盒契约；没有真实模型
  音频 canary 时不得把它提升为真实转写质量证据。
- 状态：queued/running/succeeded/failed/ambiguous。
- succeeded 只有在制品存在且哈希匹配时复用。
- failed 只有显式 `--retry` 才重新执行；ambiguous 必须先对账，禁止静默重提。
- 付费请求绑定 provider、executor、文本/音频哈希、预算、target 和 task。

## keep/protect

- keep 必须有来源时间起止、语义理由和置信度。
- protect 覆盖数字、名称、产品、结论和不确定边界。
- 合并相邻 keep 后重新计算目标时间；不要让源时间和目标时间混用。
- 删除后音效/BGM 事件按语义迁移，不机械保留旧绝对时间。

## 验收

检查主轨连续、字幕同步、发音首尾、呼吸自然度、专名完整性；播放未验证时状态最多为 cold_reopen。
