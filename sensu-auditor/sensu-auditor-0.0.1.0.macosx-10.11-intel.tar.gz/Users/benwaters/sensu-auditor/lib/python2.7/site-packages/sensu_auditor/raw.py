class RawReportableList(list):
    """

    """
    def get_total_downtime(self):
        """

        :return:
        """
        total = 0
        for entry in self:
            total += entry.downtime
        return total


class RawReportableEntry(object):
    """

    """
    def __init__(self, check_name, category, start_time, end_time):
        self.check_name = check_name
        self.start_time = start_time
        self.end_time = end_time
        self.downtime = (self.end_time - self.start_time).seconds
        self.category = category

    def __repr__(self):
        return str({'category': self.category, 'check_name': self.check_name})

    def __str__(self):
        return "{}\n{}:\n start:{}\n end:{}\ndowntime:{}".format(self.category, self.check_name, str(self.start_time), str(self.end_time), self.downtime)