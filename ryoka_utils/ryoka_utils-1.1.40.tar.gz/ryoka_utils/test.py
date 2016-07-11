#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import Utils
from debugger import Debugger
from mail import SendMail
from slack import Slack

if __name__ == '__main__':
    u = Utils()

    u.unzip_tar_gz("./test.tar.gz", "./AAA")
