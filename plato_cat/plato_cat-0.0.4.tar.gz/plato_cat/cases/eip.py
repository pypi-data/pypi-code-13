

class EIPCase():

    def run(self, API, sleep):
        eips = API.conn.call('DescribeEips', {
            'status': ['active']
        })['eipSet']

        eip_ids = API.conn.call('AllocateEips', {
            'bandwidth': 1,
        })['eipIds']

        API.conn.call('ReleaseEips', {
            'eipIds': eip_ids
        })
        new_eips = API.conn.call('DescribeEips', {
            'status': ['active']
        })['eipSet']

        if len(eips) != len(new_eips):
            raise Exception("DescribeEips length did not match")
