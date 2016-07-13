

# Object to be returned after calling activate and senddata functions
class IvenResponse:
    """ this object could be filled differently according to the related request.
        Users should check the fields if they not null or zero,
        otherwise they are set to the data came from the server.
    """

    def __init__(self):
        self.iven_code = 0
        self.description = None
        self.message = None
        self.task = 0
        self.need_conf_update = False
        self.need_firm_update = False
        self.api_key = None
        self.device_uid = None
        self.status = 0

# TODO: Add error return codes here
