from rest_framework import viewsets
from django.shortcuts import render

# Create your views here.
from m_chat.models import Conference
from m_chat.serializers import ConferenceSerializer


class ConferenceViewSet(viewsets.ModelViewSet):
    serializer_class = ConferenceSerializer
    queryset = Conference.objects.all()
