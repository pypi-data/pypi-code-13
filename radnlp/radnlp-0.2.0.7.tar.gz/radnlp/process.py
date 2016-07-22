from . import utils
from . import schema
from . import split
from . import classify

def process_report(report, modifier, target,
                   classification_rules,
                   category_rules,
                   _schema,
                   **kwargs):
    """
    """
    markup = utils.mark_report(split.get_sentences(report),
                         modifier,
                         target)
    return  classify.classify_document_targets(markup,
                                          classification_rules,
                                          category_rules,
                                          severity_rules,
                                          _schema,
                                          kwargs)
