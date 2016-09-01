'''
Created on 11/12/2015

@author: mmpe
'''
from inspect import getmembers, isfunction


if __name__ == "__main__":
    from wetb.wind import weibull
    module = weibull
    import inspect

    #for name, func in [o for o in getmembers(module) if isfunction(o[1]) and not o[0].startswith("_")]:
    #    print ("- `%s <#%s.%s>`_: %s" % (name, func.__module__, name, func.__doc__.split("\n")[0]))
    docs = module.__doc__
    if docs is None:
        docs = '"""\nContents"""'
        with open (module.__file__) as fid:
            txt = fid.read()
        with open(module.__file__, 'w') as fid:
            fid.write(docs + txt)
    if "\nContents" in docs:
        docs = docs[:docs.index("\nContents")]

    docs += "\nContents\n--------\n"
    for name, func in [o for o in getmembers(module) if isfunction(o[1]) and not o[0].startswith("_")]:
        docs += "- `%s <#%s.%s>`_: %s\n" % (name, func.__module__, name, func.__doc__.split("\n")[0])

    print (docs)
    with open (module.__file__) as fid:
        txt = fid.read()

    with open(module.__file__, 'w') as fid:
        fid.write(txt.replace(module.__doc__, docs))



    #print (weibull.__doc__)
