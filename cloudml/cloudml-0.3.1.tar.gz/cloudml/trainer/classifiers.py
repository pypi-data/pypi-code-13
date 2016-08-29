import logging
import coloredlogs
import re
import inspect
import json
from new import instancemethod

import numpy
from sklearn import *
from sklearn.base import ClassifierMixin

TYPE_MAP = {
    'string': 'string',
    'str': 'string',
    'boolean': 'boolean',
    'bool': 'boolean',
    'float': 'float',
    'integer': 'integer',
    # 'auto_dict': convert_auto_dict,
    # 'int_float_string_none': convert_int_float_string_none,
    # 'float_or_int': convert_float_or_int,
    # 'string_list_none': convert_string_list_none,
}

coloredlogs.install(level=logging.DEBUG)


def full_name(cls):
    return "{0}.{1}".format(cls.__module__,
                            cls.__name__)


def all_subclasses(cls):
    return cls.__subclasses__() + [g for s in cls.__subclasses__()
                                   for g in all_subclasses(s)]


def get_params_str(doc):
    m = re.findall(r"([A-Za-z0-9 ]+[\n ]+[-]+\n)", doc)
    if m:
        def find_between_r(s, first, last):
            try:
                start = s.rindex(first) + len(first)
                end = s.rindex(last, start)
                return s[start:end]
            except ValueError:
                return ""

        return find_between_r(doc, m[0], m[1])


def split_docstring(doc):
    descr = ""
    params = []
    extra = []
    if not doc:
        return descr, params, extra

    def parse_params(pstr):
        def parse_decl(decl):
            item = {}
            splitted_decl = decl.split(' : ')
            if len(splitted_decl) > 1:
                choices = []
                name = splitted_decl[0].strip()
                if name.endswith('_'):
                    logging.warning('Param %s has not added', name)
                    return
                item['name'] = name
                ptype_decl = splitted_decl[1].strip()
                m = re.search(r"\{([A-Za-z0-9, _']+)\}", ptype_decl)
                if m:
                    choices_str = m.group(1)
                    for ch in choices_str.split(','):
                        choices.append(ch.strip('\' '))
                splitted_ptype = ptype_decl.split(',')

                if not splitted_ptype:
                    item['type'] = 'string'
                    return item
                type_ = splitted_ptype[0]
                if type_.startswith('{'):
                    type_ = 'string'
                    logging.warning('type is not parsed properly: %s',
                                    splitted_ptype)
                cloudml_type = TYPE_MAP.get(type_, None)
                if cloudml_type is None:
                    logging.warning('Can not parse type %s', type_)
                item['type'] = cloudml_type
                if not choices and len(splitted_ptype) > 1:
                    extra_type = splitted_ptype[1]
                    splitted_extra = re.split('[,.()]+', extra_type)
                    print splitted_extra
                    for ch in splitted_extra:
                        choice = ch.strip()
                        if not (choice is None or
                                choice == '' or
                                choice == 'optional' or
                                choice.startswith('default')):
                            choices.append(choice)
                if choices:
                    item['choices'] = choices
                if 'optional' in ptype_decl:
                    item['required'] = False
                return item

        sstrings = pstr.split("\n")
        params = []
        p = None
        param_help = []
        for pstr in sstrings:
            #print "Processing", pstr
            is_new_param = ':' in pstr
            if is_new_param:
                # if p and param_help:
                #     p['help_text'] = '\n'.join(param_help)
                param_help = []
                p = parse_decl(pstr)
                if p:
                    params.append(p)
                else:
                    logging.error('Cannot parse: \n %s. Ignored', pstr)
            else:
                param_help.append(pstr.strip())
        return params
        #import pdb;pdb.set_trace()

    splitted_doc = doc.split('Parameters\n    ----------\n')
    doc_len = len(splitted_doc)
    if doc_len > 0:
        descr = splitted_doc[0].replace('\n', '').replace('  ', ' ')
        if doc_len > 1:
            params_declaration = get_params_str(doc) or splitted_doc[1]
            #logging.info('Declaration: %s', params_declaration)
            params = parse_params(params_declaration)
            if doc_len > 2:  # extra docs
                pass

    return descr, params, extra


classifiers = all_subclasses(ClassifierMixin)
cc = classifiers[5]

doc = cc.__doc__
CLASSIFIERS_CONFIG = []

i = 1
for cl in classifiers:
    if isinstance(cl.__init__, instancemethod) and \
            not cl.__name__.startswith('Base'):
        print i, full_name(cl)
        # print "==============="
        # print "Doc string: \n", cl.__doc__
        # print
        # print "==============="
        args, varargs, varkw, defaults = inspect.getargspec(cl.__init__)
        args.remove('self')
        print "\n--- inspected: ", args, defaults, '\n'
        defaults_key_map = dict(zip(args, defaults))
        descr, params, extra = split_docstring(cl.__doc__)
        clf_config = {
            'cls': full_name(cl),
            'help_text': descr,
            'parameters': [],
            'defaults': {}
        }
        print "\n---- Parsed params -----"
        for p in params:
            default = defaults_key_map.get(p['name'])
            if not default is None:
            	print dir(default)
            	if isinstance(default, numpy.ndarray):
                    default = default.tolist()
                p['default'] = default
                clf_config['defaults'][p['name']] = default
            print p['name'], p
            if p['name'] in args:
                clf_config['parameters'].append(p)
            else:
                logging.error('%s ignored' % p['name'])
        #print descr
        print "\n\n\n"
        CLASSIFIERS_CONFIG.append(clf_config)
        i += 1
    print "************* RESULT *********"
    #print CLASSIFIERS_CONFIG
    logging.info(json.dumps(CLASSIFIERS_CONFIG, indent=4, sort_keys=True))
