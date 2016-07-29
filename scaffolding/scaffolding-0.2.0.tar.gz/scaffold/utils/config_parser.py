import os
from exceptions import FileNotFound



class ConfigParser(object):
    def __init__(self, path):
        if os.path.isfile(path):
            self.path = path
        else:
            base = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(base, path)
            if os.path.isfile(path):
                self.path = path
            else:
                raise FileNotFound(path)

    def parse(self):
        result = []
        with open(self.path) as f:
            for l in f.readlines():
                l = l.rstrip()
                if ':' in l:
                    key, val = l.split(':')
                    key, val = key.strip(), val.strip()
                    result.append((key, val))
                else:
                    key = l.strip()
                    result.append((key, ''))
        return result
