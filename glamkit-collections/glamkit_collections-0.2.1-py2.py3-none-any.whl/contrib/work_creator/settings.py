from django.conf import settings

COLLECTION_MODELS = getattr(settings, 'COLLECTION_MODELS', {})

# Where to store downloaded NetX images, relative to `MEDIA_ROOT`.
WORK_IMAGE_PATH = COLLECTION_MODELS.get(
    'work_image_path', 'collection_images')
