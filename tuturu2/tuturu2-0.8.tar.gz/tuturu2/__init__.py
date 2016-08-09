__title__ = 'tuturu2'
__version__ = '0.4'
__author__ = 'pickle' 
__license__ = 'GPL 3.0'
__copyright__ = 'Pickle'

import pickle
def load(path):
    try:
        file = open(path, "rb")
        tuturu = pickle.load(file)
        file.close()
        return tuturu
    except Exception:
        return None
        
def dump(var, path):
    try:
        file = open(path, "wb")
        pickle.dump(var, file)
        file.close()
        return True
    except Exception:
        return False
