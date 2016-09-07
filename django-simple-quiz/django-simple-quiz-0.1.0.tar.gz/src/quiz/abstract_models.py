from __future__ import unicode_literals

import os

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel

from quiz.managers import QuizQuerySet


@python_2_unicode_compatible
class AbstractQuiz(TimeStampedModel):
    name = models.CharField(max_length=150)
    start_with_signup = models.BooleanField(default=True)

    objects = QuizQuerySet.as_manager()

    class Meta:
        abstract = True
        app_label = 'quiz'
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class AbstractQuestion(models.Model):
    OPEN, CHOICE = 'text', 'choice'
    QUESTION_TYPE_CHOICES = Choices(
        (CHOICE, _("Multiple choice")),
        (OPEN, _("Open question")),
    )

    quiz = models.ForeignKey('quiz.Quiz', related_name='questions')
    question = models.CharField(max_length=150)
    question_type = models.CharField(
        max_length=50, choices=QUESTION_TYPE_CHOICES, default=CHOICE)
    position = models.IntegerField(default=0)

    class Meta:
        abstract = True
        app_label = 'quiz'
        ordering = ['position']
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
        return self.question


def handle_upload_answer_image(instance, filename):
    """Handle the upload filename / location for our answer image."""
    fname, ext = os.path.splitext(filename)
    return os.path.join(
        'quiz', slugify(instance.question.quiz.name),
        '%s%s' % (slugify(instance.answer), ext))


@python_2_unicode_compatible
class AbstractAnswerChoice(models.Model):
    question = models.ForeignKey(
        'quiz.Question', related_name='available_answers')
    answer = models.CharField(max_length=150)
    image = models.ImageField(
        blank=True, null=True, upload_to=handle_upload_answer_image)
    position = models.IntegerField(default=0)

    class Meta:
        abstract = True
        app_label = 'quiz'
        ordering = ['position']
        verbose_name = _("Choice")
        verbose_name_plural = _("Choices")

    def __str__(self):
        return self.answer


@python_2_unicode_compatible
class AbstractQuizResult(TimeStampedModel):
    quiz = models.ForeignKey('quiz.Quiz', related_name='results')
    name = models.CharField(max_length=150)
    email = models.EmailField()
    date_participated = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True
        app_label = 'quiz'
        verbose_name = _("Quiz Result")
        verbose_name_plural = _("Quiz Results")

    def __str__(self):
        return self.name


class AbstractQuizResultItem(TimeStampedModel):
    quiz_result = models.ForeignKey(
        'quiz.QuizResult', related_name='result_items')
    question = models.ForeignKey('quiz.Question', related_name='+')
    answer_text = models.TextField(blank=True, null=True)
    answer_choice = models.ForeignKey(
        'quiz.AnswerChoice', related_name='+', blank=True, null=True)

    class Meta:
        abstract = True
        app_label = 'quiz'
        verbose_name = _("Quiz Result Item")
        verbose_name_plural = _("Quiz Result Items")
