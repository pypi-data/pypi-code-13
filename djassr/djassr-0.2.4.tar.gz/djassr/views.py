import urllib
import uuid

from django.conf import settings

from rest_framework import generics
from rest_framework.response import Response

import s3sign

from . import serializers


_DEFAULT_EXPIRE = 60  # seconds
DEFAULT_EXPIRE = getattr(settings, 'DJASSR_DEFAULT_EXPIRE', _DEFAULT_EXPIRE)


class BaseGetSignature(generics.GenericAPIView):
    def post(self, request):
        args = self._get_args(request)
        signer = self.signer()
        data = signer.get_signed_url(*args)
        return Response(data)

    def get_expire(self, request):
        return DEFAULT_EXPIRE


class BaseGetPUTSigneature(BaseGetSignature):
    serializer_class = serializers.PUTSignatureSerializer

    def _get_args(self, request):
        file_name = self.get_object_name(request)
        mime_type = request.data.get('mime_type')
        expire = self.get_expire(request)
        return file_name, expire, mime_type

    def get_object_name(self, request):
        file_name = request.data.get('file_name')
        new_file_name = str(uuid.uuid4())
        if file_name:
            new_file_name += '.' + file_name.split('.')[-1]

        object_name = urllib.parse.quote_plus(new_file_name)
        return object_name


class GetPUTSignature(BaseGetPUTSigneature):
    signer = s3sign.S3PUTSigner


class GetPUTPublicSignature(BaseGetPUTSigneature):
    signer = s3sign.S3PUTPublicSigner


class GetGETSignature(BaseGetSignature):

    serializer_class = serializers.GETSignatureSerializer

    signer = s3sign.S3GETSigner

    def _get_args(self, request):
        expire = self.get_expire(request)
        return request.data.get('object_name'), expire
