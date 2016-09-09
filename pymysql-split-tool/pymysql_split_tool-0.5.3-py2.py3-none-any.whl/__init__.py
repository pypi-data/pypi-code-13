import input
import pymysql_split_tool

__version__ = '0.5.3'

def init(action, task, debug=False):
    input.init(action, task, debug)

def init_by_cmd_line_args():
    input.init_by_cmd_line_args()

def do_work():
    pymysql_split_tool.do_work()


if __name__ == '__main__':
    init_by_cmd_line_args()
    do_work()