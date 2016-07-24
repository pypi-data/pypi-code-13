import os

import hark_imagestore.imagecache


BASE_IMAGE_PREFIX = 'machine_images/base'


class S3ImageCache(hark_imagestore.imagecache.S3ImageCache):
    """
    Extend the S3ImageCache from hark_imagestore to be able to talk about base
    images, and to upload images.
    """

    def full_base_image_path(self, base_image):
        key = os.path.join(BASE_IMAGE_PREFIX, base_image.s3_path())
        return self.bucket.url(key)

    def upload_image(self, image, filename, callback=None):
        """Upload an image."""
        self.bucket.put_object(image.s3_path(), filename, callback=callback)
