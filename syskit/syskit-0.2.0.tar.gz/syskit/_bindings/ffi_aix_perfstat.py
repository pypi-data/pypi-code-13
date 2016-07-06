# -*- coding: utf-8 -*-

from __future__ import (absolute_import,
                        unicode_literals, print_function, division)

INCLUDES = """
#include <alloca.h>
#include <libperfstat.h>
#include <sys/proc.h>
"""

LIBS = ['perfstat']


INT_TYPEDEFS = {
    'u_longlong_t': 'unsigned long long',
}


STRUCTS = """
typedef struct { ...; } perfstat_id_t;

typedef struct {
    ...;
    u_longlong_t loadavg[3];
    ...;
} perfstat_cpu_total_t;
"""


MACROS = """
#define SBITS ...
"""


FUNCTIONS = """
int perfstat_cpu_total(perfstat_id_t *name, perfstat_cpu_total_t *userbuff,
                       int sizeof_struct, int desired_number);
"""


VERIFY_PREAMLE = """
"""


VERIFY_EXTRA = """
"""
