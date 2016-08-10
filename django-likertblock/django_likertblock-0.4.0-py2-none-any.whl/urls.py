from django.conf.urls import url
from .views import (
    EditQuestionnaireView, DeleteQuestionView, ReorderQuestionsView,
    AddQuestionToQuestionnaireView, EditQuestionView,
)

urlpatterns = [
    url(r'^edit_questionnaire/(?P<pk>\d+)/$', EditQuestionnaireView.as_view(),
        {}, 'edit-questionnaire'),
    url(r'^edit_questionnaire/(?P<pk>\d+)/add_question/$',
        AddQuestionToQuestionnaireView.as_view(), {},
        'add-question-to-questionnaire'),
    url(r'^edit_question/(?P<pk>\d+)/$', EditQuestionView.as_view(), {},
        'likert-edit-question'),
    url(r'^delete_question/(?P<pk>\d+)/$', DeleteQuestionView.as_view(), {},
        'likert-delete-question'),
    url(r'^reorder_questions/(?P<pk>\d+)/$', ReorderQuestionsView.as_view(),
        {}, 'likert-reorder-questions'),
]
