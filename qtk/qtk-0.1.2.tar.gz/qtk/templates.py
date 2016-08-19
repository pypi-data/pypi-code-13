from qtk.common import TemplateBase, NameBase, Category as C
from qtk.fields import Field as F


class GenericTemplate(NameBase, TemplateBase):
    _id_map = {}

    def __init__(self, name, category, sub_category=C.MAIN, convention_keys=(F.CURRENCY,)):
        name_id = "%s.%s" % (sub_category.id, self.toid(name))
        super(GenericTemplate, self).__init__(name, name_id=name_id, prefix=category.id)
        TemplateBase.__init__(self, category.id, convention_keys)


class Instrument(NameBase, TemplateBase):
    _id_map = {}

    def __init__(self, instrument_name, asset_type, security_type, security_subtype,
                 convention_keys=(F.CURRENCY,)):
        self._asset_type = asset_type
        self._security_type = security_type
        self._security_subtype = security_subtype
        inst_id = "%s.%s.%s" % (security_type.id, security_subtype.id, self.toid(instrument_name))
        prefix = self.__class__.__name__
        super(Instrument, self).__init__(instrument_name, name_id=inst_id, prefix=prefix)
        TemplateBase.__init__(self, prefix, convention_keys)

    @property
    def asset_type(self):
        return self._asset_type

    @property
    def security_type(self):
        return self._security_type

    @property
    def security_subtype(self):
        return self._security_subtype


class Template(object):
    # Instruments
    INST_BOND_TBOND = GenericTemplate("Treasury Bond", C.INSTRUMENTS, C.BOND)
    INST_BOND_TBILL = GenericTemplate("Treasury Bill", C.INSTRUMENTS, C.BOND)

    # Instrument Helpers in Building Term Structures
    INST_BOND_TBOND_HELPER = GenericTemplate("Treasury Bond Helper", C.INSTRUMENTS, C.BOND)
    INST_BOND_TBILL_HELPER = GenericTemplate("Treasury Bill Helper", C.INSTRUMENTS, C.BOND)
    INST_DERIVATIVE_SWAPTION_HELPER = GenericTemplate("Swaption Helper", C.INSTRUMENTS, C.DERIVATIVE)

    # All Term Structures
    TS_YIELD_BOND = GenericTemplate("Bond Curve", C.TERM_STRUCTURE, C.YIELD)
    TS_YIELD_ZERO = GenericTemplate("Zero Curve", C.TERM_STRUCTURE, C.YIELD)
    TS_YIELD_DISCOUNT = GenericTemplate("Discount Curve", C.TERM_STRUCTURE, C.YIELD)
    TS_YIELD_FLAT = GenericTemplate("Flat Curve", C.TERM_STRUCTURE, C.YIELD)

    # All Models
    MODELS_YIELD_HW1F = GenericTemplate("Hull White 1 Factor", C.MODELS, C.YIELD)

    # All Engines
    ENGINES_BOND_DISCOUNTING = GenericTemplate("Discounting", C.ENGINES, C.BOND, convention_keys=())

    # Time Module
    TIME_MAIN_SCHEDULE = GenericTemplate("Schedule", C.TIME, C.MAIN)

    # Market Report
    REPORTS_MARKET_ALL = GenericTemplate("All", C.REPORTS, C.MARKET)

    # Analytics
    ANALYTICS_MARKET_BOND = GenericTemplate("Bond", C.ANALYTICS, C.MARKET)

    # Indexes
    INDEXES_IBOR_USDLIBOR = GenericTemplate("USD Libor", C.INDEXES, C.IBOR)
    INDEXES_IBOR_CADLIBOR = GenericTemplate("CAD Libor", C.INDEXES, C.IBOR)
    INDEXES_IBOR_AUDLIBOR = GenericTemplate("AUD Libor", C.INDEXES, C.IBOR)
    INDEXES_IBOR_JPYLIBOR = GenericTemplate("JPY Libor", C.INDEXES, C.IBOR)
    INDEXES_IBOR_GBPLIBOR = GenericTemplate("GBP Libor", C.INDEXES, C.IBOR)
    INDEXES_IBOR_EURLIBOR = GenericTemplate("EUR Libor", C.INDEXES, C.IBOR)





