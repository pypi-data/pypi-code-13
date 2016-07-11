import sys
import os

def _main(argv):
    if len(argv) < 1:
        return _main(["1"])
    number_of_pandas = int(argv[0])
    while (number_of_pandas > 0):
        print 'panda'
        number_of_pandas = number_of_pandas - 1
    print os.getcwd()

if __name__ == "__main__":
	sys.exit(_main(sys.argv[1:]))
