import ujson as json
from options import Options
from collections import namedtuple
#from cnamedtuple import namedtuple
import pysos
import starpath
import os
import dir_dict
#import finder

Node = namedtuple('Node', 'path parent key value')


DB_NAME = 'data'
root = dir_dict.DirDict(DB_NAME)

hook_cached = None
def hook_before(node):
    if isinstance(node.parent, pysos.List) or isinstance(node.parent, pysos.Dict):
        hook_cached = json.dumps(node.value)

def hook_after(node):
    if isinstance(node.parent, pysos.List) or isinstance(node.parent, pysos.Dict):
        after = json.dumps(node.value)
        if after != hook_cached:
            onchange(node, hook_cached)
        

def dirtyCheck(status):
    starpath.hook_before = hook_before if status else None
    starpath.hook_after = hook_after if status else None

def onchange(node, before):
    print(node.path)
    node.parent[node.key] = node.value
    #

def onchange2(coll, key, value, old):
    pass


#######################################################################################
#   GET
#######################################################################################

def count(path, opt=Options()):
    opt.count = True
    return find(path, opt)
    
def find(path, opt=Options()):
    res = _find(path, opt)
    return json.dumps(res)

def _find(path, opt):
    global root
    dirtyCheck(False)
    
    # distinct
    if not opt.distinct:
        results = []
    else:
        results = set()
    
    for obj in starpath.find(root, path):
        if opt.where and not opt.where(obj):
            continue

        if opt.select:
            obj = opt.select(obj)
        elif opt.ignore:
            obj = opt.ignore(obj)

        if opt.distinct:
            results.add(obj) # set
        else:
            results.append(obj) # list

        if not opt.count and opt.limit > 0 and len(results) == opt.offset + opt.limit:
            break
            
    if opt.count:
        return len(results)

    if opt.distinct:
        results = list(results)
        
    if opt.sortby:
        reverse = (opt.sortby[0] == '-')
        if opt.sortby[0] in '-+':
            opt.sortby = opt.sortby[1:]
        resuls = sorted(results, lambda item : item[opt.sortby], reverse)

    if opt.offset or opt.limit:
        results = results[opt.offset:opt.offset+opt.limit]
        
    return results



def get(path, opt=Options()):
    global root
    dirtyCheck(False)
    res = starpath.get(root, path)
    return json.dumps(res)

#######################################################################################
#   SET
#   - force: if True, empty maps will be created for non-existent path parts
#######################################################################################

def set(path, opt, data_str, force=False):
    global root
    dirtyCheck(True)
    if not path or path == '/':
        raise Exception('Setting the root directly is forbidden.')

    data = json.loads(data_str)
    res = starpath.set(root, path, data)
    #return json.dumps(res)
    return "%d item(s) modified" % len(res)


#######################################################################################
#   ADD
#######################################################################################

def add(path, opt, data_str, force=False):
    global root
    dirtyCheck(True)
    if not path or path == '/':
        raise Exception('The root is a dictionary, not a list.')

    data = json.loads(data_str)
    res = starpath.add(root, path, data)
    #return json.dumps(res)
    return "%d item(s) modified" % len(res)
    
#######################################################################################
#   UPDATE
#######################################################################################

def update(path, opt, data_str):
    global root
    dirtyCheck(True)
    data = json.loads(data_str)
    res = starpath.update(root, path, data)
    #return json.dumps(res)
    return "%d item(s) modified" % len(res)


#######################################################################################
#   DELETE
#######################################################################################

def delete(path, opt):
    global root
    dirtyCheck(True)
    if not path or path == '/':
        raise Exception('Removing the root directly is forbidden.')

    res = starpath.delete(root, path)
    #return json.dumps(res)
    return "%d item(s) modified" % len(res)


