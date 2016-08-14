# -*- coding: UTF-8 -*-
import random

def get_accent(candidate):
    chartable = dict()
    chartable['a'] = u'ãäåàá'
    chartable['e'] = u'éëèëê'
    chartable['i'] = u'ĭī'

    rand_ix = random.randint(0,len(chartable[candidate])-1)
    return unicode(chartable[candidate][rand_ix])


def accent_convert(target_string='this is a test'):

    new_string = target_string

    new_string = new_string.replace('ea', '%s%s' %
                            (get_accent('e'), get_accent('a')))
    new_string = new_string.replace('ak', '%s%srk' %
                            (get_accent('e'), get_accent('a')))
    new_string = new_string.replace('a', '%s' %
                            (get_accent('a')))
    new_string = new_string.replace('en', '%s%srn' %
                            (get_accent('e'),get_accent('a')))
    new_string = new_string.replace('es', '%s%srs' %
                            (get_accent('e'),get_accent('a')))
    new_string = new_string.replace('e', '%s' %
                            (get_accent('e')))
    new_string = new_string.replace('o', '%s%sr' %
                            (get_accent('e'),get_accent('a')))
    new_string = new_string.replace('in', '%s%srn' %
                            (get_accent('e'), get_accent('a')))
    new_string = new_string.replace('il', '%s%srl' %
                            (get_accent('e'), get_accent('a')))
    new_string = new_string.replace('i', '%s' %
                            (get_accent('i')))

    return unicode(new_string)


def run(text=None):
    return unicode(accent_convert(text))