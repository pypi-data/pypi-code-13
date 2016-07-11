#!/usr/bin/env python

import os
import argparse
from jinja2 import Template
from flast import templates

parser = argparse.ArgumentParser()
parser.add_argument("--pg", required=False, dest="pg", action='store_true',
                    help="create a project with postgresql support")
parser.add_argument("--redis", required=False, dest="rs", action='store_true',
                    help="create a project with redis support")
templates_path = templates.__path__[0]

cur_dir = os.path.abspath('.')
args = parser.parse_args()

for elem in os.listdir(templates_path):
    if not elem.endswith("py"):
        continue
    path = os.path.join(templates_path, elem)
    target = os.path.join(cur_dir, elem)

    if not os.path.exists(target):
        try:
            template = Template(open(path).read())
        except:
            import ipdb; ipdb.set_trace()
        app_type= ["BaseApp"]
        if args.pg:
            app_type.append("PostgreSQLApp")
        if args.rs:
            app_type.append("RedisApp")
        app_type.reverse()
        render = template.render(app_type=app_type)
        with open(target, "w") as fd:
            fd.write(render)

for elem in ["sql", "templates", "statics"]:
    target = os.path.join(cur_dir, elem)
    if not os.path.exists(target):
        os.mkdir(target)
