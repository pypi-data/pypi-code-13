
import webapp2
import logging

from webapptitude import testkit as helper
from webapptitude import models

from google.appengine.api import users


class TestModel(models.Model, models.UUIDKeyModel, models.TimestampModel):
    name = models.ndb.StringProperty(required=True)
    user = models.UserProperty(auto_current_user_add=True,   # user at create
                               auto_current_user=True)       # user at update
    active = models.BooleanOptionsProperty()



class ModelsTest(helper.ServiceRequestCase):

    @classmethod
    def getHandlers(cls):

        class Handler(webapp2.RequestHandler):

            def get(self):
                return 'OK'

        yield '/', Handler


    def testModels(self):
        self.testbed.loginUser("test@example.com")
        instance = TestModel(name="test", active='off')
        key = instance.put()

        # validates that the key looks like a UUID.
        self.assertEqual(len(key.id().split('-')), 5)

        # validates that the user looks right
        self.assertEqual(instance.user.email(), "test@example.com")

        # Simulate the user changing.
        # (requires altering the ID, since it resolves users by ID)
        self.testbed.loginUser("test2@example.com", id='780')
        instance.name = 'updated test'
        instance.put()  # this should update the user property...

        # logging.info(repr(instance))
        self.assertNotEqual(str(instance.user.email()), "test@example.com")
        self.assertEqual(str(instance.user.email()), "test2@example.com")



    def testModelProfile(self):
        self.testbed.loginUser("test@example.com")
        profile = models.UserProfile.current()
        profile.preferences['color'] = 'orange'
        profile.put()

        profile = models.UserProfile.for_user(users.get_current_user())
        self.assertEqual(profile.preferences['color'], 'orange')
