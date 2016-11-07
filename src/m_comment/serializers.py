from rest_framework import serializers

from m_comment.models import Comment
from m_like.serializers import LikeableMixinSerializerMixin


class CommentSerializer(LikeableMixinSerializerMixin):
    profile = serializers.ReadOnlyField(source='profile.id')
    content_type = serializers.ReadOnlyField(source='content_type.id')
    object_id = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = (
            'id',
            'profile',
            'text',
            'content_type',
            'object_id',
            'like_count',
            'dislike_count',
            'rating',
            'user_like'
        )
