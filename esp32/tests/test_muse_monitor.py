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

"""Serial-line ordering, reset timing and log capture through a fake port."""
import io
from pathlib import Path
import runpy
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

SCRIPT = Path(__file__).resolve().parents[1] / 'tools/muse/monitor.py'
BOOT_LOG = b'link.main: Muse Gadget starting\n'


class FakeSerial:
    def __init__(self):
        self.events = []
        self._dtr = True
        self._rts = True
        self.data = BOOT_LOG

    @property
    def dtr(self):
        return self._dtr

    @dtr.setter
    def dtr(self, value):
        self.events.append(('dtr', value))
        self._dtr = value

    @property
    def rts(self):
        return self._rts

    @rts.setter
    def rts(self, value):
        self.events.append(('rts', value))
        self._rts = value

    def read(self, size):
        self.events.append(('read', size))
        chunk, self.data = self.data, b''
        return chunk


class MonitorTest(unittest.TestCase):
    def capture(self, seconds='30'):
        port = FakeSerial()
        serial = SimpleNamespace(Serial=Mock(return_value=port))
        argv = [str(SCRIPT), 'fake-port'] + ([seconds] if seconds else [])
        output = io.StringIO()
        duration = float(seconds) if seconds else 8
        with patch.dict(sys.modules, serial=serial), \
                patch.object(sys, 'argv', argv), \
                patch.object(sys, 'stdout', output), \
                patch('time.time', side_effect=[0, duration - 0.1, duration]), \
                patch('time.sleep', side_effect=lambda delay: port.events.append(('sleep', delay))):
            runpy.run_path(str(SCRIPT), run_name='__main__')
        serial.Serial.assert_called_once_with('fake-port', 115200, timeout=0.2)
        return port.events, output.getvalue()

    def test_measured_reset_line_sequence_and_timing(self):
        events, _ = self.capture()
        self.assertEqual(events, [
            ('dtr', False),
            ('rts', False),
            ('sleep', 0.05),
            ('rts', True),
            ('sleep', 0.1),
            ('rts', False),
            ('read', 4096),
        ])

    def test_captures_serial_log(self):
        _, output = self.capture()
        self.assertEqual(output, BOOT_LOG.decode())

    def test_default_capture_duration(self):
        _, output = self.capture(seconds=None)
        self.assertEqual(output, BOOT_LOG.decode())


if __name__ == '__main__':
    unittest.main()
