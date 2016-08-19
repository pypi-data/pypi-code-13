import QuantLib as ql
from qtk.fields import Field as F
from qtk.templates import Template as T

_swaptions = dict.fromkeys([
    "USD."+T.INST_DERIVATIVE_SWAPTION_HELPER.id
],  {
    F.SETTLEMENT_DAYS.id: 2,
    F.FIXED_LEG_TENOR.id: ql.Period(6, ql.Months),
    F.FIXED_LEG_BASIS.id: ql.Thirty360(),
    F.FLOAT_LEG_TENOR.id: ql.Period(3, ql.Months),
    F.FLOAT_LEG_BASIS.id: ql.Actual360()
})