from django.test import TestCase
from django.utils import timezone

from todo_api import models
from todo_api.testing_utils import get_user


class TestTaskModel(TestCase):
    """Test cases for the task model."""

    def test_create(self):
        """Test creating a `Task` instance with all fields.

        A `Task` should be able to be created with a title, description,
        and due date.
        """
        user = get_user()
        title = 'My Task'
        description = 'More about task'
        due_date = timezone.now()
        done = True

        models.Task.objects.create(
            user=user, title=title, description=description, due_date=due_date,
            done=done)

    def test_defaults(self):
        """Test the defaults for the `Task` model.

        By default, tasks should have their `done` attribute set to
        `False`.
        """
        task = models.Task.objects.create(user=get_user(), title='Test Task')

        self.assertFalse(task.done)

    def test_string_conversion(self):
        """Test converting a `Task` instance to a string.

        Converting the instance to a string should return the instance's
        title.
        """
        task = models.Task(title='Test Task')

        self.assertEqual(task.title, str(task))
