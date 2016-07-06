# -*- coding: utf-8 -*-

from __future__ import (absolute_import,
                        unicode_literals, print_function, division)


INCLUDES = """
#include <alloca.h>
#include <sys/proc.h>
#include <procfs.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
"""


LIBS = []


# These get translated to "typedef {value} {key};".  The benefit of
# this is that this will also generate a function used in
# `ffi.verify()` wich checks that these declarations are done
# correctly.
INT_TYPEDEFS = {
    'ushort_t': 'unsigned short',
    'ulong_t': 'unsigned long',
    'time_t': 'long',
    'id_t': 'long',
    'pid_t': 'long',
    'uid_t': 'unsigned long',
    'gid_t': 'unsigned long',
    'dev_t': 'unsigned long',
    'zoneid_t': 'long',
}


STRUCTS = """
typedef struct timespec {
    time_t tv_sec;
    long tv_nsec;
} timestruc_t;

typedef struct lwpsinfo {
    /*int pr_flag;*/            /* lwp flags (DEPRECATED: see below) */
    /*id_t pr_lwpid;*/          /* lwp id */
    /*uintptr_t pr_addr;*/      /* DEPRECATED was internal address of lwp */
    /*uintptr_t pr_wchan;*/     /* DEPRECATED was wait addr for sleeping lwp */
    /*nchar pr_stype;*/         /* synchronization event type */
    ...;
    char pr_state;              /* numeric lwp state */
    char pr_sname;              /* printable character for pr_state */
    char pr_nice;               /* nice for cpu usage */
    /*short pr_syscall;*/       /* system call number (if in syscall) */
    /*char pr_oldpri;*/         /* pre-SVR4, low value is high priority */
    /*char pr_cpu;*/            /* pre-SVR4, cpu usage for scheduling */
    ...;
    int pr_pri;                 /* priority, high value = high priority */
    /*ushort_t pr_pctcpu;*/     /* % of recent cpu time used by this lwp */
    /*timestruc_t pr_start;*/   /* lwp start time, from the epoch */
    /*timestruc_t pr_time;*/    /* cpu time for this lwp */
    /*char pr_clname[PRCLSZ];*/ /* scheduling class name */
    /*char pr_name[PRFNSZ];*/   /* name of system lwp */
    /*processorid_t pr_onpro;*/ /* processor which last ran this lwp */
    /*processorid_t pr_bindpro;*//* processor to which lwp is bound */
    /*psetid_t pr_bindpset;*/   /* processor set to which lwp is bound */
    /*lgrp_id_t pr_lgrp;*/      /* home lgroup */
    /*hrtime_t pr_last_onproc;*//* Timestamp of when thread last ran on */
                                /* a processor */
    ...;
} lwpsinfo_t;

typedef struct psinfo {
    int pr_flag;            /* process flags (DEPRECATED: see below) */
    int pr_nlwp;            /* number of active lwps in the process */
    int pr_nzomb;           /* number of zombie lwps in the process */
    pid_t pr_pid;           /* process id */
    pid_t pr_ppid;          /* process id of parent */
    pid_t pr_pgid;          /* process id of process group leader */
    pid_t pr_sid;           /* session id */
    uid_t pr_uid;           /* real user id */
    uid_t pr_euid;          /* effective user id */
    gid_t pr_gid;           /* real group id */
    gid_t pr_egid;          /* effective group id */
    uintptr_t pr_addr;      /* DEPRECATED was address of process */
    size_t pr_size;         /* size of process image in Kbytes */
    size_t pr_rssize;       /* resident set size in Kbytes */
    dev_t pr_ttydev;        /* controlling tty device (or PRNODEV) */
    ushort_t pr_pctcpu;     /* % of recent cpu time used by all lwps */
    ushort_t pr_pctmem;     /* % of system memory used by process */
    timestruc_t pr_start;   /* process start time, from the epoch */
    timestruc_t pr_time;    /* cpu time for this process */
    timestruc_t pr_ctime;   /* cpu time for reaped children */
    char pr_fname[...];     /* name of exec'ed file [PRFNSZ] */
    char pr_psargs[...];    /* initial characters of arg list [PRARGSZ] */
    int pr_wstat;           /* if zombie, the wait() status */
    int pr_argc;            /* initial argument count */
    uintptr_t pr_argv;      /* address of initial argument vector */
    uintptr_t pr_envp;      /* address of initial environment vector */
    char pr_dmodel;         /* data model of the process */
    lwpsinfo_t pr_lwp;      /* information for representative lwp */
    /*taskid_t pr_taskid;*/     /* task id */
    /*projid_t pr_projid;*/     /* project id */
    /*poolid_t pr_poolid;*/     /* pool id */
    ...;
    zoneid_t pr_zoneid;     /* zone id */
    /*ctid_t pr_contract;*/     /* process contract id */
    ...;
} psinfo_t;

typedef struct prusage {
    id_t pr_lwpid;           /* lwp id.  0: process or defunct */
    int pr_count;            /* number of contributing lwps */
    timestruc_t pr_tstamp;   /* real time stamp, time of read() */
    timestruc_t pr_create;   /* process/lwp creation time stamp */
    timestruc_t pr_term;     /* process/lwp termination time stamp */
    timestruc_t pr_rtime;    /* total lwp real (elapsed) time */
    timestruc_t pr_utime;    /* user level CPU time */
    timestruc_t pr_stime;    /* system call CPU time */
    timestruc_t pr_ttime;    /* other system trap CPU time */
    timestruc_t pr_tftime;   /* text page fault sleep time */
    timestruc_t pr_dftime;   /* data page fault sleep time */
    timestruc_t pr_kftime;   /* kernel page fault sleep time */
    timestruc_t pr_ltime;    /* user lock wait sleep time */
    timestruc_t pr_slptime;  /* all other sleep time */
    timestruc_t pr_wtime;    /* wait-cpu (latency) time */
    timestruc_t pr_stoptime; /* stopped time */
    ...;                     /* filler for future expansion */
    ulong_t pr_minf;         /* minor page faults */
    ulong_t pr_majf;         /* major page faults */
    ulong_t pr_nswap;        /* swaps */
    ulong_t pr_inblk;        /* input blocks */
    ulong_t pr_oublk;        /* output blocks */
    ulong_t pr_msnd;         /* messages sent */
    ulong_t pr_mrcv;         /* messages received */
    ulong_t pr_sigs;         /* signals received */
    ulong_t pr_vctx;         /* voluntary context switches */
    ulong_t pr_ictx;         /* involuntary context switches */
    ulong_t pr_sysc;         /* system calls */
    ulong_t pr_ioch;         /* chars read and written */
    ...;                     /* filler for future expansion */
} prusage_t;

typedef struct prcred {
    uid_t pr_euid;          /* effective user id */
    uid_t pr_ruid;          /* real user id */
    uid_t pr_suid;          /* saved user id (from exec) */
    gid_t pr_egid;          /* effective group id */
    gid_t pr_rgid;          /* real group id */
    gid_t pr_sgid;          /* saved group id (from exec) */
    /*int pr_ngroups;*/     /* number of supplementary groups */
    /*gid_t pr_groups[1];*/ /* array of supplementary groups */
    ...;
} prcred_t;
"""


MACROS = """
#define SSLEEP ...
#define SRUN ...
#define SZOMB ...
#define SSTOP ...
#define SIDL ...
#define SONPROC ...
#define SWAIT ...

#define PR_MODEL_ILP32 ...
#define PR_MODEL_LP64 ...
"""

FUNCTIONS = """
"""

# This gets prepended to the generated `ffi.verify()` contents.
VERIFY_PREAMLE = """
/* We do not want to use the large file compilation environment as <procfs.h>
 * doesn't play nice with that on ILP32 (32-bit machines), the transitional
 * environment is fine however.  See the lfcompile(5) and lfcompile64(5)
 * manpages for details. */
#undef _FILE_OFFSET_BITS
"""


VERIFY_EXTRA = """
"""
