'''
Ex.:

'''

import re


class BaseRule(object):
    base = None
    scope = 'base'

    def __init__(self, base=None, scope=None):
        self.base = base or self.base
        self.scope = scope or self.scope

    def check(self, base, source):
        if self.base:
            if base.startswith('+'):
                base = base[1:] + base
            else:
                base = self.base
        results = source.search(base=base, scope=self.scope)
        for warning in self.check_entries(results):
            yield warning

    def check_entries(self, results):
        while False:
            yield None


class CardinalityRule(BaseRule):
    min_count = None
    max_count = None
    regexp = None

    def __init__(self, base=None, scope=None, attribute=None, min_count=None, max_count=None):
        self.attribute = attribute or self.attribute
        self.min_count = min_count
        self.max_count = max_count
        super(CardinalityRule, self).__init__(base=base, scope=scope)

    def check_entries(self, results):
        for dn, entries in results:
            for attribute, values in entries.iteritems():
                if attribute == self.attribute:
                    if self.min_count and len(values) < self.min_count:
                        yield ('attribute "{attribute}" must have at least {min_count} values, '
                               'here there are {count}.'.format(count=len(values), **self.__dict__))


class RegexpRule(BaseRule):
    attribute = None
    regexp = None

    def __init__(self, base=None, scope=None, attribute=None, regexp=None):
        self.attribute = attribute or self.attribute
        self.regexp = regexp or self.regexp
        super(RegexpRule, self).__init__(base=base, scope=scope)

    def check_entries(self, results):
        for dn, entries in results:
            for attribute, values in entries.iteritems():
                if attribute == self.attribute:
                    for value in values:
                        if not re.match(self.regexp, value):
                            yield ('attribute "{attribute}" value "{value}" does not match '
                                   '{regexp}'.format(value=value, **self.__dict__))


class Checker(object):
    '''Validate an LDAP source (LDAP connection or LDIF) against a list or rules'''

    # list of rules to check
    rules = None

    def __init__(self, source, base, rules=None):
        self.source = source
        self.base = base
        self.rules = rules or self.rules

    def check(self):
        for rule in self.rules:
            rule.check(self.base, self.source)
