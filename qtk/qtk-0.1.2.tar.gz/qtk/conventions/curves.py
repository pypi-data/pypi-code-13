import QuantLib as ql

from qtk.fields import Field as F
from qtk.templates import Template as T

# USD
_curves = dict.fromkeys([
    "USD."+T.TS_YIELD_BOND.id,
    "USD."+T.TS_YIELD_ZERO.id,
    "USD."+T.TS_YIELD_DISCOUNT.id],
    {
        F.DISCOUNT_BASIS.id: ql.Actual360(),
        F.DISCOUNT_CALENDAR.id: ql.UnitedStates(),
        F.SETTLEMENT_DAYS.id: 2
    }
)
