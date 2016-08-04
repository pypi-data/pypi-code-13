#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import posixpath
from faff import (Variable, FileTarget, RuleTarget, Rule, Run)

# ABI, architecture targets.
TARGETS = (
    ("arm-none-eabi", "cortex-m4", "debug"),
    ("arm-none-eabi", "cortex-m4", "release"),
)

# Commands.
Variable("AR", "{ABI}-ar")
Variable("CC", "{ABI}-gcc")
Variable("CP", "cp -rf")

# Compiler flags.
CFLAGS = Variable("CFLAGS")
CFLAGS += "-mthumb"
CFLAGS += "{OPTIMF}"
CFLAGS += "-mcpu={ARCH}"
CFLAGS += "-g3"
CFLAGS += "-ggdb"
CFLAGS += "-fomit-frame-pointer"
CFLAGS += "-Wall"
CFLAGS += "-Wstrict-prototypes"
CFLAGS += "-Wshadow"
CFLAGS += "-Wcast-align"
CFLAGS += "-Wcast-qual"
CFLAGS += "-D_GNU_SOURCE"
CFLAGS += "-I."
CFLAGS += "-I{INC}"
# TODO: Header dependency handling?
# CFLAGS += "-MT {_D} -MMD -MP -MF {_T}.d"

# Target definitions.
FSRC = (
    ("exceptions.c",),

    ("syst", "systConfig.c"),
)
SRC = [FileTarget("{ROOT}", *x) for x in FSRC]
OBJ = [FileTarget("{BUILD}", "{ABI}", "{ARCH}", "{OPTIM}", *x, ext=".o") for x in FSRC]

# Libary name.
Variable("NAME", "cm4")
# Library archive.
LIB = FileTarget("{BUILD}", "lib{NAME}.{ABI}.{ARCH}.{OPTIM}.a")
# Library header.
HDR = FileTarget("{ROOT}", "{NAME}.h")


def set_target_vars(abi, arch, optim):
    Variable("ABI", abi)
    Variable("ARCH", arch)
    Variable("OPTIM", optim)
    if optim in ("release",):
        Variable("OPTIMF", "-Os")
    else:
        Variable("OPTIMF", "-Og")


@Rule([LIB, RuleTarget(lib_compile)])
def lib_archive(target, depends, args):
    Variable("LST", str(LST))
    Run("{ABI}-ar rs {_T} @{LST}", root)


@Rule()
def all(target, depends, args):
    for abi, arch, optim in TARGETS:
        set_target_vars(abi, arch, optim)
        lib_archive()


@Rule()
def clean(target, depends, args):
    Run("rm -rf {BUILD}", root)


@Rule(depends=RuleTarget(all))
def install(target, depends, args):
    for abi, arch, optim in TARGETS:
        set_target_vars(abi, arch, optim)
        LIB.copy("{LIB}", "{ABI}", "{ARCH}", "lib{NAME}-{OPTIM}.a")
        HDR.copy("{INC}")


# Compiler flags.
CFLAGS = Variable("CFLAGS")
CFLAGS += "-mthumb"
CFLAGS += "-I."
CFLAGS += "-Iinclude"
# TODO: Header dependency handling?
# CFLAGS += "-MT {_D} -MMD -MP -MF {_T}.d"


# Libary name.
Variable("NAME", "emwin")
# Library archive.
LIB = FileTarget("{BUILD}", "lib{NAME}.{ABI}.{ARCH}.{OPTIM}.a")
# Library headers.
FHDR = (
    ("include", "BUTTON.h"),
    ("include", "WM_Intern.h"),
)
HDR = [FileTarget("{ROOT}", *x) for x in FHDR]


def set_target_vars(abi, arch, optim):
    Variable("ABI", abi)
    Variable("ARCH", arch)
    Variable("OPTIM", optim)
    if optim in ("release",):
        Variable("OPTIMF", "-Os")
    else:
        Variable("OPTIMF", "-Og")


@Rule([LIB, RuleTarget(lib_compile)])
def lib_archive(target, depends, args):
    Variable("LST", str(LST))
    Run("{ABI}-ar rs {_T} @{LST}", root)


@Rule()
def all(target, depends, args):
    for abi, arch, optim in TARGETS:
        set_target_vars(abi, arch, optim)
        lib_archive()


@Rule()
def clean(target, depends, args):
    Run("rm -rf {BUILD}", root)


@Rule(depends=RuleTarget(all))
def install(target, depends, args):
    for abi, arch, optim in TARGETS:
        set_target_vars(abi, arch, optim)
        LIB.copy("{LIB}", "{ABI}", "{ARCH}", "lib{NAME}-{OPTIM}.a")
        for hdr in HDR:
            hdr.copy("{INC}", "{NAME}")
