
# coding=utf-8

from csf.util import get_dataframe as __get_dataframe, format_param as __format_param, return_format as __return_format
from datetime import datetime


def get_stock_hist_bar(code, freq="d", start_date=None, end_date=None, adjusted="f", field=None):
    """获取股票历史时间段K线数据

    Parameters
    ----------
    code:str
        股票代码（600001） ，仅支持单个股票代码
    freq:str,default "d"
        数据周期，日：'d'
    start_date:str,default None
        开始日期，格式:"2015-01-10"
    end_date:str,default None
        结束日期，格式:"2015-12-31"
    adjusted:str,default "f"
        复权选项, 前复权：'f'，不复权：'n'
    field:list,default None
        选择返回字段，见下表可选返回字段

    Returns
    -------
    date:str 日期
    open:str 开盘价
    high:str 最高价
    low:str 最低价
    close :str 收盘价
    volume:str 成交量（手数）
    amount:str 成交金额（万）
    turnover:str 换手率

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_stock_hist_bar(code="000001")
    """
    params = dict()

    if not isinstance(code, tuple([str])):
        raise TypeError("get_stock_hist_bar() arg code must be a str type")
    params["codes"] = __format_param("code", code)

    if not isinstance(freq, tuple([str])):
        raise TypeError("get_stock_hist_bar() arg freq must be a str type")
    params["freq"] = __format_param("freq", freq)

    if not isinstance(start_date, tuple([str])) and start_date is not None:
        raise TypeError("get_stock_hist_bar() arg start_date must be a str type")
    params["from"] = __format_param("start_date", start_date)

    if not isinstance(end_date, tuple([str])) and end_date is not None:
        raise TypeError("get_stock_hist_bar() arg end_date must be a str type")
    params["to"] = __format_param("end_date", end_date)

    if not isinstance(adjusted, tuple([str])):
        raise TypeError("get_stock_hist_bar() arg adjusted must be a str type")
    params["adjusted"] = __format_param("adjusted", adjusted)

    if not isinstance(field, tuple([list])) and field is not None:
        raise TypeError("get_stock_hist_bar() arg field must be a list type")
    params["field"] = __format_param("field", field)

    index = None
    renames = dict()
    ret_fields = list()
    renames["dt"] = "date"
    index = "date"
    ret_fields.append("date".strip())
    ret_fields.append("open".strip())
    ret_fields.append("high".strip())
    ret_fields.append("low".strip())
    ret_fields.append("close ".strip())
    renames["vol"] = "volume"
    ret_fields.append("volume".strip())
    ret_fields.append("amount".strip())
    ret_fields.append("turnover".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/hq/stock/price", params)
    return __return_format(dfs, field=field, renames=renames, ret_fields=ret_fields, index=index)


def get_stock_last_n_bar(code, date, freq="d", n=30, adjusted="f", field=None):
    """获取股票指定时间最后N根K线数据

    Parameters
    ----------
    code:str
        股票代码（600001） ，仅支持单个股票代码
    date:str
        日期，格式:"2015-01-10"
    freq:str,default "d"
        数据周期，日：'d'
    n:int,default 30
        返回K线的数量
    adjusted:str,default "f"
        复权选项, 前复权：'f'，不复权：'n'
    field:list,default None
        选择返回字段，见下表可选返回字段

    Returns
    -------
    date:str 日期
    open:str 开盘价
    high:str 最高价
    low:str 最低价
    close :str 收盘价
    volume:str 成交量（手数）
    amount:str 成交金额（万）
    turnover:str 换手率

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_stock_last_n_bar(code="000001",date="2016-07-06")
    """
    params = dict()

    if not isinstance(code, tuple([str])):
        raise TypeError("get_stock_last_n_bar() arg code must be a str type")
    params["codes"] = __format_param("code", code)

    if not isinstance(date, tuple([str])):
        raise TypeError("get_stock_last_n_bar() arg date must be a str type")
    params["dt"] = __format_param("date", date)

    if not isinstance(freq, tuple([str])):
        raise TypeError("get_stock_last_n_bar() arg freq must be a str type")
    params["freq"] = __format_param("freq", freq)

    if not isinstance(n, tuple([int])):
        raise TypeError("get_stock_last_n_bar() arg n must be a int type")
    params["limit"] = __format_param("n", n)

    if not isinstance(adjusted, tuple([str])):
        raise TypeError("get_stock_last_n_bar() arg adjusted must be a str type")
    params["adjusted"] = __format_param("adjusted", adjusted)

    if not isinstance(field, tuple([list])) and field is not None:
        raise TypeError("get_stock_last_n_bar() arg field must be a list type")
    params["field"] = __format_param("field", field)

    index = None
    renames = dict()
    ret_fields = list()
    renames["dt"] = "date"
    index = "date"
    ret_fields.append("date".strip())
    ret_fields.append("open".strip())
    ret_fields.append("high".strip())
    ret_fields.append("low".strip())
    ret_fields.append("close ".strip())
    renames["vol"] = "volume"
    ret_fields.append("volume".strip())
    ret_fields.append("amount".strip())
    ret_fields.append("turnover".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/hq/stock/price/latest", params)
    return __return_format(dfs, field=field, renames=renames, ret_fields=ret_fields, index=index)


def get_index_com_bar(index_code, date, freq="d", field=None):
    """获取常用指数成份股历史K线数据

    Parameters
    ----------
    index_code:str
        指数代码（000300），只可输入一个指数代码
    date:str
        查询日期，格式:"2015-01-10"
    freq:str,default "d"
        数据周期，日：'d'
    field:list,default None
        选择返回字段，见下表可选返回字段

    Returns
    -------
    code:str 股票代码
    date:str 日期
    open:str 开盘价
    high:str 最高价
    low:str 最低价
    close :str 收盘价
    volume:str 成交量（手数）

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_index_com_bar(index_code="000300",date="2016-04-08")
    """
    params = dict()

    if not isinstance(index_code, tuple([str])):
        raise TypeError("get_index_com_bar() arg index_code must be a str type")
    params["index_code"] = __format_param("index_code", index_code)

    if not isinstance(date, tuple([str])):
        raise TypeError("get_index_com_bar() arg date must be a str type")
    params["dt"] = __format_param("date", date)

    if not isinstance(freq, tuple([str])):
        raise TypeError("get_index_com_bar() arg freq must be a str type")
    params["freq"] = __format_param("freq", freq)

    if not isinstance(field, tuple([list])) and field is not None:
        raise TypeError("get_index_com_bar() arg field must be a list type")
    params["field"] = __format_param("field", field)

    index = None
    renames = dict()
    ret_fields = list()
    renames["tick"] = "code"
    ret_fields.append("code".strip())
    renames["dt"] = "date"
    index = "date"
    ret_fields.append("date".strip())
    ret_fields.append("open".strip())
    ret_fields.append("high".strip())
    ret_fields.append("low".strip())
    ret_fields.append("close ".strip())
    renames["vol"] = "volume"
    ret_fields.append("volume".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/hq/index/stock/price", params)
    return __return_format(dfs, field=field, renames=renames, ret_fields=ret_fields, index=index)


def get_index_hist_bar(index_code, freq="d", start_date=None, end_date=None, adjusted="f", field=None):
    """获取常用指数历史时间段K线数据

    Parameters
    ----------
    index_code:str
        指数代码（000300） ，仅支持单个指数代码
    freq:str,default "d"
        数据周期，日：'d'
    start_date:str,default None
        开始日期，格式:"2015-01-10"
    end_date:str,default None
        结束日期，格式:"2015-12-31"
    adjusted:str,default "f"
        复权选项, 前复权：'f'，不复权：'n'
    field:list,default None
        选择返回字段，见下表可选返回字段

    Returns
    -------
    code:str 股票代码
    date:str 日期
    open:str 开盘价
    high:str 最高价
    low:str 最低价
    close :str 收盘价
    volume:str 成交量（手数）

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_index_hist_bar(index_code="000300")
    """
    params = dict()

    if not isinstance(index_code, tuple([str])):
        raise TypeError("get_index_hist_bar() arg index_code must be a str type")
    params["codes"] = __format_param("index_code", index_code)

    if not isinstance(freq, tuple([str])):
        raise TypeError("get_index_hist_bar() arg freq must be a str type")
    params["freq"] = __format_param("freq", freq)

    if not isinstance(start_date, tuple([str])) and start_date is not None:
        raise TypeError("get_index_hist_bar() arg start_date must be a str type")
    params["from"] = __format_param("start_date", start_date)

    if not isinstance(end_date, tuple([str])) and end_date is not None:
        raise TypeError("get_index_hist_bar() arg end_date must be a str type")
    params["to"] = __format_param("end_date", end_date)

    if not isinstance(adjusted, tuple([str])):
        raise TypeError("get_index_hist_bar() arg adjusted must be a str type")
    params["adjusted"] = __format_param("adjusted", adjusted)

    if not isinstance(field, tuple([list])) and field is not None:
        raise TypeError("get_index_hist_bar() arg field must be a list type")
    params["field"] = __format_param("field", field)

    index = None
    renames = dict()
    ret_fields = list()
    renames["tick"] = "code"
    ret_fields.append("code".strip())
    renames["dt"] = "date"
    index = "date"
    ret_fields.append("date".strip())
    ret_fields.append("open".strip())
    ret_fields.append("high".strip())
    ret_fields.append("low".strip())
    ret_fields.append("close ".strip())
    renames["vol"] = "volume"
    ret_fields.append("volume".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/hq/index/price", params)
    return __return_format(dfs, field=field, renames=renames, ret_fields=ret_fields, index=index)


def get_index_last_n_bar(index_code, date, freq="d", n=30, field=None):
    """获取常用指数指定时间最后N根K线数据

    Parameters
    ----------
    index_code:str
        指数代码（000300） ，仅支持单个指数代码
    date:str
        日期，格式:"2015-01-10"
    freq:str,default "d"
        数据周期，日：'d'
    n:int,default 30
        返回K线的数量
    field:list,default None
        选择返回字段，见下表可选返回字段

    Returns
    -------
    code:str 股票代码
    date:str 日期
    open:str 开盘价
    high:str 最高价
    low:str 最低价
    close :str 收盘价
    volume:str 成交量（手数）

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_index_last_n_bar(index_code="000300",date="2016-07-06")
    """
    params = dict()

    if not isinstance(index_code, tuple([str])):
        raise TypeError("get_index_last_n_bar() arg index_code must be a str type")
    params["codes"] = __format_param("index_code", index_code)

    if not isinstance(date, tuple([str])):
        raise TypeError("get_index_last_n_bar() arg date must be a str type")
    params["dt"] = __format_param("date", date)

    if not isinstance(freq, tuple([str])):
        raise TypeError("get_index_last_n_bar() arg freq must be a str type")
    params["freq"] = __format_param("freq", freq)

    if not isinstance(n, tuple([int])):
        raise TypeError("get_index_last_n_bar() arg n must be a int type")
    params["limit"] = __format_param("n", n)

    if not isinstance(field, tuple([list])) and field is not None:
        raise TypeError("get_index_last_n_bar() arg field must be a list type")
    params["field"] = __format_param("field", field)

    index = None
    renames = dict()
    ret_fields = list()
    renames["tick"] = "code"
    ret_fields.append("code".strip())
    renames["dt"] = "date"
    index = "date"
    ret_fields.append("date".strip())
    ret_fields.append("open".strip())
    ret_fields.append("high".strip())
    ret_fields.append("low".strip())
    ret_fields.append("close ".strip())
    renames["vol"] = "volume"
    ret_fields.append("volume".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/hq/index/price/latest", params)
    return __return_format(dfs, field=field, renames=renames, ret_fields=ret_fields, index=index)


def get_stock_sus_info(code=None):
    """获取股票停复牌信息

    Parameters
    ----------
    code:str,default None
        股票代码，仅支持单个股票代码

    Returns
    -------
    code:str 股票代码
    secu_name:str 股票简称
    suspend_date:str 停牌日期
    resume_date:str 复牌日期

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_stock_sus_info(code="000948")
    """
    params = dict()

    if not isinstance(code, tuple([str])) and code is not None:
        raise TypeError("get_stock_sus_info() arg code must be a str type")
    params["code"] = __format_param("code", code)

    index = None
    renames = dict()
    ret_fields = list()
    ret_fields.append("code".strip())
    renames["name"] = "secu_name"
    ret_fields.append("secu_name".strip())
    renames["his_suspend_date"] = "suspend_date"
    ret_fields.append("suspend_date".strip())
    renames["his_resume_date"] = "resume_date"
    ret_fields.append("resume_date".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/hq/stock/tfp/history", params)
    return __return_format(dfs, field=None, renames=renames, ret_fields=ret_fields, index=index)


def get_stock_sus_today(code=None, date=None):
    """获取今天停复牌的股票

    Parameters
    ----------
    code:str  or  list,default None
        股票代码，零个/多个，最多支持50个
    date:str,default None
        查询日期, 默认返回当天的停复牌信息

    Returns
    -------
    code:str 股票代码
    secu_name:str 股票简称
    status:str 股票状态，'T'：停牌，‘F'：复牌（上一日停牌，当日恢复交易）

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_stock_sus_today()
    """
    params = dict()

    if not isinstance(code, tuple([str , list])) and code is not None:
        raise TypeError("get_stock_sus_today() arg code must be a str  or  list types")
    params["code"] = __format_param("code", code)

    if not isinstance(date, tuple([str])) and date is not None:
        raise TypeError("get_stock_sus_today() arg date must be a str type")
    params["date"] = __format_param("date", date)

    index = None
    renames = dict()
    ret_fields = list()
    ret_fields.append("code".strip())
    renames["name"] = "secu_name"
    ret_fields.append("secu_name".strip())
    ret_fields.append("status".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/hq/stock/tfp/list", params)
    return __return_format(dfs, field=None, renames=renames, ret_fields=ret_fields, index=index)


def get_stock_all_product(sam, date=None):
    """公司主营产品分项报告期数据及通过数库标准产品和数库四级行业找对应公司

    Parameters
    ----------
    sam:str
        samcode
    date:str,default None
        查询日期

    Returns
    -------
    secu:str 股票代码
    income:str 行业或产品收入
    profit:str 行业或产品毛利
    income_ratio:str 产品收入占比
    profit_ratio:str 产品毛利占比

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_stock_all_product(sam="HA005",date="2016-01-01")
    """
    params = dict()

    if not isinstance(sam, tuple([str])):
        raise TypeError("get_stock_all_product() arg sam must be a str type")
    params["code"] = __format_param("sam", sam)

    if not isinstance(date, tuple([str])) and date is not None:
        raise TypeError("get_stock_all_product() arg date must be a str type")
    params["date"] = __format_param("date", date)

    index = None
    renames = dict()
    ret_fields = list()
    ret_fields.append("secu".strip())
    ret_fields.append("income".strip())
    ret_fields.append("profit".strip())
    ret_fields.append("income_ratio".strip())
    ret_fields.append("profit_ratio".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/ced/product/stock", params)
    return __return_format(dfs, field=None, renames=renames, ret_fields=ret_fields, index=index)


def get_stock_top_product(code, date=None):
    """根据股票代码获取主营四级数库行业（收入、毛利等等占比最高）及该行业下收入、毛利等等占比最高的主营数库标准产品

    Parameters
    ----------
    code:str  or  list
        股票代码，一个/多个
    date:str,default None
        查询日期

    Returns
    -------
    secu:str 行业代码或产品代码
    industry_code:str 行业代码
    industry_name:str 行业名称
    product_code:str 产品代码
    product_name:str 产品名称
    industry_income:str 行业收入
    industry_profit:str 行业毛利
    product_income:str 产品收入
    product_profit:str 产品毛利
    industry_income_ratio:str 行业收入占比
    industry_profit_ratio:str 行业毛利占比
    product_income_ratio:str 产品收入占比
    product_profit_ratio:str 产品毛利占比

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_stock_top_product(code="601398",date="2016-01-01")
    """
    params = dict()

    if not isinstance(code, tuple([str , list])):
        raise TypeError("get_stock_top_product() arg code must be a str  or  list types")
    params["secus"] = __format_param("code", code)

    if not isinstance(date, tuple([str])) and date is not None:
        raise TypeError("get_stock_top_product() arg date must be a str type")
    params["date"] = __format_param("date", date)

    index = None
    renames = dict()
    ret_fields = list()
    ret_fields.append("secu".strip())
    ret_fields.append("industry_code".strip())
    renames["industry_name_szh"] = "industry_name"
    ret_fields.append("industry_name".strip())
    ret_fields.append("product_code".strip())
    renames["product_name_szh"] = "product_name"
    ret_fields.append("product_name".strip())
    ret_fields.append("industry_income".strip())
    ret_fields.append("industry_profit".strip())
    ret_fields.append("product_income".strip())
    ret_fields.append("product_profit".strip())
    ret_fields.append("industry_income_ratio".strip())
    ret_fields.append("industry_profit_ratio".strip())
    ret_fields.append("product_income_ratio".strip())
    ret_fields.append("product_profit_ratio".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/ced/stock/product/top", params)
    return __return_format(dfs, field=None, renames=renames, ret_fields=ret_fields, index=index)


def get_supply_chain_relation(sam=None):
    """产业链关系 （限制在数库行业四级和五级）

    Parameters
    ----------
    sam:str,default None
        samcode

    Returns
    -------
    prime_cd:str 主科目编码
    prime_name:str 主科目中文名称
    related_cd:str 上下游关联科目编码
    related_name:str 关联科目中文名称
    rtyp:str 关联科目相对主科目的关系类型：A：生产工具
                                             D：贸易/销售
                                             E：生产环境
                                             F：辅助
                                             M：生产材料/原料
                                             P：主体
                                             R：依存关系
                                             T：服务

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_supply_chain_relation(sam="PS00501")
    """
    params = dict()

    if not isinstance(sam, tuple([str])) and sam is not None:
        raise TypeError("get_supply_chain_relation() arg sam must be a str type")
    params["code"] = __format_param("sam", sam)

    index = None
    renames = dict()
    ret_fields = list()
    ret_fields.append("prime_cd".strip())
    ret_fields.append("prime_name".strip())
    ret_fields.append("related_cd".strip())
    ret_fields.append("related_name".strip())
    ret_fields.append("rtyp".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/ced/supply/chain/relation", params)
    return __return_format(dfs, field=None, renames=renames, ret_fields=ret_fields, index=index)


def get_product_macro_map(industry_code):
    """根据产品（行业）代码找到对应宏观指标

    Parameters
    ----------
    industry_code:str
        数库行业代码

    Returns
    -------
    sam_code:str 数库标准产品
    acmr_code:str 宏观指标编码

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_product_macro_map(industry_code="HA005")
    """
    params = dict()

    if not isinstance(industry_code, tuple([str])):
        raise TypeError("get_product_macro_map() arg industry_code must be a str type")
    params["codes"] = __format_param("industry_code", industry_code)

    index = None
    renames = dict()
    ret_fields = list()
    renames["sam"] = "sam_code"
    ret_fields.append("sam_code".strip())
    renames["acmr"] = "acmr_code"
    ret_fields.append("acmr_code".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/ced/product/macro", params)
    return __return_format(dfs, field=None, renames=renames, ret_fields=ret_fields, index=index)


def get_stock_basic_info(code, field=None):
    """股票基本信息

    Parameters
    ----------
    code:str  or  list
        股票代码，一个/多个，最多10个
    field:list,default None
        返回字段

    Returns
    -------
    code:str 股票代码
    full_name:str 上市公司全称
    secu_name:str 股票简称
    industry:str 行业分类
    total_share:str 总股本
    outstanding:str 流通股本
    establish_date:str 成立日期
    ipo_date:str 上市日期
    exchange:str 交易市场
    region:str 所属区域
    registration:str 注册地址
    listing:str 上市状态

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_stock_basic_info(code=["601398","002183"])
    """
    params = dict()

    if not isinstance(code, tuple([str , list])):
        raise TypeError("get_stock_basic_info() arg code must be a str  or  list types")
    params["codes"] = __format_param("code", code)

    if not isinstance(field, tuple([list])) and field is not None:
        raise TypeError("get_stock_basic_info() arg field must be a list type")
    params["field"] = __format_param("field", field)

    index = None
    renames = dict()
    ret_fields = list()
    ret_fields.append("code".strip())
    renames["name"] = "full_name"
    ret_fields.append("full_name".strip())
    renames["security_name"] = "secu_name"
    ret_fields.append("secu_name".strip())
    ret_fields.append("industry".strip())
    ret_fields.append("total_share".strip())
    ret_fields.append("outstanding".strip())
    ret_fields.append("establish_date".strip())
    ret_fields.append("ipo_date".strip())
    ret_fields.append("exchange".strip())
    ret_fields.append("region".strip())
    ret_fields.append("registration".strip())
    ret_fields.append("listing".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/stock/detail", params)
    return __return_format(dfs, field=field, renames=renames, ret_fields=ret_fields, index=index)


def get_stock_csf_industry(code, field=None):
    """根据股票代码查询股票数库行业分类

    Parameters
    ----------
    code:str 
        股票代码，一个
    field:list,default None
        返回字段

    Returns
    -------
    code:str 股票代码
    secu_name:str 股票简称
    level1_name:str 一级行业
    leve2_name:str 二级行业
    level3_name:str 三级行业
    level4_name:str 四级行业
    level1_code:str 一级行业编码
    leve2_code:str 二级行业编码
    level3_code:str 三级行业编码
    level4_code:str 四级行业编码

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_stock_csf_industry(code="601398")
    """
    params = dict()

    if not isinstance(code, tuple([str ])):
        raise TypeError("get_stock_csf_industry() arg code must be a str  type")
    params["codes"] = __format_param("code", code)

    if not isinstance(field, tuple([list])) and field is not None:
        raise TypeError("get_stock_csf_industry() arg field must be a list type")
    params["field"] = __format_param("field", field)

    index = None
    renames = dict()
    ret_fields = list()
    ret_fields.append("code".strip())
    ret_fields.append("secu_name".strip())
    ret_fields.append("level1_name".strip())
    ret_fields.append("leve2_name".strip())
    ret_fields.append("level3_name".strip())
    ret_fields.append("level4_name".strip())
    ret_fields.append("level1_code".strip())
    ret_fields.append("leve2_code".strip())
    ret_fields.append("level3_code".strip())
    ret_fields.append("level4_code".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/stock/industry/csf/list", params)
    return __return_format(dfs, field=field, renames=renames, ret_fields=ret_fields, index=index)


def get_stock_industry(code, field=None):
    """根据股票代码查询股票申万行业分类

    Parameters
    ----------
    code:str 
        股票代码，一个
    field:list,default None
        返回字段

    Returns
    -------
    code:str 股票代码
    secu_name:str 股票简称
    level1_name:str 一级行业
    leve2_name:str 二级行业
    level3_name:str 三级行业
    level1_code:str 一级行业编码
    leve2_code:str 二级行业编码
    level3_code:str 三级行业编码

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_stock_industry(code="601398")
    """
    params = dict()

    if not isinstance(code, tuple([str ])):
        raise TypeError("get_stock_industry() arg code must be a str  type")
    params["codes"] = __format_param("code", code)

    if not isinstance(field, tuple([list])) and field is not None:
        raise TypeError("get_stock_industry() arg field must be a list type")
    params["field"] = __format_param("field", field)

    index = None
    renames = dict()
    ret_fields = list()
    ret_fields.append("code".strip())
    ret_fields.append("secu_name".strip())
    ret_fields.append("level1_name".strip())
    ret_fields.append("leve2_name".strip())
    ret_fields.append("level3_name".strip())
    ret_fields.append("level1_code".strip())
    ret_fields.append("leve2_code".strip())
    ret_fields.append("level3_code".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/stock/industry/list", params)
    return __return_format(dfs, field=field, renames=renames, ret_fields=ret_fields, index=index)


def get_stock_ipo_info(code, field=None):
    """根据股票代码查询股票首次上市信息

    Parameters
    ----------
    code:str 
        股票代码，一个
    field:list,default None
        返回字段

    Returns
    -------
    code:str 股票代码
    full_name:str 股票名称
    pucode:str 申购代码
    abbrszh:str 证券简称
    orgname:str 机构全称
    stran:str 发行股数
    price:str 发行价格
    pe:str 发行市盈率
    pulim:str 申购上限
    capi:str 资金上限
    rate:str 中签率
    isda:str 发行日期
    dt:str 上市日期
    ballot:str 中签号公布日
    desc:str 公司简介
    reca_amnt:str 注册资金
    reca_cur:str 货币编码
    biz:str 主营业务
    business:str 主营业务
    invt:str 募投内容

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_stock_ipo_info(code="601398")
    """
    params = dict()

    if not isinstance(code, tuple([str ])):
        raise TypeError("get_stock_ipo_info() arg code must be a str  type")
    params["codes"] = __format_param("code", code)

    if not isinstance(field, tuple([list])) and field is not None:
        raise TypeError("get_stock_ipo_info() arg field must be a list type")
    params["field"] = __format_param("field", field)

    index = None
    renames = dict()
    ret_fields = list()
    ret_fields.append("code".strip())
    ret_fields.append("full_name".strip())
    ret_fields.append("pucode".strip())
    ret_fields.append("abbrszh".strip())
    ret_fields.append("orgname".strip())
    ret_fields.append("stran".strip())
    ret_fields.append("price".strip())
    ret_fields.append("pe".strip())
    ret_fields.append("pulim".strip())
    ret_fields.append("capi".strip())
    ret_fields.append("rate".strip())
    ret_fields.append("isda".strip())
    ret_fields.append("dt".strip())
    ret_fields.append("ballot".strip())
    ret_fields.append("desc".strip())
    ret_fields.append("reca_amnt".strip())
    ret_fields.append("reca_cur".strip())
    ret_fields.append("biz".strip())
    ret_fields.append("business".strip())
    ret_fields.append("invt".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/stock/ipo/history/list", params)
    return __return_format(dfs, field=field, renames=renames, ret_fields=ret_fields, index=index)


def get_stock_dividend(code, field=None):
    """根据股票代码查询股票分红信息

    Parameters
    ----------
    code:str 
        股票代码，一个
    field:list,default None
        返回字段

    Returns
    -------
    code:str 股票代码
    secu_name:str 股票简称
    y:str 分红年份
    exrdt:str 除权日期
    bns:str 派息比例（含税）
    aft_bns:str 派息比例（扣税）
    givsr:str 送转比例
    givsr_stock:str 送股比例
    givsr_transf:str 转增比例

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_stock_dividend(code="601398")
    """
    params = dict()

    if not isinstance(code, tuple([str ])):
        raise TypeError("get_stock_dividend() arg code must be a str  type")
    params["codes"] = __format_param("code", code)

    if not isinstance(field, tuple([list])) and field is not None:
        raise TypeError("get_stock_dividend() arg field must be a list type")
    params["field"] = __format_param("field", field)

    index = None
    renames = dict()
    ret_fields = list()
    ret_fields.append("code".strip())
    ret_fields.append("secu_name".strip())
    ret_fields.append("y".strip())
    ret_fields.append("exrdt".strip())
    ret_fields.append("bns".strip())
    ret_fields.append("aft_bns".strip())
    ret_fields.append("givsr".strip())
    ret_fields.append("givsr_stock".strip())
    ret_fields.append("givsr_transf".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/stock/dividend/list", params)
    return __return_format(dfs, field=field, renames=renames, ret_fields=ret_fields, index=index)


def get_stock_rightissue(code):
    """根据股票代码查询股票配股信息

    Parameters
    ----------
    code:str 
        股票代码，一个

    Returns
    -------
    code:str 股票代码
    secu_name:str 股票简称
    exdiv_date:str 除权日期
    rightissue_price:str 配股价
    rightissue_ratio:str 配股比例

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_stock_rightissue(code="601398")
    """
    params = dict()

    if not isinstance(code, tuple([str ])):
        raise TypeError("get_stock_rightissue() arg code must be a str  type")
    params["codes"] = __format_param("code", code)

    index = None
    renames = dict()
    ret_fields = list()
    ret_fields.append("code".strip())
    ret_fields.append("secu_name".strip())
    ret_fields.append("exdiv_date".strip())
    ret_fields.append("rightissue_price".strip())
    ret_fields.append("rightissue_ratio".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/stock/rightissue/list", params)
    return __return_format(dfs, field=None, renames=renames, ret_fields=ret_fields, index=index)


def get_st_stock_today(date):
    """查询指定日期特别处理的股票

    Parameters
    ----------
    date:str
        查询日期 格式：yyyy-MM-dd

    Returns
    -------
    code:str 股票代码
    secu_name:str 股票简称
    date:str 日期
    status:str 股票状态，'ST'，‘*ST’

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_st_stock_today(date="2016-04-08")
    """
    params = dict()

    if not isinstance(date, tuple([str])):
        raise TypeError("get_st_stock_today() arg date must be a str type")
    params["dt"] = __format_param("date", date)

    index = None
    renames = dict()
    ret_fields = list()
    ret_fields.append("code".strip())
    ret_fields.append("secu_name".strip())
    ret_fields.append("date".strip())
    ret_fields.append("status".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/stock/st/list", params)
    return __return_format(dfs, field=None, renames=renames, ret_fields=ret_fields, index=index)


def get_csf_ind_stocks(ind_code, date=None):
    """查询数库行业分类包含的股票

    Parameters
    ----------
    ind_code:str
        行业代码，一个
    date:str,default None
        日期，为None取当前日期

    Returns
    -------
    code:str 股票代码
    secu_name:str 股票简称

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_csf_ind_stocks(ind_code="CSF_20")
    """
    params = dict()

    if not isinstance(ind_code, tuple([str])):
        raise TypeError("get_csf_ind_stocks() arg ind_code must be a str type")
    params["ind_code"] = __format_param("ind_code", ind_code)

    if not isinstance(date, tuple([str])) and date is not None:
        raise TypeError("get_csf_ind_stocks() arg date must be a str type")
    params["date"] = __format_param("date", date)

    index = None
    renames = dict()
    ret_fields = list()
    ret_fields.append("code".strip())
    ret_fields.append("secu_name".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/stock/csf/list", params)
    return __return_format(dfs, field=None, renames=renames, ret_fields=ret_fields, index=index)


def get_index_component(index_code, date=None, field=None):
    """常用指数（非数库）成份股

    Parameters
    ----------
    index_code:str
        指数代码（000300），不可输入多个指数代码
    date:str,default None
        查询日期，格式:'yyyy-MM-dd'
    field:list,default None
        返回字段

    Returns
    -------
    code:str 股票代码
    name:str 股票简称
    weight:float 成份股市值权重
    market_cap:float 流通市值
    industry:str 股票所属行业（默认数库二级行业）

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_index_component(index_code="000906",date="2016-04-05")
    """
    params = dict()

    if not isinstance(index_code, tuple([str])):
        raise TypeError("get_index_component() arg index_code must be a str type")
    params["idxcd"] = __format_param("index_code", index_code)

    if not isinstance(date, tuple([str])) and date is not None:
        raise TypeError("get_index_component() arg date must be a str type")
    params["date"] = __format_param("date", date)

    if not isinstance(field, tuple([list])) and field is not None:
        raise TypeError("get_index_component() arg field must be a list type")
    params["field"] = __format_param("field", field)

    index = None
    renames = dict()
    ret_fields = list()
    ret_fields.append("code".strip())
    ret_fields.append("name".strip())
    ret_fields.append("weight".strip())
    ret_fields.append("market_cap".strip())
    ret_fields.append("industry".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/market/index/stock/weight", params)
    return __return_format(dfs, field=field, renames=renames, ret_fields=ret_fields, index=index)


def get_csf_index_com(index_code, date=None, field=None):
    """数库指数成份股

    Parameters
    ----------
    index_code:str
        指数代码（AAAA），不可输入多个指数代码
    date:str,default None
        查询日期，格式:'yyyy-MM-dd'
    field:list,default None
        返回字段

    Returns
    -------
    code:str 股票代码
    name:str 股票简称
    weight:float 权重
    market_cap:float 流通市值
    industry:str 股票所属行业（默认数库二级行业）

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_csf_index_com(index_code="AAAEAB",date="2016-04-28")
    """
    params = dict()

    if not isinstance(index_code, tuple([str])):
        raise TypeError("get_csf_index_com() arg index_code must be a str type")
    params["csf_code"] = __format_param("index_code", index_code)

    if not isinstance(date, tuple([str])) and date is not None:
        raise TypeError("get_csf_index_com() arg date must be a str type")
    params["date"] = __format_param("date", date)

    if not isinstance(field, tuple([list])) and field is not None:
        raise TypeError("get_csf_index_com() arg field must be a list type")
    params["field"] = __format_param("field", field)

    index = None
    renames = dict()
    ret_fields = list()
    ret_fields.append("code".strip())
    ret_fields.append("name".strip())
    ret_fields.append("weight".strip())
    ret_fields.append("market_cap".strip())
    ret_fields.append("industry".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/csf/index/stock/weight", params)
    return __return_format(dfs, field=field, renames=renames, ret_fields=ret_fields, index=index)


def get_index_info(index_code, field=None):
    """常用指数（非数库）基本信息

    Parameters
    ----------
    index_code:str or list
        指数代码（000003.SH），可以输入多个指数代码
    field:list,default None
        返回字段

    Returns
    -------
    code:str 指数代码
    name:str 指数名称
    basedate:str 基期
    basepoint:int 基点

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_index_info(index_code=["000001.SH","000003.SH"])
    """
    params = dict()

    if not isinstance(index_code, tuple([str,list])):
        raise TypeError("get_index_info() arg index_code must be a str or list types")
    params["index_code"] = __format_param("index_code", index_code)

    if not isinstance(field, tuple([list])) and field is not None:
        raise TypeError("get_index_info() arg field must be a list type")
    params["field"] = __format_param("field", field)

    index = None
    renames = dict()
    ret_fields = list()
    ret_fields.append("code".strip())
    ret_fields.append("name".strip())
    ret_fields.append("basedate".strip())
    ret_fields.append("basepoint".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/market/index/info", params)
    return __return_format(dfs, field=field, renames=renames, ret_fields=ret_fields, index=index)


def get_csf_index_info(index_code, field=None):
    """数库指数基本信息(含京东大数据指数)

    Parameters
    ----------
    index_code:str
        指数代码（CAAA），可以输入多个指数代码
    field:list,default None
        返回字段

    Returns
    -------
    code:str 指数代码
    name:str 指数名称
    basedate:str 基期
    basepoint:int 基点
    indextype:str 指数类型
    weight_method:str 加权方式
    indexfreq:str 换期频率
    level:int 层级
    industry:str 所属行业
    curtype:str 指数货币计价单位：人民币
    crt:str 最新一期换期开始日期
    edt :str 最新一期换期结束日期

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_csf_index_info(index_code="CAP500")
    """
    params = dict()

    if not isinstance(index_code, tuple([str])):
        raise TypeError("get_csf_index_info() arg index_code must be a str type")
    params["index_code"] = __format_param("index_code", index_code)

    if not isinstance(field, tuple([list])) and field is not None:
        raise TypeError("get_csf_index_info() arg field must be a list type")
    params["field"] = __format_param("field", field)

    index = None
    renames = dict()
    ret_fields = list()
    ret_fields.append("code".strip())
    ret_fields.append("name".strip())
    ret_fields.append("basedate".strip())
    ret_fields.append("basepoint".strip())
    ret_fields.append("indextype".strip())
    ret_fields.append("weight_method".strip())
    ret_fields.append("indexfreq".strip())
    ret_fields.append("level".strip())
    ret_fields.append("industry".strip())
    ret_fields.append("curtype".strip())
    ret_fields.append("crt".strip())
    ret_fields.append("edt ".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/csf/index/info", params)
    return __return_format(dfs, field=field, renames=renames, ret_fields=ret_fields, index=index)


def get_balance_sheet(code, start_date=None, end_date=None, freq="Q", field=None):
    """资产负债表

    Parameters
    ----------
    code:str
        股票代码，一个
    start_date:str,default None
        开始年份 格式：yyyy，如“2016”
    end_date:str,default None
        结束年份 格式：yyyy，如“2016”
    freq:str,default "Q"
        财务频率 枚举：Q：季度数据
                      Q1：仅输出1季度数据
                      Q2：仅输出2季度数据
                      Q3：仅输出3季度数据
                      Q4：仅输出4季度数据
    field:list,default None
        返回字段

    Returns
    -------
    code:str 股票代码
    name_szh:str 股票中文名称
    date:str 年份季度 格式：季度/年度，如：Q1/2015
    items_cd:str 财务科目编码
    items_name_szh:str 财务科目中文名
    items_lv:str 财务科目调整值

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_balance_sheet(code="000001")
    """
    params = dict()

    if not isinstance(code, tuple([str])):
        raise TypeError("get_balance_sheet() arg code must be a str type")
    params["codes"] = __format_param("code", code)

    if not isinstance(start_date, tuple([str])) and start_date is not None:
        raise TypeError("get_balance_sheet() arg start_date must be a str type")
    params["from"] = __format_param("start_date", start_date)

    if not isinstance(end_date, tuple([str])) and end_date is not None:
        raise TypeError("get_balance_sheet() arg end_date must be a str type")
    params["to"] = __format_param("end_date", end_date)

    if not isinstance(freq, tuple([str])):
        raise TypeError("get_balance_sheet() arg freq must be a str type")
    params["freq"] = __format_param("freq", freq)

    if not isinstance(field, tuple([list])) and field is not None:
        raise TypeError("get_balance_sheet() arg field must be a list type")
    params["field"] = __format_param("field", field)

    index = None
    renames = dict()
    ret_fields = list()
    ret_fields.append("code".strip())
    ret_fields.append("name_szh".strip())
    ret_fields.append("date".strip())
    ret_fields.append("items_cd".strip())
    ret_fields.append("items_name_szh".strip())
    ret_fields.append("items_lv".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/finance/balance", params)
    return __return_format(dfs, field=field, renames=renames, ret_fields=ret_fields, index=index)


def get_income_sheet(code, start_date=None, end_date=None, type="ytd", freq="Q", field=None):
    """利润表

    Parameters
    ----------
    code:str
        股票代码，一个
    start_date:str,default None
        开始年份 格式：yyyy，如“2016”
    end_date:str,default None
        结束年份 格式：yyyy，如“2016”
    type:str,default "ytd"
        数据类型：cur：单季度数据
               ytd：报告期数据
               ltm：最近12月数据
    freq:str,default "Q"
        财务频率：Q：季度数据
               Q1：仅输出1季度数据，
               Q2：仅输出2季度数据，
               Q3：仅输出3季度数据，
               Q4：仅输出4季度数据，
               A：年报。
               注意：若type 为cur，则
               （1） Q指1-3、4-6、7-9、10-12
               （2） Q1指1-3
               （3） Q2指4-6
               （4） Q3指7-9
               （5） Q4指10-12
               若type为ytd，则
               （1） Q指1-3、1-6、1-9、1-12
               （2） Q1指1-3
               （3） Q2指1-6
               （4） Q3指1-9
               （5） Q4指1-12
               若type为ltm，则
               （1） Q1指上年Q1至今年Q1
               （2） Q2指上年Q2至今年Q2
               （3） Q3指上年Q3至今年Q3
               （4） Q4指上年Q4至今年Q4
               （5） Q指包含Q1,Q2,Q3,Q4


    field:list,default None
        返回字段

    Returns
    -------
    code:str 股票代码
    name_szh:str 股票中文名称
    date:str 年份季度 格式：季度/年度，如：Q1/2015
    items_cd:str 财务科目编码
    items_name_szh:str 财务科目中文名
    items_lv:str 财务科目调整值

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_income_sheet(code="000001")
    """
    params = dict()

    if not isinstance(code, tuple([str])):
        raise TypeError("get_income_sheet() arg code must be a str type")
    params["codes"] = __format_param("code", code)

    if not isinstance(start_date, tuple([str])) and start_date is not None:
        raise TypeError("get_income_sheet() arg start_date must be a str type")
    params["from"] = __format_param("start_date", start_date)

    if not isinstance(end_date, tuple([str])) and end_date is not None:
        raise TypeError("get_income_sheet() arg end_date must be a str type")
    params["to"] = __format_param("end_date", end_date)

    if not isinstance(type, tuple([str])):
        raise TypeError("get_income_sheet() arg type must be a str type")
    params["type"] = __format_param("type", type)

    if not isinstance(freq, tuple([str])):
        raise TypeError("get_income_sheet() arg freq must be a str type")
    params["freq"] = __format_param("freq", freq)

    if not isinstance(field, tuple([list])) and field is not None:
        raise TypeError("get_income_sheet() arg field must be a list type")
    params["field"] = __format_param("field", field)

    index = None
    renames = dict()
    ret_fields = list()
    ret_fields.append("code".strip())
    ret_fields.append("name_szh".strip())
    ret_fields.append("date".strip())
    ret_fields.append("items_cd".strip())
    ret_fields.append("items_name_szh".strip())
    ret_fields.append("items_lv".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/finance/incomes", params)
    return __return_format(dfs, field=field, renames=renames, ret_fields=ret_fields, index=index)


def get_cashflow_sheet(code, start_date=None, end_date=None, type="ytd", freq="Q", field=None):
    """现金流量表

    Parameters
    ----------
    code:str
        股票代码，一个
    start_date:str,default None
        开始年份 格式：yyyy，如“2016”
    end_date:str,default None
        结束年份 格式：yyyy，如“2016”
    type:str,default "ytd"
        数据类型：cur：单季度数据
               ytd：报告期数据
               ltm：最近12月数据
    freq:str,default "Q"
        财务频率：Q：季度数据
               Q1：仅输出1季度数据，
               Q2：仅输出2季度数据，
               Q3：仅输出3季度数据，
               Q4：仅输出4季度数据，
               A：年报。
               注意：若type 为cur，则
               （1） Q指1-3、4-6、7-9、10-12
               （2） Q1指1-3
               （3） Q2指4-6
               （4） Q3指7-9
               （5） Q4指10-12
               若type为ytd，则
               （1） Q指1-3、1-6、1-9、1-12
               （2） Q1指1-3
               （3） Q2指1-6
               （4） Q3指1-9
               （5） Q4指1-12
               若type为ltm，则
               （1） Q1指上年Q1至今年Q1
               （2） Q2指上年Q2至今年Q2
               （3） Q3指上年Q3至今年Q3
               （4） Q4指上年Q4至今年Q4
               （5） Q指包含Q1,Q2,Q3,Q4


    field:list,default None
        返回字段

    Returns
    -------
    code:str 股票代码
    name_szh:str 股票中文名称
    date:str 年份季度 格式：季度/年度，如：Q1/2015
    items_cd:str 财务科目编码
    items_name_szh:str 财务科目中文名
    items_lv:str 财务科目调整值

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_cashflow_sheet(code="000979")
    """
    params = dict()

    if not isinstance(code, tuple([str])):
        raise TypeError("get_cashflow_sheet() arg code must be a str type")
    params["codes"] = __format_param("code", code)

    if not isinstance(start_date, tuple([str])) and start_date is not None:
        raise TypeError("get_cashflow_sheet() arg start_date must be a str type")
    params["from"] = __format_param("start_date", start_date)

    if not isinstance(end_date, tuple([str])) and end_date is not None:
        raise TypeError("get_cashflow_sheet() arg end_date must be a str type")
    params["to"] = __format_param("end_date", end_date)

    if not isinstance(type, tuple([str])):
        raise TypeError("get_cashflow_sheet() arg type must be a str type")
    params["type"] = __format_param("type", type)

    if not isinstance(freq, tuple([str])):
        raise TypeError("get_cashflow_sheet() arg freq must be a str type")
    params["freq"] = __format_param("freq", freq)

    if not isinstance(field, tuple([list])) and field is not None:
        raise TypeError("get_cashflow_sheet() arg field must be a list type")
    params["field"] = __format_param("field", field)

    index = None
    renames = dict()
    ret_fields = list()
    ret_fields.append("code".strip())
    ret_fields.append("name_szh".strip())
    ret_fields.append("date".strip())
    ret_fields.append("items_cd".strip())
    ret_fields.append("items_name_szh".strip())
    ret_fields.append("items_lv".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/finance/cash", params)
    return __return_format(dfs, field=field, renames=renames, ret_fields=ret_fields, index=index)


def get_finance_item_sheet(rpt):
    """财务科目表

    Parameters
    ----------
    rpt:str
        财报类型：2.1.2：利润表（标准化数据）
               2.2.2：资产负债表（标准化数据）
               2.3.2：现金流量表（标准化数据）

    Returns
    -------
    code:str 科目代码
    name_szh:str 科目中文名称
    name_en:str 科目英文名称

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_finance_item_sheet(rpt="2.2.2")
    """
    params = dict()

    if not isinstance(rpt, tuple([str])):
        raise TypeError("get_finance_item_sheet() arg rpt must be a str type")
    params["rpt"] = __format_param("rpt", rpt)

    index = None
    renames = dict()
    ret_fields = list()
    ret_fields.append("code".strip())
    ret_fields.append("name_szh".strip())
    ret_fields.append("name_en".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/finance/items", params)
    return __return_format(dfs, field=None, renames=renames, ret_fields=ret_fields, index=index)


def get_stock_factor_list():
    """量化因子列表

    Parameters
    ----------
    

    Returns
    -------
    code:str 因子代码
    parent:str 父级代码
    level:str 层级(共2级)
    szh:str 中文名

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_stock_factor_list()
    """
    params = dict()

    index = None
    renames = dict()
    ret_fields = list()
    ret_fields.append("code".strip())
    ret_fields.append("parent".strip())
    ret_fields.append("level".strip())
    ret_fields.append("szh".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/quant/factor", params)
    return __return_format(dfs, field=None, renames=renames, ret_fields=ret_fields, index=index)


def get_stock_factor_search(q, start=0, limit=10):
    """量化因子搜索

    Parameters
    ----------
    q:str
        关键字
    start:int,default 0
        起始值
    limit:int,default 10
        限制数量

    Returns
    -------
    code:str 因子代码
    szh:str 中文名

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_stock_factor_search(q="M")
    """
    params = dict()

    if not isinstance(q, tuple([str])):
        raise TypeError("get_stock_factor_search() arg q must be a str type")
    params["q"] = __format_param("q", q)

    if not isinstance(start, tuple([int])):
        raise TypeError("get_stock_factor_search() arg start must be a int type")
    params["start"] = __format_param("start", start)

    if not isinstance(limit, tuple([int])):
        raise TypeError("get_stock_factor_search() arg limit must be a int type")
    params["limit"] = __format_param("limit", limit)

    index = None
    renames = dict()
    ret_fields = list()
    ret_fields.append("code".strip())
    ret_fields.append("szh".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/quant/factor/search", params)
    return __return_format(dfs, field=None, renames=renames, ret_fields=ret_fields, index=index)


def get_stock_factor(factors, start_date="2007-01-01", end_date="2015-12-31", index="000300", freq="M"):
    """量化因子值

    Parameters
    ----------
    factors:str  or  list
        因子，支持一个或多个
    start_date:str,default "2007-01-01"
        回测起始日期 格式:yyyy-MM-dd
    end_date:str,default "2015-12-31"
        回测结束日期 格式:yyyy-MM-dd
    index:str,default "000300"
        指数(股票池)代码
    freq:str,default "M"
        调仓频率 W(周) :M(月) :Q(季度)

    Returns
    -------
    cd:str 因子代码
    date:str 日期
    code:str 股票代码
    value:str 因子值

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_stock_factor(factors="M001007")
    """
    params = dict()

    if not isinstance(factors, tuple([str , list])):
        raise TypeError("get_stock_factor() arg factors must be a str  or  list types")
    params["factors"] = __format_param("factors", factors)

    if not isinstance(start_date, tuple([str])):
        raise TypeError("get_stock_factor() arg start_date must be a str type")
    params["start_date"] = __format_param("start_date", start_date)

    if not isinstance(end_date, tuple([str])):
        raise TypeError("get_stock_factor() arg end_date must be a str type")
    params["end_date"] = __format_param("end_date", end_date)

    if not isinstance(index, tuple([str])):
        raise TypeError("get_stock_factor() arg index must be a str type")
    params["index"] = __format_param("index", index)

    if not isinstance(freq, tuple([str])):
        raise TypeError("get_stock_factor() arg freq must be a str type")
    params["freq"] = __format_param("freq", freq)

    index = None
    renames = dict()
    ret_fields = list()
    renames["cd"] = "cd"
    ret_fields.append("cd".strip())
    renames["dt"] = "date"
    ret_fields.append("date".strip())
    renames["tick"] = "code"
    ret_fields.append("code".strip())
    renames["v"] = "value"
    ret_fields.append("value".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/quant/factor/value", params)
    return __return_format(dfs, field=None, renames=renames, ret_fields=ret_fields, index=index)


def get_macro_list(key=None):
    """宏观指标信息

    Parameters
    ----------
    key:str,default None
        查询关键字 默认返回全部指标列表

    Returns
    -------
    code:str 指标代码
    name:str 中文简称

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_macro_list(key="生产量")
    """
    params = dict()

    if not isinstance(key, tuple([str])) and key is not None:
        raise TypeError("get_macro_list() arg key must be a str type")
    params["key"] = __format_param("key", key)

    index = None
    renames = dict()
    ret_fields = list()
    ret_fields.append("code".strip())
    ret_fields.append("name".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/ced/indicator", params)
    return __return_format(dfs, field=None, renames=renames, ret_fields=ret_fields, index=index)


def get_macro_data(marco_code, start_date, end_date):
    """宏观数据

    Parameters
    ----------
    marco_code:str
        指标代码
    start_date:str
        起始日期
    end_date:str
        结束日期

    Returns
    -------
    code:str 数据编码
    name:str 名称
    date:str 日期
    value:str 数据值
    unit:str 单位
    type:str 类型

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_macro_data(marco_code="CHBA02090S0N03",start_date="2005-01-01",end_date="2016-06-01")
    """
    params = dict()

    if not isinstance(marco_code, tuple([str])):
        raise TypeError("get_macro_data() arg marco_code must be a str type")
    params["codes"] = __format_param("marco_code", marco_code)

    if not isinstance(start_date, tuple([str])):
        raise TypeError("get_macro_data() arg start_date must be a str type")
    params["from"] = __format_param("start_date", start_date)

    if not isinstance(end_date, tuple([str])):
        raise TypeError("get_macro_data() arg end_date must be a str type")
    params["to"] = __format_param("end_date", end_date)

    index = None
    renames = dict()
    ret_fields = list()
    ret_fields.append("code".strip())
    ret_fields.append("name".strip())
    ret_fields.append("date".strip())
    ret_fields.append("value".strip())
    ret_fields.append("unit".strip())
    ret_fields.append("type".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/ced/indicator/detail", params)
    return __return_format(dfs, field=None, renames=renames, ret_fields=ret_fields, index=index)


def get_notice_by_type(notice_type, start_date, end_date, field=None, skip=0, limit=10):
    """返回过去一段时间内某类型的公告数据

    Parameters
    ----------
    notice_type:str
        数库公告类型代码，一次只能查询一种类型的公告数据
    start_date:str
        开始日期
    end_date:str
        结束日期
    field:list,default None
        返回字段
    skip:int,default 0
        偏移量
    limit:int,default 10
        返回条数

    Returns
    -------
    code:str 股票代码
    secu_name:str 股票简称
    notice_type:str 公告类型代码
    notice_name:str 公告类型简称
    notice_title:str 公告标题
    pdt:str 公告日期

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_notice_by_type(notice_type="260201",start_date="2010-01-01",end_date="2016-01-01")
    """
    params = dict()

    if not isinstance(notice_type, tuple([str])):
        raise TypeError("get_notice_by_type() arg notice_type must be a str type")
    params["type"] = __format_param("notice_type", notice_type)

    if not isinstance(start_date, tuple([str])):
        raise TypeError("get_notice_by_type() arg start_date must be a str type")
    params["from"] = __format_param("start_date", start_date)

    if not isinstance(end_date, tuple([str])):
        raise TypeError("get_notice_by_type() arg end_date must be a str type")
    params["to"] = __format_param("end_date", end_date)

    if not isinstance(field, tuple([list])) and field is not None:
        raise TypeError("get_notice_by_type() arg field must be a list type")
    params["field"] = __format_param("field", field)

    if not isinstance(skip, tuple([int])):
        raise TypeError("get_notice_by_type() arg skip must be a int type")
    params["start"] = __format_param("skip", skip)

    if not isinstance(limit, tuple([int])):
        raise TypeError("get_notice_by_type() arg limit must be a int type")
    params["limit"] = __format_param("limit", limit)

    index = None
    renames = dict()
    ret_fields = list()
    renames["secu"] = "code"
    ret_fields.append("code".strip())
    ret_fields.append("secu_name".strip())
    ret_fields.append("notice_type".strip())
    ret_fields.append("notice_name".strip())
    ret_fields.append("notice_title".strip())
    ret_fields.append("pdt".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/announce", params)
    return __return_format(dfs, field=field, renames=renames, ret_fields=ret_fields, index=index)


def get_notice_by_stock(code, start_date=None, end_date=None, field=None, skip=0, limit=10):
    """返回某只股票过去一段时间内的公告数据

    Parameters
    ----------
    code:str
        股票代码，只能输入一个股票代码
    start_date:str,default None
        开始日期
    end_date:str,default None
        结束日期
    field:list,default None
        返回字段
    skip:int,default 0
        偏移量
    limit:int,default 10
        返回条数

    Returns
    -------
    code:str 股票代码
    secu_name:str 股票简称
    notice_type:str 公告类型代码
    notice_name:str 公告类型简称
    notice_title:str 公告标题
    pdt:str 公告日期

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_notice_by_stock(code="600628",start_date="2010-01-01",end_date="2016-01-01")
    """
    params = dict()

    if not isinstance(code, tuple([str])):
        raise TypeError("get_notice_by_stock() arg code must be a str type")
    params["codes"] = __format_param("code", code)

    if not isinstance(start_date, tuple([str])) and start_date is not None:
        raise TypeError("get_notice_by_stock() arg start_date must be a str type")
    params["from"] = __format_param("start_date", start_date)

    if not isinstance(end_date, tuple([str])) and end_date is not None:
        raise TypeError("get_notice_by_stock() arg end_date must be a str type")
    params["to"] = __format_param("end_date", end_date)

    if not isinstance(field, tuple([list])) and field is not None:
        raise TypeError("get_notice_by_stock() arg field must be a list type")
    params["field"] = __format_param("field", field)

    if not isinstance(skip, tuple([int])):
        raise TypeError("get_notice_by_stock() arg skip must be a int type")
    params["start"] = __format_param("skip", skip)

    if not isinstance(limit, tuple([int])):
        raise TypeError("get_notice_by_stock() arg limit must be a int type")
    params["limit"] = __format_param("limit", limit)

    index = None
    renames = dict()
    ret_fields = list()
    renames["secu"] = "code"
    ret_fields.append("code".strip())
    ret_fields.append("secu_name".strip())
    ret_fields.append("notice_type".strip())
    ret_fields.append("notice_name".strip())
    ret_fields.append("notice_title".strip())
    ret_fields.append("pdt".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/announce", params)
    return __return_format(dfs, field=field, renames=renames, ret_fields=ret_fields, index=index)


def get_notice_by_date(date=None, field=None, skip=0, limit=10):
    """获取某一天披露的所有股票的所有公告数据

    Parameters
    ----------
    date:str,default None
        查询日期
    field:list,default None
        返回字段
    skip:int,default 0
        偏移量
    limit:int,default 10
        返回条数

    Returns
    -------
    code:str 股票代码
    secu_name:str 股票简称
    notice_type:str 公告类型代码
    notice_name:str 公告类型简称
    notice_title:str 公告标题
    pdt:str 公告日期

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_notice_by_date(date="2016-02-01")
    """
    params = dict()

    if not isinstance(date, tuple([str])) and date is not None:
        raise TypeError("get_notice_by_date() arg date must be a str type")
    params["from"] = __format_param("date", date)
    params["to"] = __format_param("date", date)

    if not isinstance(field, tuple([list])) and field is not None:
        raise TypeError("get_notice_by_date() arg field must be a list type")
    params["field"] = __format_param("field", field)

    if not isinstance(skip, tuple([int])):
        raise TypeError("get_notice_by_date() arg skip must be a int type")
    params["start"] = __format_param("skip", skip)

    if not isinstance(limit, tuple([int])):
        raise TypeError("get_notice_by_date() arg limit must be a int type")
    params["limit"] = __format_param("limit", limit)

    index = None
    renames = dict()
    ret_fields = list()
    renames["secu"] = "code"
    ret_fields.append("code".strip())
    ret_fields.append("secu_name".strip())
    ret_fields.append("notice_type".strip())
    ret_fields.append("notice_name".strip())
    ret_fields.append("notice_title".strip())
    ret_fields.append("pdt".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/announce", params)
    return __return_format(dfs, field=field, renames=renames, ret_fields=ret_fields, index=index)


def get_notice_type_list(field=None):
    """获取公告类型列表

    Parameters
    ----------
    field:list,default None
        返回字段

    Returns
    -------
    level1_name:str 公告一级名称
    level1_code:str 公告一级代码
    level2_name:str 公告二级名称
    level2_code:str 公告二级代码
    level3_name:str 公告三级名称
    level3_code:str 公告三级代码

    Examples
    --------
    >>> import csf
    >>> csf.config.set_token(csf.config.EXAMPLES_ACCESS_KEY,csf.config.EXAMPLES_SECRET_KEY)
    >>> csf.get_notice_type_list()
    """
    params = dict()

    if not isinstance(field, tuple([list])) and field is not None:
        raise TypeError("get_notice_type_list() arg field must be a list type")
    params["field"] = __format_param("field", field)

    index = None
    renames = dict()
    ret_fields = list()
    renames["name"] = "level1_name"
    ret_fields.append("level1_name".strip())
    renames["code"] = "level1_code"
    ret_fields.append("level1_code".strip())
    renames["children_name"] = "level2_name"
    ret_fields.append("level2_name".strip())
    renames["children_code"] = "level2_code"
    ret_fields.append("level2_code".strip())
    renames["children_children_name"] = "level3_name"
    ret_fields.append("level3_name".strip())
    renames["children_children_code"] = "level3_code"
    ret_fields.append("level3_code".strip())
    renames = renames if renames else None

    dfs = __get_dataframe("/api/sdk/announce/type/tree", params)
    return __return_format(dfs, field=field, renames=renames, ret_fields=ret_fields, index=index)


