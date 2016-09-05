"""
 Copyright (C) 2016 Maruf Maniruzzaman
 Website: http://cosmosframework.com
 Author: Maruf Maniruzzaman
 License :: OSI Approved :: MIT License
"""

import os
import base64


def generate_password_b64(length=48):
    password = os.urandom(length)
    return base64.b64encode(password)
