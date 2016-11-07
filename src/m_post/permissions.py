from rest_framework import permissions

from m_post.models import Post
from m_profile.models import Profile


class IsOwnerOrReadOnlyDeleteForYou(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if view.tt_get_as_profile() == obj.sender:
            return True
        if obj.profile == view.tt_get_as_profile() and request.method == 'DELETE':
            return True
        return False


class IsPostSenderOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.tt_get_as_profile() == obj.message.sender:
            return True
        if (request.method in permissions.SAFE_METHODS) and (
            (obj.message.profile == view.tt_get_as_profile())
                or (obj.message.profile.is_friends_with_id(view.tt_get_as_profile_id()))
        ):
            return True
        return False


class CorrectForProfile(permissions.BasePermission):
    def has_permission(self, request, view):
        as_profile = request.query_params.get('for_profile', default=None)
        if as_profile is not None:
            try:
                as_profile = int(as_profile)
            except (TypeError, ValueError):
                return False
            as_profile = Profile.objects.filter(id=as_profile).first()
            if as_profile is None:
                return False
            else:
                if not hasattr(as_profile, 'userprofile'):
                    as_profile = as_profile.communityprofile
                    if as_profile.is_deleted:
                        return False
                return True
        else:
            return True


class HasCorrectForPost(permissions.BasePermission):
    def has_permission(self, request, view):
        for_post = request.query_params.get('for_post', default=None)
        if for_post is not None:
            try:
                for_post = int(for_post)
            except (TypeError, ValueError):
                return False
            for_post = Post.objects.filter(is_deleted=False).filter(id=for_post).first()
            if for_post is None:
                return False
            else:
                if not for_post.sender == view.tt_get_as_profile():
                    if not for_post.profile == view.tt_get_as_profile():
                        if not (for_post.profile.is_friends_with_id(view.tt_get_as_profile_id()) or for_post.sender == for_post.profile):
                            return False
                return True
        else:
            return False
