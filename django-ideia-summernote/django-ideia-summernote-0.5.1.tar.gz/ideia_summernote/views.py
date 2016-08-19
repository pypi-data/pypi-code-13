import os

from django.http import JsonResponse
from django.template.defaultfilters import slugify
from django.views.generic import View
from django.core.files.storage import default_storage
from django.conf import settings
from django.utils.translation import ugettext as _

from default import SUMMERNOTE_DEFAULT_CONFIG
from ..ideia_summernote.local_exceptions import FileSizeNotSupported

SUMMERNOTE_SETTINGS =  getattr(settings, 'SUMMERNOTE_CONFIG', SUMMERNOTE_DEFAULT_CONFIG)
MAXIMUM_SIZE = getattr(SUMMERNOTE_SETTINGS, 'maximum_image_upload', SUMMERNOTE_DEFAULT_CONFIG['maximum_image_upload'])


def check_sizes(files):

    if files:
        for file in files.values():
            if file.size > MAXIMUM_SIZE:
                raise FileSizeNotSupported()


class Upload(View):

    def post(self, request):

        files = request.FILES
        urls = []

        is_user_authenticated = request.user.is_authenticated()
        if SUMMERNOTE_SETTINGS['restrict_to_user']:
            if not is_user_authenticated:
                return JsonResponse(data={'message': _('Only authenticated users can submit images!')}, status=403)


        if request.FILES:

            try:
                check_sizes(request.FILES)
            except FileSizeNotSupported:
                return JsonResponse(data={'message': _('File size not supported!')}, status=400)

            for file in files.values():
                user_path=''

                if SUMMERNOTE_SETTINGS['use_path_user'] and is_user_authenticated:
                    user_path = request.user.username

                filename = file.name
                ext = slugify(filename.split('.')[-1])
                name = slugify(".".join(filename.split('.')[0:-1]))
                filename = "{0}.{1}".format(name, ext)

                path = os.path.join(settings.MEDIA_ROOT, user_path, filename)
                path = default_storage.save(path, file)
                if path:
                    urls.append(os.path.join(settings.MEDIA_URL, user_path, filename))

        return JsonResponse(data={'urls': urls})