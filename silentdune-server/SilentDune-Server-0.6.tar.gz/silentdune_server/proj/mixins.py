from django.utils.decorators import decorator_from_middleware

from proj.middleware import RequestLogMiddleware

from rest_framework.decorators import list_route
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from proj.serializer import RecordCountSerializer

# Note: This doesn't seem to work with viewsets.ModelViewSet
# class RequestLogViewMixin(object):
#     """
#     Adds RequestLogMiddleware to any Django View by overriding as_view.
#     """
#
#     # TODO: Add activity logging code here somewhere.
#
#     @classmethod
#     def as_view(cls, **initkwargs):
#         view = super(RequestLogViewMixin, cls).as_view(**initkwargs)
#         return view


