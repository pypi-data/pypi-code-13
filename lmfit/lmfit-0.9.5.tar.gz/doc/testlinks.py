from sphinx.ext.intersphinx import fetch_inventory
import warnings
uri = 'file:///Users/Newville/Codes/lmfit-py/doc/_build/html/'
inv = fetch_inventory(warnings, uri, uri + 'objects.inv')
print (" INV : ", inv)

for key in inv.keys():
    for key2 in inv[key]:
        print(key2)
