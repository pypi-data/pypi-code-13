# -*- coding: utf-8 -*-

"""
.. module:: dreq.__init__.py

   :copyright: Copyright "February 27, 2016", IPSL
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Library constructor.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
__title__ = 'dreq'
__version__ = '0.2.0.1'
__author__ = 'IPSL'
__license__ = 'GPL'
__copyright__ = 'Copyright 2016 IPSL'


from dreq._initializer import initialize

from dreq.constants import LABEL_MAP
from dreq.constants import CONFIG_FILENAME
from dreq.constants import CONTENT_FILENAME

from dreq.config.wrapper import Wrapper as ConfigWrapper
from dreq.config.table import Table as ConfigTable
from dreq.config.table_attribute import TableAttribute as ConfigTableAttribute
from dreq.content.query import pluck as query
from dreq.content.wrapper import Wrapper as ContentWrapper
from dreq.content.section import Section as ContentSection
from dreq.content.section_item import SectionItem as ContentSectionItem
