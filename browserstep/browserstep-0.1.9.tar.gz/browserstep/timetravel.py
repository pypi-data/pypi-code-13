"""
These steps work by making a request to the server that then
internally uses something like `freezegun` to change the time
on the server. You'll need to install `requests` too.

You would use it like this:

1. Import freezegun before anything else that uses date or time

   ::

       # Do NOT enable time travel on production
       # or users could go back in time and mess things up
       TIME_TRAVEL = not str(os.environ.get('TIME_TRAVEL')).lower() == 'false'
       if TIME_TRAVEL:
           # Must import this before the datetime module (and hence before Django)
           import freezegun

2. Add the implementation (this is for Django for example):

   ::

       from django.http import HttpResponse
       from django.conf import settings

       if settings.TIME_TRAVEL:
           freezer = None
       
           def timetravel_to(request, date):
               global freezer
               if freezer is not None:
                   freezer.stop()
               freezer = freezegun.freeze_time(date, tick=True)
               freezer.start()
               return HttpResponse('ok')
       
       
           def timetravel_freeze(request, date):
               global freezer
               if freezer is not None:
                   freezer.stop()
               freezer = freezegun.freeze_time(date)
               freezer.start()
               return HttpResponse('ok')
       
       
           def timetravel_cancel(request):
               global freezer
               if freezer is None:
                   return HttpResponse('not time travelling')
               freezer.stop()
               freezer = None
               return HttpResponse('ok')


3. Make requests to change things.

Bear in mind that if you have a multi-process deployment (Heroku?) that
different requests might end up in different times!
"""

from behave import *


@step('I time travel to {date}')
def step_impl(context, date):
    time_travel_url = '{}{}'.format(
        context.config.userdata['test_host'],
        context.config.userdata['time_travel_path'],
    )
    r = requests.get(time_travel_url+'/to/'+date)
    assert r.status_code == 200, r.status_code
    assert r.text == 'ok'

@step('I freeze time at {date}')
def step_impl(context, date):
    time_travel_url = '{}{}'.format(
        context.config.userdata['test_host'],
        context.config.userdata['time_travel_path'],
    )
    r = requests.get(time_travel_url+'/freeze/'+date)
    assert r.status_code == 200, r.status_code
    assert r.text == 'ok'

@step('I return to the current time')
def step_impl(context):
    time_travel_url = '{}{}'.format(
        context.config.userdata['test_host'],
        context.config.userdata['time_travel_path'],
    )
    r = requests.get(time_travel_url+'/cancel')
    assert r.status_code == 200, r.status_code
    assert r.text == 'ok'
