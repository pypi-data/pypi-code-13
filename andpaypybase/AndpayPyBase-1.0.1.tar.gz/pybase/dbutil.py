import  cx_Oracle
import os
import json
import mysql.connector


#oracle数据连接
def connectOracle(config):

    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

    dsn = "%s:%s/%s" % (config["host"], config["port"], config["sid"])
    conn = cx_Oracle.connect(config["user"],config["pwd"], dsn);
    return conn


def connectMysql(config):

    cnx = mysql.connector.connect(user=config["user"], password=config["pwd"],
                                  host=config["host"],port=config["port"],
                                  database=config["dbName"])


    return cnx;

def __loadConfig(dialect="Oracle"):
    userHome = os.path.expanduser("~")
    pyconfigPath = userHome + os.path.sep + ".py_config"

    configName = None
    if dialect == "Oracle":
        configName = "oracle.json"
    elif dialect == "MySql":
        configName = "mysql.json"
    config = json.load(open(pyconfigPath + os.path.sep + configName))
    return config


def connectDb(dialect="Oracle"):

    supportDialect = ["Oracle","MySql"]
    if dialect not in supportDialect:
        raise Exception("not support dialect="+dialect)

    config = __loadConfig(dialect)

    if dialect == "Oracle":
        return connectOracle(config)
    elif dialect == "MySql":
        return connectMysql(config)

    return None


if __name__ == "__main__":
    connectDb(dialect="MySql")
    connectDb()