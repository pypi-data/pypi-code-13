from django.db.models.signals import post_init, post_save

from .models import ImageUpload, Thumbnail
from .settings import UPLOADER_SETTINGS
from .utils import make_thumbnail


def create_thumbnails(sender, instance, created, **kwargs):
    """
    Creates the thumbnails for an image upload
    """
    for size in instance.resize_image.all():
        tn = make_thumbnail(
            instance.image.url,
            width=size.width,
            height=size.height,
        )

        if tn:
            thumb, created = Thumbnail.objects.get_or_create(
                size=size,
                upload=instance,
            )

            thumb.image = tn
            thumb.save()


def force_thumbnails(sender, instance, **kwargs):
    """
    Forces an image upload to be resaved when it doesn't have any thumbnails
    """
    if instance.id and instance.thumbnail_set.count() == 0:
        instance.save()


post_save.connect(create_thumbnails, sender=ImageUpload)

if UPLOADER_SETTINGS['enable_force_thumbnails_receiver']:
    post_init.connect(force_thumbnails, sender=ImageUpload)
