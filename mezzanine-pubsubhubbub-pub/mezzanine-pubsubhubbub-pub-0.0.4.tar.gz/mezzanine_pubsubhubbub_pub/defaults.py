# -*- coding: utf-8 -*-
"""
   Copyright 2016 Kem

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from __future__ import print_function
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from mezzanine.conf import register_setting
from mezzanine_pubsubhubbub_pub import PROTOCOL_TYPE_CHOICES, PROTOCOL_TYPE_HTTP

register_setting(
    name="PUSH_HUB",
    description=_("You can either use your own or use a public hub. "
                  "add your hub’s URL as a PUSH_HUB setting (the URL must be a full URL)"),
    editable=False,
    default=("https://pubsubhubbub.appspot.com/",),
)

register_setting(
    name="PUSH_URL_PROTOCOL",
    description=_("Your feed url protcol."
                  "You can choice in HTTP_ONLY , HTTPS_ONLY, BOTH"),
    editable=True,
    default=PROTOCOL_TYPE_HTTP,
    choices=PROTOCOL_TYPE_CHOICES,
)
