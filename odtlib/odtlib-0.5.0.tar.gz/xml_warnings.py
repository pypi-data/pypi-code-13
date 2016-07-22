from __future__ import with_statement

class DocWarnings(object):
    def __init__(self, w_type, warnings, headers=(), specs=(), help_msg=(), level=None):
        pass

    def print_html(self):
	"""html report"""
        raise NotImplementedError

class XMLWarnings(object):
    def __init__(self, warnings, level="war"):
        pass

    def print_row(self):
	"""html report"""
        raise NotImplementedError
