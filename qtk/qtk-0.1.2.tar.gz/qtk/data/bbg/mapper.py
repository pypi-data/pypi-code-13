from blpapi.exception import NotFoundException

from qtk.fields import Field as fl
from qtk.templates import Template as tmpl

# TODO: Scale coupon and yield by 100 to get all in fraction

__field_list_pair = [
    ("BPIPE_REFERENCE_SECURITY_CLASS", fl.ASSET_CLASS),
    ("CPN", fl.COUPON),
    ("CPN_FREQ", fl.COUPON_FREQ),
    ("DAY_CNT_DES", fl.ACCRUAL_BASIS),
    ("ISSUE_DT", fl.ISSUE_DATE),
    ("MATURITY", fl.MATURITY_DATE),
    ("date", fl.ASOF_DATE),
    ("PX_LAST", fl.PRICE),
    ("PX_MID", fl.PRICE),
    ("SECURITY_TYP", fl.SECURITY_TYPE),
    ("SECURITY_TYP2", fl.SECURITY_SUBTYPE),
    ("CRNCY", fl.CURRENCY)
]

__bbg_to_std = {}
__std_to_bbg = {}

_govt_curve_ticker_map = {"US": "YCGT0025 Index",
                          "UK": "YCGT0022 Index",
                          "NL": "YCGT0020 Index",
                          "JP": "YCGT0018 Index",
                          "HK": "YCGT0095 Index",
                          "DE": "YCGT0016 Index",
                          "FR": "YCGT0014 Index",
                          "EU": "YCGT0013 Index",
                          "AU": "YCGT0001 Index",
                          "CA": "YCGT0007 Index"
                          }


for bbg, std in __field_list_pair:
    __bbg_to_std[bbg] = std
    __std_to_bbg[std] = bbg


def bbg_to_std(key):
    return __bbg_to_std[key]


def std_to_bbg(key):
    return __std_to_bbg[key]


def fmt(e, f):
    key = bbg_to_std(f)

    def _to_str(ele, field):
        return ele.getElementAsString(field)

    """
    def _to_int(ele, field):
        return ele.getElementAsInteger(field)

    def _to_float(ele, field):
        return ele.getElementAsFloat(field)

    def _to_day_count(ele, field):
        dc = ele.getElementAsString(field)
        return qlf.to_daycount(dc)

    def _to_date(ele, field):
        date = ele.getElementAsString(field)
        date_py = qlf.to_date(date)
        return date_py

    def _to_freq(ele, field):
        return ele.getElementAsInteger(field)

    _format_map = {
        dt.STRING: _to_str,
        dt.INT: _to_int,
        dt.FLOAT: _to_float,
        dt.DATE: _to_date,
        dt.DAYCOUNT: _to_day_count,
        dt.FREQUENCY: _to_freq,
    }

    #converter = _format_map[key.data_type()]
    """
    converter = _to_str
    try:
        val = converter(e, f)
    except NotFoundException as e:
        val = None

    return key, val


def get_instrument(asset_type, security_type, security_subtype):
    _instrument_map = {
        "USGOVERNMENT.BILL": tmpl.INST_BOND_TBILL_HELPER,
        "USGOVERNMENT.NOTE": tmpl.INST_BOND_TBOND_HELPER,
        "USGOVERNMENT.BOND": tmpl.INST_BOND_TBOND_HELPER,
    }

    key_members = [security_type, security_subtype]
    key = ".".join([k.upper().replace(" ", "") for k in key_members])
    return _instrument_map[key]

