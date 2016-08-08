#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
import sys
import datetime

from itertools import groupby

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class RemoveBackups:

    def __init__(self, PATH_TO_BACKUPS, MASK):
        total = 0
        remain = 0
        for root, dirs, files in os.walk(PATH_TO_BACKUPS):
            newarr = [(re.search(MASK, item).groups(), item)
                      for item in files if re.search(MASK, item)]
            newarr.sort()
            total += len(newarr)
            self.today = datetime.date.today()
            self.ignore = []
            result = self.group(newarr)
            if result:
                self.addFull(result)
                self.ignore.sort()
                self.removeFiles(files, root)
                remain += len(self.ignore)
        print bcolors.HEADER + 'Total: %d' % total + bcolors.ENDC
        print bcolors.HEADER + 'Remain: %d' % remain + bcolors.ENDC

    def group(self, newarr):
        """ Группируем результаты следующий образом {'тип': {'год': {'месяц': ['список результатов']}}} """
        result = {}
        for item, group in groupby(newarr, lambda x: x[0][0]):
            result[item] = {}
            for item2, group2 in groupby(list(group), lambda x: x[0][1]):
                result[item][item2] = []
                for item3 in enumerate(group2):
                    result[item][item2].append(item3[1][1])
        return result

    def addFull(self, result):
        """ Добавляем список игнорируемых бэкапов для full """
        for year in result:
            if year == str(self.today.year):
                for month in result[year]:
                    if int(month) == self.today.month:
                        self.ignore += result[year][month]
                    else:
                        self.ignore.append(result[year][month][0])
            else:
                for month in result[year]:
                    self.ignore.append(result[year][month][0])
                    break

    def removeFiles(self, files, root):
        """ Удаляем файлы """
        for fn in files:
            if fn not in self.ignore:
                os.remove(os.path.join(root, fn))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print bcolors.FAIL + 'Enter PATH_TO_BACKUPS and MASK(for re module.)' + bcolors.ENDC
    else:
        RemoveBackups(sys.argv[1], sys.argv[2])
