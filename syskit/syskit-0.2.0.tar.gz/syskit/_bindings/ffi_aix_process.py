# -*- coding: utf-8 -*-

from __future__ import (absolute_import,
                        unicode_literals, print_function, division)


INCLUDES = """
#include <alloca.h>
#include <procinfo.h>
#include <sys/types.h>
#include <sys/proc.h>
#include <sys/procfs.h>
#include <sys/cred.h>
#include <sys/resource.h>
"""


LIBS = []


INT_TYPEDEFS = {
    'pid32_t': 'int32_t',
    'uid_t': 'unsigned long',
    'gid_t': 'unsigned long',
    'dev64_t': 'uint64_t',
    'uint': 'unsigned int',
    'longlong_t': 'long long',
    'time64_t': 'int64_t',
}


STRUCTS = """
typedef struct psinfo
{
    ...;
  /*uint32_t pr_flag;*/            /* process flags from proc struct p_flag */
  /*uint32_t pr_flag2;*/           /* process flags from proc struct p_flag2 */
  /*uint32_t pr_nlwp;*/            /* number of threads in process */
  /*uint32_t pr__pad1;*/           /* reserved for future use */
  /*uint64_t pr_uid;*/             /* real user id */
  /*uint64_t pr_euid;*/            /* effective user id */
  /*uint64_t pr_gid;*/             /* real group id */
  /*uint64_t pr_egid;*/            /* effective group id */
    uint64_t pr_pid;               /* unique process id */
    ...;
  /*uint64_t pr_ppid;*/            /* process id of parent */
  /*uint64_t pr_pgid;*/            /* pid of process group leader */
  /*uint64_t pr_sid;*/             /* session id */
  /*uint64_t pr_ttydev;*/          /* controlling tty device */
  /*prptr64_t   pr_addr;*/         /* internal address of proc struct */
  /*uint64_t pr_size;*/            /* process image size in KB (1024) units */
  /*uint64_t pr_rssize;*/          /* resident set size in KB (1024) units */
  /*pr_timestruc64_t pr_start;*/   /* process start time, time since epoch */
  /*pr_timestruc64_t pr_time;*/    /* usr+sys cpu time for this process */
  /*uint32_t pr__pad2;*/           /* reserved for future use */
  /*uint32_t pr_argc;*/            /* initial argument count */
  /*prptr64_t   pr_argv;*/         /* address of initial argument vector in
                                    * user process */
  /*prptr64_t   pr_envp;*/         /* address of initial environment vector
                                    * in user process */
    char     pr_fname[...];        /* last component of exec()ed pathname*/
    char     pr_psargs[...];       /* initial chars of arg list [PRARGSZ] */
    ...;
  /*uint64_t pr__pad[8];*/         /* reserved for future use */
  /*struct   lwpsinfo pr_lwp;*/    /* "representative" thread info */
} psinfo_t;

typedef struct ucred_ext {

    /* User ID values */
    uid_t   crx_ruid;           /* real user id */
    uid_t   crx_uid;            /* effective user id */
    uid_t   crx_suid;           /* saved user id */
    uid_t   crx_luid;           /* login user id */
    uid_t   crx_acctid;         /* accounting id */

    /* Group ID values */
    gid_t   crx_gid;            /* effective group id */
    gid_t   crx_rgid;           /* real group id */
    gid_t   crx_sgid;           /* saved group id */

    ...;
} cred_ext_t;

struct timeval64 {
    int64_t tv_sec;              /* 64bit time_t value */
    int32_t tv_usec;
    ...;
};

struct	trusage64
{
    struct timeval64 ru_utime;    /* user time used */
    struct timeval64 ru_stime;    /* system time used */
    ...;
  /*longlong_t   ru_maxrss;*/
  /*longlong_t   ru_ixrss;*/      /* integral shared memory size */
  /*longlong_t   ru_idrss;*/      /* integral unshared data " */
  /*longlong_t   ru_isrss;*/      /* integral unshared stack " */
  /*longlong_t   ru_minflt;*/     /* page reclaims */
  /*longlong_t   ru_majflt;*/     /* page faults */
  /*longlong_t   ru_nswap;*/      /* swaps */
  /*longlong_t   ru_inblock;*/    /* block input operations */
  /*longlong_t   ru_oublock;*/    /* block output operations */
  /*longlong_t   ru_msgsnd;*/     /* messages sent */
  /*longlong_t   ru_msgrcv;*/     /* messages received */
  /*longlong_t   ru_nsignals;*/   /* signals received */
  /*longlong_t   ru_nvcsw;*/      /* voluntary context switches */
  /*longlong_t   ru_nivcsw;*/     /* involuntary " */
};

struct procentry64
{
    /* identification/authentication */
    pid32_t         pi_pid;             /* process ID */
    pid32_t         pi_ppid;            /* parent process ID */
    pid32_t         pi_sid;             /* session identifier */
    pid32_t         pi_pgrp;            /* process group */
    uid_t           pi_uid;             /* real user ID */
    uid_t           pi_suid;            /* saved user ID */

    /* controlling tty info */
    pid32_t         pi_ttyp;            /* has a controlling terminal */
    ...;
  /*uint            pi_pad0;*/          /* alignment padding */
    dev64_t         pi_ttyd;            /* controlling terminal */
    ...;
  /*longlong_t      pi_ttympx;*/        /*      "         "     channel */

    /* scheduler information */
    uint            pi_nice;            /* nice for priority */
    uint            pi_state;           /* process state -- from proc.h */
    ...;
  /*uint            pi_flags;*/         /* process flags -- from proc.h */
  /*uint            pi_flags2;*/        /* process flags ext -- from proc.h */
    uint            pi_thcount;         /* thread count */
   ...;
  /*uint            pi_cpu;*/           /* first thread's tick count */
    uint            pi_pri;             /* first thread's priority */

    /* file management */
    ...;
  /*uint            pi_maxofile;*/      /* maximum u_ofile index in use */
  /*u_longlong_t    pi_cdir;*/          /* current directory of process */
  /*u_longlong_t    pi_rdir;*/          /* root directory of process */
  /*short           pi_cmask;*/         /* mask for file creation */
  /*short           pi_pad1;*/          /* alignment padding */

    /* program name */
    char            pi_comm[...];       /* (truncated) program name */

    /* memory */
    ...;
  /*u_longlong_t    pi_adspace;*/         /* process address space */
    longlong_t      pi_majflt;          /* i/o page faults */
    longlong_t      pi_minflt;          /* non i/o page faults */
    longlong_t      pi_repage;          /* repaging count */
    ...;
  /*longlong_t      pi_size;*/            /* size of image (pages) */

    /* valid when the process is a zombie only */
    time64_t        pi_utime;           /* this process user time */
    time64_t        pi_stime;           /* this process system time */

    /* credentials information */
    cred_ext_t      pi_cred;

    /* accounting and profiling data */
    struct trusage64 pi_ru;             /* this process' rusage info */
    ...;
  /*struct trusage64 pi_cru;*/          /* children's rusage info */
  /*longlong_t      pi_ioch;*/          /* I/O character count  */
  /*longlong_t      pi_irss;*/          /* accumulator for memory integral */
    time64_t        pi_start;           /* time at which process began */

    /* resource limits info */
    ...;
  /*struct rlimit64 pi_rlimit[RLIM_NLIMITS];*/    /* resource limits */

    /* memory usage info */
    ...;
    u_longlong_t    pi_drss;            /* data resident set size */
    u_longlong_t    pi_trss;            /* text resident set size */
    u_longlong_t    pi_dvm;             /* data virtual memory size */
    u_longlong_t    pi_prm;             /* percent real memory usage */
    u_longlong_t    pi_tsize;           /* size of text */
    u_longlong_t    pi_dsize;           /* current break value */
    u_longlong_t    pi_sdsize;          /* data size from shared library*/

    /* signal management */
    ...;
  /*u_longlong_t    pi_signal[NSIG64];*/  /* disposition of sigs */
  /*uint            pi_sigflags[NSIG64];*//* sig action flags */
  /*sigset64_t      pi_sig;*/             /* pending sigs */


    /* WLM information. 34+31=65 bytes, padded to 72 */
    ...;
  /*char            pi_classname[2*(WLM_CLASSNAME_LENGTH+1)];*/
  /*char            pi_tag[WLM_TAG_LENGTH+1];*/

    /* pagesize information */
    ...;
    char            pi_data_l2psize;     /* log2 of a proc's data pg sz */
    char            pi_text_l2psize;     /* log2 of a proc's text pg sz */
    char            pi_stack_l2psize;    /* log2 of a proc's stack pg sz */

  /*char            pi_pad4[4];*/

  /*suseconds_t     pi_chk_utime;*/      /* user time at checkpoint  */
  /*suseconds_t     pi_chk_ctime;*/      /* child time at checkpoint  */

    /* other scheduler information */
    ...;
  /*uint            pi_policy;*/         /* process policy */
    uint            pi_ppri;             /* process priority */

    /* loader segment for 64bit process */
    ...;
  /*u_longlong_t    pi_adspace_ldr;*/
};

struct fdsinfo64 { ...; };
"""


MACROS = """
#define SNONE ...
#define SIDL ...
#define SZOMB ...
#define SSTOP ...
#define SACTIVE ...
#define SSWAP ...
"""


FUNCTIONS = """
int getprocs64(struct procentry64 *ProcessBuffer, int ProcessSize,
               struct fdsinfo64 *FileBuffer, int FileSize,
               long *IndexPointer, int Count);
int getargs(struct procentry64 *processBuffer, int bufferLen,
            char *argsBuffer, int argsLen);
int getevars(struct procentry64 *processBuffer, int bufferLen,
             char *argsBuffer, int argsLen);
"""


VERIFY_PREAMLE = """
"""


VERIFY_EXTRA = """
"""
