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
        file = open(path, "rb")
        pickle.dump(var, file)
        file.close()
        return True
    except Exception:
        return False
