import argparse
import os

def get_root(start_location="."):
    location = os.path.abspath(start_location)
    if not os.path.isdir(location):
        location = os.path.dirname(location)
    while location != "/":
        if os.path.isfile(os.path.join(location, "buildout.cfg")):
            break
        location = os.path.dirname(location)
    if not os.path.isfile(os.path.join(location, "buildout.cfg")):
        raise RuntimeError("can't locate buildout root directory")
    return location
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest="location", default=".", nargs="?")
    opts = parser.parse_args()
    print(get_root(opts.location))


if __name__ == "__main__":
    main()    
