from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from redactor.widgets import RedactorEditor

from ..nyssance.django.contrib.admin import SuperAdmin

from .models import Question, Answer


class QuestionAdminForm(forms.ModelForm):
    tags = forms.CharField(label=_('tags'), widget=forms.Textarea, required=False)

    class Meta:
        model = Question
        fields = '__all__'


class AnswerAdminForm(forms.ModelForm):
    text = forms.CharField(label=_('text'), widget=RedactorEditor())

    class Meta:
        model = Answer
        fields = '__all__'


class QuestionAdmin(SuperAdmin):
    list_display = ('title', 'summary')
    list_filter = ('title',)
    search_fields = ('title', 'summary')
    form = QuestionAdminForm


class AnswerAdmin(SuperAdmin):
    list_display = ('text', 'upvote_count', 'downvote_count')
    list_filter = ('user_id', 'question_id')
    search_fields = ('text',)
    form = AnswerAdminForm

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
