from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions

from m_profile.models import Profile


class CorrectForObject(permissions.BasePermission):
    def has_permission(self, request, view):
        for_content_type = request.query_params.get('for_content_type', default=None)
        for_object_id = request.query_params.get('for_object_id', default=None)
        for_object = None

        as_profile = request.query_params.get('as_profile', default=request.user.profile.id)
        as_profile = Profile.objects.get(id=as_profile)
        user = request.user

        if for_content_type is None or for_object_id is None:
            return False
        else:
            try:
                for_object_id = int(for_object_id)
                for_content_type = int(for_content_type)
            except (TypeError, ValueError):
                return False
            for_object = ContentType.objects.filter(id=for_content_type).first()
            if for_object is None:
                return False
            for_object = for_object.get_object_for_this_type(id=for_object_id)
            if for_object is None:
                return False
            if hasattr(for_object, 'is_deleted') and for_object.is_deleted:
                return False
            if not hasattr(for_object, 'tt_is_likeable') or not for_object.tt_is_likeable:
                return False
            if not for_object.get_object_permissions_for_profile('GET', user, as_profile):
                return False
            return True
