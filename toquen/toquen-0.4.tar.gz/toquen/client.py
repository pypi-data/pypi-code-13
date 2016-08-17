import boto3


class AWSClient(object):
    def __init__(self, key_id=None, secret_key=None, regions=None, cache=True):
        self.clients = []
        regions = regions or []
        self.should_cache = cache
        self.cache = None
        if len(regions) == 0:
            self.clients = [boto3.client('ec2', aws_access_key_id=key_id, aws_secret_access_key=secret_key)]
        for region in regions:
            client = boto3.client('ec2', aws_access_key_id=key_id, aws_secret_access_key=secret_key, region_name=region)
            self.clients.append(client)

    def server_with_role(self, role, env=None):
        return self.servers_with_roles([role], env)

    def servers_with_roles(self, roles, env=None, match_all=False):
        """
        Get servers with the given roles.  If env is given, then the environment must match as well.
        If match_all is True, then only return servers who have all of the given roles.  Otherwise,
        return servers that have one or more of the given roles.
        """
        result = []
        roles = set(roles)
        for instance in self.server_details():
            instroles = set(instance['roles'])
            envmatches = (env is None) or (instance['environment'] == env)
            if envmatches and match_all and roles <= instroles:
                result.append(instance)
            elif envmatches and not match_all and len(roles & instroles) > 0:
                result.append(instance)
        return result

    def server_details(self):
        filters = [{'Name': 'instance-state-name', 'Values': ['running']}]
        if self.cache is not None:
            return self.cache
        results = []
        for client in self.clients:
            for reservation in client.describe_instances(Filters=filters)['Reservations']:
                for instance in reservation['Instances']:
                    results.append(self._parse_instance(instance))
        if self.should_cache:
            self.cache = results
        return results

    def _parse_instance(self, details):
        tags = {f['Key']: f['Value'] for f in details['Tags']}
        name = tags.get('Name', None)
        return {
            'id': name,
            'internal_ip': details['PrivateIpAddress'],
            'external_ip': details['PublicIpAddress'],
            'name': name,
            'roles': [s.strip() for s in tags.get('Roles', '').split(' ') if s != ''],
            'type': details['InstanceType'],
            'external_dns': details['PublicDnsName'],
            'internal_dns': details['PrivateDnsName'],
            'security_groups': [sg['GroupId'] for sg in details['SecurityGroups']],
            'environment': tags.get('Environment', None)
        }


class FabricFriendlyClient(AWSClient):
    def ips_with_roles(self, roles, env=None, match_all=False):
        """
        Returns a function that, when called, gets servers with the given roles.
        If env is given, then the environment must match as well.  If match_all is True,
        then only return servers who have all of the given roles.  Otherwise, return
        servers that have one or more of the given roles.
        """
        def func():
            return [s['external_ip'] for s in self.servers_with_roles(roles, env, match_all)]
        return func
