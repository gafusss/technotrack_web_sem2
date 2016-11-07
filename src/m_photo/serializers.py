from rest_framework import serializers

from m_like.serializers import LikeableMixinSerializerMixin
from m_photo.models import PhotoAlbum, Photo


class PhotoAlbumSerializer(LikeableMixinSerializerMixin):
    profile = serializers.ReadOnlyField(source='profile.id')

    class Meta:
        model = PhotoAlbum
        fields = (
            'id',
            'profile',
            'name',
            'description',
            'like_count',
            'dislike_count',
            'rating',
            'user_like'
        )


class PhotoSerializer(LikeableMixinSerializerMixin):
    album = serializers.ReadOnlyField(source='album.id')
    profile = serializers.ReadOnlyField(source='profile.id')
    image = serializers.ImageField()
    height = serializers.ReadOnlyField()
    width = serializers.ReadOnlyField()

    class Meta:
        model = Photo
        fields = (
            'id',
            'album',
            'profile',
            'image',
            'height',
            'width',
            'description',
            'like_count',
            'dislike_count',
            'rating',
            'user_like'
        )
