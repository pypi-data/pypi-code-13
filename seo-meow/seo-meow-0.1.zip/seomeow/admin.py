from django.contrib import admin
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.contrib import messages

from .models import SeoMeow


@admin.register(SeoMeow)
class SeoMeowAdmin(admin.ModelAdmin):

    list_display = (
        'url',
        'description',
        'keywords',
        'modified',
    )

    readonly_fields = (
        'modified',
    )


class SeoMeowShortcut(object):

    _seo_meow_change_url = 'admin:seomeow_seomeow_change'
    _seo_meow_add_url = 'admin:seomeow_seomeow_add'

    def change_view(self, request, object_id, *a, **kw):

        _can_change = request.user.has_perm('seomeow.change_seomeow')
        _can_add = request.user.has_perm('seomeow.add_seomeow')

        if any([_can_add, _can_change]):

            if hasattr(self.model, 'get_absolute_url'):
                instance = self.model.objects.get(pk=object_id)
                instance_url = instance.get_absolute_url()

                try:
                    seo_meow = SeoMeow.objects\
                        .get(url__iexact=instance_url)

                    seo_meow_url = reverse(
                        self._seo_meow_change_url,
                        args=(seo_meow.pk,))

                    message = 'SeoMeow: edit tags at <a href="' \
                        + seo_meow_url + '">' + seo_meow_url + '</a>'

                    if _can_change:
                        self.message_user(request,
                            mark_safe(message),
                            messages.SUCCESS)

                except SeoMeow.DoesNotExist:
                    seo_meow_url = reverse(self._seo_meow_add_url)
                    seo_meow_url += '?url=' + instance_url

                    message = 'SeoMeow: create tags at <a href="' \
                        + seo_meow_url + '">' + seo_meow_url + '</a>'

                    if _can_add:
                        self.message_user(request,
                            mark_safe(message),
                            messages.WARNING)

            else:
                message = 'SeoMeow: "' + self.model.__name__ + '"' \
                    + ' has no "get_absolute_url" method.'
                self.message_user(request, message, messages.ERROR)

        return super(SeoMeowShortcut, self).change_view(
                request, object_id, *a, **kw)
