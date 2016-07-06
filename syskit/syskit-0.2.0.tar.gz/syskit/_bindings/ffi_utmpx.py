# -*- coding: utf-8 -*-

"""Minimal definitions for umtpx

We roughly only define what we use instead of having a complete utmpx
binding.  Currently this is only used in ``syskit._utils.boottime()``
so this is pretty minimal.

This should really expose the reentrant versions where available.

"""

from __future__ import (absolute_import,
                        unicode_literals, print_function, division)


INCLUDES = """
#include <alloca.h>
#include <utmpx.h>
"""


LIBS = []


INT_TYPEDEFS = {
    'time_t': 'long',
    'pid_t': 'long',
}


STRUCTS = """
struct timeval {
    time_t tv_sec;        /* seconds */
    long tv_usec;         /* microseconds */
};

struct utmpx {
    char ut_user[...];           /* user login name */
    char ut_id[...];             /* /etc/inittab id */
    char ut_line[...];           /* device name */
    pid_t ut_pid;                /* process id */
    short ut_type;               /* type of entry */
    struct timeval ut_tv;        /* time entry was made */
    char ut_host[...];           /* host name if remote */
};
"""


MACROS = """
#define EMPTY ...              /* no valid info */
#define RUN_LVL ...            /* change in system run-level */
#define BOOT_TIME ...          /* time of system boot */
#define OLD_TIME ...           /* time before clock change */
#define NEW_TIME ...           /* time after clock change */
#define USER_PROCESS ...       /* normal process */
#define INIT_PROCESS ...       /* process spawned by init */
#define LOGIN_PROCESS ...      /* session leader process for user login */
#define DEAD_PROCESS ...       /* terminated process */
"""


FUNCTIONS = """
struct utmpx *getutxent(void);
struct utmpx *getutxid(const struct utmpx *id);
struct utmpx *getutxline(const struct utmpx *line);
struct utmpx *pututxline(const struct utmpx *utmpx);
void setutxent(void);
void endutxent(void);
"""


VERIFY_PREAMLE = """
"""


VERIFY_EXTRA = """
"""
