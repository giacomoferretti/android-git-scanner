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


from android_git_scanner.utils import cleanup_version, extract_oat_version


def test_extract_oat_version():
    # 4.4
    data = "const uint8_t OatHeader::kOatVersion[] = { '0', '0', '7', '\\0' };"
    assert extract_oat_version(data) == "007"

    # 4.4.3
    data = "const uint8_t OatHeader::kOatVersion[] = { '0', '0', '8', '\\0' };"
    assert extract_oat_version(data) == "008"

    # 5.0.0
    data = "const uint8_t OatHeader::kOatVersion[] = { '0', '3', '9', '\\0' };"
    assert extract_oat_version(data) == "039"

    # 6.0.0
    data = "static constexpr uint8_t kOatVersion[] = { '0', '6', '4', '\\0' };"
    assert extract_oat_version(data) == "064"

    # 10.0.0
    data = "static constexpr std::array<uint8_t, 4> kOatVersion { { '1', '7', '0', '\\0' } };"
    assert extract_oat_version(data) == "170"

    # 15.0.0
    data = "static constexpr std::array<uint8_t, 4> kOatVersion{{'2', '4', '4', '\\0'}};"
    assert extract_oat_version(data) == "244"


def test_cleanup_version():
    # 4.4
    data = "'0', '0', '7', '\\0'"
    assert cleanup_version(data) == "007"

    # 4.4.3
    data = "'0', '0', '8', '\\0'"
    assert cleanup_version(data) == "008"

    # 5.0.0
    data = "'0', '3', '9', '\\0'"
    assert cleanup_version(data) == "039"

    # 6.0.0
    data = "'0', '6', '4', '\\0'"
    assert cleanup_version(data) == "064"

    # 10.0.0
    data = "'1', '7', '0', '\\0'"
    assert cleanup_version(data) == "170"

    # 15.0.0
    data = "'2', '4', '4', '\\0'"
    assert cleanup_version(data) == "244"
