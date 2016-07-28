try:
    import cPickle as pickle
except ImportError:
    import pickle
try:
    from StringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

def enpickle(data):
    f = BytesIO()
    p = pickle.Pickler(f)
    p.dump(data)
    return f.getvalue()
    
def depickle(data):
    f = BytesIO(data)
    p = pickle.Unpickler(f)
    return p.load()