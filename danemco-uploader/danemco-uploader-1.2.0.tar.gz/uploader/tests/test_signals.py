from django.test import TestCase

from ..models import ImageUpload, ThumbnailSize


class SignalsTest(TestCase):
    fixtures = [
        'initial_data.json',
        'uploader_test_data.json',
    ]

    def test_image_upload_post_init(self):
        image_upload = ImageUpload.objects.get(pk=1)
        image_upload.resize_image.add(ThumbnailSize.objects.get(pk=1))
        self.assertEqual(image_upload.thumbnail_set.count(), 0)
        image_upload = ImageUpload.objects.get(pk=1)

        # Verify that initializing the image upload caused the
        # `force_thumbnails` receiver function to execute.

        self.assertEqual(image_upload.thumbnail_set.count(), 1)

    def test_image_upload_post_save(self):
        image_upload = ImageUpload.objects.get(pk=1)
        image_upload.resize_image.add(ThumbnailSize.objects.get(pk=1))
        self.assertEqual(image_upload.thumbnail_set.count(), 0)
        image_upload.save()

        # Verify that saving the image upload caused the
        # `create_thumbnails` receiver function to execute.

        self.assertEqual(image_upload.thumbnail_set.count(), 1)
