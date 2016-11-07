from rest_framework import serializers

from m_chat.models import Conference, Dialogue, ConferenceMembership, Message, MessageInclude


class MessageSerializer(serializers.ModelSerializer):
    chat = serializers.ReadOnlyField(source='chat.id')
    sender = serializers.ReadOnlyField(source='sender.id')

    class Meta:
        model = Message
        fields = (
            'id',
            'chat',
            'sender',
            'text'
        )


class ConferenceMembershipSerializer(serializers.ModelSerializer):
    conference = serializers.ReadOnlyField(source='conference.id')
    invite_from = serializers.ReadOnlyField(source='invite_from.id')
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = ConferenceMembership
        fields = (
            'id',
            'conference',
            'profile',
            'invite_from',
            'created_at'
        )


class ConferenceSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='profile.id')
    member_count = serializers.ReadOnlyField()
    created_at = serializers.ReadOnlyField()
    last_message = MessageSerializer(read_only=True)

    class Meta:
        model = Conference
        fields = ('id', 'owner', 'member_count', 'created_at', 'last_message')


class DialogueSerializer(serializers.ModelSerializer):
    profile1 = serializers.ReadOnlyField(source='profile1.id')
    created_at = serializers.ReadOnlyField()
    last_message = MessageSerializer(read_only=True)

    class Meta:
        model = Dialogue
        fields = (
            'id',
            'profile1',
            'profile2',
            'created_at',
            'last_message'
        )


