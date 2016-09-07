import os
import glob
from cffi import FFI
from os.path import join as path_join

def here(*name):
    return path_join(os.path.dirname(__file__), *name)

library_dirs = []
include_dirs = []

FIRM_PROVIDED = os.path.exists(here('../libfirm/Makefile'))
FIRM_HOME = os.environ.get('FIRM_HOME', False)
obj_path = None

if FIRM_HOME:
    for variant in 'debug profile coverage optimise'.split():
        library_dirs.append(path_join(FIRM_HOME, 'build', variant))
        libfirm_a = path_join(FIRM_HOME, 'build', variant, 'libfirm.a')
        if os.path.exists(libfirm_a) and obj_path is None:
            obj_path = libfirm_a
    for loc in 'include build/gen/include build/gen/include/libfirm'.split():
        include_dirs.append(path_join(FIRM_HOME, loc))
elif FIRM_PROVIDED:
    obj_path = '%(build_dir)s/%(variant)s/libfirm.a'
    include_dirs = ['%(build_dir)s/gen/include/',
                    '%(build_dir)s/gen/include/libfirm/',
                    here('../libfirm/include/')]

ffi = FFI()
if obj_path:
    ffi.set_source("_python_firm", '#include "libfirm/firm.h"',
                   extra_objects = [obj_path],
                   include_dirs = include_dirs)
else:
    ffi.set_source("_python_firm", '#include "libfirm/firm.h"',
                   libraries = ['firm'],
                   library_dirs = library_dirs,
                   include_dirs = include_dirs)


#with open(here('fn_defs.h')) as f:
#    defs = list(f)
with open(here('firmtypes.h')) as f:
    defs = list(f)
with open(here('node_defs.h')) as f:
    defs.extend(f)

for filename in sorted(glob.glob(here('symbols/*.h'))):
    with open(filename) as f:
        defs.extend(f)

ffi.cdef('\n'.join(defs))

if __name__ == '__main__':
    ffi.compile()
