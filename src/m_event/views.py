from django.shortcuts import render
from rest_framework import permissions

from rest_framework import viewsets
# Create your views here.
from core.permissions import CorrectAsProfile, ModelObjectPermissions
from m_event.models import Event
from m_event.serializers import EventSerializer
from m_profile.models import Profile


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = (
        permissions.IsAuthenticated, CorrectAsProfile, ModelObjectPermissions)

    def tt_get_as_profile_id(self):
        return self.request.query_params.get('as_profile', default=self.request.user.profile.id)

    def tt_get_as_profile(self):
        return Profile.objects.get(id=self.tt_get_as_profile_id())

    def get_queryset(self):
        qs = super(EventViewSet, self).get_queryset()
        # TODO: Add friends events. profile__in = friends | self
        # TODO: Maybe add events for profile?
        # TODO: Hyperlinks?
        qs = qs.filter(profile=self.tt_get_as_profile())
        return qs
