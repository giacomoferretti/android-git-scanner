# Copyright 2024 Giacomo Ferretti
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

import re

from git import Repo

ignored_tag_words = [
    "platform-tools",
    "-preview",
    "-dp",
    "-beta",
    "-vts",
    "-cts",
    "-security",
    "aml_",
    "frc_",
]

android_tag_regex = re.compile(r"android-(\d+\.\d+(?:\.\d+)?)_(r.*)")

c_char_array_regex = re.compile(r"'(\d)',\s*'(\d)',\s*'(\d)'")

# Oat
oat_version_regex = re.compile(r"kOatVersion\s*{\s*{(.*?)}\s*};")
oat_version_regex_legacy = re.compile(r"kOatVersion\[\]\s*=\s*{(.*?)};")

# Vdex
vdex_version_regex_legacy = re.compile(r"kVdexVersion\[\]\s*=\s*{(.*?)};")
vdex_version_regex_new = re.compile(r"kVerifierDepsVersion\[\]\s*=\s*{(.*?)};")


def cleanup_version(oat_version: str):
    match = c_char_array_regex.search(oat_version)
    if match:
        return f"{match.group(1)}{match.group(2)}{match.group(3)}"

    return None


def _extract_oat_version(data: str):
    match = oat_version_regex.search(data)
    if match:
        return match.group(1).strip()

    return None


def _extract_oat_version_legacy(data: str):
    match = oat_version_regex_legacy.search(data)
    if match:
        return match.group(1).strip()

    return None


def extract_oat_version(data: str):
    version = _extract_oat_version(data)
    if version:
        return cleanup_version(version.strip())

    # Legacy
    version = _extract_oat_version_legacy(data)
    if version:
        return cleanup_version(version.strip())

    return None


def _extract_vdex_version(data: str):
    match = vdex_version_regex_new.search(data)
    if match:
        return match.group(1).strip()

    return None


def _extract_vdex_version_legacy(data: str):
    match = vdex_version_regex_legacy.search(data)
    if match:
        return match.group(1).strip()

    return None


def extract_vdex_version(data: str):
    version = _extract_vdex_version(data)
    if version:
        return cleanup_version(version.strip())

    # Legacy
    version = _extract_vdex_version_legacy(data)
    if version:
        return cleanup_version(version.strip())

    return None


def extract_android_version_from_tag(tag_name: str):
    match = android_tag_regex.search(tag_name)
    if match:
        return match.group(1), match.group(2)

    return None


def iterate_tags(repo: Repo):
    for tag in repo.tags:
        commit = tag.commit

        # Ignore tags with specific words
        if any(word in tag.name for word in ignored_tag_words):
            continue

        yield commit, tag
