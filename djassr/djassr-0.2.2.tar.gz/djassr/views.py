import urllib
import uuid

from rest_framework import generics
from rest_framework.response import Response

import s3sign

from . import serializers


DEFAULT_VALID = 60  # seconds


class BaseGetSignature(generics.GenericAPIView):
    def post(self, request):
        args = self._get_args(request)
        signer = self.signer()
        data = signer.get_signed_url(*args)
        return Response(data)

    def get_valid(self, request):
        return DEFAULT_VALID


class BaseGetPUTSigneature(BaseGetSignature):
    serializer_class = serializers.PUTSignatureSerializer

    def _get_args(self, request):
        file_name = self.get_object_name(request)
        mime_type = request.data.get('mime_type')
        valid = self.get_valid(request)
        return file_name, valid, mime_type

    def get_object_name(self, request):
        file_name = request.data.get('file_name')
        extension = file_name.split('.')[-1]
        file_name = str(uuid.uuid4()) + '.' + extension
        object_name = urllib.parse.quote_plus(file_name)
        return object_name


class GetPUTSignature(BaseGetPUTSigneature):
    signer = s3sign.S3PUTSigner


class GetPUTPublicSignature(BaseGetPUTSigneature):
    signer = s3sign.S3PUTPublicSigner


class GetGETSignature(BaseGetSignature):

    serializer_class = serializers.GETSignatureSerializer

    signer = s3sign.S3GETSigner

    def _get_args(self, request):
        valid = self.get_valid(request)
        return request.data.get('object_name'), valid
