from qtk.common import DataType as D, NameBase


class FieldName(NameBase):
    _id_map = {}

    def __init__(self, name, desc, data_type):
        super(FieldName, self).__init__(name, desc=desc)
        self._data_type = data_type
        self._outer = None
        self._inner = None

    @property
    def data_type(self):
        return self._data_type

    def check_type(self, value):
        return isinstance(value, self._data_type.type)


class FieldNameModifier(FieldName):

    def __call__(self, field, data_type):
        new_field = FieldName(self.name+" "+field.name, self.description+" "+field.description,
                              data_type)
        new_field._outer = self
        new_field._inner = field
        return new_field

_LIST = FieldNameModifier("List Of", "List Of", D.LIST)

class Field(object):
    # In alphabetical order
    ACCRUAL_BASIS = FieldName("Accrual Basis", "Accrual Basis", D.DAYCOUNT)
    ACCRUAL_CALENDAR = FieldName("Accrual Calendar", "Accrual Calendar", D.CALENDAR)
    ACCRUAL_DAY_CONVENTION = FieldName("Accrual Day Convention", "Accrual Bussiness day convention",
                                       D.DAY_CONVENTION)

    ASOF_DATE = FieldName("As Of Date", "Reference date or as of date", D.DATE)
    ASSET_CLASS = FieldName("Asset Class", "Asset class of a security", D.STRING)
    COMPOUNDING = FieldName("Compounding", "Compounding", D.COMPOUNDING)
    COMPOUNDING_FREQ = FieldName("Compounding Frequency", "Compounding Frequency", D.FREQUENCY)
    CONVENTIONS = FieldName("Conventions", "Conventions for instruments, models or indices", D.DICT)
    COUNTRY = FieldName("Country", "Country", D.STRING)
    COUPON = FieldName("Coupon", "Coupon of a bond in % units", D.FLOAT)
    COUPON_FREQ = FieldName("Coupon Frequency", "Coupon frequency of a bond", D.FREQUENCY)
    CURRENCY = FieldName("Currency", "Currency", D.STRING)
    DATA_SOURCE = FieldName("Data Source", "Data vendor source", D.STRING)
    DATE = FieldName("Date", "Date", D.DATE)
    DATE_GENERATION = FieldName("Date Generation", "Date Generation", D.DATE_GENERATION)
    DIRTY_PRICE = FieldName("Dirty Price", "Boolean indicating if quote is dirty or clean", D.BOOL)
    DISCOUNT_BASIS = FieldName("Discount Basis", "Discount Basis", D.DAYCOUNT)
    DISCOUNT_CALENDAR = FieldName("Discount Calendar", "Discount Calendar", D.CALENDAR)
    DISCOUNT_CURVE = FieldName("Discount Curve", "Discount Curve", D.TERM_STRUCTURE_YIELD)
    END_OF_MONTH = FieldName("End Of Month", "End of month rule", D.BOOL)
    EXCOUPON_PERIOD = FieldName("Ex Coupon Period", "Ex Coupon Period", D.PERIOD)
    EXCOUPON_CALENDAR = FieldName("Ex Coupon Calendar", "Ex Coupon Calendar", D.CALENDAR)
    EXCOUPON_DAY_CONVENTION = FieldName("Ex Coupon Day Convention", "Ex Coupon Day Convention", D.DAY_CONVENTION)
    EXCOUPON_END_OF_MONTH = FieldName("Ex Coupon End Of Month", "Ex Coupon End Of Month", D.BOOL)
    EXTRAPOLATION = FieldName("Extrapolation", "Enable Extrapolation", D.BOOL)
    FACE_AMOUNT = FieldName("Face Amount", "Face amount", D.FLOAT)
    INTERPOLATION_METHOD = FieldName("Interpolation Method", "Interpolation Method", D.STRING)
    INSTRUMENT_COLLECTION = FieldName("Instrument Collection", "Collection of instruments", D.LIST)
    ISSUE_DATE = FieldName("Issue Date", "Date of issuance of a security", D.DATE)

    MATURITY_DATE = FieldName("Maturity Date", "Maturity date of a security", D.DATE)
    OBJECT = FieldName("Object", "Instantiation of a QuantLib class",
                       D.OBJECT)  # hardcoded field in creators/common; do not change
    OBJECT_ID = FieldName("Object Id", "ID of a QuantLib object", D.STRING)

    PAYMENT_BASIS = FieldName("Payment Basis", "Payment Basis", D.DAYCOUNT)
    PAYMENT_CALENDAR = FieldName("Payment Calendar", "Payment Calendar", D.CALENDAR)
    PAYMENT_DAY_CONVENTION = FieldName("Payment Day Convention", "Payment Bussiness day convention",
                                       D.DAY_CONVENTION)
    PRICE = FieldName("Price", "Price of a security", D.FLOAT)
    PRICE_FLAVOR = FieldName("Price Flavor", "Flavor such as bid, ask or mid", D.STRING)
    PRICING_ENGINE = FieldName("Pricing Engine", "Pricing Engine", D.PRICING_ENGINE)
    REDEMPTION = FieldName("Redemption", "Redemption", D.FLOAT)
    ROUNDING = FieldName("Rounding", "Decimal Places of Rounding", D.INT)
    SECURITY_DATA = FieldName("Security Data", "Security refernce data", D.DICT)
    SECURITY_ID = FieldName("Security Id", "Security identifier", D.STRING)
    SECURITY_TYPE = FieldName("Security Type", "Security Type", D.STRING)
    SECURITY_SUBTYPE = FieldName("Security Subtype", "Security Subtype", D.STRING)
    SETTLEMENT_DAYS = FieldName("Settlement Days", "Settlement days", D.INT)
    SETTLEMENT_CALENDAR = FieldName("Settlement Calendar", "Settlement Calendar", D.CALENDAR)
    TEMPLATE = FieldName("Template", "Instantiation template",
                         D.TEMPLATE)  # hardcoded field in creators/common; do not change
    TERMINATION_DAY_CONVENTION = FieldName("Termination Day Convention",
                                           "Termination day convention", D.DAY_CONVENTION)
    TICKER = FieldName("Ticker", "Ticker identifier for a security", D.STRING)
    YIELD = FieldName("Yield", "Security Yield", D.FLOAT)
    ZERO_RATE = FieldName("Zero Rate", "Zero Rate", D.FLOAT)

    # Field Name Modified Entries
    LIST_OF_DATES = _LIST(DATE, D.LIST_DATE)
    LIST_OF_ZERO_RATES = _LIST(ZERO_RATE, D.LIST_FLOAT)
    LIST_OF_COUPONS = _LIST(COUPON, D.LIST_FLOAT)

