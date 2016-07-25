# allow to disable validations
validate_slicecount = True
validate_orientation = True
validate_orthogonal = True
validate_sliceincrement = True


def disable_validate_sliceincrement():
    global validate_sliceincrement
    validate_sliceincrement = False


def disable_validate_orientation():
    global validate_orientation
    validate_orientation = False


def disable_validate_orthogonal():
    global validate_orthogonal
    validate_orthogonal = False


def disable_validate_slicecount():
    global validate_slicecount
    validate_slicecount = False


def enable_validate_sliceincrement():
    global validate_sliceincrement
    validate_sliceincrement = True


def enable_validate_orientation():
    global validate_orientation
    validate_orientation = True


def enable_validate_orthogonal():
    global validate_orthogonal
    validate_orthogonal = True


def enable_validate_slicecount():
    global validate_slicecount
    validate_slicecount = True
