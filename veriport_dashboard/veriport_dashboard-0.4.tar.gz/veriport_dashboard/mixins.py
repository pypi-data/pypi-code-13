from django.contrib.auth.mixins import UserPassesTestMixin


class AdminAccessMixin(UserPassesTestMixin):
    """
    custom mixin to check of admin user access
    """

    def test_func(self):
        return self.request.user.is_superuser


class DashboardAccessMixin(UserPassesTestMixin):
    """
    custom mixin to check of admin user access
    """

    def test_func(self):
        return self.request.user.is_tpa or self.request.user.is_mro
