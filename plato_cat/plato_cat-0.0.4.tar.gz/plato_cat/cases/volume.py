

class VolumeCase():

    def run(self, API, sleep):
        volumes = API.conn.call('DescribeVolumes', {
            'status': ['active']
        })['volumeSet']

        volume_ids = API.conn.call('CreateVolumes', {
            'size': 1,
            'volumeType': 'normal',
        })['volumeIds']
        while True:
            actived = API.conn.call('DescribeVolumes', {
                'volumeIds': volume_ids,
                'status': ['active']
            })['total']
            if actived == len(volume_ids):
                break
            sleep(10)

        API.conn.call('DeleteVolumes', {
            'volumeIds': volume_ids
        })
        new_volumes = API.conn.call('DescribeVolumes', {
            'status': ['active']
        })['volumeSet']

        if len(volumes) != len(new_volumes):
            raise Exception("DescribeVolumes length did not match")
