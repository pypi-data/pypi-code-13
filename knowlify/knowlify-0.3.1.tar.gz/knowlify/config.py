import sys
import os

DATA_DIR = './data/'

if not os.path.isdir(DATA_DIR):
    os.mkdir(DATA_DIR)

sys.path.append(DATA_DIR)