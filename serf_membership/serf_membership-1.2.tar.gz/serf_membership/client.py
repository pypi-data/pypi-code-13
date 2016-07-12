from serfclient.client import SerfClient

class SerfMembershipNoMembers(Exception): pass

class SerfMembership:
    def __init__(self, **kwargs):
        self.role = kwargs.get('role', False)

        serf = SerfClient()
        members = serf.members().body['Members']

        if self.role:
            self.members = [member for member in members \
                if member["Tags"]["role"] == self.role and member["Status"] == "alive"]
        else:
            self.members = members

        for member in self.members:
            member['Tags']['startedat'] = int(member['Tags'].get('startedat', 999999999999999999999999))

    def primary(self):
        oldest_member = {}
        oldest_member_time = self._oldest_member_time()

        for member in self.members:
            if member['Tags']['startedat'] == oldest_member_time:
                oldest_member = member
                break
        return oldest_member

    def secondaries(self):
        result = []
        oldest_member_time = self._oldest_member_time()

        for member in self.members:
            if member['Tags']['startedat'] != oldest_member_time:
                result.append(member)
        return result

    def is_primary(self,**kwargs):
        member_name = kwargs['name']
        if self.primary()['Name'] == member_name:
            return True
        else:
            return False
    def is_secondary(self, **kwargs):
        return not self.is_primary(name=kwargs['name'])


    def _oldest_member_time(self):
        if len(self.members) is 0:
            raise SerfMembershipNoMembers("Error: No members with role {0}".format(self.role))
        result = min([member['Tags']['startedat'] \
            for member in self.members])
        return result

if __name__ == '__main__':
    members = SerfMembership(role="master")
    print(members.primary())
    print(members.secondaries())
    print(members.is_primary(name="os3-4.devnodes.eu-bg-sof.startappcloud.com"))
    print(members.is_primary(name="os3-1.devnodes.eu-bg-sof.startappcloud.com"))
    print(members.is_secondary(name="os3-4.devnodes.eu-bg-sof.startappcloud.com"))
    print(members.is_secondary(name="os3-1.devnodes.eu-bg-sof.startappcloud.com"))

