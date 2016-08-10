from .utils import pickchance, pickone
from .tsv import TSV
import random


class Address(TSV):
    def __init__(self, num, st, suburb, postcode, state):
        self.number = num
        self.street = st
        self.suburb = suburb
        self.postcode = postcode
        self.state = state
        self.country = 'Australia'

    def to_list(self):
        return [str(i) for i in [self.number, self.street, self.suburb, self.postcode, self.state, self.country]]

    def __str__(self):
        return '\n'.join(self.to_list())

    def tsv(self):
        return '\t'.join(self.to_list())


def random_st_num():
    return random.randint(1, 1999)


def random_street():
    names = ['Bridge', 'Church', 'Sloane', 'Lincoln', 'Harris', 'Meadow', 'Beech', 'Essex', 'Sussex', 'Madison',
             'Broad', 'Cedar', 'Maple', 'River', 'Washington', 'Pitt', 'Oak', 'Hillside', 'Miller', 'Jefferson',
             'Monroe', 'New', 'Victoria', 'Franklin', 'Highland', 'Market', 'Geroge', 'Wellington', 'Vine', 'Walnut',
             'Park', 'Green', 'Cherry', 'Chestnut', 'Mango', 'Chilli', 'Waterloo', 'Watson', 'Holyfield', 'Tyson',
             'Granger', 'Peterson', 'St George', 'Tank']
    types = ['Avenue', 'Road', 'Street', 'Drive', 'Way']
    suffix = ['North', 'South', 'East', 'West']

    n = pickone(names)
    t = pickone(types)
    full_street_name = n + ' ' + t

    if pickchance(0.2):
        return full_street_name + ' ' + pickone(suffix)

    return full_street_name


def random_suburb():
    names = ['Arts District', 'Baldwin Hills', 'Beverly Crest', 'Brentwood', 'Bunker Hill', 'Central City',
             'Cypress Park', 'Downtown', 'Echo Park', 'Eagle Rock', 'Fairfax', 'Flower District', 'Gallery Row',
             'Hancock Park', 'Lincoln Heights', 'Manchester Square', 'Miracle Mile', 'Nicolas Canyon',
             'North University Park', 'Pacoima', 'Rose Hills', 'San Pedro', 'Silver Lake', 'Skid Row',
             'South Park', 'Sun Valley', 'Tarzana', 'Valley Glen', 'Westdale', 'Westlake', 'Woodland Hills']
    postcode = [str(1000 + i) for i in range(len(names))]

    return pickone(list(zip(names, postcode)))


def random_state():
    names = ['ACT', 'NSW', 'NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA']
    return pickone(names)


def random_address():
    return format_address(['No.', str(random.randint(1, 1999)), random_street(), random_state()])


def format_address(l):
    return (' '.join(l)).strip()
