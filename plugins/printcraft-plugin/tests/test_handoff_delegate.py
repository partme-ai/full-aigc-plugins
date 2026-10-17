"""插件 Harness 经公开入口校验交接，独立包无需兄弟仓或原生安装。"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]

class HandoffDelegate(unittest.TestCase):
    def test_public_delegate_preserves_read_only_result(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);pdf=root/'provided.pdf';pdf.write_bytes(b'%PDF-1.4\n%%EOF')
            request=root/'handoff.json';request.write_text(json.dumps({'protocol':'artcraft.printcraft-handoff/1','producer':'artcraft','producerVersion':'0.1.0-dev.113-runtime.1','files':[{'path':str(pdf),'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest()}]}))
            result=subprocess.run([sys.executable,'-I','-B',str(ROOT/'skills/printcraft-harness/scripts/harness.py'),'delegate','handoff',str(request),'--producer-version','0.1.0-dev.113-runtime.1'],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            data=json.loads(result.stdout);self.assertEqual(data['status'],'HANDOFF_INTEGRITY_PASS');self.assertFalse(data['automaticExecution']);self.assertEqual(data['producerExecution'],'NOT_RUN')

if __name__=='__main__':unittest.main()
