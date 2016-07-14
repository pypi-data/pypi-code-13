from monocular import api, util

BGS_ENDPOINT='/background-subtractors'

def create(label, bgs_type, **kwargs):
    path = '{0}/'.format(BGS_ENDPOINT)
    options = {
        'label': label,
        'type': bgs_type,
    }


    params = util.merge_two_dicts(options, **kwargs)
    return api.post(path, params)

def add_image_id(background_subtractor_id, image_id, learning_rate):
    """
    Add an image to a background subtractor by ID.
    """
    path = '{0}/{1}/add/{2}'.format(BGS_ENDPOINT, background_subtractor_id, image_id)
    params = {
        'learning_rate': learning_rate
    }
    return api.post(path, params)

def add_image(background_subtractor_id, image, learning_rate):
    """
    Add a new image to a background subtractor.
    """
    if util.validate_image(image):
        params['image'] = util.produce_request_image(image)
        params['learningRate'] = learning_rate

        response = api.post(path, params)

        return response
    else:
        raise ValueError('Image must be a PIL Image')

def add_image_url(background_subtractor_id, url, learning_rate):
    """
    Add a new image to a background subtractor.
    """
    params = {
        'url': url,
        'learning_rate': learning_rate
    }
    return api.post(path, params)

def find_all():
    """
    Find all owned background subtractors.
    """
    path = '{0}/'.format(BGS_ENDPOINT)
    params = {}
    return api.get(path, params)

def find_one(background_subtractor_id):
    """
    Find a particular background subtractor.
    """

    path = '{0}/{1}'.format(BGS_ENDPOINT, background_subtractor_id)
    params = {}
    return api.get(path, params)

def update(background_subtractor_id, options):
    """
    Update a particular background subtractor.
    """
    path = '{0}/{1}'.format(BGS_ENDPOINT, background_subtractor_id)
    return api.put(path, options)

def delete(background_subtractor_id):
    """
    Delete a particular background subtractor.
    """
    path = '{0}/{1}'.format(BGS_ENDPOINT, background_subtractor_id)
    return api.delete(path)
