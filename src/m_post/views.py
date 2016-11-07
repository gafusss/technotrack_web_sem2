from django.db.models import Q
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import GenericViewSet

from core.permissions import CorrectAsProfile, HasCorrectAsProfile, ModelObjectPermissions
from m_post.models import Post, PostInclude
from m_post.permissions import CorrectForProfile, IsOwnerOrReadOnlyDeleteForYou, IsPostSenderOrReadOnly, \
    HasCorrectForPost
from m_post.serializers import PostSerializer, PostIncludeSerializer
from m_profile.models import Friendship, Profile


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.filter(is_deleted=False).order_by('-created_at')
    permission_classes = (
        permissions.IsAuthenticated, CorrectAsProfile, CorrectForProfile, ModelObjectPermissions)

    def perform_create(self, serializer):
        serializer.save(sender=self.tt_get_as_profile(),
                        user=self.request.user)

    def tt_get_as_profile_id(self):
        return self.request.query_params.get('as_profile', default=self.request.user.profile.id)

    def tt_get_as_profile(self):
        return Profile.objects.get(id=self.tt_get_as_profile_id())

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def get_queryset(self):
        qs = super(PostViewSet, self).get_queryset()
        as_profile = self.tt_get_as_profile_id()
        for_profile = self.request.query_params.get('for_profile')
        if for_profile:
            qs = qs.filter(profile__id=for_profile)
            if not Profile.objects.get(id=for_profile).is_friends_with_id(as_profile):
                qs = qs.filter(sender=for_profile)
        else:
            qs = qs.filter(profile__id=as_profile)
        return qs


class PostIncludeViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         GenericViewSet):
    serializer_class = PostIncludeSerializer
    queryset = PostInclude.objects.filter(message__is_deleted=False)
    permission_classes = (permissions.IsAuthenticated, CorrectAsProfile, HasCorrectForPost, ModelObjectPermissions)

    def tt_get_as_profile_id(self):
        return self.request.query_params.get('as_profile', default=self.request.user.profile.id)

    def tt_get_as_profile(self):
        return Profile.objects.get(id=self.tt_get_as_profile_id())

    def get_queryset(self):
        for_post = self.request.query_params.get('for_post')
        qs = super(PostIncludeViewSet, self).get_queryset()
        qs = qs.filter(message__id=for_post)
        return qs
