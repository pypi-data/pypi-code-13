""" Async jobs
"""
import logging
from zope import event
from plone import api
from zope.component import queryAdapter
from eea.relations.events import ForwardRelatedItemsWorkflowStateChanged
from eea.relations.events import BackwardRelatedItemsWorkflowStateChanged
from eea.relations.rules.interfaces import IContextWrapper
logger = logging.getLogger('eea.relations')


def forward_transition_change(obj, transition):
    """ Forward workflow state changed related items
    """
    relatedItems = obj.getRelatedItems()
    if not relatedItems:
        return

    succeeded = set()
    failed = set()
    for item in relatedItems:
        try:
            api.content.transition(obj=item, transition=transition)
        except Exception, err:
            logger.debug("%s: %s", item.absolute_url(), err)
            failed.add(item.absolute_url())
        else:
            succeeded.add(item.absolute_url())

    if not (succeeded or failed):
        return

    wrapper = queryAdapter(obj, IContextWrapper)
    if wrapper is not None:
        obj = wrapper(
            related_items_changed=succeeded,
            related_items_unchanged=failed,
            related_items_transition=transition)

    event.notify(ForwardRelatedItemsWorkflowStateChanged(obj))


def backward_transition_change(obj, transition):
    """ Backward workflow state changed related items
    """
    backRefs = obj.getBRefs()
    if not backRefs:
        return

    succeeded = set()
    failed = set()
    for item in backRefs:
        try:
            api.content.transition(obj=item, transition=transition)
        except Exception, err:
            logger.debug("%s: %s", item.absolute_url(), err)
            failed.add(item.absolute_url())
        else:
            succeeded.add(item.absolute_url())

    if not (succeeded or failed):
        return

    wrapper = queryAdapter(obj, IContextWrapper)
    if wrapper is not None:
        obj = wrapper(
            related_items_changed=succeeded,
            related_items_unchanged=failed,
            related_items_transition=transition)

    event.notify(BackwardRelatedItemsWorkflowStateChanged(obj))
