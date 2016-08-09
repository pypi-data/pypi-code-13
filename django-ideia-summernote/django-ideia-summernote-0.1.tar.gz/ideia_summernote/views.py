from django.http import JsonResponse
from django.views.generic import View
from django.core.files.storage import default_storage
from django.conf import settings
import os
from default import SUMMERNOTE_DEFAULT_CONFIG
class Upload(View):

    def post(self, request):

        files = request.FILES

        urls = []

        SUMMERNOTE_SETTINGS =  getattr(settings, 'SUMMERNOTE_CONFIG', SUMMERNOTE_DEFAULT_CONFIG)

        is_user_authenticated = request.user.is_authenticated()
        if SUMMERNOTE_SETTINGS['restrict_to_user']:
            if not is_user_authenticated:
                return JsonResponse(data={'urls': urls})

        if request.FILES:
            for file in files.values():
                user_path=''
                if SUMMERNOTE_SETTINGS['use_path_user'] and is_user_authenticated:
                    user_path = request.user.username

                path = os.path.join(settings.MEDIA_ROOT, user_path, file.name)
                path = default_storage.save(path, file)
                if path:
                    urls.append(os.path.join(settings.MEDIA_URL, user_path, file.name))

        return JsonResponse(data={'urls': urls})