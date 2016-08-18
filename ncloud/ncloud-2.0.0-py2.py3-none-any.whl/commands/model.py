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
Subcommands for training, deploying, and otherwise managing models.
"""
from __future__ import print_function
from builtins import str

from functools import partial
import io
import os
import sys
import py_compile
import zipfile
from datetime import datetime
import logging

import requests
from ncloud.vendor.argcomplete.argcomplete.completers import FilesCompleter

from ncloud.commands.command import Command, build_subparser, string_argument
from ncloud.commands.command import LS, SHOW, TRAIN, STOP, IMPORT, DEPLOY
from ncloud.commands.command import RESULTS
from ncloud.formatting.time_zone import utc_to_local
from ncloud.formatting.output import print_table
from ncloud.util.api_call import api_call, api_call_json
from ncloud.util.file_transfer import multipart_upload
from ncloud.config import MODELS, STREAM_PREDICTIONS
from ncloud.completers import NeonVersionCompleter
from ncloud.completers import DatasetCompleter, HTTPCompleter
from ncloud.completers import DirectoriesCompleter, ModelCompleter

logger = logging.getLogger()


class Show(Command):
    """
    Show model details for a given model ID.
    """
    @classmethod
    def parser(cls, subparser):
        show_model = subparser.add_parser(SHOW.name, aliases=SHOW.aliases,
                                          help=Show.__doc__,
                                          description=Show.__doc__)
        show_model.add_argument(
            "model_id",
            help="ID of model to show details of."
        ).completer = ModelCompleter
        show_model.add_argument("-l", "--console-log", action="store_true",
                                help="Show console log from model runtime.")
        show_model.add_argument("-n", "--neon-log", action="store_true",
                                help="Show neon log file.")
        show_model.add_argument("-r", "--rename",
                                type=string_argument,
                                help="Rename a model.")
        show_model.add_argument('-z', "--model_zoo", action="store_true",
                                help="Show model in the model zoo.")

        show_model.set_defaults(func=cls.arg_call)

    @staticmethod
    def call(config, model_id, console_log=False,
             neon_log=False, rename=None, model_zoo=False):
        model_id = str(model_id)
        if console_log or neon_log:
            results_path = os.path.join(MODELS, model_id, "results")
            vals = {"format": "zip", "filter": ["*.log"]}
            if model_zoo:
                vals["model_zoo"] = "True"
            zipfiles = api_call(config, results_path, params=vals)
            zipbytes = io.BytesIO(zipfiles)
            archive = zipfile.ZipFile(zipbytes)
            ziplogs = archive.namelist()

            # has to be done here because of pytest shenanigans
            # pytest replaces sys.stdout specifically
            write = getattr(sys.stdout, 'buffer', sys.stdout).write
            if neon_log:
                try:
                    write(archive.read('neon.log'))

                except KeyError:
                    logger.warning("attempting to view non-existent neon.log")
            else:
                log = 'launcher.log'
                if log in ziplogs:
                    write(archive.read(log))
        else:
            show_path = os.path.join(MODELS, model_id)
            if rename:
                vals = {"operation": "replace", "name": rename}
                # yes, this will fail
                if model_zoo:
                    vals["model_zoo"] = "True"
                res = api_call_json(config, show_path, method="PATCH",
                                    data=vals)
            else:
                vals = {}
                if model_zoo:
                    vals["model_zoo"] = "True"
                res = api_call_json(config, show_path, data=vals)

            try:
                fstr = '{0:g}'.format(res['epochs_completed'])
                res['epochs_completed'] = fstr
            except ValueError:
                # prior to helium v1.1.0, we only returned a string
                pass
            for tm in ["train_request", "train_start", "train_end"]:
                if tm in res and res[tm] is not None:
                    res[tm] = utc_to_local(res[tm])
            return res


class List(Command):
    """
    List all submitted, queued, and running models.
    """
    @classmethod
    def parser(cls, subparser):
        list_models = subparser.add_parser(LS.name, aliases=LS.aliases,
                                           help=List.__doc__,
                                           description=List.__doc__)
        list_models_type = list_models.add_mutually_exclusive_group()
        list_models_type.add_argument("--done", action="store_true",
                                      help="Show only models finished "
                                           "training.")
        list_models_type.add_argument("--training", action="store_true",
                                      help="Show only training models.")
        list_models.add_argument("-n", "--count", type=int, default='10',
                                 help="Show up to n most recent models. "
                                      "For unlimited set n=0.")
        list_models_type.add_argument("--details", action="store_true",
                                      help="Show more details about models.")
        list_models_type.add_argument('-z', "--model-zoo", action="store_true",
                                      help="List all models in the model zoo.")

        list_models.set_defaults(func=cls.arg_call)

    @staticmethod
    def call(config, count=10, details=False, done=False, training=False,
             model_zoo=False):
        vals = {"count": count}

        if details:
            vals["details"] = "True"

        if done:
            vals["filter"] = ["Completed", "Error", "Deploying", "Deployed",
                              "Undeploying", "Imported"]
        elif training:
            vals["filter"] = ["Preparing Data (1/4)", "Preparing Data (2/4)",
                              "Preparing Data (3/4)", "Preparing Data (4/4)",
                              "Queued", "Running"]
        else:
            vals["filter"] = ["Received", "Preparing Data (1/4)",
                              "Preparing Data (2/4)", "Preparing Data (3/4)",
                              "Preparing Data (4/4)", "Submitted", "Queued",
                              "Running", "Removed", "Completed", "Error",
                              "Deploying", "Deployed", "Undeploying",
                              "Imported"]

        if model_zoo:
            vals["model_zoo"] = "True"

        return api_call_json(config, MODELS, params=vals)

    @staticmethod
    def display_after(config, args, res):
        if res:
            print_table(res['models'])


class Train(Command):
    """
    Submit a deep learning model for training.
    """
    @classmethod
    def parser(cls, subparser):
        train = subparser.add_parser(TRAIN.name, aliases=TRAIN.aliases,
                                     help=Train.__doc__,
                                     description=Train.__doc__)
        train.add_argument("filename",
                           type=string_argument,
                           help=".yaml or .py script file for Neon to "
                                "execute.")
        train.add_argument("-n", "--name",
                           type=string_argument,
                           help="Colloquial name of the model. Default"
                                " name will be given if not provided.")
        train.add_argument(
            "-d", "--dataset-id", help="ID of dataset to use."
        ).completer = DatasetCompleter
        train.add_argument("-v", "--validation-percent", default=.2,
                           help="Percent of dataset to use as validation "
                                "split.")
        train.add_argument("-e", "--epochs",
                           help="Number of epochs to train this model.")
        train.add_argument("-z", "--batch-size",
                           help="Mini-batch size to train this model.")
        train.add_argument(
            "-f", "--framework-version",
            help="Neon tag, branch or commit to use."
        ).completer = NeonVersionCompleter
        train.add_argument(
            "-m", "--mgpu-version",
            help="MGPU tag, branch or commit to use, if 'gpus' > 1."
        )
        train.add_argument("-a", "--args", help="Neon command line arguments.")
        train.add_argument("-i", "--resume-model-id",
                           help="Start training a new model using the state "
                                "parameters of a previous one.")
        train.add_argument("-g", "--gpus", default=1,
                           help="Number of GPUs to train this model with.")
        train.add_argument("-r", "--replicas", default=0,
                           help="Number of replicas of the main process to "
                                "invoke.  0 means use standard process, 1 "
                                "means use a parameter server, 2-N means "
                                "use peer-to-peer communication.")
        train.add_argument(
            "-u", "--custom-code-url",
            help="URL for codebase containing custom neon "
                 "scripts and extensions."
        ).completer = HTTPCompleter
        train.add_argument("-c", "--custom-code-commit", default="master",
                           help="Commit ID or branch specifier for custom "
                                "code repo.")

        train.set_defaults(func=cls.arg_call)

    @staticmethod
    def call(config, filename, gpus=1, replicas=0, framework_version=None,
             mgpu_version=None, name=None, dataset_id=None,
             validation_percent=None, custom_code_url=None,
             args=None, resume_model_id=None, epochs=10, batch_size=128,
             custom_code_commit=None):

        vals = {"filename": filename, "gpus": gpus,
                "replicas": replicas}
        extension = os.path.splitext(filename)[1][1:]
        if extension in ["py", "yaml"] and custom_code_url is None:
            with open(filename, "r") as model_file:
                model_data = model_file.read()

            if extension == "py":
                try:
                    py_compile.compile(filename, doraise=True)
                except py_compile.PyCompileError as pe:
                    print(pe)
                    sys.exit(1)
            # skip yaml syntax checking here and instead do it server side to
            # keep third party libraries to a minimum (pyyaml / libyaml).

            vals[extension] = model_data

        if framework_version:
            vals["framework_version"] = framework_version

        if mgpu_version:
            vals["mgpu_version"] = mgpu_version

        if name:
            vals["name"] = name

        if dataset_id:
            vals["dataset_id"] = dataset_id
            assert validation_percent is not None
            vals["validation_percent"] = validation_percent

        if args:
            vals["args"] = args

        if resume_model_id:
            vals["resume_model_id"] = resume_model_id

        if epochs:
            vals["epochs"] = epochs

        if batch_size:
            vals["batch_size"] = batch_size

        if custom_code_url:
            vals["custom_code_url"] = custom_code_url
            vals["custom_code_cmd"] = filename

        if custom_code_commit:
            vals["custom_code_commit"] = custom_code_commit

        return api_call_json(config, MODELS, method="POST", data=vals)


class Stop(Command):
    """
    Stop training a model given a model ID.
    """
    @classmethod
    def parser(cls, subparser):
        stop_training = subparser.add_parser(STOP.name, aliases=STOP.aliases,
                                             help=Stop.__doc__,
                                             description=Stop.__doc__)
        stop_training.add_argument("model_id", help="ID of model to stop.")
        stop_training.set_defaults(func=cls.arg_call)

    @staticmethod
    def arg_names():
        return ['model_id']

    @staticmethod
    def call(config, model_id):
        return api_call_json(config, MODELS + model_id, method="DELETE")


class Import(Command):
    """
    Import a previously trained model.
    """
    @classmethod
    def parser(cls, subparser):
        i_pars = subparser.add_parser(IMPORT.name, aliases=IMPORT.aliases,
                                      help=Import.__doc__,
                                      description=Import.__doc__)
        i_pars.add_argument("input",
                            help="Serialized neon model filename or url "
                                 "to import.")
        i_pars.add_argument(
            "-s", "--script",
            help=".py or .yaml script used to train the imported model."
        ).completer = FilesCompleter('py', 'yaml')
        i_pars.add_argument("-e", "--epochs",
                            help="Number of epochs imported model trained. "
                                 "(amount originally requested)")
        i_pars.add_argument("-n", "--name", type=string_argument,
                            help="Colloquial name of the model. Default "
                                 "name will be given if not provided.")

        i_pars.set_defaults(func=cls.arg_call)

    @staticmethod
    def call(config, input, epochs=None, name=None, script=None):
        vals = dict()
        files = None
        if epochs:
            vals["epochs_requested"] = epochs
        if name:
            vals["name"] = name
        if script and os.path.exists(script):
            files = [('script_file', (os.path.basename(script),
                                      open(script, "rb")))]

        def import_model(vals, files):
            return api_call_json(config, MODELS + "import", method="POST",
                                 data=vals, files=files)

        if input.startswith("http") or input.startswith("s3"):
            vals["model_url"] = input
            res = import_model(vals, files)
        elif os.path.exists(input):
            chunksize = 5242880

            basename = os.path.basename(input)

            if os.path.getsize(input) <= chunksize:
                if files is None:
                    files = []
                files.append(('model_file', (basename, open(input, "rb"))))
                res = import_model(vals, files)
            else:
                vals['multipart'] = True
                vals['model_filename'] = basename
                res = import_model(vals, files)
                print("Model ID: {}".format(res['id']))
                multipart_id = res['multipart_id']

                res = multipart_upload(config, input, multipart_id, chunksize)
        else:
            print("no/invalid input model specified")
            sys.exit(1)

        return res

    @staticmethod
    def display_before(conf, args):
        print("importing (may take some time)...")


class Results(Command):
    """
    Retrieve model training results files: model weights, callback outputs and
    neon log.
    """
    @classmethod
    def parser(cls, subparser):
        train_results = subparser.add_parser(RESULTS.name,
                                             aliases=RESULTS.aliases,
                                             help=Results.__doc__,
                                             description=Results.__doc__)
        train_results.add_argument(
            "model_id", help="ID of model to retrieve results of."
        ).completer = ModelCompleter
        train_results.add_argument(
            "-d", "--directory",
            help="Location to download files {directory}/results_files. "
                 "Defaults to current directory."
        ).completer = DirectoriesCompleter
        train_results_mode = train_results.add_mutually_exclusive_group()
        train_results_mode.add_argument("-u", "--url", action="store_true",
                                        help="Obtain URLs to directly "
                                             "download individual results.")
        train_results_mode.add_argument("-o", "--objects", action="store_true",
                                        help="Download objects directly "
                                             "to specified directory.")
        train_results_mode.add_argument("-z", "--zip", action="store_true",
                                        help="Retrieve a zip file of results.")
        train_results_mode.add_argument("-t", "--tar", action="store_true",
                                        help="Retrieve a tar file of results.")
        train_results.add_argument("-f", "--filter", action='append',
                                   help="Only retrieve files with names "
                                        "matching <filter>.  Note - uses glob "
                                        "style syntax. Multiple --filter "
                                        "arguments will be combined with "
                                        "logical or.")

        train_results.set_defaults(func=cls.arg_call)

    @staticmethod
    def call(config, model_id, filter=None, zip=None, tar=None,
             url=None, objects=None, directory=None):
        vals = dict()
        results_path = os.path.join(MODELS, model_id, "results")
        if filter:
            vals["filter"] = filter

        results = None
        if url or objects:
            vals["format"] = "url"
            results = api_call_json(config, results_path, params=vals)
            if objects:
                directory = directory if directory else '.'
                if not os.path.exists(directory):
                    os.makedirs(directory)
                for result in results["result_list"]:
                    obj = requests.get(result["url"], stream=True)
                    local_file = os.path.join(directory, result["filename"])
                    with open(local_file, 'wb') as f:
                        for chunk in obj.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                return
        elif zip or tar:
            if zip:
                ext = "zip"
                stream = False
            else:
                ext = "tar"
                stream = True
            vals["format"] = ext
            results = api_call(config, results_path, params=vals,
                               stream=stream)
            if results:
                directory = directory if directory else '.'
                if not os.path.exists(directory):
                    os.makedirs(directory)
                filename = (
                    'results_%d_%s.%s' % (
                        int(model_id),
                        datetime.strftime(datetime.today(), "%Y%m%d%H%M%S"),
                        ext
                    )
                )

                with open(os.path.join(directory, filename), 'wb') as f:
                    if stream:
                        for chunk in results.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                        return
                    else:
                        f.write(results)
        else:
            # default to listing results
            vals["format"] = "list"
            results = api_call_json(config, results_path, params=vals)
            if results and 'result_list' in results:
                result_list = results['result_list']
                for result in result_list:
                    result['last_modified'] = \
                        utc_to_local(result["last_modified"])

        return results

    @staticmethod
    def display_after(config, args, res):
        if res and 'result_list' in res:
            if args.url:
                print("Public URLs will expire 1 hour from now.")
            print_table(res['result_list'])


class Deploy(Command):
    """
    Make a trained model available for generating predictions against.
    """
    @classmethod
    def parser(cls, subparser):
        deploy = subparser.add_parser(
            DEPLOY.name, aliases=DEPLOY.aliases,
            help=Deploy.__doc__, description=Deploy.__doc__
        )
        deploy.add_argument(
            "model_id",
            help="ID of model to deploy."
        ).completer = ModelCompleter
        deploy.add_argument(
          "-g", "--gpus",
          default=0,
          help="Number of GPUs to use to generate predictions.  Defaults to 0 "
               "(use CPU only)."
        )
        deploy.add_argument(
            "-d", "--dataset_id",
            help="ID of dataset to include."
        )
        deploy.add_argument(
            "-f", "--extra_files",
            help="Zip of extra files to include in the deployment."
        )
        deploy.add_argument(
            "--custom_code_url",
            help="URL for codebase containing custom neon scripts and "
                 "extensions."
        )
        deploy.add_argument(
            "--custom_code_commit",
            default="master",
            help="Commit ID or branch specifier for custom code repo."
        )

        deploy.set_defaults(func=cls.arg_call)

    @staticmethod
    def call(config, model_id, gpus=0, dataset_id=None, extra_files=None,
             custom_code_url=None, custom_code_commit=None):
        vals = {"model_id": model_id, "gpus": gpus}

        if dataset_id is not None:
            vals["dataset_id"] = dataset_id

        files = None
        if extra_files is not None:
            files = [('extra_files', (os.path.basename(extra_files),
                     open(extra_files, "rb")))]

        if custom_code_url is not None:
            vals["custom_code_url"] = custom_code_url

        if custom_code_commit is not None:
            vals["custom_code_commit"] = custom_code_commit

        return api_call_json(config, STREAM_PREDICTIONS,
                             method="POST", data=vals, files=files)


parser = partial(
    build_subparser, 'model', ['m'], __doc__,
    (Show, List, Train, Stop, Import, Results, Deploy)
)
