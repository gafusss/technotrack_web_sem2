from django.contrib import admin

# Register your models here.
from m_photo.models import PhotoAlbum, Photo

admin.site.register(Photo)
admin.site.register(PhotoAlbum)
