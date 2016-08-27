from django.test import TestCase
from django.utils import timezone

from todo_api import models, serializers
from todo_api.testing_utils import create_task, get_user


class TestTaskSerializer(TestCase):
    """Test cases for the task serializer."""

    def test_serialize(self):
        """Test serializing a task.

        Serializing a task should return the task's details in JSON
        form.
        """
        data = {
            'user': get_user(),
            'title': 'Test Task',
            'description': 'A task to be completed.',
            'due_date': timezone.now(),
            'done': False,
        }
        task = create_task(**data)

        serializer = serializers.TaskSerializer(task)

        expected = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'due_date': task.due_date.isoformat(),
            'done': task.done,
        }

        self.assertEqual(expected, serializer.data)

    def test_deserialize(self):
        """Test deserializing a task.

        If valid data is given, a task should be able to be created from
        the given data.
        """
        now = timezone.now()
        data = {
            'title': 'Test Task',
            'description': 'A task to be completed.',
            'due_date': now.isoformat(),
            'done': True,
        }

        serializer = serializers.TaskSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        task = serializer.save(user=get_user())

        self.assertEqual(1, models.Task.objects.count())
        self.assertEqual(data['title'], task.title)
        self.assertEqual(data['description'], task.description)
        self.assertEqual(now, task.due_date)
        self.assertEqual(data['done'], task.done)
