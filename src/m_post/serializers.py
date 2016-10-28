from rest_framework import serializers

from m_post.models import Post, PostInclude


class PostSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.id')
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Post
        fields = '__all__'


class PostIncludeSerializer(serializers.ModelSerializer):
    message = serializers.ReadOnlyField(source='message.id')

    class Meta:
        model = PostInclude
        fields = '__all__'
