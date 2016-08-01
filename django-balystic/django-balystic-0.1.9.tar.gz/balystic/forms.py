from django import forms
from django.forms import widgets


class QAQuestionForm(forms.Form):
    title = forms.CharField(label='title', required=True)
    description = forms.CharField(
        label='description', required=True)
    tags = forms.CharField(
        label='tags', help_text='tags separated by comma',
        required=True)


class QAAnswerForm(forms.Form):
    answer_text = forms.CharField(label='answer', required=True)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=widgets.PasswordInput)
