# 正常路径：分割并移动片段

1. 读取轨道、segment ID、帧率和当前范围。
2. 量化切点后用 `console.segment.split` 分割。
3. 用稳定新 segment ID 移动目标片段。
4. 检查连续性、重叠、材料引用并播放验证。
