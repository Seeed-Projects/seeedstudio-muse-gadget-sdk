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

import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import cjson_source


class CjsonSourceTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        self.home = self.root / "home"
        self.managed = self.root / "managed_components/espressif__cjson/cJSON"
        self.cache = self.home / "Library/Caches/Espressif/ComponentManager"
        for mocked in (
            patch.object(cjson_source, "ROOT", self.root),
            patch.object(cjson_source.Path, "home", return_value=self.home),
            patch.object(cjson_source.sys, "platform", "darwin"),
            patch.dict(os.environ, {}, clear=True),
        ):
            mocked.start()
            self.addCleanup(mocked.stop)

    def sources(self, directory):
        directory.mkdir(parents=True)
        for name in ("cJSON.c", "cJSON.h"):
            (directory / name).touch()
        return directory

    def cached_sources(self, cache=None):
        return self.sources((cache or self.cache)
                            / "service_1234/espressif__cjson_1.7.19~2_abcd/cJSON")

    def test_override_precedes_managed_and_cache(self):
        override = self.sources(self.root / "override")
        os.environ["CJSON_SOURCE_DIR"] = str(override)
        self.sources(self.managed)
        self.cached_sources()
        self.assertEqual(cjson_source.cjson_source_dir(), override)

    def test_managed_precedes_cache(self):
        self.sources(self.managed)
        self.cached_sources()
        self.assertEqual(cjson_source.cjson_source_dir(), self.managed)

    def test_relative_override_returns_an_absolute_path(self):
        override = self.sources(self.root / "relative-override")
        os.environ["CJSON_SOURCE_DIR"] = os.path.relpath(override)
        self.assertEqual(cjson_source.cjson_source_dir(), override)

    def test_cache_after_managed_components_cleanup(self):
        cached = self.cached_sources()
        self.assertFalse(self.managed.parent.exists())
        self.assertEqual(cjson_source.cjson_source_dir(), cached)

    def test_incomplete_override_falls_back_to_managed(self):
        override = self.root / "override"
        override.mkdir()
        (override / "cJSON.c").touch()
        os.environ["CJSON_SOURCE_DIR"] = str(override)
        self.sources(self.managed)
        self.assertEqual(cjson_source.cjson_source_dir(), self.managed)

    def test_incomplete_cache_entry_is_skipped(self):
        incomplete = self.cache / "service_0000/espressif__cjson_1.7.18_abcd/cJSON"
        incomplete.mkdir(parents=True)
        (incomplete / "cJSON.h").touch()
        cached = self.cached_sources()
        self.assertEqual(cjson_source.cjson_source_dir(), cached)

    def test_custom_component_cache(self):
        cache = self.root / "custom-cache"
        os.environ["IDF_COMPONENT_CACHE_PATH"] = str(cache)
        cached = self.cached_sources(cache)
        self.assertEqual(cjson_source.cjson_source_dir(), cached)

    def test_linux_default_cache(self):
        with patch.object(cjson_source.sys, "platform", "linux"):
            cached = self.cached_sources(self.home / ".cache/Espressif/ComponentManager")
            self.assertEqual(cjson_source.cjson_source_dir(), cached)

    def test_linux_xdg_cache(self):
        os.environ["XDG_CACHE_HOME"] = str(self.root / "xdg")
        with patch.object(cjson_source.sys, "platform", "linux"):
            cached = self.cached_sources(self.root / "xdg/Espressif/ComponentManager")
            self.assertEqual(cjson_source.cjson_source_dir(), cached)

    def test_windows_cache(self):
        os.environ["LOCALAPPDATA"] = str(self.root / "local")
        with patch.object(cjson_source.sys, "platform", "win32"):
            cached = self.cached_sources(self.root / "local/Espressif/ComponentManager/Cache")
            self.assertEqual(cjson_source.cjson_source_dir(), cached)

    def test_missing_sources_names_override_and_checked_locations(self):
        with self.assertRaises(unittest.SkipTest) as missing:
            cjson_source.cjson_source_dir()
        message = str(missing.exception)
        for expected in ("CJSON_SOURCE_DIR", "cJSON.c", "cJSON.h", str(self.managed), str(self.cache)):
            self.assertIn(expected, message)


if __name__ == "__main__":
    unittest.main()
