"""Common exceptions for the kube package."""


class KubeError(Exception):
    """Base exception for all other exceptions from kube."""


class APIError(KubeError):
    """Error from the Kubernetes API server."""

    def __init__(self, response, message=None):
        self.response = response
        self.message = message
        self.status_code = response.status_code
        super().__init__(response, message)

    def __str__(self):
        try:
            api_message = self.response.json()['message']
        except Exception:       # pylint: disable=broad-except
            api_message = None
        if self.message and api_message:
            return self.message + ' ' + api_message
        else:
            return self.message or api_message or ''


class StatusError(KubeError):
    """The requested status item is unavailable."""


class NamespaceError(KubeError):
    """The namespace does not exist."""
