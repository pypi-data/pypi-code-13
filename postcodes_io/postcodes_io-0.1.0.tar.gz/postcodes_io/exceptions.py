
class PostcodeError(Exception):
    """
    General postcode error
    """
    #TODO: init with http status code and a message
    pass


class PostcodeNotFoundError(PostcodeError):
    pass
