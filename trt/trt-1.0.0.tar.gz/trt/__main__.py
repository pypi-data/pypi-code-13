#!/usr/bin/python
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# Thomas Quintana <quintana.thomas@gmail.com>

import os

from argparse import ArgumentParser

from jinja2 import Environment, FileSystemLoader

def main():
  parser = ArgumentParser(
    description="Renders a Jinja2 template using command line arguments or " +
                "environment variables as parameters for the template."
  )
  parser.add_argument(
    "-s", dest="source", required=True,
    help="The path to the source template."
  )
  parser.add_argument(
    "-d", dest="destination", required=True,
    help="The path to the destination file."
  )
  parser.add_argument(
    "-ps", dest="parameter_source", choices=["environment", "cli"], required=True,
    help="The source of the parameters for the template. The options " +
         "are 'environment' if you want to use the environment variables " +
         "as parameters or 'cli' if you want to pass in the parameters " +
         "as arguments to this script. Note: All parameter names are " +
         "converted to lower case irrelevant of the parameters source."
  )
  parser.add_argument(
    "-p", dest="parameters", nargs="*", required=False,
    help="A parameter to pass into the template renderer if the " +
         "parameters-source is 'cli'."
  )
  args = parser.parse_args()
  # Load the parameters.
  parameters = None
  if args.parameter_source == "cli":
    parameters = args.parameters
  elif args.parameter_source == "environment":
    parameters = dict(os.environ)
  parameters = to_lowercase_keys(parameters)
  # Load the templates.
  folder_name, file_name = split_path(args.source)
  if folder_name is None:
    folder_name = os.getcwd()
  loader = FileSystemLoader(folder_name)
  templates = Environment(loader=loader)
  # Render the template.
  template = templates.get_template(file_name).render(parameters)
  # Write the rendered template to disk.
  with open(args.destination, "wb") as output:
    output.write(template)

def split_path(path):
  split_point = path.rfind("/")
  if not split_point == -1:
    return path[:split_point], path[split_point + 1:]
  else:
    return None, path

def to_lowercase_keys(parameters):
  if isinstance(parameters, list):
    return {k.lower(): v for k, v in [p.split("=") for p in parameters]}
  elif isinstance(parameters, dict):
    return {k.lower(): v for k, v in parameters.iteritems()}
  else:
    raise ValueError("Invalid type for parameters.")

if __name__ == "__main__":
  main()
