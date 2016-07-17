


import argparse


argParser=argparse.ArgumentParser()

argParser.add_argument("-f","--file", help="Specify a theme to apply.", type=str,default=None)
argParser.add_argument("theme", help="Specify a buid-in theme name.", type=str,nargs='?', default=None)
argParser.add_argument("-l","--list", help="List build in themes", action="store_true", default=False)
argParser.add_argument("-c","--clean", help="Remove theme lines from ~/.i3/config",action="store_true", default=False)
