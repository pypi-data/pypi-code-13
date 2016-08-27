"""Views for the `todo_api` app."""

from rest_framework import permissions, viewsets

from todo_api import models, serializers


class TaskViewSet(viewsets.ModelViewSet):
    """View set for viewing/editing tasks."""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.TaskSerializer

    def get_queryset(self):
        """Return the tasks owned by the user making the request."""
        return models.Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Assign the new task to the user making the request."""
        serializer.save(user=self.request.user)
