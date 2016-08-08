from behave import *


@then(u'the alert says "{text}"')
def step_impl(context, text):
    if context.browser_vendor == 'phantomjs':
        raise Exception("PhantomJS does not support alerts")
    alert = context.browser.switch_to_alert()
    assert alert.text == text


@then(u'I cancel the alert')
def step_impl(context):
    if context.browser_vendor == 'phantomjs':
        raise Exception("PhantomJS does not support alerts")
    alert = context.browser.switch_to_alert()
    alert.dismiss()


@then(u'I accept the alert')
def step_impl(context):
    if context.browser_vendor == 'phantomjs':
        raise Exception("PhantomJS does not support alerts")
    alert = context.browser.switch_to_alert()
    alert.accept()
