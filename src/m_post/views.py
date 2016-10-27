from rest_framework import permissions
from rest_framework import viewsets
from django.shortcuts import render

# Create your views here.
from m_post.models import Post
from m_post.permissions import IsOwnerOrReadOnly
from m_post.serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def get_queryset(self):
        qs = super(PostViewSet, self).get_queryset()
        if self.request.query_params.get('sender'):
            qs = qs.filter(sender__owner__username=self.request.query_params.get('sender'))
        return qs
