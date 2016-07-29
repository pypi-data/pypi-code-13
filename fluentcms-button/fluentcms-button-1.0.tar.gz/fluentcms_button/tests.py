from django.test import TestCase
from fluent_contents.tests.factories import create_content_item
from fluent_contents.tests.utils import render_content_items
from fluentcms_button.models import ButtonItem


class ButtonTests(TestCase):
    """
    Testing private notes
    """

    def test_no_output(self):
        """
        Test that the item doens't produce output.
        """
        item = create_content_item(ButtonItem, url='http://example.com', style='btn-primary', title='TEST')
        self.assertEqual(render_content_items([item]).html, u'<a href="http://example.com" class="btn btn-primary">TEST</a>\n')
