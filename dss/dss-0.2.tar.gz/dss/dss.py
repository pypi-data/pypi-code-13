from core.core import Core

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("cmd")

args = parser.parse_args()

if args.cmd == "start":
    dss_core = Core()
    dss_core.run()

elif args.cmd == "parse":
    dss_core = Core()
    dss_core.parse()

elif args.cmd == "suspend":
    dss_core = Core()
    dss_core.suspend()

elif args.cmd == "resume":
    dss_core = Core()
    dss_core.resume()

elif args.cmd == "terminate":
    dss_core = Core()
    dss_core.terminate()

