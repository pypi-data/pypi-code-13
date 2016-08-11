from zope import schema
from z3c.form.interfaces import ITextWidget
from collective.z3cform.quantitywidget import _
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

class IQuantityWidget(ITextWidget):

    step = schema.Float(title=_(u"step"),
        required=True,
        default=1.0)

    min_value = schema.Float(title=_(u"min"),
        required=True,
        default=1.0)

    max_value = schema.Float(title=_(u"max"), required=False)

    unit = schema.TextLine(title=_(u"Unit"), required=False)

    unit_display = schema.Choice(title=_(u"Display unit"),
        description=_(u"label_unit_dipsplay", default=u"Hide or display unit before or after quantity field"),
        vocabulary=SimpleVocabulary([
            SimpleTerm('hidden', 'hidden', _(u"label_hidden", default=u"Hidden")),
            SimpleTerm('before', 'before', _(u"label_before", default=u"Before")),
            SimpleTerm('after', 'after', _(u"label_after", default=u"After")),
        ]),
        required=True,
        default='after')
