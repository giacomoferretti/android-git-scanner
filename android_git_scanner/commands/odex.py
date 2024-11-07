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
from git import Commit, Repo
from packaging.version import parse

from ..utils import extract_android_version_from_tag, extract_oat_version, iterate_tags


def find_oat_version_file(commit: Commit):
    file = None
    try:
        # Newer Android versions
        file = commit.tree["runtime/oat/oat.h"]
    except KeyError:
        try:
            # Older Android versions
            file = commit.tree["runtime/oat.h"]
        except KeyError:
            return None, None

    oat_version = extract_oat_version(file.data_stream.read().decode())
    if oat_version:
        return oat_version, file

    try:
        # Fallback
        file = commit.tree["runtime/oat.cc"]
    except KeyError:
        return None, None

    oat_version = extract_oat_version(file.data_stream.read().decode())
    if oat_version:
        return oat_version, file

    return None, None


@click.command(name="oat")
@click.argument("git-folder", type=click.Path(exists=True))
@click.option("--output", type=click.Path(), default="oat_versions.json")
@click.option("--invert", help="Invert the output", is_flag=True)
def oat(git_folder, output, invert):
    git_folder = pathlib.Path(git_folder)

    repo = Repo(git_folder)

    android_versions = {}
    for commit, tag in iterate_tags(repo):
        oat_version, file = find_oat_version_file(commit)
        if not oat_version:
            continue

        # Extract Android version from tag
        android_version_match = extract_android_version_from_tag(tag.name)
        if android_version_match:
            android_version, android_version_revision = android_version_match

            if invert:
                if oat_version not in android_versions:
                    android_versions[oat_version] = set()

                android_versions[oat_version].add(android_version)
            else:
                if android_version not in android_versions:
                    android_versions[android_version] = set()

                android_versions[android_version].add(oat_version)

    with open(output, "w") as f:
        if invert:
            output_data = dict(
                (key, sorted(list(values), key=parse) if values else [])
                for key, values in sorted(android_versions.items())
            )
        else:
            output_data = dict(
                (version, sorted(list(items)))
                for version, items in sorted(android_versions.items(), key=lambda x: parse(x[0]))
            )
        json.dump(output_data, f, separators=(",", ":"))
