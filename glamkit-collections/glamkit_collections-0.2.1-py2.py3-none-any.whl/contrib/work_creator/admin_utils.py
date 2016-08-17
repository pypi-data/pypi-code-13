from django.core.urlresolvers import reverse
from generic.admin.mixins import ThumbnailAdminMixin
from django.conf import settings

def admin_link(obj):
    return "<a href='%s'>%s</a>" % (admin_url(obj), obj)

def admin_url(obj):
    return reverse(
        'admin:%s_%s_change' % (obj._meta.app_label,  obj._meta.model_name),
        args=[obj.id]
    )


def get_thumbnail_options():
    try:
        thumbnail_options = settings.THUMBNAIL_ALIASES['']['admin_collection']
    except KeyError:
        try:
            thumbnail_options = settings.THUMBNAIL_ALIASES['']['admin']
        except:
            thumbnail_options = {'size': (250, 250)}
    return thumbnail_options


class WorkThumbnailMixin(ThumbnailAdminMixin):
    thumbnail_options = get_thumbnail_options()
