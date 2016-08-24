from django.conf.urls import url
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
urlpatterns = router.urls


urlpatterns += [
    # 问答:
    url(r'^questions/$', views.QuestionList.as_view()),
    url(r'^questions/(?P<pk>[0-9]+)/$', views.QuestionDetail.as_view()),
    url(r'^questions/(?P<pk>[0-9]+)/answers/$', views.QuestionAnswerList.as_view()),
    url(r'^answers/(?P<pk>[0-9]+)/$', views.AnswerDetail.as_view()),
    url(r'^answers/(?P<pk>[0-9]+)/votes/$', views.AnswerVoteList.as_view()),
    url(r'^votes/(?P<pk>[0-9]+)/$', views.VoteDetail.as_view()),

    # 卡片:
    url(r'^cards/$', views.CardList.as_view()),
    url(r'^cards/(?P<pk>[0-9]+)/$', views.CardDetail.as_view()),
    url(r'^cards/(?P<pk>[0-9]+)/comments/$', views.CardCommentList.as_view()),
    url(r'^cards/(?P<pk>[0-9]+)/likes/$', views.CardLikeList.as_view()),

    url(r'^comments/(?P<pk>[0-9]+)/$', views.CardCommentDetail.as_view()),
    url(r'^comments/(?P<pk>[0-9]+)/likes/$', views.CommentLikeList.as_view()),

    url(r'^likes/(?P<pk>[0-9]+)/$', views.CardLikeDetail.as_view()),
    # 评论:
    # 当起时间
    url(r'^time/$', views.CurTimeView.as_view()),
]
