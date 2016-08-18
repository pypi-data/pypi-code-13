from .. sdk.actions import params


class InstanceCase():

    def run(self, API):
        payload = {}
        payload = params.filter_status(payload, ['active'])

        instances = API.conn.call('DescribeInstances', payload)
        return instances
