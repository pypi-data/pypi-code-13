import os

import hark_imagestore.lib.aws

from hark.models.image import Image

DEFAULT_S3_REGION = 'ap-southeast-2'
DEFAULT_S3_BUCKET = 'harkvm'

BASE_IMAGE_PREFIX = 'machine_images/base'
BUILT_IMAGE_PREFIX = 'machine_images/built'


class S3ImageCache(object):
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None):
        self.bucket = hark_imagestore.lib.aws.S3Bucket(
            DEFAULT_S3_REGION, DEFAULT_S3_BUCKET,
            aws_access_key_id, aws_secret_access_key)

    def images(self):
        objects = self.bucket.list()
        objects = [
            o for o in objects
            if o.startswith('machine_images/built/')
            and len(o.split('/')) == 5
            and '.' in o
        ]
        im = []
        for obj in objects:
            image = Image.from_s3_path(obj)
            im.append(image)
        return im

    def full_image_path(self, image):
        return self.bucket.signed_url(
            os.path.join(BUILT_IMAGE_PREFIX, image.s3_path())
        )

    def full_base_image_path(self, base_image, signed=False):
        key = os.path.join(BASE_IMAGE_PREFIX, base_image.s3_path())
        if signed:
            return self.bucket.signed_url(key)
        else:
            return self.bucket.url(key)
