from monocular import api, util

IDENTIFIER_ENDPOINT='/face-identifiers'

def create(label):
    path = '{0}/'.format(IDENTIFIER_ENDPOINT)
    params = {
        'label': label
    }
    return api.post(path, params)

def add_face(face_identifier_id, bucket_id, face_label):
    path = '{0}/{1}/images/'.format(IDENTIFIER_ENDPOINT, face_identifier_id)
    params = {
        'data': image_ids
    }
    return api.post(path, params)

def remove_face(face_identifier_id, face_label):
    path = '{0}/{1}/images/'.format(IDENTIFIER_ENDPOINT, face_identifier_id)
    params = {
        'data': image_ids
    }
    return api.delete(path, params)

def find_all():
    path = '{0}/'.format(IDENTIFIER_ENDPOINT)
    params = {}
    return api.get(path, params)

def find_one(face_identifier_id):
    path = '{0}/{1}'.format(IDENTIFIER_ENDPOINT, face_identifier_id)
    params = {}
    return api.get(path, params)

def identify(face_identifier_id, **kwargs):
    path = '{0}/{1}/identify'.format(IDENTIFIER_ENDPOINT, face_identifier_id)
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
            path = '{0}/{1}/identify/{2}'.format(IDENTIFIER_ENDPOINT, face_identifier_id, image_id)
        else:
            raise TypeError('Missing required keyword argument image or url')
    else:
        raise TypeError('Missing required keyword argument image or url')

    return api.post(path, params)

def train(face_identifier_id):
    path = '{0}/{1}'.format(IDENTIFIER_ENDPOINT, face_identifier_id)
    params = {}
    return api.get(path, params)

def update(face_identifier_id, options):
    path = '{0}/{1}'.format(IDENTIFIER_ENDPOINT, face_identifier_id)
    return api.put(path, options)

def delete(face_identifier_id):
    path = '{0}/{1}'.format(IDENTIFIER_ENDPOINT, face_identifier_id)
    return api.delete(path, {})
