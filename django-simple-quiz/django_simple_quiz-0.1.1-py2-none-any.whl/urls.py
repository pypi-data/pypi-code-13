from django.conf.urls import url

from quiz import views

urlpatterns = [
    url(r'^$', views.QuizWizard.as_view(), name='quiz-wizard'),
    url(r'^thankyou/$', views.ThankYouView.as_view(), name='quiz-thankyou'),
]
