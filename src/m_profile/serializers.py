from rest_framework import serializers

from m_profile.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = UserProfile
        fields = '__all__'
