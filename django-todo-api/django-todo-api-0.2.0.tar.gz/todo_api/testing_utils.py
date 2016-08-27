from django.contrib.auth import get_user_model

from todo_api import models


def create_task(user=None, title='Test Task', description=None, due_date=None,
                done=None):
    """Create a task with defaults for testing.

    Args:
        user (User,optional):
            The task's owner. Defaults to the test user.
        title (str,optional):
            The task's title. Defaults to `'Test Task'`.
        description (str,optional):
            The task's description. Defaults to `None`.
        due_date:
            The task's due date. Defaults to `None`.
        done:
            Whether or not the task is complete. Defaults to `None`.

    Returns:
        Task:
            A task with the given attributes.
    """
    if user is None:
        user = get_user()

    kwargs = {
        'user': user,
        'title': title,
    }

    if description is not None:
        kwargs['description'] = description

    if due_date is not None:
        kwargs['due_date'] = due_date

    if done is not None:
        kwargs['done'] = done

    return models.Task.objects.create(**kwargs)


def get_user(username='testuser', password='password', email=None):
    """Get a user for testing.

    If there is a user with the given username, that user is returned.
    Otherwise a new user is created.

    Args:
        username (str,optional):
            The user's username. Defaults to `'testuser'`.
        password (str,optional):
            The user's password. Defaults to `'password'`.
        email (str,optional):
            The user's email. Defaults to `None`.

    Returns:
        User:
            The user with the given username if they exist. Otherwise a
            new user with the given parameters is created and returned.
    """
    if get_user_model().objects.filter(username=username).exists():
        return get_user_model().objects.get(username=username)

    kwargs = {
        'username': username,
        'password': password,
    }

    if email is not None:
        kwargs['email'] = email

    return get_user_model().objects.create_user(**kwargs)
