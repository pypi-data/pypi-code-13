from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField, SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer

from ..nyssance.rest_framework.mixins import IdStrMixin, ImageUrlsMixin
from . import mixins
from ..cards.models import Card, SITE_CHOICES
from ..comments.models import Comment
from ..likes.models import Like
from ..questions.models import Question, Answer, Vote


class QuestionDetailSerializer(mixins.UserMixin, ModelSerializer):
    class Meta:
        model = Question
        exclude = ('updated_time', 'image_urls', 'username', 'user_image_urls', 'user_id')


class AnswerDetailSerializer(mixins.UserMixin, ModelSerializer):
    class Meta:
        model = Answer
        exclude = ('updated_time', 'username', 'user_id', 'user_image_urls')


class VoteDetailSerializer(IdStrMixin, mixins.UserMixin, ModelSerializer):
    class Meta:
        model = Vote
        exclude = ('updated_time', 'username', 'user_id', 'user_image_urls')

    def validate_type(self, value):
        if value not in ['u', 'd']:
            raise ValidationError('{} not allow'.format(value))
        return value


class CardListSerialiser(IdStrMixin, mixins.UserMixin, ImageUrlsMixin, ModelSerializer):
    site = SerializerMethodField()

    class Meta:
        model = Card
        exclude = ('image_urls', 'updated_time', 'user_id', 'username', 'user_image_urls')

    def get_site(self, value):
        size_list = [siteinfo[1] for siteinfo in SITE_CHOICES if siteinfo[0] == value.site]
        return size_list[0] if size_list else ''


class CardCommentListSerializer(IdStrMixin, mixins.UserMixin, ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('updated_time', 'username', 'user_id', 'user_image_urls')


class CardLikeListSerializer(IdStrMixin, mixins.UserMixin, mixins.CardMixin, ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'id_str', 'created_time', 'user', 'card')


class CommentLikeSerializer(Serializer):
    comment_id = IntegerField()
