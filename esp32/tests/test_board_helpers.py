# Copyright (c) Meta Platforms, Inc. and affiliates.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Run the board helpers against an isolated, fake ESP-IDF installation."""

import shlex
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELPERS = (
    ('tools/board.sh', ('devkit', 'build')),
    ('tools/muse/board.sh', ('build', 'xiao147')),
)


class BoardHelpers(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='board-helpers-')
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name)
        self.project = self.folder / 'project'
        for helper, _ in HELPERS:
            destination = self.project / helper
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / helper, destination)
        self.idf = self.folder / 'fake esp-idf'
        self.idf.mkdir()
        self.export = self.idf / 'export.sh'
        self.bin = self.folder / 'bin'
        self.bin.mkdir()
        self.calls = self.folder / 'idf-calls'
        self.env = {
            'HOME': str(self.folder),
            'PATH': '/usr/bin:/bin',
            'IDF_PATH': str(self.idf),
            'TMPDIR': str(self.folder),
        }

    def run_helper(self, helper, args, explicit=False):
        env = self.env.copy()
        if explicit:
            env['IDF_EXPORT'] = str(self.export)
        return subprocess.run(
            ['/bin/bash', str(self.project / helper), *args],
            cwd=self.folder, env=env, capture_output=True, text=True, timeout=10,
        )

    def install_fake_idf(self):
        fake = self.bin / 'idf.py'
        fake.write_text('#!/bin/bash\nprintf "%s\\n" "$@" > "$IDF_CALLS"\n')
        fake.chmod(0o755)
        # Cleanup is inert inside the fake project.
        clean = self.bin / 'rm'
        clean.write_text('#!/bin/bash\nexit 0\n')
        clean.chmod(0o755)
        self.env['IDF_CALLS'] = str(self.calls)

    def test_failed_activation_reports_path_tail_and_python_recovery(self):
        self.export.write_text(
            'echo "Activation preamble"\n'
            'for n in {1..30}; do echo "Checking tool $n"; done\n'
            'echo "Python environment selected"\n'
            'echo "ERROR: Python virtual environment not found" >&2\n'
            'return 23\n'
        )
        for helper, args in HELPERS:
            for explicit in (False, True) if 'muse/' in helper else (False,):
                with self.subTest(helper=helper, explicit=explicit):
                    result = self.run_helper(helper, args, explicit)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(result.stdout, '')
                    self.assertIn(str(self.export), result.stderr)
                    self.assertIn('Python environment selected', result.stderr)
                    self.assertIn('ERROR: Python virtual environment not found', result.stderr)
                    self.assertIn('IDF_PYTHON_ENV_PATH', result.stderr)
                    self.assertIn('install.sh', result.stderr)
                    self.assertNotIn('Activation preamble', result.stderr)
                    self.assertNotIn('Checking tool 12\n', result.stderr)
                    self.assertIn('Checking tool 13\n', result.stderr)

    def test_successful_activation_is_quiet_and_preserves_environment(self):
        self.install_fake_idf()
        self.export.write_text(
            'echo "Activation output"\n'
            'echo "Activation stderr" >&2\n'
            f'export PATH={shlex.quote(str(self.bin))}:"$PATH"\n'
        )
        for helper, args in HELPERS:
            for explicit in (False, True) if 'muse/' in helper else (False,):
                with self.subTest(helper=helper, explicit=explicit):
                    self.calls.write_text('')
                    result = self.run_helper(helper, args, explicit)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stdout, '')
                    self.assertEqual(result.stderr, '')
                    self.assertIn('build', self.calls.read_text().splitlines())

    def test_failed_activation_stops_even_if_idf_was_added_to_path(self):
        self.install_fake_idf()
        self.export.write_text(
            f'export PATH={shlex.quote(str(self.bin))}:"$PATH"\n'
            'echo "ERROR: tool validation failed" >&2\n'
            'return 23\n'
        )
        for helper, args in HELPERS:
            with self.subTest(helper=helper):
                result = self.run_helper(helper, args)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('ERROR: tool validation failed', result.stderr)
                self.assertFalse(self.calls.exists())

    def test_failed_python_activation_stops_before_export_returns_success(self):
        self.export.write_text(
            'idf_exports=$(echo "ERROR: Python virtual environment not found" >&2; exit 23)\n'
            'eval "$idf_exports"\n'
            'return 0\n'
        )
        for helper, args in HELPERS:
            with self.subTest(helper=helper):
                result = self.run_helper(helper, args)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(str(self.export), result.stderr)
                self.assertIn('ERROR: Python virtual environment not found', result.stderr)
                self.assertIn('IDF_PYTHON_ENV_PATH', result.stderr)

    def test_explicit_activation_failure_stops_with_idf_already_on_path(self):
        self.install_fake_idf()
        self.env['PATH'] = f'{self.bin}:/usr/bin:/bin'
        self.export.write_text(
            'echo "ERROR: Python version mismatch" >&2\n'
            'exit 23\n'
        )
        result = self.run_helper(*HELPERS[1], explicit=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(str(self.export), result.stderr)
        self.assertIn('ERROR: Python version mismatch', result.stderr)
        self.assertIn('IDF_PYTHON_ENV_PATH', result.stderr)
        self.assertFalse(self.calls.exists())

    def test_existing_idf_on_path_skips_discovery(self):
        self.install_fake_idf()
        self.env['PATH'] = f'{self.bin}:/usr/bin:/bin'
        self.export.write_text('echo "Unexpected activation" >&2\nexit 23\n')
        for helper, args in HELPERS:
            with self.subTest(helper=helper):
                self.calls.write_text('')
                result = self.run_helper(helper, args)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, '')
                self.assertEqual(result.stderr, '')
                self.assertIn('build', self.calls.read_text().splitlines())
        self.assertFalse(list(self.folder.glob('muse-idf-export.*')))


if __name__ == '__main__':
    unittest.main()
