# The MIT License (MIT)
#
# Copyright (c) 2016,Christoph Paulik
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''
Interface to wget command line utility.
'''

import subprocess
import os


def download(url, target, username=None, password=None, cookie_file=None):
    """
    Download a url using wget.
    Retry as often as necessary and store cookies if
    authentification is necessary.

    Parameters
    ----------
    url: string
        URL to download
    target: string
        path on local filesystem where to store the downloaded file
    username: string, optional
        username
    password: string, optional
        password
    cookie_file: string, optional
        file where to store cookies
    """
    cmd_list = ['wget',
                url,
                '-O', target,
                '--retry-connrefused']

    target_path = os.path.split(target)[0]
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    if username is not None:
        cmd_list.append('--user={}'.format(username))
    if password is not None:
        cmd_list.append('--password={}'.format(password))
    if cookie_file is not None:
        cmd_list = cmd_list + [
            '--load-cookies', cookie_file,
            '--save-cookies', cookie_file,
            '--keep-session-cookies']

    subprocess.call(cmd_list)


def map_download(url_target, username=None, password=None, cookie_file=None):
    """
    variant of the function that only takes one argument.
    Otherwise map_async of the multiprocessing module can not work with the function.

    Parameters
    ----------
    url_target: list
        first element the url, second the target string
    username: string, optional
        username
    password: string, optional
        password
    cookie_file: string, optional
        file where to store cookies
    """
    download(url_target[0], url_target[1],
             username=username,
             password=password,
             cookie_file=cookie_file)
