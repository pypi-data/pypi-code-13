from monocular import api, util

DATABUCKET_ENDPOINT='/databuckets'

def create(label):
    path = '{0}/'.format(DATABUCKET_ENDPOINT)
    params = {
        'label': label
    }
    return api.post(path, params)

def add_data(databucket_id, data_ids):
    path = '{0}/{1}/objects/'.format(DATABUCKET_ENDPOINT, databucket_id)
    params = {
        'data': data_ids
    }
    return api.post(path, params)

def remove_data(databucket_id, image_ids):
    path = '{0}/{1}/objects/'.format(DATABUCKET_ENDPOINT, databucket_id)
    params = {
        'data': data_ids
    }
    return api.delete(path, params)

def get_data(databucket_id):
    path = '{0}/{1}/objects/'.format(DATABUCKET_ENDPOINT, databucket_id)
    return api.get(path)

def find_all():
    path = '{0}/'.format(DATABUCKET_ENDPOINT)
    params = {}
    return api.get(path, params)

def find_one(databucket_id):
    path = '{0}/{1}'.format(DATABUCKET_ENDPOINT, databucket_id)
    params = {}
    return api.get(path, params)

def update(databucket_id, options):
    path = '{0}/{1}'.format(DATABUCKET_ENDPOINT, databucket_id)
    return api.put(path, options)

def delete(databucket_id):
    path = '{0}/{1}'.format(DATABUCKET_ENDPOINT, databucket_id)
    return api.delete(path, {})
