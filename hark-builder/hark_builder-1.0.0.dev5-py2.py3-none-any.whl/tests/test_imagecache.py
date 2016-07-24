import hark_builder.imagecache

import hark.models.base_image
import hark.models.image

import unittest
from .util import patch, MagicMock


class TestS3ImageCache(unittest.TestCase):

    @patch('hark_imagestore.lib.aws.S3Bucket.url')
    def test_full_base_image_path(self, mockS3BucketUrl):
        ic = hark_builder.imagecache.S3ImageCache('foo', 'bar')

        base_image = hark.models.base_image.BaseImage(
            guest='Debian-7', version=1)
        base_image.validate()

        ret = 'blah blah blah'
        mockS3BucketUrl.return_value = ret
        assert ic.full_base_image_path(base_image) == ret

    @patch('hark_imagestore.lib.aws.S3Bucket.put_object')
    def test_upload_image(self, mockPutObject):
        image = hark.models.image.Image(
            guest='Debian-7', driver='virtualbox', version=1)

        ic = hark_builder.imagecache.S3ImageCache('foo', 'bar')
        body = MagicMock()
        ic.upload_image(image, body)
        mockPutObject.assert_called_with(image.s3_path(), body, callback=None)
