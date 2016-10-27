from rest_framework import serializers

from m_chat.models import Conference, Dialogue


class ConferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conference
        fields = ('id', 'owner', 'members', 'is_active', 'member_count', 'created_at', 'last_message')

class DialogueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dialogue
        fields = '__all__'

