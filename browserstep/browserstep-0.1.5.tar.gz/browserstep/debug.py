from behave import *


@step('I debug')
def step_impl(context):
    import pdb; pdb.set_trace()
