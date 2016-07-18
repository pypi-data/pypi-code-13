import logging
from dateutil.parser import parse
from isa.plugin import Plugin

_logger = logging.getLogger(__name__)


def plugin_init(args):
    return IOStat(args.interval)


class IOStat(Plugin):
    def __init__(self, timewindow=None):
        self.timewindow = timewindow

    def collect(self, server):
        """
        Execute iostat on the server.

        :return: list of result objects (list of dictionaries)
        """
        timewindow_str = ""
        if self.timewindow is not None and self.timewindow > 0:
            timewindow_str = "%d 2" % self.timewindow
        command = "iostat -k -t -x %s" % timewindow_str
        result = server.execute(command)
        _logger.debug(command)
        return self.parse_iostat(result)

    @staticmethod
    def parse_iostat(str):
        """
        Parse the raw response from iostat.

        :param str: raw response from iostat
        :return: list of result objects (list of dictionaries)
        """
        lines = str.replace("\r", "").split("\n")
        data = {}
        execution_time = None
        header = None
        headers = {}
        for line in lines:
            try:
                parsed = parse(line, dayfirst=True)
                execution_time = parsed
                # Reset all other data, since this is the more recent one
                data = {}
                headers = {}
                continue
            except ValueError:
                pass
            line = line.replace(",", ".")
            if ':' in line:
                items = line.split()
                key = items[0][:-1]
                header = items[1:]
                headers[key] = header
                data[key] = []
            else:
                if header is not None:
                    row = line.split()
                    if len(row) == 0:
                        header = None
                    else:
                        data[key].append(row)

        # Now transform to a useful format
        devices = {}
        for device_data in data['Device']:
            devices[device_data[0]] = {
                header: float(value)
                for (header, value) in zip(headers['Device'], device_data[1:])
                }

        cpu = {
            header: float(value)
            for (header, value) in zip(headers['avg-cpu'], data['avg-cpu'][0])
            }

        # Figure out all fields
        fields = ["execution_time", "device"]
        device_fields = []
        cpu_fields = []
        first = True
        for device in devices:
            for field in devices[device]:
                if first:
                    device_fields += [field]
            first = False
        for field in cpu:
            cpu_fields += [field]
        fields += device_fields
        fields += cpu_fields

        results = []
        for device in devices:
            result = {}
            result['execution_time'] = execution_time
            result['device'] = device
            for field in device_fields:
                result[field] = devices[device][field]
            for field in cpu_fields:
                result[field] = cpu[field]
            results += [result]

        return results
