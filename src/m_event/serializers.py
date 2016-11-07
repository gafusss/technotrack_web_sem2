from rest_framework import serializers

from core.serializers import GetAsProfileMixin
from m_event.models import Event


class EventSerializer(GetAsProfileMixin):
    profile = serializers.ReadOnlyField(source='profile.id')
    timestamp = serializers.ReadOnlyField()
    content_type = serializers.ReadOnlyField(source='content_type.id')
    object_id = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = (
            'id',
            'profile',
            'timestamp',
            'content_type',
            'object_id'
        )
