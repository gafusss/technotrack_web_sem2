from rest_framework import permissions

from m_profile.models import Profile


class CorrectAsProfile(permissions.BasePermission):
    def has_permission(self, request, view):
        as_profile = request.query_params.get('as_profile', default=None)
        user = request.user
        if as_profile is not None:
            try:
                as_profile = int(as_profile)
            except (TypeError, ValueError):
                return False
            as_profile = Profile.objects.filter(id=as_profile).first()
            if as_profile is None:
                return False
            else:
                if hasattr(as_profile, 'userprofile'):
                    as_profile = as_profile.userprofile
                else:
                    as_profile = as_profile.communityprofile
                    if as_profile.is_deleted:
                        return False
                if as_profile.owner != user:
                    return False
                return True
        else:
            if not hasattr(user, 'profile'):
                return False
            return True


class HasCorrectAsProfile(permissions.BasePermission):
    def has_permission(self, request, view):
        as_profile = request.query_params.get('as_profile', default=None)
        user = request.user
        if as_profile is not None:
            try:
                as_profile = int(as_profile)
            except (TypeError, ValueError):
                return False
            as_profile = Profile.objects.filter(id=as_profile).first()
            if as_profile is None:
                return False
            else:
                if hasattr(as_profile, 'userprofile'):
                    as_profile = as_profile.userprofile
                else:
                    as_profile = as_profile.communityprofile
                    if as_profile.is_deleted:
                        return False
                if as_profile.owner != user:
                    return False
                return True
        else:
            return False


class HasUserProfile(permissions.BasePermission):
    def has_permission(self, request, view):
        if hasattr(request.user, 'profile'):
            return True
        return False


class ModelObjectPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        as_profile = request.query_params.get('as_profile', default=None)
        if as_profile is None:
            as_profile = request.user.profile.profile_ptr
        else:
            as_profile = Profile.objects.get(id=int(as_profile))
        return obj.get_object_permissions_for_profile(request.method, request.user, as_profile)
