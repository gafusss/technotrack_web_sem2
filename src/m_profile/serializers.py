from rest_framework import serializers

from m_post.models import Post, PostInclude


class UserProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Post
        fields = '__all__'
