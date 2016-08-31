try:
    from test_variables import variables, server_uri_test
except ImportError:
    variables = False
import unittest
from models import Mail
from client import PostMan


class TestAuthentication(unittest.TestCase):
    def setUp(self):
        if variables:
            self.test_server_uri = server_uri_test
            self.variables = variables
        else:
            self.test_server_uri = None
            self.variables = {
                "recipients": [
                    "Foo Bar <foo.bar@gmail.com>",
                    "Fulano Aquino <fulano.aquino@gmail.com>",
                    "<ciclano.norego@gmail.com>"
                ],
                "context_per_recipient": {
                    "foo.bar@gmail.com": {"foo": True},
                    "fulano.arquino@gmail.com.br": {"bar": True}
                },
                "from_name": 'Beutrano',
                "from_email": 'beutrano@gmail.com',
                "template_name": 'test-101',
                "key": '2e7be7ced03535958e35',
                "secret": 'ca3cdba202104fd88d01'
            }
        self.postman = PostMan(key=self.variables['key'], secret=self.variables['secret'],
                               server_uri=self.test_server_uri)

    def test_method_post_text(self):
        mail = Mail(
            recipient_list=self.variables['recipients'],
            message="Just a Test, delete if you want.",
            from_name=self.variables['from_name'],
            from_email=self.variables['from_email'],
            subject="Just a test"
        )
        response = self.postman.send(mail)
        if response and 'emails_enviados' in response:
            self.assertGreater(len(response['emails_enviados']), 0)
        else:
            self.assertIsNotNone(response)

    def test_method_post_template(self):
        mail = Mail(
            headers={'X_CLIENT_ID': 1},
            recipient_list=self.variables['recipients'],
            from_name=self.variables['from_name'],
            from_email=self.variables['from_email'],
            template_name=self.variables['template_name'],
            context={'foobar': True},
            context_per_recipient=self.variables['context_per_recipient'],
            use_template_subject=True,
            use_template_email=False,
            use_template_from=False,
            activate_tracking=True,
            get_text_from_html=True,
            expose_recipients_list=True
        )
        response = self.postman.send_template(mail)
        if response and 'emails_enviados' in response:
            self.assertGreater(len(response['emails_enviados']), 0)
        else:
            self.assertIsNotNone(response)


if __name__ == '__main__':
    unittest.main()
