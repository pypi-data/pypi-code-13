import os
import random
import datetime
import cStringIO
import zipfile
import collections
from PIL import Image

from django.db import models
from django.conf import settings
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from cms.models import CMSPlugin


def generate_thumbnail(photo):
    size = (250, 250)

    abs_path = os.path.join(settings.MEDIA_ROOT,
                            photo.image.name)
    image = Image.open(abs_path)
    image.thumbnail(size)

    outfile = '/tmp/thumb_{0}'.format(photo.image.name.split('/')[-1])
    image.save(outfile, 'JPEG')

    with open(outfile, 'r') as image:
        photo.thumb.save(outfile, File(image), True)

    photo.save()
    os.remove(outfile)


def process_zipfile(uploaded_album):

    if default_storage.exists(uploaded_album.zip_file.name):
        zip = zipfile.ZipFile(uploaded_album.zip_file)
        bad_file = zip.testzip()
        if bad_file:
            raise Exception('"%s" in the .zip archive is corrupt.' % bad_file)

        if not uploaded_album.album:
            uploaded_album.album = PhotoAlbum.objects.create(
                name=uploaded_album.new_album_name
            )

        for filename in sorted(zip.namelist()):
            if filename.startswith('__'):  # do not process meta files
                continue
            print(filename.encode('ascii', errors='replace'))
            data = zip.read(filename)
            if len(data):
                try:
                    # the following is taken from
                    # django.forms.fields.ImageField:
                    # load() could spot a truncated JPEG,
                    # but it loads the entire
                    # image in memory, which is a DoS vector.
                    # See #3848 and #18520.
                    # verify() must be called immediately
                    # after the constructor.
                    Image.open(cStringIO.StringIO(data)).verify()
                except Exception as ex:
                    # if a "bad" file is found we just skip it.
                    print('Error verify image: %s' % ex.message)
                    continue
                if (hasattr(data, 'seek') and
                        isinstance(data.seek, collections.Callable)):
                    print('seeked')
                    data.seek(0)
                try:
                    img = Photo(album=uploaded_album.album)
                    img.image.save(filename, ContentFile(data))
                    img.save()
                except Exception as ex:
                    print('error create Image: %s' % ex.message)
                else:
                    generate_thumbnail(img)
        zip.close()
        uploaded_album.delete()
        # TODO: delete the actual archiver


class PhotoAlbum(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_photo_count(self):
        return self.get_photos().count()

    def get_cover(self):
        photos = self.get_photos()
        try:
            cover = photos.get(is_album_cover=True)
        except Photo.DoesNotExist:
            cover = random.choice(photos)
        else:
            return cover

    def get_photos(self):
        return self.photos.all()


def generate_folder_path(instance, filename):
    folder = 'photos-{0}'.format(datetime.date.today().isoformat())

    filename = filename.split('/')[-1]
    return os.path.join('albums', folder, filename)


class Photo(models.Model):
    image = models.ImageField(upload_to=generate_folder_path)
    thumb = models.ImageField(upload_to=generate_folder_path,
                              null=True, blank=True)
    album = models.ForeignKey(PhotoAlbum, related_name='photos')
    is_album_cover = models.BooleanField(default=False)
    caption = models.TextField(null=True, blank=True)


TEMP_FILE = getattr(settings, 'TEMP_DIR', 'temp/')


# TODO: PostSave signal to process zip file
class AlbumUpload(models.Model):
    zip_file = models.FileField(upload_to=TEMP_FILE)
    album = models.ForeignKey(PhotoAlbum, null=True, blank=True)
    new_album_name = models.CharField(max_length=250, null=True, blank=True)

    def save(self, *args, **kwargs):
        super(AlbumUpload, self).save(*args, **kwargs)
        process_zipfile(self)


class AlbumsPlugin(CMSPlugin):
    album = models.ForeignKey(PhotoAlbum)

    def __unicode__(self):
        return self.album.name
