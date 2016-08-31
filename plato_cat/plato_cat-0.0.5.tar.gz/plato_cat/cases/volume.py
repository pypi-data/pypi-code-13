from plato_cat.cases import wait_for_job
from plato_cat.cases import get_resource
from plato_cat.cases import post_resource


class VolumeCase():

    def run(self, API, sleep):
        result = API.conn.call('CreateVolumes', {
            'size': 1,
            'name': 'create-volume-name',
            'volumeType': 'normal',
            'count': 2
        })

        job_id = result['jobId']
        volume_ids = result['volumeIds']

        wait_for_job(API, job_id, sleep)

        volumes = get_resource(API, 'DescribeVolumes', {
            'status': ['active'],
            'volumeIds': volume_ids
        }, 'volumeSet')

        for v in volumes:
            if v['status'] != 'active':
                raise Exception('volume (%s) creation job finished, but status is not [active], but [%s]' % (v['volumeId'], v['status']))


class CleanVolumes():

    def run(self, API, sleep):
        volumes = get_resource(API, 'DescribeVolumes', {
            'status': ['active', 'inuse']
        }, 'volumeSet')

        # detach volumes
        for volume in volumes:
            if volume['instanceId']:
                API.conn.call('DetachVolumes', {
                    'volumeIds': [volume['volumeId']],
                    'instanceId': volume['instanceId']
                })

        volume_ids = [v['volumeId'] for v in volumes]
        post_resource(API, 'DeleteVolumes', volume_ids, 'volumeIds')

