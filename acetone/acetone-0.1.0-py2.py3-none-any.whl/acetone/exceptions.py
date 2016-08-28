class AcetoneError(Exception):
    pass


class AcetoneNotFoundError(AcetoneError):
    pass


class AcetoneAlreadyRegisteredError(AcetoneError):
    pass


class AcetoneLoadError(AcetoneError):
    pass
