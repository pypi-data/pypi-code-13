#!/usr/bin/python3


class DmatsaviPattern(object):
    def __init__(self, unit_name):
        self.unit_name = unit_name


class DmatsaviMessagePattern(DmatsaviPattern):
    def __init__(self, unit_name, blacklist_message_patterns, whitelist_message_patterns):
        from re import compile

        super(DmatsaviMessagePattern, self).__init__(unit_name)
        self.blacklist_message_patterns = [compile(blacklist_message_pattern) for blacklist_message_pattern in blacklist_message_patterns]
        self.whitelist_message_patterns = [compile(whitelist_message_pattern) for whitelist_message_pattern in whitelist_message_patterns]

    def _result_from_match(self, color, match):
        try:
            ipv4_address = match.group('ipv4_address')
        except IndexError:
            ipv4_address = None

        try:
            ipv6_address = match.group('ipv6_address')
        except IndexError:
            ipv6_address = None

        return color, ipv4_address, ipv6_address

    def match(self, event):
        message = event.get('MESSAGE', None)

        if message is None:
            return None, None, None

        for blacklist_message_pattern in self.blacklist_message_patterns:
            blacklist_match = blacklist_message_pattern.match(message)

            if blacklist_match:
                return self._result_from_match(False, blacklist_match)

        for whitelist_message_pattern in self.whitelist_message_patterns:
            whitelist_match = whitelist_message_pattern.match(message)

            if whitelist_match:
                return self._result_from_match(True, whitelist_match)

        return None, None, None
