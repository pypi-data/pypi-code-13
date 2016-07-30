from django.contrib import admin

from .models import PhotoAlbum, Photo, AlbumUpload

admin.site.register(PhotoAlbum)
admin.site.register(Photo)
admin.site.register(AlbumUpload)
