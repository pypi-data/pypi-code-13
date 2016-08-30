#!/usr/bin/python3


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class DmatsaviAction(object):
    def __init__(self):
        pass

    def perform(self, **kwargs):
        pass


class DmatsaviIPTables4Manager(object, metaclass=Singleton):
    def __init__(self):
        from iptc import Rule
        from iptc import Table

        self.filter_table = Table(Table.FILTER)
        self.chain = None
        self.ipv4 = set()
        self.ipv6 = set()

        for chain in self.filter_table.chains:
            if chain.name == 'DAMTSAVI':
                self.chain = chain
                break

        if self.chain is None:
            self.chain = self.filter_table.create_chain('DAMTSAVI')

        for chain in self.filter_table.chains:
            if chain.name == 'INPUT':
                has_rule = False

                for rule in chain.rules:
                    if rule.target.name == 'DAMTSAVI':
                        has_rule = True

                if not has_rule:
                    rule = Rule()
                    rule.src = '0.0.0.0/0.0.0.0'
                    rule.create_target('DAMTSAVI')
                    chain.insert_rule(rule)

        for rule in self.chain.rules:
            print('iptables v4 already banned; {0}.'.format(rule.src))
            self.ipv4.add(rule.src)

    def append(self, ipv4_address):
        from iptc import Rule

        if not ipv4_address in self.ipv4:
            print('iptables v4 ban; {0}.'.format(ipv4_address))
            self.ipv4.add(ipv4_address)

            rule = Rule()
            rule.src = ipv4_address
            rule.create_target('DROP')
            self.chain.insert_rule(rule)


class DmatsaviIPTables4DenyAction(DmatsaviAction):
    def __init__(self):
        pass

    def perform_ipv4(self, ipv4_address):
        DmatsaviIPTables4Manager().append(ipv4_address + '/255.255.255.255')

    def perform_ipv6(self, ipv6_address):
        pass
