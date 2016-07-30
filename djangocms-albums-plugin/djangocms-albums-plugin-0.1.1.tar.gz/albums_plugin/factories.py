import factory

from . import models


class PhotoAlbumFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.PhotoAlbum


class PhotoFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Photo

    image = factory.django.ImageField(color='blue')
    album = factory.SubFactory(PhotoAlbumFactory)
