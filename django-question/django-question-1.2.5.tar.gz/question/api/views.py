from django.utils import timezone
from rest_framework import exceptions, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..nyssance.rest_framework.permissions import IsOwnerOrReadOnly

from . import serializers
from ..cards.models import Card
from ..comments.models import Comment
from ..likes.models import Like
from ..nyssance.django.db.utils import get_pk_int, db_slave, get_object_or_none, get_user_id, db_master
from ..nyssance.rest_framework.mixins import PutToPatchMixin
from ..questions.models import Question, Answer, Vote


class UserQuestionList(generics.ListAPIView):
    """用户 : 问题"""
    serializer_class = serializers.QuestionDetailSerializer

    def get_queryset(self):
        user_id = get_pk_int(self)
        return Question.objects.filter(user_id=user_id)


class QuestionList(generics.ListCreateAPIView):
    """问题"""
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionDetailSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id,
                        username=self.request.user.username,
                        user_image_urls=self.request.user.image_urls)


class QuestionDetail(PutToPatchMixin, generics.RetrieveUpdateDestroyAPIView):
    """问题 详情"""
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionDetailSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)


class QuestionAnswerList(generics.ListCreateAPIView):  # FIXME  List走从库, Create走主库
    """问题 : 回答"""
    serializer_class = serializers.AnswerDetailSerializer

    def get_queryset(self):
        return Answer.objects.filter(question_id=get_pk_int(self))

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id,
                        username=self.request.user.username,
                        user_image_urls=self.request.user.image_urls,
                        question_id=get_pk_int(self))


class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    """删除 回答"""
    queryset = Answer.objects.all()
    serializer_class = serializers.AnswerDetailSerializer


class AnswerVoteList(generics.CreateAPIView):
    """回答 : 投票"""
    serializer_class = serializers.VoteDetailSerializer

    def get_queryset(self):
        return Vote.objects.all().using(db_master(self.request.user.id))

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id,
                        username=self.request.user.username,
                        user_image_urls=self.request.user.image_urls,
                        answer_id=int(get_pk_int(self)),
                        type=self.request.POST.get('type'))


class VoteDetail(PutToPatchMixin, generics.RetrieveUpdateDestroyAPIView):  # FIXME 主从库分开:
    """投票 详情"""
    queryset = Vote.objects.all()
    serializer_class = serializers.VoteDetailSerializer

    def perform_update(self, serializer):
        serializer.save(type=str(self.request.data.get('type')))


class CardList(generics.ListAPIView):
    '''卡片'''
    serializer_class = serializers.CardListSerialiser

    def get_queryset(self):
        return Card.objects.all()

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id,
                        username=self.request.user.username,
                        user_image_urls=self.request.user.image_urls,
                        object_id=1)


class CardDetail(generics.RetrieveAPIView):
    '''卡片： 详情'''
    serializer_class = serializers.CardListSerialiser

    def get_queryset(self):
        return Card.objects.all()


class CardCommentList(generics.ListCreateAPIView):
    '''卡片 评论 '''

    serializer_class = serializers.CardCommentListSerializer

    def get_queryset(self):
        return Comment.objects.filter(card_id=get_pk_int(self))
#         return Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id,
                        username=self.request.user.username,
                        user_image_urls=self.request.user.image_urls,
                        card_id=get_pk_int(self),
                        )


class CardCommentDetail(generics.DestroyAPIView):

    serializer_class = serializers.CardLikeListSerializer

    def get_queryset(self):
        return Comment.objects.all()

    def destroy(self, request, *args, **kwargs):
        pk = get_pk_int(self)
        comments = Comment.objects.filter(pk=(get_pk_int(self))).using(db_slave(get_user_id(pk)))
        if comments:
            for commentItem in comments:
                if get_user_id(commentItem.card_id) != get_user_id(pk):
                    instance = self.get_object().using(db_master(get_user_id(commentItem.card_id)))
                    instance.delete()
            comments.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise exceptions.NotFound

    def retrieve(self, request, *args, **kwargs):
        return generics.RetrieveDestroyAPIView.retrieve(self, request, *args, **kwargs)


class CommentLikeList(generics.CreateAPIView):

    serializer_class = serializers.CommentLikeSerializer

    def create(self, request, *args, **kwargs):
        pk = get_pk_int(self)
        comment = get_object_or_none(Comment, using=db_slave(get_user_id(pk), pk=pk))
        if comment:
            comment.like_count += 1
            comment.save()


class CardLikeDetail(generics.DestroyAPIView):
    serializers_class = serializers.CardLikeListSerializer

    def get_queryset(self):
        return Like.objects.all()

    def destroy(self, request, *args, **kwargs):
        pk = get_pk_int(self)
        likes = Like.objects.filter(pk=(get_pk_int(self))).using(db_slave(get_user_id(pk)))
        if likes:
            for likeItem in likes:
                if get_user_id(likeItem.card_id) != get_user_id(pk):
                    instance = self.get_object().using(db_master(get_user_id(likeItem.card_id)))
                    instance.delete()
            likes.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise exceptions.NotFound


class CardLikeList(generics.ListCreateAPIView):
    '''卡片 喜欢'''
    serializer_class = serializers.CardLikeListSerializer

    def get_queryset(self):
        return Like.objects.filter(card_id=get_pk_int(self))

    def perform_create(self, serializer):
        pk = get_pk_int(self)
        card = get_object_or_none(Card, using=db_slave(get_user_id(pk)), pk=pk)
        serializer.save(user_id=self.request.user.id,
                        username=self.request.user.username,
                        user_image_urls=self.request.user.image_urls,
                        card_id=get_pk_int(self),
                        card_image_urls=card.image_urls,
                        card_caption=card.caption
                        )


class CurTimeView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return Response({'current_time': timezone.now()})
