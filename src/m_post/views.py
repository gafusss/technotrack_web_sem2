from rest_framework import permissions
from rest_framework import viewsets
from django.shortcuts import render

# Create your views here.
from m_post.models import Post, PostInclude
from m_post.permissions import IsOwnerOrReadOnly
from m_post.serializers import PostSerializer, PostIncludeSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        # TODO: Check if they match. Only give your profiles as options
        serializer.save(sender=self.request.user.profile.all().first(),
                        user=self.request.user)

    def get_queryset(self):
        qs = super(PostViewSet, self).get_queryset()
        if self.request.query_params.get('sender'):
            qs = qs.filter(sender__owner__username=self.request.query_params.get('sender'))
        return qs


class PostIncludeViewSet(viewsets.ModelViewSet):
    serializer_class = PostIncludeSerializer
    queryset = PostInclude.objects.all()

    def get_queryset(self):
        qs = super(PostIncludeViewSet, self).get_queryset()
        if self.request.query_params.get('message'):
            qs = qs.filter(message__id=self.request.query_params.get('message'))
        return qs

