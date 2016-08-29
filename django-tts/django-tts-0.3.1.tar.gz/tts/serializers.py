# coding: utf-8
from rest_framework import serializers
from . import models


class Generation(serializers.Serializer):
    text = serializers.CharField(required=True)


class GetFile(serializers.Serializer):
    uuid = serializers.UUIDField(required=True)

    def validate_uuid(self, value):
        if not models.SoundFile.objects.filter(uuid=value).exists():
            raise serializers.ValidationError('Sound file with uuid "%s" not found' % value)
        return value
