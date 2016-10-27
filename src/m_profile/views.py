from django.shortcuts import render

# Create your views here.
from rest_framework import permissions
from rest_framework import viewsets

from m_profile.models import UserProfile
from m_profile.permissions import IsOwnerOrReadOnly
from m_profile.serializers import UserProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
