@when('I go home')
def step(context):
    context.browser.get('http://localhost:8000')
