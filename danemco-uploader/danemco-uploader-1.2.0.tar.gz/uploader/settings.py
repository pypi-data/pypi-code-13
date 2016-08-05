from django.conf import settings

default_settings = {
    'enable_force_thumbnails_receiver': True,
}

UPLOADER_SETTINGS = {}


def compute_settings():
    for name, value in default_settings.items():
        UPLOADER_SETTINGS[name] = value

    if hasattr(settings, 'UPLOADER'):
        UPLOADER_SETTINGS.update(settings.UPLOADER)

compute_settings()
