from django.conf.urls import url
from .views import (
    EditQuizRandomView,
    AddQuestionToQuizRandomView,
    EditQuestionRandomView,
    AddAnswerToQuestionRandomView,
    EditAnswerRandomView,
    DeleteAnswerRandomView,
    DeleteQuestionRandomView
)
urlpatterns = [
    url(r'^edit_quiz/(?P<pk>\d+)/$', EditQuizRandomView.as_view(),
        {}, 'edit-quiz-random'),
    url(r'^edit_quiz/(?P<pk>\d+)/add_question/$',
        AddQuestionToQuizRandomView.as_view(),
        {}, 'add-question-to-quiz-random'),
    url(r'^edit_question/(?P<pk>\d+)/$', EditQuestionRandomView.as_view(), {},
        'edit-question-random'),
    url(r'^edit_question/(?P<pk>\d+)/add_answer/$',
        AddAnswerToQuestionRandomView.as_view(), {},
        'add-answer-to-question-random'),
    url(r'^delete_question/(?P<pk>\d+)/$', DeleteQuestionRandomView.as_view(),
        {}, 'delete-question-random'),
    url(r'^delete_answer/(?P<pk>\d+)/$', DeleteAnswerRandomView.as_view(),
        {}, 'delete-answer-random'),
    url(r'^edit_answer/(?P<pk>\d+)/$', EditAnswerRandomView.as_view(),
        {}, 'edit-answer-random'),
]

'''
urlpatterns = patterns(
    'quizblock.views',
    (r'^edit_quiz/(?P<pk>\d+)/$', EditQuizView.as_view(), {}, 'edit-quiz'),
    (r'^edit_quiz/(?P<pk>\d+)/add_question/$', AddQuestionToQuizView.as_view(),
     {}, 'add-question-to-quiz'),
    (r'^edit_question/(?P<pk>\d+)/$', EditQuestionView.as_view(), {},
     'edit-question'),
    (r'^edit_question/(?P<pk>\d+)/add_answer/$',
     AddAnswerToQuestionView.as_view(), {}, 'add-answer-to-question'),
    (r'^delete_question/(?P<pk>\d+)/$', DeleteQuestionView.as_view(), {},
     'delete-question'),
    (r'^reorder_answers/(?P<pk>\d+)/$', ReorderAnswersView.as_view(), {},
     'reorder-answer'),
    (r'^reorder_questions/(?P<pk>\d+)/$', ReorderQuestionsView.as_view(), {},
     'reorder-questions'),
    (r'^delete_answer/(?P<pk>\d+)/$', DeleteAnswerView.as_view(),
     {}, 'delete-answer'),
    (r'^edit_answer/(?P<pk>\d+)/$', EditAnswerView.as_view(),
     {}, 'edit-answer'),
)
'''
