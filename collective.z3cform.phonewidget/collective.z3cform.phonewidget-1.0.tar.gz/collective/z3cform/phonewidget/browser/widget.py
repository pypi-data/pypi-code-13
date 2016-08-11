import logging
from zope import schema
import zope.interface
import zope.component
import zope.schema.interfaces
from z3c.form.interfaces import IWidget, ITextWidget, IFormLayer, IFieldWidget
from zope.schema.fieldproperty import FieldProperty
from zope.schema.interfaces import IInt, IFloat
from zope.interface import Invalid
from z3c.form.widget import Widget, FieldWidget
from z3c.form.browser.text import TextWidget
from z3c.form.validator import SimpleFieldValidator
from collective.z3cform.phonewidget.interfaces import IPhoneWidget
from collective.z3cform.phonewidget import _
try:
    import phonenumbers
    from phonenumbers.phonenumberutil import NumberParseException
    has_phonenumbers = True
except:
    has_phonenumbers = False
    
LOG = logging.getLogger(__name__)
    
@zope.interface.implementer_only(IPhoneWidget)
class PhoneWidget(TextWidget):
    """PhoneWidget"""


@zope.component.adapter(zope.schema.interfaces.IField, IFormLayer)
@zope.interface.implementer(IFieldWidget)
def PhoneFieldWidget(field, request):
    """IFieldWidget factory for PhoneWidget."""
    return FieldWidget(field, PhoneWidget(request))


class PhoneWidgetValidator(SimpleFieldValidator):
    
    def validate(self, value, force=False):
        if has_phonenumbers:
            try:
                phonenumbers.parse(value, None)
            except NumberParseException as e:
                raise Invalid(_(unicode(e._msg)))
        return super(PhoneWidgetValidator, self).validate(value, force)
        
