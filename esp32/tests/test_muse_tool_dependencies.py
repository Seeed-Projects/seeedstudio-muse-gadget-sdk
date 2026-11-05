# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Muse serial tools explain how to provide a missing pyserial dependency."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / 'tools/muse'


class MissingPyserial(unittest.TestCase):
    def test_serial_tools_explain_missing_pyserial(self):
        cases = (
            ('monitor.py', 'fake-port', '0'),
            ('chat.py', '--status'),
            ('chat.py', '--port', 'fake-port', '--status'),
            ('ports.py', '--list'),
            ('paced_esptool.py', '--help'),
            ('snap.py', 'fake-port', '', 'screen.png'),
            ('echo_turn.py', 'fake-port'),
        )
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / 'serial.py').write_text(
                "raise ImportError(\"No module named 'serial'\")\n")
            env = dict(os.environ, PYTHONPATH=directory, PYTHONDONTWRITEBYTECODE='1')
            for script, *args in cases:
                with self.subTest(script=script, args=args):
                    result = subprocess.run(
                        [sys.executable, '-S', str(TOOLS / script), *args],
                        cwd=directory, env=env, capture_output=True, text=True, timeout=5)
                    self.assertEqual(result.returncode, 1, result.stderr)
                    self.assertEqual(result.stdout, '')
                    self.assertIn('pyserial is missing', result.stderr)
                    self.assertIn('ESP-IDF', result.stderr)
                    self.assertIn('export.sh', result.stderr)
                    self.assertIn('python3 -m pip install pyserial', result.stderr)
                    self.assertNotIn('Traceback', result.stderr)
                    self.assertEqual(len(result.stderr.splitlines()), 1)


if __name__ == '__main__':
    unittest.main()
