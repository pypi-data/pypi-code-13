from django import forms


class QAQuestionForm(forms.Form):
    title = forms.CharField(label='title', required=True)
    description = forms.CharField(
        label='description', required=True)
    tags = forms.CharField(
        label='tags', help_text='tags separated by comma',
        required=True)


class QAAnswerForm(forms.Form):
    answer_text = forms.CharField(label='answer', required=True)
