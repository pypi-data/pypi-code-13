#!/usr/bin/env python

__author__ = 'Ronie Martinez'


class DidYouMeanError(AttributeError):
    def __init__(self, class_name, attribute_name, close_matches):
        self.message = "\n".join(["AttributeError: '%s' object has no attribute '%s'." % (class_name, attribute_name),
                                  "Did you mean one of these?"] +
                                 ["\t%s" % match for match in close_matches])
        self.close_matches = close_matches


class TimeLimitExceededError(Exception):
    message = "TimeLimitExceededError: Time limit exceeded!"
