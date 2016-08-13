from flake8_meiqia import core


@core.flake8ext
def meiqia_no_cr(physical_line):
    """Checks there is no windows style line endings."""

    pos = physical_line.find('\r')
    if pos >= 0 and pos == len(physical_line) - 2:
        return pos, "MQ903: Windows style line endings not allowed"
