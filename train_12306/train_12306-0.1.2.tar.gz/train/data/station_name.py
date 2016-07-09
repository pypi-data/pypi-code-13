# -*- coding: utf-8 -*-
import re
import os


def station_name():
    file_path = os.path.join(os.path.dirname(__file__), 'station_name.js')
    with open(file_path, encoding="utf-8") as f:
        result = f.read()
    data_upper = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', result)
    data_lower = re.findall(u'@([a-z]+)\|([\u4e00-\u9fa5]+)', result)
    return dict(data_upper), dict(data_lower)
