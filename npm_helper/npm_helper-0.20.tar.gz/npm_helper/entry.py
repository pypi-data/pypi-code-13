#!usr/bin/env python
"""

Usage:
    pnpm [-s | -d] <keywords>

Options:
    -h --help  显示帮助菜单
    -keywords  关键字
    # -s         按star数排序
    # -d         按下载量排序

Examples:
    pnpm lazyloading
    pnpm jquery-lazyloading
"""
from docopt import docopt
from npm_helper import BASE_URL, TABLE_HEADER, TABLE_ROW
from prettytable import PrettyTable
from threads_creator.entry import ThreadCreator
from threads_creator.utils import message
from threads_creator.config import config_creator
from .spiders.spider_list import NpmSearchSpider
from .spiders.spider_page import NpmPageSpider
from .data import database_creator

npm_helper = None


def npm_helper_creator():
    global npm_helper
    if npm_helper is None:
        config_threads()
        database = database_creator()
        npm_helper = NpmHelper()
        database.attach_observer(npm_helper)
        npm_helper.print_row()
        npm_helper.urls_generation()
    return npm_helper


def config_threads():
    config = config_creator()
    config.debug = 0


class NpmHelper(object):
    def __init__(self):
        arguments = docopt(__doc__, version="beta 0.1")
        keywords = arguments['<keywords>'].split('-')
        self.keywords = keywords

    def urls_generation(self):
        keywords = self.keywords
        try:
            assert type(keywords) is list
            urls = [BASE_URL.format(query='+'.join(keywords), page=i) for i in range(1, 2)]
            NpmHelper.thread_generation(urls)
        except AssertionError:
            message.error_message('except to receive a list')

    @staticmethod
    def thread_generation(urls):
        threads = ThreadCreator(main_spider=NpmSearchSpider, branch_spider=NpmPageSpider)
        threads.get_entry_urls(urls)
        threads.finish_all_threads()

    @staticmethod
    def print_header(row=None):
        row = TABLE_HEADER if row is None else row
        npm_table = PrettyTable(row)
        print(npm_table)

    @staticmethod
    def print_row(row=None):
        row = TABLE_HEADER if row is None else row
        npm_table = PrettyTable()
        npm_table.add_row(row)
        print(npm_table)

    # @staticmethod
    # def print_table():
    #     database = database_creator()
    #     npm_table = PrettyTable(TABLE_HEADER)
    #     for index, package in enumerate(database.data):
    #         package["index"] = index
    #         package_row = [package[item] for item in TABLE_ROW]
    #         npm_table.add_row(package_row)
    #     print(npm_table)

    @staticmethod
    def update(data):
        print(data)
        package_row = [data[item] for item in TABLE_ROW]
        NpmHelper.print_row(package_row)

