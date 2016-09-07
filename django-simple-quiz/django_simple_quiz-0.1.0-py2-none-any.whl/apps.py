from django.apps import AppConfig
from django.utils.translation import ugettext_lazy


class QuizAppConfig(AppConfig):
    label = 'Quiz'
    name = 'quiz'
    verbose_name = ugettext_lazy("Quiz App")
