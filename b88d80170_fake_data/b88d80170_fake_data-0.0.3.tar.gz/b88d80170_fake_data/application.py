import random
from .date import dob_rough_random, valid_date
from .tsv import TSV


class Application(TSV):
    def __init__(self, argv):
        if 'applicationId' in argv:
            self.applicationId = argv['applicationId']
        if 'applicationType' in argv:
            self.applicationType = argv['applicationType']

    def to_list(self):
        return [str(i) for i in [self.applicationId, self.applicationType]]

    def __str__(self):
        return '\n'.join(self.to_list())

    def tsv(self):
        return '\t'.join(self.to_list())


def random_application_id():
    s = ''
    while True:
        l = dob_rough_random()
        if valid_date(l):
            s = ''.join([str(n) if n >= 10 else '0' + str(n) for n in l])
            break
    return 'APP' + s + str(random.randint(100, 999)) + str(random.randint(10, 99))
