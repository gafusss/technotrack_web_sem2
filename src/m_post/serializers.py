from django.db.models import Q
from rest_framework import serializers

from core.serializers import GetAsProfileMixin
from m_like.serializers import LikeableMixinSerializerMixin
from m_post.models import Post, PostInclude
from m_profile.models import Profile


class PostSerializer(LikeableMixinSerializerMixin):
    sender = serializers.ReadOnlyField(source='sender.id')
    repost_count = serializers.ReadOnlyField()
    comment_count = serializers.ReadOnlyField()

    def validate_profile(self, data):
        as_profile = self.get_as_profile()
        if not data.is_friends_with(self.get_as_profile()) and not as_profile == data:
            raise serializers.ValidationError('Can only post to friends or self')
        return data

    class Meta:
        model = Post
        fields = ('id',
                  'profile',
                  'sender',
                  'text',
                  'comment_count',
                  'repost_count',
                  'like_count',
                  'dislike_count',
                  'rating',
                  'user_like')


class PostIncludeSerializer(GetAsProfileMixin):

    def validate_message(self, data):
        if not data.sender == self.get_as_profile():
            raise serializers.ValidationError('Can only include in own messages')
        return data

    def validate(self, attrs):
        content_type = attrs['content_type']
        object_id = attrs['object_id']
        obj = content_type.get_object_for_this_type(id=object_id)
        if not hasattr(obj, 'tt_is_post_includable') or not obj.tt_is_post_includable:
            raise serializers.ValidationError('Can\'t include that shit')
        if obj.tt_can_profile_include_in_post(self.get_as_profile()):
            raise serializers.ValidationError('Can\'t include that shit')
        return attrs

    class Meta:
        model = PostInclude
        fields = ('id', 'message', 'content_type', 'object_id')
