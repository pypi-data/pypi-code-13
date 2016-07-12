# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-12 12:43:44
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-12 12:47:38

import os
from email_extractor import EE

class ResourceEmail():

    res_names_path = os.path.join(os.path.dirname(__file__), 'names.json')

    def match(self, token):
        if EE.extract_email(token):
            return True
        return False

res_email_obj = ResourceEmail()