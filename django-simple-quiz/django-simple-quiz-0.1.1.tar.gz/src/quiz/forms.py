from django import forms
from django.apps import apps

Question = apps.get_model('quiz', 'Question')
Quiz = apps.get_model('quiz', 'Quiz')
QuizResult = apps.get_model('quiz', 'QuizResult')
QuizResultItem = apps.get_model('quiz', 'QuizResultItem')


class QuizResultItemForm(forms.ModelForm):
    """Form to save the result of each `Question` in a `QuizResultItem`"""

    class Meta:
        model = QuizResultItem
        fields = [
            'question',
            'answer_text',
            'answer_choice',
        ]
        widgets = {
            'question': forms.HiddenInput,
            'answer_choice': forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        self.question = kwargs['initial'].get('question')
        super(QuizResultItemForm, self).__init__(*args, **kwargs)

        if self.question.question_type == Question.CHOICE:
            self.fields['answer_choice'].empty_label = None
            self.fields['answer_choice'].queryset = (
                self.question.available_answers.all())
            del self.fields['answer_text']
        else:
            del self.fields['answer_choice']

        del self.fields['question']

    def get_question_text(self):
        return self.question.question

    def clean(self):
        data = super(QuizResultItemForm, self).clean()
        data['question'] = self.question
        return data

    def save(self, result, commit=True):
        result_item = super(QuizResultItemForm, self).save(commit=False)
        result_item.quiz_result = result
        result_item.save()
        return result_item


class QuizResultForm(forms.ModelForm):

    class Meta:
        model = QuizResult
        fields = [
            'quiz',
            'name',
            'email',
        ]
        widgets = {
            'quiz': forms.HiddenInput,
        }
