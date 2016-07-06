# -*- coding: utf-8 -*-
#
# Copyright 2012-2016 BigML
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Utilities for BigMLer

"""
from __future__ import absolute_import

import fileinput
import ast
import glob
import os
import sys
import datetime

try:
    import simplejson as json
except ImportError:
    import json

import bigml.api
from bigml.util import console_log, empty_resource
from bigml.fields import get_fields_structure, Fields
from bigml.io import UnicodeReader

PYTHON3 = sys.version_info[0] == 3
PAGE_LENGTH = 200
ATTRIBUTE_NAMES = ['name', 'label', 'description']
NEW_DIRS_LOG = u".bigmler_dirs"
BRIEF_MODEL_QS = "exclude=root,fields"

# Base Domain
BIGML_DOMAIN = os.environ.get('BIGML_DOMAIN', 'bigml.io')
BIGML_DASHBOARD_URL = os.environ.get('BIGML_DASHBOARD_URL')
BIGML_DASHBOARD_DOMAIN = (
    "%s.com" % BIGML_DOMAIN[:-3] if BIGML_DOMAIN[-3:] == '.io' else
    BIGML_DOMAIN.replace("-io.", "."))
RESOURCE_URL = ("https://%s/dashboard/" % BIGML_DASHBOARD_DOMAIN
                if BIGML_DASHBOARD_URL is None
                else BIGML_DASHBOARD_URL)
RESOURCE_SHARED_URL = "%s/shared/" % "/".join(RESOURCE_URL.split('/')[:-2])
RESOURCE_EMBEDDED_URL = ("%s/embedded/%%s/tree" %
                         "/".join(RESOURCE_URL.split('/')[:-2]))


SYSTEM_ENCODING = 'cp1252' if sys.platform == 'win32' else 'utf-8'
FILE_ENCODING = 'utf-8'


def read_description(path):
    """Reads a text description from a file.

    """
    return ''.join(fileinput.input([path]))


def read_field_attributes(path):
    """Reads field attributes from a csv file to update source fields.

    A column number and a list of attributes separated by a comma per line.
    The expected structure is:
    column number, name, label, description

    For example:

    0,'first name','label for the first field','fist field full description'
    1,'last name','label for the last field','last field full description'

    """
    field_attributes = {}
    try:
        with UnicodeReader(path, quotechar="'") as attributes_reader:
            for row in attributes_reader:
                attributes = {}
                if len(row) > 1:
                    for index in range(0, min(len(ATTRIBUTE_NAMES),
                                              len(row) - 1)):
                        attributes.update(
                            {ATTRIBUTE_NAMES[index]: row[index + 1]})
                    field_attributes.update({
                        int(row[0]): attributes})
            return field_attributes
    except IOError:
        sys.exit("Error: cannot read field attributes %s" % path)


def read_types(path):
    """Types to update source fields types.

    A column number and type separated by a comma per line.

    For example:

    0, 'categorical'
    1, 'numeric'

    """
    types_dict = {}
    for line in fileinput.input([path]):
        try:
            pair = ast.literal_eval(line)
            types_dict.update({
                pair[0]: {'optype': pair[1]}})
        except SyntaxError:
            console_log("WARNING: The following line in file %s"
                        " does not match the expected"
                        " syntax: %s" % (path, line))
    return types_dict


def read_json(path):
    """Reads attributes from a json file to update or create resources.
       For instance, to change the text analysis mode to full text in the
       field whose id is '000001'

        {"fields": {
            "000001": {
                "term_analysis": {
                    "token_mode": "full_terms_only"}}}}

    """
    json_attributes = {}
    try:
        attributes_reader = open(path, open_mode('r'))
    except IOError:
        sys.exit("Error: cannot read json file %s" % path)
    try:
        json_attributes = json.loads(attributes_reader.read())
    except ValueError:
        sys.exit("Error: no valid json found in %s" % path)
    return json_attributes


def read_fields_map(path):
    """Fields map from evaluated model to test dataset.

    The the evaluated model field column and the test dataset field column
    separated by a comma per line.

    For example:

    0, 0
    1, 2
    2, 1

    """
    map_dict = {}
    for line in fileinput.input([path]):
        try:
            pair = ast.literal_eval(line)
            map_dict.update({
                pair[0]: pair[1]})
        except SyntaxError:
            console_log("WARNING: The following line in file %s"
                        " does not match the expected"
                        " syntax: %s" % (path, line))
    return map_dict


def read_resources(path):
    """Reads resources ids from a file.

    For example:

    model/50974922035d0706da00003d
    model/509748b7035d0706da000039
    model/5097488b155268377a000059

    """
    resources = []
    for line in fileinput.input([path]):
        resources.append(line.rstrip())
    return resources


def read_datasets(path):
    """Reads dataset ids from a file.

    For example:

    dataset/50978822035d0706da000069
    dataset/50978822035d0706da000073
    dataset/50978822035d0706da000085

    """
    datasets = []
    for line in fileinput.input([path]):
        datasets.append(line.rstrip())
    return datasets


def read_json_filter(path):
    """Reads a json filter from a file.

    For example:

    [">", 3.14, ["field", "000002"]]

    """
    with open(path) as json_data:
        return json.load(json_data)


def read_lisp_filter(path):
    """Reads a lisp filter from a file.

    For example:

    (> (/ (+ (- (field "00000") 4.4)
            (field 23)
            (* 2 (field "Class") (field "00004")))
       3)
       5.5)

    """
    return read_description(path)


def read_votes_files(dirs_list, path):
    """Reads a list of directories to look for votes.

    If model's prediction files are found, they are retrieved to be combined.
    Models' predictions files are expected to be named after the model id,
    for instance: model_50974922035d0706da00003d__predictions.csv
    """
    file_name = "%s%scombined_predictions" % (path, os.sep)
    check_dir(file_name)
    group_predictions = open(file_name, "wb", 0)
    current_directory = os.getcwd()
    predictions_files = []
    for directory in dirs_list:
        directory = os.path.abspath(directory)
        os.chdir(directory)
        for predictions_file in glob.glob("model_*_predictions.csv"):
            predictions_files.append("%s%s%s" % (os.getcwd(),
                                                 os.sep, predictions_file))
            message = "%s\n" % predictions_file
            if PYTHON3:
                message = message.encode(FILE_ENCODING)
            group_predictions.write(message)
        os.chdir(current_directory)
    group_predictions.close()
    return predictions_files


def read_local_resource(path, csv_properties=None):
    """Read the JSON resource structure information from the given file.

    """
    resource = empty_resource()
    if csv_properties is None:
        csv_properties = {}
    fields = None
    with open(path, open_mode('r')) as resource_file:
        try:
            resource = json.loads(resource_file.read())
        except IOError:
            pass
    resource_id = resource.get('resource')
    if resource_id is None:
        sys.exit("Failed to extract a BigML resource structure from the"
                 " contents of file %s." % path)
    if resource.get('object') is None:
        resource = {'resource': resource_id,
                    'object': resource,
                    'error': None,
                    'code': bigml.api.HTTP_OK}

    fields, resource_locale, missing_tokens, \
    objective_column = get_fields_structure(resource)
    if not 'objective_field' in csv_properties and \
            objective_column is not None:
        csv_properties['objective_field'] = objective_column
    if missing_tokens:
        csv_properties['missing_tokens'] = missing_tokens
    if resource_locale:
        csv_properties['data_locale'] = resource_locale
    if fields:
        fields = Fields(resource, **csv_properties)
    return resource, csv_properties, fields


def list_ids(api_function, query_string, status_code=bigml.api.FINISHED):
    """Lists BigML resources filtered by `query_string`.

    """
    q_s = 'status.code=%s;limit=%s;%s' % (
        status_code, PAGE_LENGTH, query_string)
    resources = api_function(q_s)
    ids = [obj['resource'] for obj in (resources['objects'] or [])]
    while (resources['objects'] and
           (resources['meta']['total_count'] > (resources['meta']['offset'] +
                                                resources['meta']['limit']))):
        offset = resources['meta']['offset'] + PAGE_LENGTH
        q_s = 'status.code=%s;offset=%s;limit=%s;%s' % (
            status_code, offset, PAGE_LENGTH, query_string)
        resources = api_function(q_s)
        if resources['objects']:
            ids.extend([obj['resource'] for obj in resources['objects']])
    return ids


def delete(api, delete_list, exe_outputs=True):
    """ Deletes the resources given in the list. If the exe_outputs is set,
        deleting an execution causes the deletion of any outpur resource.

    """
    for resource_id in delete_list:
        resource_type = None
        try:
            for resource_type in bigml.api.RESOURCE_RE.keys():
                try:
                    bigml.api.get_resource(resource_type, resource_id)
                    break
                except ValueError:
                    pass
            if resource_type == "execution" and exe_outputs:
                query_string = "delete_all=true"
                api.deleters[resource_type](resource_id,
                                            query_string=query_string)
            else:
                api.deleters[resource_type](resource_id)
        except ValueError:
            console_log("Failed to delete resource %s" % resource_id)


def check_dir(path):
    """Creates a directory if it doesn't exist

    """
    directory = os.path.dirname(path)
    if len(directory) > 0 and not os.path.exists(directory):
        os.makedirs(directory)
        sys_log_message(u"%s\n" % os.path.abspath(directory),
                        log_file=NEW_DIRS_LOG)
    return directory


def print_tree(directory, padding):
    """Returns a graphical directory tree structure as a string

    """
    if padding != u' ':
        output = padding[:-1] + u'├─'
    else:
        output = padding
    output += os.path.basename(os.path.abspath(directory)) + u'\n'
    padding = padding + u' '
    files = []
    files = os.listdir(directory)
    count = 0
    for i in range(0, len(files)):
        file_name = files[i]
        count += 1
        path = directory + os.sep + file_name
        if os.path.isdir(path):
            if count == len(files):
                output += print_tree(path, padding + u' ')
            else:
                output += print_tree(path, padding + u'|')
        else:
            if i < (len(files) - 1):
                output += padding + u'├─' + file_name + u'\n'
            else:
                output += padding + u'└─' + file_name + u'\n'
    return output


def dated(message):
    """Prepends date in log format in string

    """
    return "[%s] %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        message)


def get_url(resource, shared=False, embedded=False):
    """Returns the resource's url in bigml.com

    """
    if shared:
        return (RESOURCE_SHARED_URL + bigml.api.get_resource_type(resource)
                + os.sep + resource['object']['shared_hash'])
    elif embedded:
        return (RESOURCE_EMBEDDED_URL % (bigml.api.get_resource_type(resource)
                                         + os.sep +
                                         resource['object']['shared_hash']))
    else:
        resource_id = bigml.api.get_resource_id(resource)
        if not resource_id:
            return ""
        return RESOURCE_URL + resource_id


def log_message(message, log_file=None, console=False):
    """Logs a message in a file and/or to console

       If log_file is set, logs the message in the file.
       If console is True, sends the message to console.
    """

    if isinstance(message, unicode) and not PYTHON3:
        message = message.encode(FILE_ENCODING)
    if console:
        console_log(message)
    if log_file is not None:
        if PYTHON3:
            message = message.encode(FILE_ENCODING)
        with open(log_file, 'ab', 0) as log_file:
            log_file.write(message)


def sys_log_message(message, log_file=None):
    """Logs a message in a file using the system encoding

       If log_file is set, logs the message in the file.
    """
    if isinstance(message, unicode):
        message = message.encode(SYSTEM_ENCODING)
    if log_file is not None:
        with open(log_file, 'ab', 0) as log_file:
            log_file.write(message)


def plural(text, num):
    """Pluralizer: adds "s" at the end of a string if a given number is > 1

    """
    return "%s%s" % (text, "s"[num == 1:])


def check_resource_error(resource, message):
    """If a given resource is faulty, or some other error has occured, exits.
       Returns the resource id otherwise.

    """
    if ('error' in resource and resource['error'] or
            bigml.api.get_status(resource)['code'] == bigml.api.FAULTY):
        if ('status' in resource['error'] and
                'message' in resource['error']['status']):
            error_message = resource['error']['status']['message']
        sys.exit("%s%s" % (message, error_message))
    return bigml.api.get_resource_id(resource)


def log_created_resources(file_name, path, resource_id, mode='w',
                          comment=None):
    """Logs the created resources ids in the given file

    """
    if path is not None:
        file_name = "%s%s%s" % (path, os.sep, file_name)
        try:
            with open(file_name, "%sb" % mode, 0) as resource_file:
                if resource_id is not None:
                    message = "%s\n" % resource_id
                    if PYTHON3 or isinstance(message, unicode):
                        message = message.encode(SYSTEM_ENCODING)
                    resource_file.write(message)
                if comment is not None:
                    if PYTHON3 or isinstance(comment, unicode):
                        comment = comment.encode(SYSTEM_ENCODING)
                    resource_file.write(comment)
        except IOError, exc:
            print "Failed to write %s: %s" % (file_name, str(exc))


def check_resource(*args, **kwargs):
    """Wrapper to catch errors in resource retrieval

    """
    try:
        result = bigml.api.check_resource(*args, **kwargs)
        return result
    except ValueError, exc:
        sys.exit("\nFailed to obtain a finished resource:\n%s." % str(exc))


def objective_field_names(models_or_ensembles, api):
    """Gets the objective field names for a list of models or ensembles

    """
    objective_fields = []
    for model_or_ensemble in models_or_ensembles:
        name = None
        if isinstance(model_or_ensemble, dict):
            status_code = bigml.api.get_status(model_or_ensemble)['code']
            if status_code == bigml.api.FINISHED:
                name = objective_field_name(model_or_ensemble, api)
        if name is None:
            resource_type = bigml.api.get_resource_type(model_or_ensemble)
            if resource_type == bigml.api.MODEL_PATH:
                model_id = bigml.api.get_model_id(model_or_ensemble)
                if model_id is not None:
                    try:
                        model = check_resource(model_id, api.get_model,
                                               query_string=BRIEF_MODEL_QS)
                    except ValueError, exception:
                        sys.exit("Failed to get a finished model: %s" %
                                 str(exception))
                    name = objective_field_name(model, api)
            elif resource_type == bigml.api.ENSEMBLE_PATH:
                ensemble_id = bigml.api.get_ensemble_id(model_or_ensemble)
                if ensemble_id is not None:
                    try:
                        ensemble = check_resource(
                            ensemble_id, api.get_ensemble)
                    except ValueError, exception:
                        sys.exit("Failed to get a finished ensemble: %s" %
                                 str(exception))
                    name = objective_field_name(ensemble, api)
            else:
                sys.exit("No valid model or ensemble id.")
        if name is not None:
            objective_fields.append(name)

    return objective_fields


def objective_field_name(model_or_ensemble, api):
    """Gets the objective field name from a dict model or ensemble structure

    """
    if not isinstance(model_or_ensemble, dict):
        return None
    if not 'object' in model_or_ensemble:
        return None
    objective_field = None
    resource_info = model_or_ensemble['object']
    if 'objective_field' in resource_info:
        objective_field = resource_info['objective_field']
    elif 'objective_fields' in resource_info:
        objective_field = resource_info['objective_fields'][0]
    if objective_field is None:
        return None
    resource_type = bigml.api.get_resource_type(model_or_ensemble)
    if resource_type == bigml.api.ENSEMBLE_PATH:
        bigml.api.get_ensemble_id(model_or_ensemble)
        model = model_or_ensemble['object']['models'][0]
        model = api.get_model(model, query_string=BRIEF_MODEL_QS)
    elif resource_type == bigml.api.MODEL_PATH:
        model = model_or_ensemble
    else:
        sys.exit("No valid model or ensemble structure.")
    return model['object']['model']['model_fields'][objective_field]['name']


def read_objective_weights(path):
    """Reads objective weights from a CSV file in a class, weight format.

    The expected structure is:
    class name, weight

    For example:

    Iris-setosa,5
    Iris-versicolor,10

    """
    objective_weights = []
    try:
        with UnicodeReader(path, quotechar="'") as weights_reader:
            for row in weights_reader:
                weights = []
                if len(row) != 2:
                    sys.exit("Error: wrong objective field file syntax\n%s" %
                             ",".join(row))
                weights = row[:]
                try:
                    weights[1] = int(weights[1])
                except ValueError:
                    sys.exit("Error: wrong objective field file syntax\n%s" %
                             ",".join(row))
                objective_weights.append(weights)
            return objective_weights
    except IOError:
        sys.exit("Error: cannot read objective weights %s" % path)


def is_shared(resource):
    """Checks if a resource is shared

    """
    return resource['object'].get('shared', False)


def get_options_list(args, options, prioritary=None):
    """Creates the list of values that generates the options in `options`
       from the args object.

    """
    options_list = []
    filtered_options = options[:]
    non_equivalent_options = {'dev': 'dev_mode'}
    # removes the options that are already set as prioritary
    for element in prioritary:
        try:
            filtered_options.remove(element)
        except ValueError:
            pass
    # adds the options that have not been assigned a value in prioritary
    for option in filtered_options:
        try:
            flag = option[2:].replace("-", "_")
            if flag in non_equivalent_options.keys():
                flag = non_equivalent_options[flag]
            value = getattr(args, flag)
            if value is not None:
                if isinstance(value, bool):
                    if value:
                        options_list.append(option)
                elif isinstance(value, list):
                    if value:
                        options_list.append("%s=%s" %
                                            (option, ",".join(value)))
                else:
                    if not isinstance(value, basestring):
                        value = str(value)
                    options_list.append("%s=%s" % (option, value))
        except AttributeError:
            pass
    return options_list


def print_generated_files(path, log_file=None, verbosity=1):
    """Prints the file structure generated while running bigmler

    """
    message = (u"\nGenerated files:\n\n" +
               print_tree(path, u" ") + u"\n")
    log_message(message, log_file=log_file, console=verbosity)


def storage_file_name(directory, resource_id):
    """Returns the path to the JSON file that contains a stored resource
       structure

    """
    return os.path.normpath(
        os.path.join(directory, resource_id.replace("/", "_")))


def get_objective_id(fields, objective):
    """Checks if the objective given by the user in the --objective flag
       is in the list of fields. Returns its column number or None otherwise.

    """
    if objective is None:
        return None
    try:
        objective_id = fields.field_id(objective)
    except ValueError:
        return None
    return objective_id


def open_mode(mode):
    """Python 3 compatible open mode

    """
    return "%st" % mode if PYTHON3 else "%s" % mode


def encode2(value, encoding=FILE_ENCODING):
    """Conditional encoding only for Python2

    """
    if isinstance(value, basestring) and not PYTHON3:
        return value.encode(encoding)
    return value


def decode2(value, encoding=FILE_ENCODING):
    """Conditional decoding only for Python2

    """
    if isinstance(value, basestring) and not PYTHON3:
        return value.decode(encoding)
    return value


def transform_fields_keys(json_attributes, fields):
    """Transforms the fields structure keys if they are expressed in columns
       to the corresponding IDs

    """
    fields_structure = {}
    if fields is None:
        return json_attributes
    if "fields" in json_attributes.keys():
        old_keys = json_attributes["fields"].keys()
        for old_key in old_keys:
            try:
                if not old_key in fields.fields:
                    key = fields.field_id(int(old_key))
                else:
                    key = old_key
            except ValueError:
                key = old_key
            fields_structure[key] = json_attributes["fields"][old_key]
        json_attributes["fields"] = fields_structure
    return json_attributes
