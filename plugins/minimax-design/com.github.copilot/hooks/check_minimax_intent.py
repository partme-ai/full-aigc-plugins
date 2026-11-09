#!/usr/bin/env python3
"""UserPromptSubmit hook: point MiniMax-shaped requests at the plugin skills.

Advisory only — always exits 0; silent unless the prompt looks MiniMax-related.
"""
from __future__ import annotations

import json
import re
import sys

INTENT_RE = re.compile(
    r"minimax|海螺|hailuo|h3|文生视频|图生视频|首尾帧|视频生成",
    re.IGNORECASE,
)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}

    prompt = ""
    if isinstance(payload, dict):
        prompt = str(payload.get("prompt") or "")

    if prompt.strip().startswith("/"):
        return 0

    if INTENT_RE.search(prompt):
        print(
            "提示：该请求疑似 MiniMax（海螺）相关。入口技能 minimax-design-use 会先做"
            "能力预检（MINIMAX_API_KEY / 网关 / mmx CLI）；视频生成走 minimax-video-generation"
            "（H3 v2：t2v、i2v、白模首尾帧 FL2VA），提示词结构用 h3-prompt-writing，文本/图像/语音/音乐走 minimax-multimodal-toolkit。"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
