import kilometer

CUSTOMER_APP_ID = 'abcdefghi1234567890'
ENDPOINT_URL = 'http://172.31.32.100:9000'
USER_ID = 'jeka pupkin'
GROUP_ID = 'Public GYM'

client = kilometer.EventsAPIClient(CUSTOMER_APP_ID)

client.add_user(USER_ID, {
    'age': 25,
    'birthday_date': '1988-08-22T05:30:00.000Z',
    'is_active': True,
    'name': 'Jevgen',
    'colors': ['red', 'green', 'blue'],
    'strength_level': 10,
    'weight': 100.5},
    endpoint_url=ENDPOINT_URL)

client.add_event(USER_ID, 'workout', {
    'repetitions': 5,
    'day': '2005-01-04T06:25:02.023Z',
    'feel_good': True,
    'exercise': 'Push-Up',
    'colors': ['red', 'green', 'blue']},
    endpoint_url=ENDPOINT_URL)

# kilometer.updateUserProperties(USER_ID, {"strong": True}, endpoint_url=ENDPOINT_URL)
client.update_user_properties(USER_ID, {
    'age': 25,
    'birthday_date': '1988-08-22T05:30:00.000Z',
    'is_active': True,
    'name': 'Jevgen',
    'colors': ['red', 'green', 'blue'],
    'strength_level': 10,
    'weight': 100.5},
    endpoint_url=ENDPOINT_URL)

client.increase_user_property(USER_ID, 'strength_level', 1, endpoint_url=ENDPOINT_URL)

client.decrease_user_property(USER_ID, 'weight', 10, endpoint_url=ENDPOINT_URL)

client.link_user_to_group(USER_ID, GROUP_ID, endpoint_url=ENDPOINT_URL)

client.update_group_properties(GROUP_ID, {
    'days_of_trial': 15,
    'licensed_until': '2015-01-04T06:25:02.023Z',
    'receive_credit_card': True,
    'colors': ['red', 'green', 'blue'],
    'director': 'George Hummerton'},
    endpoint_url=ENDPOINT_URL)
