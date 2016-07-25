# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from .request import (
    Request,
)

from .response import (
    FileResponse,
    HtmlResponse,
    JsonResponse,
    Response,
    template_or_json_response,
    TemplateResponse,
    TerminatingResponse,
    wrapped_template_or_json_response,
    WrappedTemplateResponse,
)

from .utils import (
    disinfect_or_json_400,
)

from .gate import (
    Gate,
)

from . import (
    utils,
)

__version__ = '0.3.4'

__package__ = 'poort'
__title__ = 'Poort'
__description__ = 'Poort: The quick gateway.'
__uri__ = 'https://github.com/corverdevelopment/Poort/'

__author__ = 'Nils Corver'
__email__ = 'nils@corverdevelopment.nl'

__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2016 Corver Development B.V.'

__all__ = [
    'Request',

    'FileResponse',
    'HtmlResponse',
    'JsonResponse',
    'Response',
    'template_or_json_response',
    'TemplateResponse',
    'TerminatingResponse',
    'wrapped_template_or_json_response',
    'WrappedTemplateResponse',

    'Gate',

    'disinfect_or_json_400',

    'utils',
]
