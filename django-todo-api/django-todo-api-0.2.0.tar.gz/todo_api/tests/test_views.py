from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from todo_api import models, serializers
from todo_api.testing_utils import create_task, get_user


class TestTaskDetailView(APITestCase):
    """Test the view for retrieving a task's details."""

    def setUp(self):
        """Create a test user."""
        self.user = get_user()

    def test_delete(self):
        """Test deleting a task.

        A DELETE request to a task's detail view should delete that
        task.
        """
        self.client.force_authenticate(user=self.user)

        task = create_task(user=self.user)

        url = reverse('task-detail', kwargs={'pk': task.pk})
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_get_details(self):
        """Test getting the details of a task.

        If a valid pk is given, the view should return the details of
        the task with that pk.
        """
        self.client.force_authenticate(user=self.user)

        task = create_task(user=self.user)
        serializer = serializers.TaskSerializer(task)

        url = reverse('task-detail', kwargs={'pk': task.pk})
        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

    def test_invalid_pk(self):
        """Test the view with an invalid pk.

        If no task has the given pk, the view should return a 404 status
        code.
        """
        self.client.force_authenticate(user=self.user)

        url = reverse('task-detail', kwargs={'pk': 1})
        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_multiple_users(self):
        """Test viewing another user's task.

        A user should not be able to view a task owned by a different
        user.
        """
        self.client.force_authenticate(user=self.user)

        other_user = get_user(username='otheruser')
        other_task = create_task(user=other_user)

        url = reverse('task-detail', kwargs={'pk': other_task.pk})
        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_no_permission(self):
        """Test the view as an unauthenticated user.

        An unauthenticated user who tries to access the view should
        receive a 403 status code.
        """
        task = create_task()

        url = reverse('task-detail', kwargs={'pk': task.pk})
        response = self.client.get(url)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_partial_update(self):
        """Test partially updating a task.

        A PATCH request to a task's detail view should allow partial
        updates to be made to that task.
        """
        self.client.force_authenticate(user=self.user)

        task = create_task(user=self.user, title='Test Task', done=False)
        data = {
            'done': True,
        }

        url = reverse('task-detail', kwargs={'pk': task.pk})
        response = self.client.patch(url, data)

        task.refresh_from_db()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(task.done)

    def test_update(self):
        """Test fully updating a task.

        A PUT request to the task's detail view should allow for a full
        update of the task.
        """
        self.client.force_authenticate(user=self.user)

        task = create_task(user=self.user, title='Boring Title')
        data = {
            'title': 'Awesome Title',
        }

        url = reverse('task-detail', kwargs={'pk': task.pk})
        response = self.client.put(url, data)

        task.refresh_from_db()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(data['title'], task.title)


class TestTaskListView(APITestCase):
    """Test the view for listing tasks."""
    url = reverse('task-list')

    def setUp(self):
        """Create a test user."""
        self.user = get_user()

    def test_create(self):
        """Test creating a new task.

        If a POST request is sent to the view, it should create a new
        task.
        """
        self.client.force_authenticate(user=self.user)

        data = {
            'title': 'My Task',
        }

        response = self.client.post(self.url, data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, models.Task.objects.count())
        self.assertEqual(data['title'], models.Task.objects.get().title)

    def test_list_tasks(self):
        """Test the task list view with tasks.

        If there are tasks, the task list view should return a list of
        serialized tasks.
        """
        self.client.force_authenticate(user=self.user)

        task1 = create_task(user=self.user, title='Task 1')
        task2 = create_task(user=self.user, title='Task 2')
        serializer = serializers.TaskSerializer([task1, task2], many=True)

        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

    def test_multiple_users(self):
        """Test the task list with multiple users.

        Users should only see tasks that they own.
        """
        self.client.force_authenticate(user=self.user)

        other_user = get_user(username='otheruser')

        task = create_task(user=self.user, title='My Task')
        create_task(user=other_user, title='Other Task')

        serializer = serializers.TaskSerializer([task], many=True)

        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

    def test_no_permission(self):
        """Test the view as an unauthenticated user.

        If an unauthenticated user tries to access the view, they should
        receive a 403 status code.
        """
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_no_tasks(self):
        """Test the view with no tasks.

        A `GET` request to the view when there are no tasks should
        return an empty list.
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([], response.data)
