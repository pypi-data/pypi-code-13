from monocular import api, util

DETECTOR_ENDPOINT='/detectors'

def create(label):
    path = '{0}/'.format(DETECTOR_ENDPOINT)
    params = {
        'label': label
    }
    return api.post(path, params)

def find_all():
    path = '{0}/'.format(DETECTOR_ENDPOINT)
    params = {}
    return api.get(path, params)

def find_one(detector_id):
    path = '{0}/{1}'.format(DETECTOR_ENDPOINT, detector_id)
    params = {}
    return api.get(path, params)

def detect(detector_id, **kwargs):
    path = '{0}/{1}/detect'.format(DETECTOR_ENDPOINT, detector_id)
    params = {}
    if kwargs is not None:
        if 'image' in kwargs:
            image = kwargs.get('image')

            if util.validate_image(image):
                params['image'] = util.produce_request_image(image)
            else:
                raise ValueError('Image must be a PIL image')

        elif 'url' in kwargs:
            params['url'] = kwargs.get('url')
        elif 'image_id' in kwargs:
            path = '{0}/{1}/detect/{2}'.format(DETECTOR_ENDPOINT, detector_id, image_id)
        else:
            raise TypeError('Missing required keyword argument image or url')
    else:
        raise TypeError('Missing required keyword argument image or url')

    return api.post(path, params)

def train(detector_id):
    path = '{0}/{1}'.format(DETECTOR_ENDPOINT, detector_id)
    params = {}
    return api.get(path, params)

def update(detector_id, options):
    path = '{0}/{1}'.format(DETECTOR_ENDPOINT, detector_id)
    return api.put(DETECTOR_ENDPOINT + '/' + detector_id, options)

def delete(detector_id):
    path = '{0}/{1}'.format(DETECTOR_ENDPOINT, detector_id)
    return api.delete(DETECTOR_ENDPOINT + '/' + detector_id, {})
