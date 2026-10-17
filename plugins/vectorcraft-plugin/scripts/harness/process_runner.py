"""在插件持久记录进程身份后才允许 exec 独立技能。"""
import json
import os
import sys

marker=sys.argv[1]
message=sys.stdin.buffer.readline(4097)
if len(message)>4096:
    raise SystemExit('invalid_launch_gate')
try:
    gate=json.loads(message)
except (ValueError,UnicodeError):
    raise SystemExit('launch_not_authorized')
if gate!={'task':marker,'go':True}:
    raise SystemExit('launch_not_authorized')
os.execv(sys.executable,[sys.executable,*sys.argv[2:]])
