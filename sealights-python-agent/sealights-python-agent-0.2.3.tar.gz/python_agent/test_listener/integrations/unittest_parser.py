import argparse
from python_agent.test_listener import config

global_parser = argparse.ArgumentParser()


def add_options():
    global_parser.add_argument("--customer_id", required=True, help="An id representing the client")
    global_parser.add_argument("--app_name", required=True, help="The name of the application")
    global_parser.add_argument("--server", required=True, help="Sealights Server. Must be of the form: http://<server>/api")
    global_parser.add_argument("--build", default="1", help="The build number of the application")
    global_parser.add_argument("--branch", default="master", help="The branch of the current build")
    global_parser.add_argument("--env", default="python-dev", help="The environment of the current build")


def parse(parser):
    args, unknown_args = parser.parse_known_args()

    config.app["customer_id"] = args.customer_id
    config.app["app_name"] = args.app_name
    config.app["server"] = args.server
    config.app["build"] = args.build
    config.app["branch"] = args.branch
    config.app["env"] = args.env

    return args, unknown_args
