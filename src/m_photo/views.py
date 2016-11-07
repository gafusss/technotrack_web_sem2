from django.shortcuts import render

# Create your views here.
from rest_framework import permissions
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser

from core.permissions import CorrectAsProfile, ModelObjectPermissions
from m_photo.models import PhotoAlbum, Photo
from m_photo.permissions import HasCorrectForAlbum
from m_photo.serializers import PhotoAlbumSerializer, PhotoSerializer
from m_post.permissions import CorrectForProfile
from m_profile.models import Profile


class PhotoAlbumViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoAlbumSerializer
    queryset = PhotoAlbum.objects.filter(is_deleted=False)
    permission_classes = (
        permissions.IsAuthenticated, CorrectAsProfile, CorrectForProfile, ModelObjectPermissions)

    def tt_get_as_profile_id(self):
        return self.request.query_params.get('as_profile', default=self.request.user.profile.id)

    def tt_get_as_profile(self):
        return Profile.objects.get(id=self.tt_get_as_profile_id())

    def perform_create(self, serializer):
        serializer.save(profile=self.tt_get_as_profile(),
                        user=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def get_queryset(self):
        qs = super(PhotoAlbumViewSet, self).get_queryset()
        as_profile = self.tt_get_as_profile_id()
        for_profile = self.request.query_params.get('for_profile')
        if for_profile:
            qs = qs.filter(profile__id=for_profile)
            for_profile = Profile.objects.get(id=for_profile)
            if not for_profile.is_friends_with_id(as_profile):
                # empty queryset
                qs = qs.filter(user=self.request.user)
        else:
            qs = qs.filter(profile__id=as_profile)
        return qs


class PhotoViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.filter(is_deleted=False).filter(album__is_deleted=False)
    permission_classes = (
        permissions.IsAuthenticated, CorrectAsProfile, HasCorrectForAlbum, ModelObjectPermissions)

    def tt_get_as_profile_id(self):
        return self.request.query_params.get('as_profile', default=self.request.user.profile.id)

    def tt_get_as_profile(self):
        return Profile.objects.get(id=self.tt_get_as_profile_id())

    def perform_update(self, serializer):
        if self.request.data.get('image', None) is not None:
            raise serializers.ValidationError('You are not allowed to change the image')
        serializer.save()

    def perform_create(self, serializer):
        for_album = self.request.query_params.get('for_album')
        for_album = PhotoAlbum.objects.get(id=for_album)
        # TODO: Allow upload to community profiles?
        if not for_album.profile == self.tt_get_as_profile():
            raise serializers.ValidationError('Can only upload to own profile')
        serializer.save(album=for_album,
                        profile=self.tt_get_as_profile(),
                        user=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def get_queryset(self):
        for_album = self.request.query_params.get('for_album')
        for_album = PhotoAlbum.objects.get(id=for_album)
        qs = super(PhotoViewSet, self).get_queryset()
        qs = qs.filter(album=for_album)
        return qs
