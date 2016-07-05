#!/usr/bin/env python3
"""
This is an example script demonstrating the usage of the axsemantics API client.
Please use the configuration section below to customize behaviour and proceed
at your own risk.

This script will upload data found in an excel file to a given content project.
It expects the excel file name as command line parameter.

Take care to include an 'name' and a 'uid' field in either your data or the
MAPPING dict if you want to create the Objects.

Required dependencies:
    - axsemantics
    - pandas
    - xlrd
"""
import click
import json
import re
import sys

import axsemantics
from axsemantics_cli.mapping_helpers import *


# IMPORT_UNCONFIGURED: Boolean
#  - True: columns not defined in MAPPING will be camel-cased and imported
#  - False: only columns in MAPPING will be imported
IMPORT_UNCONFIGURED = True

# MAPPING: dict
#  - {"column name": "datafield name"}: map a column name to a different data field name
#  - {"column name": [function, params]}: map a column name to a parsing method (returning a dict)
#    the mapping function will be passed the parameters 'field' and 'key' aswell as everything in
#    the params dict
# left is the name of your excel column, right is the configuration (renaming or split).
# remember: uid and name *must* be present in the output


MAPPING = {
    'MPID': [int_uid, {}],
    'Title English': 'name',
    'Sizes': [splitlist, {'separator': '~'}],
    'Specification': [splitdata, {'row_separator': '~',
                                  'value_separator': ':'}]
}

# EXPORT: Boolean
#  - set this if you don't want to upload directly
#  - True: save things as json instead of creating them
#  - False: create things in API
EXPORT = False

# AXSEMANTICS_*: values to use with the axsemantics library
AXSEMANTICS_USER = 'user@example.com'
AXSEMANTICS_PASSWORD = 'securepassword'
AXSEMANTICS_CONTENT_PROJECT = 4004


def normalize_key(key):
    pattern = re.compile('[^A-Za-z0-9_]')
    key = key.strip()
    key = pattern.sub('', key)
    return key


def _parse_row(row):
    data = {}

    for xslx_key in row.keys():
        xslx_value = row[xslx_key]

        if xslx_key in MAPPING:
            mapped_key = MAPPING[xslx_key]
            if isinstance(mapped_key, str):
                data[mapped_key] = xslx_value

            elif isinstance(mapped_key, list):
                try:
                    _params = mapped_key[1]
                    data.update(mapped_key[0](field=xslx_value,
                                              key=xslx_key,
                                              **_params))
                except:
                    click.echo('Failed to parse field {} with content {}.'.format(xslx_key, xslx_value))

        elif IMPORT_UNCONFIGURED:
            data[normalize_key(xslx_key)] = xslx_value
    return data

from .main import cli


@cli.group()
@click.option('--filename', '-f',)
@click.pass_context
def excel(ctx, filename, ):
    try:
        import pandas as pd
    except:
        ctx.fail('Please install pandas to enable this command\n'
                 "to do this type 'pip install pandas'")
    try:
        xslx = pd.ExcelFile(sys.argv[-1])
    except FileNotFoundError:
        sys.exit('Could not find .xlsx file {}.'.format(sys.argv[-1]))

    click.echo('obj')
    ctx.obj['data'] = []
    sheet = xslx.parse(0)
    # replace float with value `nan` with none
    sheet_with_none = sheet.where((pd.notnull(sheet)), None)

    for index, row in sheet_with_none.iterrows():
        ctx.obj['data'].append(_parse_row(row))


@excel.command()
@click.pass_obj
def convert(obj):
    json_name = re.sub(r'.xlsx', '.json', sys.argv[-1])
    with open(json_name, 'w') as f:
        json.dump(obj['data'], f)


@excel.command('import')
@click.pass_obj
def importer(obj):
    axsemantics.login(AXSEMANTICS_USER, AXSEMANTICS_PASSWORD)
    for pure_data in obj['data']:
        try:
            thing = axsemantics.Thing(
                uid=pure_data['uid'],
                name=pure_data['name'],
                pure_data=pure_data,
                cp_id=AXSEMANTICS_CONTENT_PROJECT,
            )
            thing.create()
            click.echo('.', nl=False)
        except KeyError as e:
            click.echo('Could not create thing for data {}, missing key {}.'.format(pure_data, e))
        except axsemantics.APIError as e:
                message = (
                    'An error occurred while saving thing {}.\n'
                    'Method: {}\nResource: {}\nPayload: {}\nResponse: {} {}\n'
                )

                click.echo(message.format(thing,
                                          e.request.request.method,
                                          e.request.url,
                                          e.request.request.body,
                                          e.request.status_code,
                                          e.request.content))
