#!/usr/bin/env python

"""
  Author:  Yeison Cardona --<yeison.eng@gmail.com>
  Purpose:
  Created: 22/10/15
"""

import random
import string

#----------------------------------------------------------------------
def new_key():
    """"""
    secret_key = ''.join([random.SystemRandom().choice(string.ascii_letters + string.digits + string.punctuation) for i in range(50)])
    return secret_key