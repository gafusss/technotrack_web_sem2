from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import GenericViewSet

from core.permissions import CorrectAsProfile, ModelObjectPermissions
from m_profile.models import UserProfile, CommunityProfile, Friendship, Profile
from m_profile.permissions import CorrectAsProfileOrCreate
from m_profile.serializers import UserProfileSerializer, CommunityProfileSerializer, FriendshipOutgoingSerializer, \
    FriendshipIncomingSerializer, \
    FriendshipSerializer


class UserProfileViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = (permissions.IsAuthenticated, CorrectAsProfileOrCreate, ModelObjectPermissions)

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'profile'):
            raise PermissionDenied(detail='User already has a profile')
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        qs = super(UserProfileViewSet, self).get_queryset()
        if self.request.query_params.get('self'):
            qs = qs.filter(owner=self.request.user)
        if self.request.query_params.get('id'):
            qs = qs.filter(id=self.request.query_params.get('id'))
        return qs


class CommunityProfileViewSet(viewsets.ModelViewSet):
    serializer_class = CommunityProfileSerializer
    queryset = CommunityProfile.objects.filter(is_deleted=False)
    permission_classes = (permissions.IsAuthenticated, CorrectAsProfileOrCreate, ModelObjectPermissions)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def get_queryset(self):
        qs = super(CommunityProfileViewSet, self).get_queryset()
        if self.request.query_params.get('self'):
            qs = qs.filter(owner=self.request.user)
        return qs

class FriendshipIncomingViewSet(mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.DestroyModelMixin,
                                mixins.ListModelMixin,
                                GenericViewSet):
    serializer_class = FriendshipIncomingSerializer
    queryset = Friendship.objects.filter(is_deleted=False).filter(is_accepted=False)
    permission_classes = (permissions.IsAuthenticated, CorrectAsProfile, ModelObjectPermissions)

    def perform_update(self, serializer):
        serializer.save(accepted_by_user=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def get_queryset(self):
        qs = super(FriendshipIncomingViewSet, self).get_queryset()
        as_profile = self.request.query_params.get('as_profile', default=self.request.user.profile.id)
        qs = qs.filter(request_to__id=as_profile)
        return qs


class FriendshipOutgoingViewSet(mixins.CreateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.DestroyModelMixin,
                                mixins.ListModelMixin,
                                GenericViewSet):
    serializer_class = FriendshipOutgoingSerializer
    queryset = Friendship.objects.filter(is_deleted=False).filter(is_accepted=False)
    permission_classes = (permissions.IsAuthenticated, CorrectAsProfile, ModelObjectPermissions)

    def perform_create(self, serializer):
        serializer.save(request_from_user=self.request.user,
                        request_from=Profile.objects.get(
                            id=self.request.query_params.get('as_profile', default=self.request.user.profile.id)))

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def get_queryset(self):
        qs = super(FriendshipOutgoingViewSet, self).get_queryset()
        as_profile = self.request.query_params.get('as_profile', default=self.request.user.profile.id)
        qs = qs.filter(request_from__id=as_profile)
        return qs


class FriendshipViewSet(mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    serializer_class = FriendshipSerializer
    queryset = Friendship.objects.filter(is_active=True)
    permission_classes = (permissions.IsAuthenticated, CorrectAsProfile, ModelObjectPermissions)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def get_queryset(self):
        qs = super(FriendshipViewSet, self).get_queryset()
        as_profile = self.request.query_params.get('as_profile', default=self.request.user.profile.id)
        qs = qs.filter(Q(request_from__id=as_profile) | Q(request_to__id=as_profile))
        return qs
