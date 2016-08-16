#!/usr/bin/env python3

import pprint as pp
import re
import random
import time


class Head():
    """A dummy class used to anchor the beginning of an input chain."""

    def __len__(self):
        return 0
class Tail():
    def __len__(self):
        return 0
    def __str__(Self):
        return ''

class Markov:

    """Get a lot of input and produce a short output multiple times.
    Input should be lists of strings beginning with an emptystring.
    The Head object is used as the entry point every time generate() is called."""
    empty = dict()
    start = Head()

    def __init__(self, seeds, orders=(0,)):
        """Seeds should be an iterable or iterables.
        This is so that entry points can be determined automatically."""
        if 0 not in orders:
            raise ValueError("0 is a required order.")
        self.transitions = self.empty.copy()
        self.orders = orders
        self.feed(seeds)
        self.cur_state = self.start

    def feed(self, seeds, sep=' '):
        """Feed the generator with a list of seeds (iterables).
        I.e. m = pymarkoff.Markov()
        m.feed([['The','quick','brown','fox','jumped','over','the','lazy','dog.']])
        m.generate() => ['The','lazy','dog.']

        """
        for seed in seeds:
            # print(seed)
            seed = [Head()] + seed + [Tail()]
            for cur_order in self.orders:
                # for each head + tail
                # Or rather count(tail|head)
                for i in range(len(seed) - cur_order):
                    try:
                        head = tuple(
                            s for s in seed[i:i + cur_order + 1] if len(s) > 0)

                        tail = seed[i + cur_order + 1]
                        self.transitions[head].append(tail
                                                      )
                    except KeyError:
                        self.transitions[head] = [tail]
                    except IndexError:
                        pass

    def generate(self, *, max_length=100, terminators=(Tail(),), sep=' '):
        """Returns a list of states chosen by simulation.
        Simulation starts from a state chosen fro mknown head states
        and ends at either a known terminating state or when the chain
        reaches max_length, whichever comes first."""
        result = []
        state = Head()
        choice = ''
        i = 0
        while i <= max_length and not isinstance(state,Tail):
            # check for transitions in the highest allowed order first
            # then check lower orders
            for cur_order in self.orders[::-1]:
                try:
                    # reach back for a sequence of states of length less equal
                    # to the current order.
                    temp_state = tuple(result[-(cur_order + 1):len(result)])
                    choice = random.choice(self.transitions[temp_state])
                    break
                except KeyError as e:
                    # A KeyError happens where there aren't transitions for an
                    # arbitrary higher order state
                    # In which case, carry on and continue to the next lowest
                    # order.
                    pass

            state = choice
            result.append(choice)
            i += 1
        return result[:-1] #slice off the tail

    def __str__(self):
        return str(self.transitions)

    def __iter__(self):
        for t in self.transitions.items():
            yield (t[0], sorted(t[1]))


def prepare_str(s):
    """For massaging purposes."""
    return [''] + s.split(" ")


def clean_data(s):
    return s


def filter_by_user(data):
    good = []
    for sentence in data:
        print(sentence)
        res = input("Good? y/n >>>").lower()
        if res == 'y':
            good.append(sentence)
        elif res == 'e':
            break
        else:
            pass
    return good


def main():
    seeds = ["the quick brown fox jumped over the lazy dog".split(' ') + ['.']]
    m = Markov(seeds)

    results_f = tuple((m.generate(max_length=30)) for i in range(5))
    pp.pprint(results_f)

if __name__ == '__main__':
    main()

    # from itertools import product
# combs = '\n'.join(' '.join([''.join(line) for line in zip(*sol)])
#                   for sol in product(permutations(prefixes), permutations(suffixes)))
# print(combs)
