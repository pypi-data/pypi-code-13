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
            self.process_children(target)


    def on_data(self, target):
        target.element.text = target.text


    def process_children(self, target):
        element = target.element
        logger.debug("Process chidlren %s" % target.element.tag)
        clippathid = None
        maskedElements = []
        for e in element:
            logger.debug("chidlren %s" % e.tag)
            if clippathid:
                if e.tag == "g":
                    g = e
                    g.attrib['clip-path'] = 'url(#%s)' % clippathid
                else:
                    g = etree.Element(
                        "g",
                        **{'clip-path': 'url(#%s)' % clippathid}
                    )
                    g.append(e)
                maskedElements.append(g)
            if e.tag == "clipPath":
                clippathid = e.attrib['id']
        logger.debug(maskedElements)
        for e in maskedElements:
            element.append(e)

