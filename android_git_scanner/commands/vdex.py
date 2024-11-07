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

import json
import pathlib

import click
from git import Repo
from packaging.version import parse

from ..utils import extract_android_version_from_tag, extract_vdex_version, iterate_tags


@click.command(name="vdex")
@click.argument("git-folder", type=click.Path(exists=True))
@click.option("--output", type=click.Path(), default="vdex_versions.json")
def vdex(git_folder, output):
    git_folder = pathlib.Path(git_folder)

    repo = Repo(git_folder)

    android_versions = {}
    for commit, tag in iterate_tags(repo):
        # Search for vdex_file.h
        try:
            file = commit.tree["runtime/vdex_file.h"]
        except KeyError:
            continue

        # Extract Vdex version
        vdex_version = extract_vdex_version(file.data_stream.read().decode())
        if not vdex_version:
            continue

        # Extract Android version from tag
        android_version_match = extract_android_version_from_tag(tag.name)
        if android_version_match:
            android_version, android_version_revision = android_version_match

            if android_version not in android_versions:
                android_versions[android_version] = set()

            android_versions[android_version].add(vdex_version)

    with open(output, "w") as f:
        output_data = dict(
            (version, sorted(list(items)))
            for version, items in sorted(
                android_versions.items(), key=lambda x: parse(x[0])
            )
        )
        json.dump(output_data, f, separators=(",", ":"))
