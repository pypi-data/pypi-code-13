#!/usr/bin/env python2.7

from nagios import BaseCheckCommand

try:
    from requests import HTTPError
    requests_installed = True
except ImportError:
    requests_installed = False

try:
    from sumologic import SumoLogic
    sumo_installed = True
except ImportError:
    sumo_installed = False

from optparse import OptionParser
import time

class CollectorLastMessageCheckCommand(BaseCheckCommand):
    def __init__(self, **kwargs):
        # Exit early if prereqs are not installed
        self.prerequites_test()

        # Invoke parent class's constructor
        self.__class__.__bases__[0].__init__(self,\
                parser=OptionParser(usage='%prog [options] COLLECTOR_NAME', version="%prog 1.0"))

        # Constructor for CollectorLastMessage
        self.add_options()
        params      = kwargs
        opts, args  = self.parse_args()

        self.access_id      = params.get('access_id') or opts.access_id
        self.secret_key     = params.get('secret_key') or opts.secret_key
        self.collector_name = params.get('collector_name') or args[0]

        self.warning        = int(opts.warning)
        self.critical       = int(opts.critical)

        # Instantiating the session will not raise if there are invalid credentials
        self.session        = SumoLogic(self.access_id, self.secret_key)

    def check(self):
        if not self.collector_alive():
            # state is critical because the collector is dead as a doorknob
            self.status = "CRITICAL: %s is not alive!" % self.collector_name
            self.perf_data = "alive=0;1;1;;"
            self.exit(exit_code=self.CRITICAL_EXIT)

        time_diff = time.time() - self.last_message_time()
        if time_diff >= self.critical:
            # state is critical
            self.status = "CRITICAL: %s last logged %s seconds ago" % (self.collector_name, time_diff)
            self.perf_data = "last_message=%ss;%s;%s;; alive=1;1;1;;" % (time_diff, self.warning, self.critical)
            self.exit(exit_code=self.CRITICAL_EXIT)
        elif time_diff >= self.warning:
            # state is warning
            self.status = "WARNING: %s last logged %s seconds ago" % (self.collector_name, time_diff)
            self.perf_data = "last_message=%ss;%s;%s;; alive=1;1;1;;" % (time_diff, self.warning, self.critical)
            self.exit(exit_code=self.WARNING_EXIT)
        else:
            # state is OK
            self.status = "OK: %s last logged %s seconds ago" % (self.collector_name, time_diff)
            self.perf_data = "last_message=%ss;%s;%s;; alive=1;1;1;;" % (time_diff, self.warning, self.critical)
            self.exit()

    def add_options(self):
        self.parser.add_option('-a', '--access-id',
                                dest='access_id',
                                action='store',
                                help='Sets the SumoLogic API access ID to use for queries.',
                                metavar='ACCESS_ID')
        self.parser.add_option('-s', '--secret-key',
                                dest='secret_key',
                                action='store',
                                help='sets the SumoLogic API secret key to use for queries.',
                                metavar='SECRET_KEY')

    def prerequites_test(self):
        if not requests_installed:
            self.usage(UNKNOWN_EXIT,
                        msg='Unable to import requests. Ensure the "requests" package is installed. To install: `pip install requests`')

        if not sumo_installed:
            self.usage(UNKNOWN_EXIT, 
                        msg='Unable to import sumologic-sdk. Ensure the "sumologic-sdk" package is installed. To install: `pip install sumologic-sdk`')

    def collector_alive(self):
        try:
            collectors = self.session.collectors()
            for collector in collectors:
                if collector.get('name') == self.collector_name:
                    return collector.get('alive')
        except HTTPError as e:
            self.exit(err=e)

    def last_message_time(self):
        try:
            last_message = self.session.search('_collector=%s | limit 1' % self.collector_name).pop()
            assert isinstance(last_message, dict),\
                    "Invalid API response."
        except HTTPError as e:
            self.exit(err=e)
        return int(last_message.get('_messagetime') / 1000)
