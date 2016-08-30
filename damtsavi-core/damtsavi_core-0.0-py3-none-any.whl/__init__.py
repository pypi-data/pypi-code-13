#!/usr/bin/python3


class DmatsaviProtectedService(object):
    def __init__(self, patterns, actions):
        self.patterns = patterns
        self.actions = actions


class DmatsaviJournalProcessor(object):
    def _parse_event(self, event):
        result_ipv4 = []
        result_ipv6 = []
        unit_name = event.get('_SYSTEMD_UNIT', None)

        if unit_name:
            services = self._observed_units.get(unit_name, None)

            if services:
                for service in services:
                    for pattern in service.patterns:
                        color, ipv4_address, ipv6_address = pattern.match(event)

                        if not color is None:
                            break

                    if not color is None:
                        if color:
                            if ipv4_address:
                                result_ipv4.append((True, ipv4_address))

                            if ipv6_address:
                                result_ipv6.append((True, ipv6_address))
                        else:
                            if ipv4_address:
                                result_ipv4.append((False, ipv4_address))

                            if ipv6_address:
                                result_ipv6.append((False, ipv6_address))

                return services, result_ipv4, result_ipv6

        return None, result_ipv4, result_ipv6

    def __init__(self, protected_services):
        from collections import defaultdict
        from systemd.journal import Reader

        self._observed_units = defaultdict(list)

        for service in protected_services:
            for pattern in service.patterns:
                self._observed_units[pattern.unit_name].append(service)

        self._journal = Reader()
        self._journal.this_boot()
        self._journal.add_conjunction()

        for unit_name in self._observed_units.keys():
            print('Processor; subscribe to journal; {0}.'.format(unit_name))
            self._journal.add_match(_SYSTEMD_UNIT=unit_name)

        self._whitelist_ipv4 = set()
        self._blacklist_ipv4 = set()
        self._whitelist_ipv6 = set()
        self._blacklist_ipv6 = set()

    def _process_events(self):
        for event in self._journal:
            services, result_ipv4, result_ipv6 = self._parse_event(event)

            if services:
                for item_ipv4 in result_ipv4:
                    if item_ipv4[0] and (not item_ipv4[1] in self._whitelist_ipv4):
                        print('Whitelist; adding IPv4; {0}.'.format(item_ipv4[1]))
                        self._whitelist_ipv4.add(item_ipv4[1])

                for item_ipv6 in result_ipv6:
                    if item_ipv6[0] and (not item_ipv6[1] in self._whitelist_ipv6):
                        print('Whitelist; adding IPv6; {0}.'.format(item_ipv6[1]))
                        self._whitelist_ipv6.add(item_ipv6[1])

                for service in services:
                    for item_ipv4 in result_ipv4:
                        if not item_ipv4[0] and (not item_ipv4[1] in self._whitelist_ipv4) and (not item_ipv4[1] in self._blacklist_ipv4):
                            print('Blacklist; adding IPv4; {0}.'.format(item_ipv4[1]))
                            self._blacklist_ipv4.add(item_ipv4[1])

                            for action in service.actions:
                                action.perform_ipv4(item_ipv4[1])

                    for item_ipv6 in result_ipv6:
                        if not item_ipv6[0] and (not item_ipv6[1] in self._whitelist_ipv6) and (not item_ipv6[1] in self._blacklist_ipv6):
                            print('Blacklist; adding IPv6; {0}.'.format(item_ipv6[1]))
                            self._blacklist_ipv6.add(item_ipv6[1])

                            for action in service.actions:
                                action.perform_ipv6(item_ipv6[1])

    def loop(self):
        from select import poll
        from systemd.journal import APPEND

        self._process_events()

        journal_poll = poll()
        journal_poll.register(self._journal, self._journal.get_events())

        while journal_poll.poll():
            if self._journal.process() != APPEND:
                continue

            self._process_events()
