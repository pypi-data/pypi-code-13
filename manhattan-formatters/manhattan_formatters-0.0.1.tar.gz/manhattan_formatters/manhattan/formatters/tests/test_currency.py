from manhattan.formatters import currency


def test_price():
    """Format an integer as a price"""

    # Check default format is correct
    assert currency.price(200) == '£2.00'
    assert currency.price(200000) == '£2,000.00'

    # Check user defined symbol
    assert currency.price(200, '$') == '$2.00'

    # Check user defined unit conversion
    assert currency.price(200, '$', 1) == '$200.00'