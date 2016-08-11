from zope import schema
from z3c.form.interfaces import ITextWidget
from collective.z3cform.phonewidget import _
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


class IPhoneWidget(ITextWidget):
    """A Phone widget ( html5 type="tel")"""
