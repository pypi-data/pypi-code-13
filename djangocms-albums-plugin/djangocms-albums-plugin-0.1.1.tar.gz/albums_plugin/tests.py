import os
from PIL import Image

from django.test import TestCase
from django.core.files.base import ContentFile

from models import generate_thumbnail 
from models import Photo
from models import PhotoAlbum

class PhotoTest(TestCase):
    def setUp(self):
        image_loc = os.path.join(
            os.path.dirname(__file__),
            'test_assets/photo.jpg'
        )
        data = open(image_loc, 'r')
        album = PhotoAlbum.objects.create(name='test_album')
        photo = Photo(album=album)
        photo.image.save(image_loc, ContentFile(data))

    def test_it_fails(self):
        self.assertTrue(False)


class PhotoAlbumTest(TestCase):
    def setUp(self):
        pass

    def test_it_passes(self):
        self.assertTrue(True)
