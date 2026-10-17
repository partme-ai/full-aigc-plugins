"""单请求串行 stdio MCP 会话；超时不重试有副作用的请求。"""
import json
import importlib.util
from contextlib import suppress
from pathlib import Path
import os
import select
import subprocess
import tempfile
import time

_spec = importlib.util.spec_from_file_location('craft_session_commands', Path(__file__).with_name('commands.py'))
_commands = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_commands)


class Session:
    def __init__(self, argv, timeout=120, control=None, filesystem=None):
        self.control = control
        self.filesystem = filesystem
        self.timeout = timeout
        self.buffer = b''
        self.sequence = 0
        self.stderr = tempfile.TemporaryFile()
        launch = _commands.load('filesystem_scope').launch(argv,filesystem) if filesystem is not None else argv
        self.process = subprocess.Popen(launch, env=_commands.load('input_security').native_environment(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self.stderr, preexec_fn=control.apply_limits if control else None)
        try:
            if self.control:
                self.control.emit('session_created', pid=self.process.pid)
            self.request('initialize', {'protocolVersion': '2024-11-05', 'capabilities': {}, 'clientInfo': {'name': 'craft-skill', 'version': '0.1.0'}})
            self.send({'jsonrpc': '2.0', 'method': 'notifications/initialized'})
        except BaseException:
            self.close()
            raise

    def send(self, value):
        encoded = (json.dumps(value, allow_nan=False) + '\n').encode()
        try:
            self.process.stdin.write(encoded)
            self.process.stdin.flush()
        except OSError:
            # 写入／flush 失败不能证明对端没有接收编辑请求。
            raise RuntimeError('outcome_unknown: mcp_write_failed; request not retried') from None

    def request(self, method, params):
        if self.filesystem is not None and method == 'tools/call' and isinstance(params, dict):
            arguments = params.get('arguments', {})
            if params.get('name') == 'run_command' and isinstance(arguments, dict):
                _commands.load('filesystem_scope').authorize_command(arguments.get('command'), arguments.get('params', {}), self.filesystem)
        self.sequence += 1
        identifier = self.sequence
        if self.control:
            self.control.before_request(method, params, identifier, self.process.pid)
        self.send({'jsonrpc': '2.0', 'id': identifier, 'method': method, 'params': params})
        deadline = time.monotonic() + self.timeout
        while True:
            if time.monotonic() >= deadline:
                raise TimeoutError('outcome_unknown: request not retried')
            if b'\n' in self.buffer:
                line, self.buffer = self.buffer.split(b'\n', 1)
                if not line.strip():
                    continue
                try:
                    response = _commands.reply_json(line)
                except (ValueError, UnicodeError):
                    raise RuntimeError('outcome_unknown: invalid_mcp_json; request not retried') from None
                if not isinstance(response, dict):
                    raise RuntimeError('outcome_unknown: invalid_mcp_response; request not retried')
                if 'id' not in response and isinstance(response.get('method'), str) and not ({'result', 'error'} & response.keys()):
                    continue
                if type(response.get('id')) is not int or response['id'] != identifier or response.get('jsonrpc', '2.0') != '2.0':
                    raise RuntimeError('outcome_unknown: mismatched_mcp_response; request not retried')
                if ('error' in response) == ('result' in response):
                    raise RuntimeError('outcome_unknown: missing_or_ambiguous_mcp_result; request not retried')
                if 'error' in response:
                    error = response['error']
                    if (not isinstance(error, dict) or type(error.get('code')) is not int
                            or not isinstance(error.get('message'), str)):
                        raise RuntimeError('outcome_unknown: invalid_mcp_error; request not retried')
                    raise RuntimeError('mcp_error: native diagnostic withheld')
                result = response['result']
                if method == 'tools/call':
                    if (not isinstance(result, dict)
                            or not isinstance(result.get('isError', False), bool)
                            or not isinstance(result.get('content'), list)
                            or any(not isinstance(entry, dict)
                                   or not isinstance(entry.get('type'), str)
                                   or (entry['type'] == 'text' and not isinstance(entry.get('text'), str))
                                   for entry in result.get('content', []))):
                        raise RuntimeError('outcome_unknown: invalid_tool_reply; request not retried')
                if self.control:
                    self.control.after_request(identifier, self.process.pid, result)
                return result
            remaining = deadline - time.monotonic()
            if remaining <= 0 or not select.select([self.process.stdout], [], [], remaining)[0]:
                raise TimeoutError('outcome_unknown: request not retried')
            chunk = os.read(self.process.stdout.fileno(), 65536)
            if not chunk:
                raise RuntimeError('mcp_disconnected: outcome may be unknown')
            self.buffer += chunk
            if len(self.buffer) > 64 * 1024 * 1024:
                raise RuntimeError('mcp_response_too_large')

    def command(self, identifier, params):
        result = self.request('tools/call', {'name': 'run_command', 'arguments': {'command': identifier, 'params': params}})
        return _commands.parse_reply(result)

    def close(self):
        if self.process.stdin:
            with suppress(BrokenPipeError):
                self.process.stdin.close()
        try:
            self.process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            self.process.terminate()
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
        self.process.stdout.close()
        self.stderr.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
