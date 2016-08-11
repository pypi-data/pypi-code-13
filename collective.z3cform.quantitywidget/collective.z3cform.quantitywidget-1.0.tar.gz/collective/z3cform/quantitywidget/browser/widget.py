import logging
from zope import schema
import zope.interface
import zope.component
import zope.schema.interfaces
from decimal import Decimal
from z3c.form.interfaces import IWidget, ITextWidget, IFormLayer, IFieldWidget
from zope.schema.fieldproperty import FieldProperty
from zope.schema.interfaces import IInt, IFloat
from z3c.form.widget import Widget, FieldWidget
from z3c.form.browser.text import TextWidget
from z3c.form.validator import SimpleFieldValidator
from z3c.form.converter import FloatDataConverter, IntegerDataConverter, DecimalDataConverter
from collective.z3cform.quantitywidget.interfaces import IQuantityWidget
LOG = logging.getLogger(__name__)
    
@zope.interface.implementer_only(IQuantityWidget)
class QuantityWidget(TextWidget):
    """QuantityWidget"""
    
    step = FieldProperty(IQuantityWidget['step'])
    min_value = FieldProperty(IQuantityWidget['min_value'])
    max_value = FieldProperty(IQuantityWidget['max_value'])
    unit = FieldProperty(IQuantityWidget['unit'])
    unit_display = FieldProperty(IQuantityWidget['unit_display'])

    @property
    def stepIsInteger(self):
        return int(self.step) == self.step


@zope.component.adapter(zope.schema.interfaces.IField, IFormLayer)
@zope.interface.implementer(IFieldWidget)
def QuantityFieldWidget(field, request):
    """IFieldWidget factory for QuantityWidget."""
    return FieldWidget(field, QuantityWidget(request))


class QuantityDataConverter(object):

    def toWidgetValue(self, value):
        """See interfaces.IDataConverter"""
        if value is self.field.missing_value:
            return u''
        if self.widget.stepIsInteger:
            value = int(value)
        return str(self.formatter.format(value)).replace(',','.')


class QuantityIntDataConverter(QuantityDataConverter, IntegerDataConverter):
    """We store an int bu display a text."""
    zope.component.adapts(
        zope.schema.interfaces.IInt, IQuantityWidget)


class QuantityFloatDataConverter(QuantityDataConverter, FloatDataConverter):
    """We store a float bu display a text."""
    zope.component.adapts(
        zope.schema.interfaces.IFloat, IQuantityWidget)

    def toFieldValue(self, value):
        """See interfaces.IDataConverter"""
        if value == u'':
            return self.field.missing_value
        try:
            value = float(value.replace(',','.'))
            value = self.formatter.format(value)
            value = self.formatter.parse(value)
            return value
        except zope.i18n.format.NumberParseError:
            raise FormatterValidationError(self.errorMessage, value)

class QuantityDecimalDataConverter(QuantityDataConverter, DecimalDataConverter):
    """We store a decimal bu display a text."""
    zope.component.adapts(
        zope.schema.interfaces.IDecimal, IQuantityWidget)


class QuantityWidgetValidator(SimpleFieldValidator):
    
    def validate(self, value, force=False):
        value = float(value)
        if getattr(self.widget, 'min_value', None) != None and value <= self.widget.min_value:
            raise ValueError("The value is too low.")
        if getattr(self.widget, 'max_value', None) != None and value >= self.widget.max_value:
            raise ValueError("The value is too high.")
        if getattr(self.widget, 'step', None) != None and value%self.widget.step != 0:
            raise ValueError("The value does not conform to step.")
        
