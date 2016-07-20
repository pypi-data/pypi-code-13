from lxml import etree
import logging


logger = logging.getLogger(__name__)


class DefaultTagProcessor(object):

    def on_start(self, target):
        target.element = etree.SubElement(
            target.element,
            "foreignObject"
        )

    def on_end(self, target):
        parent = target.element.getparent()
        if parent is not None:
            target.element = parent


    def on_data(self, target):
        target.element.text = target.text
