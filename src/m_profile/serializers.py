from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.validators import UniqueTogetherValidator

from core.serializers import GetAsProfileMixin
from m_like.serializers import LikeableMixinSerializerMixin
from m_profile.models import UserProfile, CommunityProfile, Friendship, Profile


class UserProfileSerializer(LikeableMixinSerializerMixin):

    class Meta:
        model = UserProfile
        fields = ('id',
                  'first_name',
                  'last_name',
                  'gender',
                  'birthday',
                  'like_count',
                  'dislike_count',
                  'rating',
                  'user_like')


class CommunityProfileSerializer(LikeableMixinSerializerMixin):

    class Meta:
        model = CommunityProfile
        fields = ('id',
                  'name',
                  'description',
                  'like_count',
                  'dislike_count',
                  'rating',
                  'user_like')


class FriendshipOutgoingSerializer(GetAsProfileMixin):
    request_from = serializers.ReadOnlyField(source='request_from.id')

    def validate_request_to(self, data):
        as_profile = self.get_as_profile()
        if data == as_profile:
            raise serializers.ValidationError('Do you really have no friends other than yourself? :(')
        qs = Friendship.objects\
            .filter(is_deleted=False)\
            .filter((Q(request_from=as_profile) & Q(request_to=data))
                    | (Q(request_from=data) & Q(request_to=as_profile)))\
            .first()
        if qs is not None:
            raise serializers.ValidationError('Friendship already exists')
        return data

    class Meta:
        model = Friendship
        fields = ('id',
                  'request_from',
                  'request_to',
                  'request_text')
        extra_kwargs = {
            'request_to': {
                'queryset': Profile.objects.filter(Q(userprofile__isnull=False) | Q(communityprofile__is_deleted=False))
            }
        }


class FriendshipIncomingSerializer(GetAsProfileMixin):
    request_from = serializers.ReadOnlyField(source='request_from.id')
    request_to = serializers.ReadOnlyField(source='request_to.id')
    request_text = serializers.ReadOnlyField()

    def validate_is_accepted(self, data):
        if not data:
            raise serializers.ValidationError('Y tho? U didn\'t change shit')
        return data

    class Meta:
        model = Friendship
        fields = ('id',
                  'request_from',
                  'request_to',
                  'request_text',
                  'is_accepted')


class FriendshipSerializer(GetAsProfileMixin):
    request_from = serializers.ReadOnlyField(source='request_from.id')

    def validate_request_to(self, data):
        if data == self.get_as_profile():
            raise serializers.ValidationError('Do you really have no friends other than yourself? :(')
        return data

    class Meta:
        model = Friendship
        fields = ('id',
                  'request_from',
                  'request_to',
                  'request_text')
