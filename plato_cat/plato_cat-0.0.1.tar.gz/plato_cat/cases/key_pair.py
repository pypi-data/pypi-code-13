from .. sdk.actions import params


class KeyPairCase():

    def run(self, API):
        payload = {}
        payload = params.filter_status(payload, ['active'])

        keypairs = API.conn.call('DescribeKeyPairs', payload)
        return keypairs
