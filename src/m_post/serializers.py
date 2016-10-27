from rest_framework import serializers

from m_post.models import Post


class PostSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.id')

    class Meta:
        model = Post
        fields = '__all__'
