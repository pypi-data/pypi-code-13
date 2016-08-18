# ----------------------------------------------------------------------------
# Copyright 2015-2016 Nervana Systems Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------------
"""
Subcommands for performing stream predictions using deployed models.
"""
from __future__ import print_function
import io
import zipfile
import os
import sys
import json
from collections import OrderedDict
from functools import partial
import logging

from ncloud.config import STREAM_PREDICTIONS
from ncloud.util.api_call import api_call, api_call_json
from ncloud.formatting.time_zone import utc_to_local
from ncloud.commands.command import Command, print_table, build_subparser
from ncloud.commands.command import LS, SHOW, UNDEPLOY, PREDICT
from ncloud.completers import ModelCompleter

logger = logging.getLogger()


class Undeploy(Command):
    """
    Remove a deployed model.
    """
    @classmethod
    def parser(cls, subparser):
        undeploy = subparser.add_parser(
            UNDEPLOY.name, aliases=UNDEPLOY.aliases,
            help=Undeploy.__doc__, description=Undeploy.__doc__
        )
        undeploy.add_argument(
            "stream_id",
            help="ID of stream to undeploy."
        ).completer = ModelCompleter

        undeploy.set_defaults(func=cls.arg_call)

    @staticmethod
    def call(config, stream_id):
        delete_path = os.path.join(STREAM_PREDICTIONS, str(stream_id))
        return api_call_json(config, delete_path, method="DELETE")


class Predict(Command):
    """
    Generate predicted outcomes from a deployed model and input data.
    """
    @classmethod
    def parser(cls, subparser):
        predict = subparser.add_parser(
            PREDICT.name, aliases=PREDICT.aliases,
            help=Predict.__doc__, description=Predict.__doc__
        )
        predict.add_argument(
            "presigned_token",
            help="Presigned token for sending prediction requests."
        )
        predict.add_argument(
            "input",
            help="Input data filename or url to generate predictions for."
        )
        predict.add_argument(
            "-t", "--in-type",
            default="image",
            help="Type of input.  Valid choices are: image (default), json"
        )
        predict.add_argument(
            "-f", "--formatter", default="raw",
            choices=('raw', 'classification'),
            help="How to format predicted outputs from the network. Valid "
                 "choices are: raw (default), classification"
        )
        predict.add_argument(
            "-a", "--args",
            help="Additional arguments for the formatter. These vary, details "
                  "can be found at: http://doc.cloud.nervanasys.com (Output "
                  "Formatters)"
        )

        predict.set_defaults(func=cls.arg_call)

    @staticmethod
    def call(config, presigned_token, input, in_type=None, formatter=None,
             args=None):

        vals = {}
        files = None

        if input.startswith("http") or input.startswith("s3"):
            vals["url"] = input
        elif os.path.exists(input):
            files = [('input', (os.path.basename(input), open(input, "rb")))]
        else:
            print("no/invalid input data specified")
            sys.exit(1)

        if in_type:
            vals["type"] = in_type
        if formatter:
            vals["formatter"] = formatter
        if args:
            vals["args"] = args

        if not presigned_token.isdigit():
            endpoint = os.path.join(STREAM_PREDICTIONS, presigned_token)
        else:
            endpoint = os.path.join('/predictions/', presigned_token)
        return api_call(config, endpoint, method="POST", data=vals,
                        files=files)

    @staticmethod
    def display_after(config, args, res):
        if not args.formatter or args.formatter == "raw":
            print(res)
        else:
            res = json.loads(res, object_pairs_hook=OrderedDict)
            if "predictions" in res:
                print_table(res["predictions"])
            else:
                print_table(res)


class List(Command):
    """
    List all stream prediction deployments.
    """
    @classmethod
    def parser(cls, subparser):
        list_stream_prediction = subparser.add_parser(
            LS.name, aliases=LS.aliases,
            help=List.__doc__, description=List.__doc__
        )
        list_stream_prediction.set_defaults(func=cls.arg_call)

    @staticmethod
    def call(config):
        return api_call_json(config, STREAM_PREDICTIONS)

    @staticmethod
    def display_after(config, args, res):
        if res:
            print_table(res['stream_predictions'])


class Show(Command):
    """
    Show stream prediction details for a given stream ID.
    """
    @classmethod
    def parser(cls, subparser):
        stream_predict_show = subparser.add_parser(
            SHOW.name, aliases=SHOW.aliases,
            help=Show.__doc__, description=Show.__doc__
        )
        stream_predict_show.add_argument(
            "stream_id",
            help="ID of stream to show details of."
        )
        stream_predict_show.add_argument(
            "-l", "--log", action="store_true",
            help="Show console log from predict runtime.")

        stream_predict_show.set_defaults(func=cls.arg_call)

    @staticmethod
    def call(config, stream_id, log=False):
        show_path = os.path.join(STREAM_PREDICTIONS, stream_id)
        if log:
            res = api_call(config, show_path, params={'log': 'True'})
            write = getattr(sys.stdout, 'buffer', sys.stdout).write
            try:
                write(zipfile.ZipFile(io.BytesIO(res)).read('krypton.log'))
            except KeyError:
                logger.warning("attempting to view non-existent krypton.log")
            return

        res = api_call_json(config, show_path)

        for tm in ["time_launched"]:
            if tm in res and res[tm] is not None:
                res[tm] = utc_to_local(res[tm])

        return res


parser = partial(
    build_subparser, 'stream', ['s'], __doc__, (List, Show, Undeploy, Predict)
)
