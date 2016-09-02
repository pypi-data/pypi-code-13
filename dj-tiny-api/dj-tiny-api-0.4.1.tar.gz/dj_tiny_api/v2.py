# coding: utf-8

from functools import wraps
import logging

from django.conf import settings
from django.conf.urls import url as django_url
from django.http import HttpResponse
from typeddict import fields as f
from typeddict import TypedDict
from typeddict.validators import DummyValidator, ValidationError
from typeddict.api import opt
import ujson


logger = logging.getLogger(__name__)


class ApiError(Exception):
    def __init__(self, td, *args, **kwargs):
        self.td = td
        return super().__init__(*args, **kwargs)


class TdSimplifier(object):
    @staticmethod
    def serialize(data):
        return data.simplify()


class TdField(f.FieldAsIs):
    simplifier = staticmethod(TdSimplifier)
    validator = staticmethod(DummyValidator)


class BaseResult(TypedDict):

    ERROR_AUTH = "api:auth"
    ERROR_BAD_JSON = "api:bad_json"
    ERROR_EMPTY_REQUEST = "api:empty_request"
    ERROR_REQUEST_NOT_DICT = "api:request_data_not_dict"
    ERROR_UNKNOWN = "api:unknown"
    ERROR_UNKNOWN_ACCEPT = "api:unknown_accept"
    ERROR_VALIDATION = "api:validation"

    data = opt(TdField)
    error = f.StringNotEmpty(required=False, choices=[
        ERROR_AUTH,
        ERROR_BAD_JSON,
        ERROR_EMPTY_REQUEST,
        ERROR_REQUEST_NOT_DICT,
        ERROR_UNKNOWN,
        ERROR_UNKNOWN_ACCEPT,
        ERROR_VALIDATION,
    ])


def unknown_error():
    return BaseResult(error=BaseResult.ERROR_UNKNOWN)


class Endpoint(object):

    ACCEPT_JSON = "application/json"
    ACCEPTED_FORMATS = (
        ACCEPT_JSON,
    )

    def __init__(
        self,
        data_spec=None,
        result_spec=None,
        slug=None,
        url=None,
    ):
        self.data_spec = data_spec
        self.result_spec = result_spec
        self.slug = slug
        self.url = url

    def __call__(self, f):

        self.slug = self.slug or f.__name__
        self.f = f

        @wraps(f)
        def wrapped_f(request, *args, **kwargs):
            self.request = request
            view_result = result = None
            self.request_id = request.META.get("HTTP_REQUEST_ID")
            self.format = request.META.get("HTTP_ACCEPT")
            try:
                if self.format not in self.ACCEPTED_FORMATS:
                    raise ApiError(td=BaseResult(error=BaseResult.ERROR_UNKNOWN_ACCEPT))

                self.auth_check()
                self._get_data()
                self._validate_data()

                kwargs["request"] = request

                view_result = f(self.data, *args, **kwargs)
            except ApiError as e:
                result = e.td
            except Exception as e:
                self._log_error(msg=str(e))
                result = unknown_error()

            if isinstance(view_result, HttpResponse):
                return view_result

            if result is None:
                result = BaseResult(data=view_result)
            body = result.dumps(result)

            if self.format == self.ACCEPT_JSON:
                return HttpResponse(body, status=200, content_type=self.format)
            else:
                return HttpResponse(body, status=200, content_type=self.ACCEPT_JSON)

        if self.url:
            urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])
            url = django_url(self.url, wrapped_f, name=self.slug)
            urlconf.urlpatterns.append(url)

        return wrapped_f

    def _log_error(self, msg):
        logger.error(
            "request_id: {}, message: {}".format(self.request_id, msg),
            exc_info=True,
        )

    def auth_check(self):
        pass

    def _get_data(self):
        if self.request.method == 'POST':
            content_type = self.request.META.get('CONTENT_TYPE')
            if content_type == 'application/json':
                if not self.request.body:
                    td = BaseResult(error=BaseResult.ERROR_EMPTY_REQUEST)
                    raise ApiError(td=td)

                try:
                    data = ujson.loads(self.request.body)
                except ValueError as e:
                    self._log_error(msg=str(e))
                    td = BaseResult(error=BaseResult.ERROR_BAD_JSON)
                    raise ApiError(td=td)
            else:
                data = self.request.POST.dict()

        elif self.request.method == 'GET':
            data = self.request.GET.dict()
        else:
            raise ApiError(td=unknown_error())
        self.raw_data = data

    def _validate_data(self):
        if self.data_spec is not None:
            if self.raw_data is None:
                td = BaseResult(error=BaseResult.ERROR_EMPTY_REQUEST)
                raise ApiError(td=td)
            elif not isinstance(self.raw_data, dict):
                td = BaseResult(error=BaseResult.ERROR_REQUEST_NOT_DICT)
                raise ApiError(td=td)

            try:
                self.data = self.data_spec(**self.raw_data)
            except ValidationError as e:
                self._log_error(msg=str(e))
                td = BaseResult(error=BaseResult.ERROR_VALIDATION)
                raise ApiError(td=td)
