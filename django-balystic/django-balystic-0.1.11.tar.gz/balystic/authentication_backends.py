from django.contrib.auth import get_user_model
from balystic.client import Client


class BalysticBackend(object):
    """
    Sends the credentials to balystic for authentication
    and allows the user to log in depending on the outcome
    of the operation.
    """
    user_model = get_user_model()

    def authenticate(self, email, password):
        client = Client()
        response = client.authenticate_user(email=email, password=password)
        if 'username' in response.keys():
            try:
                user = self.user_model.objects.get(email=email)
            except self.user_model.DoesNotExist:
                user = self.user_model(email=email, username=response['username'])
                user.save()
            return user
        else:
            return None

    def get_user(self, user_id):
        try:
            return self.user_model.objects.get(pk=user_id)
        except self.user_model.DoesNotExist:
            return None
