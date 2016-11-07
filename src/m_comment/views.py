from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from rest_framework import permissions
from rest_framework import viewsets
# Create your views here.
from core.permissions import CorrectAsProfile, ModelObjectPermissions
from m_comment.models import Comment
from m_comment.permissions import HasCorrectForObject
from m_comment.serializers import CommentSerializer
from m_profile.models import Profile


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.filter(is_deleted=False)
    permission_classes = (
        permissions.IsAuthenticated, CorrectAsProfile, HasCorrectForObject, ModelObjectPermissions
    )

    def tt_get_as_profile_id(self):
        return self.request.query_params.get('as_profile', default=self.request.user.profile.id)

    def tt_get_as_profile(self):
        return Profile.objects.get(id=self.tt_get_as_profile_id())

    def perform_create(self, serializer):
        for_content_type = self.request.query_params.get('for_content_type', default=None)
        for_object_id = self.request.query_params.get('for_object_id', default=None)

        for_content_type = ContentType.objects.get(id=for_content_type)

        serializer.save(sender=self.request.user,
                        profile=self.tt_get_as_profile(),
                        content_type=for_content_type,
                        object_id=for_object_id)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def get_queryset(self):
        for_content_type = self.request.query_params.get('for_content_type', default=None)
        for_object_id = self.request.query_params.get('for_object_id', default=None)

        for_content_type = ContentType.objects.get(id=for_content_type)

        qs = super(CommentViewSet, self).get_queryset()
        qs = qs.filter(content_type=for_content_type).filter(object_id=for_object_id)
        return qs
