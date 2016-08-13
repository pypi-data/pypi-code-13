import django
from django.conf.urls import patterns, url
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import JsonResponse, Http404
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from . import models


class NotificationAdminMixin(admin.ModelAdmin):
    """
    Notification mixing for administration
    """
    def __init__(self, model, admin_site):
        super(NotificationAdminMixin, self).__init__(model, admin_site)
        self.url_name_prefix = '%(app_label)s_%(module_name)s_' % {
            'app_label': self.model._meta.app_label,
            'module_name': self.model._meta.model_name
            if django.VERSION >= (1, 7) else self.model._meta.module_name,
        }
        self.follow_reverse = '%s:%sfollow' % (self.admin_site.name, self.url_name_prefix,)
        self.unfollow_reverse = '%s:%sunfollow' % (self.admin_site.name, self.url_name_prefix,)
        self.followers_reverse = '%s:%sfollowers' % (self.admin_site.name, self.url_name_prefix,)

    def get_urls(self):
        """
        Adds views for 'Followers' tab in the side panel.
        """
        urls = super(NotificationAdminMixin, self).get_urls()

        follow_name = '%sfollow' % (self.url_name_prefix,)
        unfollow_name = '%sunfollow' % (self.url_name_prefix,)
        followers_name = '%sfollowers' % (self.url_name_prefix,)

        followers_urls = patterns(
            '',
            url(r'^(?P<object_id>\d+)/follow/$', self.follow_view, name=follow_name),
            url(r'^(?P<object_id>\d+)/unfollow/$', self.unfollow_view, name=unfollow_name),
            url(r'^(?P<object_id>\d+)/followers/$', self.get_followers_view, name=followers_name),
        )

        return followers_urls + urls

    def get_followers_view(self, request, object_id):
        """
        View to obtain a list of current followers.
        """
        if not request.is_ajax():
            raise Http404

        obj = self.get_model_object(request, object_id)

        response_kwargs = {
            'success': True,
            'followers': [],
            'group_followers': [],
        }

        try:
            follower_information = models.FollowerInformation.objects.get_object_for_instance(obj)

            response_kwargs['followers'] = follower_information.get_followers_display_list()
            response_kwargs['group_followers'] = follower_information\
                .get_group_followers_display_list()

        except models.FollowerInformation.DoesNotExist:
            pass

        return JsonResponse(response_kwargs)

    def follow_view(self, request, object_id, action='add'):
        """
        View to add user or group into the list of followers for a object.
        """
        if not request.is_ajax():
            raise Http404

        if action not in ['add', 'remove']:
            return JsonResponse(
                {
                    'success': False,
                    'error_message': 'The action "%s" is not recognized.' % action
                }
            )

        obj = self.get_model_object(request, object_id)

        required_post_attributes = (
            'type', 'type_id'
        )

        for attr in required_post_attributes:
            if attr not in request.POST.keys():
                return JsonResponse(
                    {
                        'success': False,
                        'error_message': 'Please specify a type and type id.'
                    }
                )

        type_of_follower = request.POST.get('type')
        follower_id = request.POST.get('type_id')

        if type_of_follower not in ['group', 'user']:
            return JsonResponse(
                {
                    'success': False,
                    'error_message': 'The type specified is not accepted.'
                }
            )

        follower_information = models.FollowerInformation.objects.get_or_create_object_for_instance(
            obj
        )

        if type_of_follower == 'group':
            try:
                group = Group.objects.get(id=follower_id)
                getattr(follower_information.group_followers, action)(group)
            except Group.DoesNotExist:
                return JsonResponse(
                    {
                        'success': False,
                        'error_message': 'Group with ID %s could not be found.' % follower_id
                    }
                )
        elif type_of_follower == 'user':
            User = get_user_model()
            try:
                user = User.objects.get(id=follower_id)
                getattr(follower_information.followers, action)(user)
            except User.DoesNotExist:
                return JsonResponse(
                    {
                        'success': False,
                        'error_message': 'User with ID %s could not be found.' % follower_id
                    }
                )

        return JsonResponse(
            {
                'success': True,
                'followers': follower_information.get_followers_display_list(),
                'group_followers': follower_information.get_group_followers_display_list(),
            }
        )

    def unfollow_view(self, request, object_id):
        """
        View to remove user or group into the list of followers for a object.
        """
        return self.follow_view(request, object_id, action='remove')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        Add extra context to the change view to include API URLs.

        :param request: Django request object.
        :param object_id: The id of the object.
        :param form_url: The URL of the form.
        :param extra_context: Extra context dictionary.
        :return: Change view.
        """
        extra_context = extra_context or {}
        extra_context['follow_btn'] = reverse(self.follow_reverse, args=(object_id, ))
        extra_context['unfollow_btn'] = reverse(self.unfollow_reverse, args=(object_id,))
        extra_context['followers_list'] = reverse(self.followers_reverse, args=(object_id,))

        return super(NotificationAdminMixin, self).change_view(
            request, object_id, form_url, extra_context
        )

    def get_model_object(self, request, object_id):
        """
        Obtain the objects model if it exists

        :param request: Django request
        :param object_id: The id of the object to get
        :return: Object
        """
        obj = self.model.objects.get(pk=object_id)

        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(
                _('%s object with primary key %s does not exist.') % (
                    force_text(self.model._meta.verbose_name),
                    escape(object_id)
                )
            )

        if not self.has_change_permission(request) and not self.has_add_permission(request):
            raise PermissionDenied

        return obj
