#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yuki Furuta <furushchev@jsk.imi.i.u-tokyo.ac.jp>

from __future__ import print_function
import cmakelists_parsing.parsing as cmake
from colorama import Fore as ANSI
from colorama import Style
from lxml import etree
import os
import pkgutil
import re
import subprocess
import tempfile
import traceback

try:
    input = raw_input
except NameError:
    pass

def error(s):
    print(Style.BRIGHT, ANSI.RED, s, ANSI.RESET, Style.NORMAL)
def warn(s):
    print(Style.BRIGHT, ANSI.MAGENTA, s, ANSI.RESET, Style.NORMAL)
def info(s):
    print(Style.BRIGHT, ANSI.GREEN, s, ANSI.RESET, Style.NORMAL)

def ask_yn(query):
    while True:
        ans = input(Style.BRIGHT + ANSI.GREEN + query + " [y/n]: " + ANSI.RESET + Style.NORMAL)
        if ans == "y" or ans == "Y":
            return True
        elif ans == "n" or ans == "N":
            return False
        else:
            warn("Please answer y or n!")

def update_with_diff(src_path, updated):
    with tempfile.NamedTemporaryFile() as tf:
        tf.write(updated)
        tf.flush()
        try:
            diff = subprocess.check_output(["cdiff", src_path, tf.name])
        except subprocess.CalledProcessError as e:
            if e.returncode == 1 and e.output is not None:
                diff = e.output
            else:
                raise e
        if len(diff) == 0:
            info("Your package.xml is already clean!")
            return True
        print(diff)
        if ask_yn("Does this looks good?"):
            info("Overriding " + src_path)
            with open(src_path, "w") as f:
                f.write(updated)
            return True
        else:
            error("Aborting...")
            return False

def cmake_to_package():
    cmake_path = os.path.join(os.getcwd(), "CMakeLists.txt")
    with open(cmake_path, "r") as f:
        cmake_file = cmake.parse(f.read())
    cmake_pkgs = set()
    for elem in cmake_file:
        try:
            name = elem.name
            if name != "find_package":
                continue
            find_pkg_args = elem.body
        except:
            continue
        if len(find_pkg_args) == 0 or find_pkg_args[0].contents != "catkin":
            continue
        cmake_pkgs = set([arg.contents for arg in find_pkg_args][1:])
        if "REQUIRED" in cmake_pkgs: cmake_pkgs.remove("REQUIRED")
        if "COMPONENTS" in cmake_pkgs: cmake_pkgs.remove("COMPONENTS")
        break
    if len(cmake_pkgs) == 0:
        error("no package is defined in CMakeLists.txt")
        return False

    xml_path = os.path.join(os.getcwd(), "package.xml")
    doc = etree.parse(xml_path)
    xml_pkgs = set([e.text for e in doc.findall("build_depend")])
    info("Checking package.xml -> CMakeLists.txt")
    diff_pkgs = xml_pkgs - cmake_pkgs
    if len(diff_pkgs) > 0:
        warn("some build dependencies are missed in CMakeLists.txt:")
        for pkg in sorted(list(diff_pkgs)):
            warn("  " + pkg)
    else:
        info("All packages defined in package.xml are also defined in CMakeLists.txt")
    info("Checking CMakeLists.txt -> package.xml")
    diff_pkgs = cmake_pkgs - xml_pkgs
    if len(diff_pkgs) == 0:
        info("All packages defined in CMakeLists.txt are also defined in package.xml")
        return True
    warn("following packages are not defined in package.xml:")
    for p in list(diff_pkgs):
        warn(" - " + p)
    if ask_yn("Append them to package.xml?"):
        for pkg in list(diff_pkgs):
            e = etree.Element("build_depend")
            e.text = pkg
            doc.getroot().append(e)
        xml = etree.tostring(doc, pretty_print=True)
        return update_with_diff(xml_path, xml)
    else:
        return False

def sort_package_xml():
    xml_path = os.path.join(os.getcwd(), "package.xml")
    tree = etree.parse(xml_path)
    xsl = pkgutil.get_data("catechin", "data/package.xsl")
    transform = etree.XSLT(etree.XML(xsl))
    transformed = transform(tree)
    xml = etree.tostring(transformed, pretty_print=True)
    return update_with_diff(xml_path, xml)

def main(args=None):
    try:
        cmake_to_package()
        sort_package_xml()
        return True
    except Exception as e:
        error("Error: " + str(e))
        print(Style.BRIGHT, ANSI.YELLOW, traceback.format_exc(), ANSI.RESET, Style.NORMAL)
        return False
