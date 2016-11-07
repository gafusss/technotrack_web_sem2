from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from core.serializers import GetAsProfileMixin
from m_like.models import Like


class LikeableMixinSerializerMixin(GetAsProfileMixin):
    like_count = serializers.ReadOnlyField()
    dislike_count = serializers.ReadOnlyField()
    rating = serializers.ReadOnlyField()
    user_like = serializers.SerializerMethodField()

    def get_user_like(self, obj):
        return obj.get_like_for_profile(self.get_as_profile())


class LikeSerializer(GetAsProfileMixin):
    profile = serializers.ReadOnlyField(source='profile.id')
    content_type = serializers.ReadOnlyField(source='content_type.id')
    object_id = serializers.ReadOnlyField()

    def validate(self, attrs):
        request = self.context['request']

        for_content_type = request.query_params.get('for_content_type', default=None)
        for_object_id = request.query_params.get('for_object_id', default=None)
        for_content_type = ContentType.objects.get(id=for_content_type)

        content_type = for_content_type

        user = request.user
        obj = content_type.get_object_for_this_type(id=for_object_id)
        if obj.get_like_for_profile(self.get_as_profile()) is not None:
            raise serializers.ValidationError('Like already exists')
        return attrs

    class Meta:
        model = Like
        fields = (
            'id',
            'profile',
            'dislike',
            'content_type',
            'object_id'
        )
