import markdown

from qtk.common import TemplateBase, NameBase, Category as C
from qtk.fields import Field as F


class GenericTemplate(NameBase, TemplateBase):
    _id_map = {}

    def __init__(self, name, category, sub_category=C.MAIN, convention_keys=(F.CURRENCY,)):
        name_id = "%s.%s" % (sub_category.id, self.toid(name))
        super(GenericTemplate, self).__init__(name, name_id=name_id, prefix=category.id)
        TemplateBase.__init__(self, category.id, convention_keys)

    def info(self):
        creator = self.get_creator()
        return creator.class_info() + "\n\n" + creator.field_info(self)

    def sample_data(self):
        creator = self.get_creator()
        return creator.sample_data(self)

    def help(self):
        print self.info()

    def _repr_html_(self):
        return markdown.markdown(self.info())


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
    INSTRUMENT_BOND_TBOND = GenericTemplate("Treasury Bond", C.INSTRUMENT, C.BOND)
    INSTRUMENT_BOND_TBILL = GenericTemplate("Treasury Bill", C.INSTRUMENT, C.BOND)

    INSTRUMENT_DERIVATIVE_EUROPEANOPTION = GenericTemplate("European Option", C.INSTRUMENT, C.DERIVATIVE,
                                                           convention_keys=())
    INSTRUMENT_DERIVATIVE_AMERICANOPTION = GenericTemplate("American Option", C.INSTRUMENT, C.DERIVATIVE,
                                                           convention_keys=())
    INSTRUMENT_DERIVATIVE_BERMUDANOPTION = GenericTemplate("Bermudan Option", C.INSTRUMENT, C.DERIVATIVE,
                                                           convention_keys=())

    # Instrument Helpers in Building Term Structures
    INSTRUMENT_BOND_TBOND_HELPER = GenericTemplate("Treasury Bond Helper", C.INSTRUMENT, C.BOND)
    INSTRUMENT_BOND_TBILL_HELPER = GenericTemplate("Treasury Bill Helper", C.INSTRUMENT, C.BOND)
    INSTRUMENT_DERIVATIVE_SWAPTION_HELPER = GenericTemplate("Swaption Helper", C.INSTRUMENT, C.DERIVATIVE)

    # All Term Structures
    TS_YIELD_BOND = GenericTemplate("Bond Curve", C.TERM_STRUCTURE, C.YIELD)
    TS_YIELD_ZERO = GenericTemplate("Zero Curve", C.TERM_STRUCTURE, C.YIELD)
    TS_YIELD_DISCOUNT = GenericTemplate("Discount Curve", C.TERM_STRUCTURE, C.YIELD)
    TS_YIELD_FLAT = GenericTemplate("Flat Curve", C.TERM_STRUCTURE, C.YIELD)

    TS_VOLATILITY_BLACKCONSTANT = GenericTemplate("Black Constant", C.TERM_STRUCTURE, C.VOLATILITY, convention_keys=())
    TS_VOLATILITY_BLACKCURVE = GenericTemplate("Black Curve", C.TERM_STRUCTURE, C.VOLATILITY, convention_keys=())
    TS_VOLATILITY_BLACKSURFACE = GenericTemplate("Black Surface", C.TERM_STRUCTURE, C.VOLATILITY, convention_keys=())

    # All Models
    MODEL_YIELD_HW1F = GenericTemplate("Hull White 1 Factor", C.MODEL, C.YIELD, convention_keys=())

    # All Engines
    ENGINE_BOND_DISCOUNTING = GenericTemplate("Discounting", C.ENGINE, C.BOND, convention_keys=())
    ENGINE_EQUITY_ANALYTICEUROPEAN = GenericTemplate("Analytic European", C.ENGINE, C.EQUITY, convention_keys=())
    ENGINE_EQUITY_FDAMERICAN = GenericTemplate("FD American", C.ENGINE, C.EQUITY, convention_keys=())
    ENGINE_EQUITY_FDBERMUDAN = GenericTemplate("FD Bermudan", C.ENGINE, C.EQUITY, convention_keys=())

    # Time Module
    TIME_MAIN_SCHEDULE = GenericTemplate("Schedule", C.TIME, C.MAIN)

    # Market Report
    REPORT_MARKET_ALL = GenericTemplate("All", C.REPORT, C.MARKET)

    # Analytics
    ANALYTIC_MARKET_BOND = GenericTemplate("Bond", C.ANALYTIC, C.MARKET, convention_keys=())

    # Indexes
    INDEX_IBOR_USDLIBOR = GenericTemplate("USD Libor", C.INDEX, C.IBOR, convention_keys=())
    INDEX_IBOR_CADLIBOR = GenericTemplate("CAD Libor", C.INDEX, C.IBOR, convention_keys=())
    INDEX_IBOR_AUDLIBOR = GenericTemplate("AUD Libor", C.INDEX, C.IBOR, convention_keys=())
    INDEX_IBOR_JPYLIBOR = GenericTemplate("JPY Libor", C.INDEX, C.IBOR, convention_keys=())
    INDEX_IBOR_GBPLIBOR = GenericTemplate("GBP Libor", C.INDEX, C.IBOR, convention_keys=())
    INDEX_IBOR_EURLIBOR = GenericTemplate("EUR Libor", C.INDEX, C.IBOR, convention_keys=())

    # Processes
    PROCESS_EQUITY_BLACKSCHOLESMERTON = GenericTemplate("Black Scholes Merton", C.PROCESS, C.EQUITY,convention_keys=())



