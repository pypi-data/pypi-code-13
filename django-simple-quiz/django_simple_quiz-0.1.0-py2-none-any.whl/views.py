from collections import OrderedDict

from django.apps import apps
from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views.generic import TemplateView
from formtools.wizard.views import SessionWizardView

from quiz import forms

Quiz = apps.get_model('quiz', 'Quiz')
Question = apps.get_model('quiz', 'Question')


class QuizWizard(SessionWizardView):
    template_name = 'quiz/wizard.html'
    item_form = forms.QuizResultItemForm
    signup_form = forms.QuizResultForm
    form_list = [
        forms.QuizResultForm,
    ]

    def dispatch(self, request, *args, **kwargs):
        self.object = Quiz.objects.get_current()
        if not self.object:
            raise Http404("Quiz doesn't exist.")
        return super(QuizWizard, self).dispatch(request, *args, **kwargs)

    def get_form_list(self):
        form_list = OrderedDict()
        if self.object.start_with_signup:
            form_list['0'] = self.signup_form

        for i, q in enumerate(self.object.questions.all(), len(form_list)):
            form_list[str(i)] = self.item_form

        if not self.object.start_with_signup:
            form_list[str(len(form_list))] = self.signup_form

        return form_list

    def get_form_initial(self, step):
        intstep = int(step)
        questions = list(self.object.questions.all())

        if (
            self.object.start_with_signup and intstep == 0 or
            not self.object.start_with_signup and intstep == len(questions)
        ):
            return {'quiz': self.object}

        return {
            'question': questions[intstep - 1]
        }

    def get_form(self, step=None, data=None, files=None):
        """
        This method was copied from the base Django 1.6 wizard
        class in order to support a callable `get_form_class`
        method which allows dynamic modelforms.
        """
        if step is None:
            step = self.steps.current

        form_list = self.get_form_list()
        kwargs = self.get_form_kwargs(step)
        kwargs.update({
            'data': data,
            'files': files,
            'initial': self.get_form_initial(step),
        })

        return form_list[step](**kwargs)

    def done(self, form_list, **kwargs):
        first = self.object.start_with_signup
        result_form = form_list.pop(0) if first else form_list.pop()
        result = result_form.save()

        for form in form_list:
            form.save(result)

        return HttpResponseRedirect(
            getattr(settings, 'QUIZ_REDIRECT_URL', reverse('quiz-thankyou')))


class ThankYouView(TemplateView):
    template_name = 'quiz/thankyou.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = Quiz.objects.get_current()
        if not self.object:
            raise Http404("Quiz doesn't exist.")
        return super(ThankYouView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(ThankYouView, self).get_context_data(**kwargs)
        ctx['object'] = self.object
        return ctx
