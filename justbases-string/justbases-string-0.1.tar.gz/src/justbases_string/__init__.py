# Copyright 2016 Red Hat, Inc.
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

"""
Top level of justbases_string.
"""

from ._approx import ApproxPrefix

from ._config import ApproxConfig
from ._config import BaseConfig
from ._config import DigitsConfig
from ._config import DisplayConfig
from ._config import StripConfig

from ._errors import BaseDisplayError

from ._string import String

from ._version import __version__
