

class KeyPairCase():

    def run(self, API, sleep):
        keypairs = API.conn.call('DescribeKeyPairs', {
            'status': ['active']
        })['keyPairSet']
        keypair_id = API.conn.call('CreateKeyPair')['keyPairId']
        API.conn.call('DeleteKeyPairs', {
            'keyPairIds': [keypair_id]
        })
        new_keypairs = API.conn.call('DescribeKeyPairs', {
            'status': ['active']
        })['keyPairSet']

        if len(keypairs) != len(new_keypairs):
            raise Exception("DescribeVolumes length did not match")
