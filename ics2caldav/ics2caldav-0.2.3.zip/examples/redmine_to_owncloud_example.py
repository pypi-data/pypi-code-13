# -*- coding:utf-8 -*-
'''
Example to connect redmine to owncloud

You must have these installed:
    1. Redmine instance
    2. OwnCloud instance
    3. redmine_ics_export plugin in your redmine instance

Using:
    0. you could run this command without virtualenv but for clear workspace
        and number of dependancy it is recommended to install it in virtualenv.
    1. create a virtalenv and then `pip install ics2caldav` in it
    2. create a copy of this examples and change the `args` below
        or run it with args from commandline.
    3. don't forget to add hashbang at start of file to run it in correct place.
        `#!/path/to/virtualenv/bin/python`
    4. run it from bash or cron!
    5. if you don't like the report just remove `config_logger` line or
        create your own logger handlers/filters

@author: wTayyeb  https://github.com/wtayyeb
@license: MIT
'''

import sys

from ics2caldav.redmine2owncloud import Redmine2Owncloud


if __name__ == '__main__':
    if len(sys.argv) == 1:
        args = [
            '-i', 'https://examples.com/redmine/icalendar/<project_id>/all/open/issues.ics?key=<API-KEY>',
            '-c', 'https://examples.com/owncloud/remote.php/caldav/',
            '-d', '<calendar_id>',
            '-u', '<owncloud username>',
            '-p', '<owncloud password>',
            '--purge', '--delay',
        ]
    else:
        args = None

    Redmine2Owncloud.config_logger()
    Redmine2Owncloud.parse_args(args)


