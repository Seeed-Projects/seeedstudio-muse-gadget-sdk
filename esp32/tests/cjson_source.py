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
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


def cjson_source_dir():
    """Find cJSON.c and cJSON.h for host harnesses, or skip with setup instructions."""
    candidates = []
    override = os.environ.get("CJSON_SOURCE_DIR")
    if override:
        candidates.append(Path(override).expanduser())
    candidates.append(ROOT / "managed_components/espressif__cjson/cJSON")

    cache_override = os.environ.get("IDF_COMPONENT_CACHE_PATH")
    if cache_override:
        cache = Path(cache_override).expanduser()
    elif sys.platform == "darwin":
        cache = Path.home() / "Library/Caches/Espressif/ComponentManager"
    elif sys.platform == "win32":
        cache = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local"))
        cache /= "Espressif/ComponentManager/Cache"
    else:
        cache = Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache")
        cache /= "Espressif/ComponentManager"
    candidates.extend(sorted(cache.glob("service_*/espressif__cjson_*/cJSON")))

    for source in candidates:
        if all((source / name).is_file() for name in ("cJSON.c", "cJSON.h")):
            return source.resolve()
    checked = ", ".join(str(path) for path in [*candidates, cache])
    raise unittest.SkipTest(
        "cJSON sources not found: set CJSON_SOURCE_DIR to a directory containing "
        f"cJSON.c and cJSON.h (checked {checked})"
    )
