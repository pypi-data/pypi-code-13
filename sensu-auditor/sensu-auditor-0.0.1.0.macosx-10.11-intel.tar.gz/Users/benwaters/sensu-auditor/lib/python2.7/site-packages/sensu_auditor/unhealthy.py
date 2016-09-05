class UnhealthyList(list):
    """
    """
    def get_by_name(self, name):
        """

        :param name:
        :return:
        """
        try:
            return [index for index, x in enumerate(self) if x.check_name == name][0]
        except ValueError:
            return None

    def names(self):
        """

        :return:
        """
        return [x.check_name for x in self]


class UnhealthyEntry(object):
    """

    """
    def __init__(self, check_name, start_time=None, end_time=None):
        self.check_name = check_name
        self.start_time = start_time
        self.end_time = end_time