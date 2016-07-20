"""
FlashXmlGraphics to ScalableVectorGraphic converter.
"""

from lxml import etree

from .svgtarget import SVGTarget


def fxg2svg(fxg_bytes, fontdir=None):
    return etree.parse(fxg_bytes, etree.XMLParser(target=SVGTarget(fontdir=fontdir)))
