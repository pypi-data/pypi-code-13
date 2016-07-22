from qtk.templates import Template as T
from qtk.fields import Field as F
import QuantLib as ql

# http://help.derivativepricing.com/1571.htm
# USD
_govt_bonds = dict.fromkeys([
    "USD."+T.INST_BOND_TBOND.id,
    "USD."+T.INST_BOND_TBOND_HELPER.id
], {
    F.COUPON_FREQ.id: ql.Semiannual,
    F.ACCRUAL_BASIS.id: ql.ActualActual(ql.ActualActual.Bond),
    F.ACCRUAL_DAY_CONVENTION.id: ql.Following,
    F.ACCRUAL_CALENDAR.id: ql.UnitedStates(ql.UnitedStates.GovernmentBond),
    F.END_OF_MONTH.id: True,
    F.COMPOUNDING.id: ql.Compounded,
    F.SETTLEMENT_DAYS.id: 1,
    F.PAYMENT_CALENDAR.id: ql.UnitedStates(),
    F.PAYMENT_DAY_CONVENTION.id: ql.Following,
    F.SETTLEMENT_CALENDAR.id: ql.UnitedStates(),
    F.ROUNDING.id: ql.ClosestRounding(12)
})

_govt_bonds.update(
    dict.fromkeys([
        "USD." + T.INST_BOND_TBILL.id,
        "USD." + T.INST_BOND_TBILL_HELPER.id,
    ], {
        F.ACCRUAL_BASIS.id: ql.Actual360(),
        F.ACCRUAL_DAY_CONVENTION.id: ql.Following,
        F.ACCRUAL_CALENDAR.id: ql.UnitedStates(ql.UnitedStates.GovernmentBond),
        F.END_OF_MONTH.id: True,
        F.COMPOUNDING.id: ql.Simple,
        F.SETTLEMENT_DAYS.id: 0,
        F.PAYMENT_CALENDAR.id: ql.UnitedStates(),
        F.PAYMENT_DAY_CONVENTION.id: ql.Following,
        F.SETTLEMENT_CALENDAR.id: ql.UnitedStates(),
        F.ROUNDING.id: ql.ClosestRounding(12)
    })
)
