from rest_framework import permissions

from m_profile.models import Profile


class CorrectAsProfileOrCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        print request.method
        print 'Checking perm'
        as_profile = request.query_params.get('as_profile', default=None)
        user = request.user
        if as_profile is not None:
            try:
                as_profile = int(as_profile)
            except (TypeError, ValueError):
                # incorrect as_profile
                return False
            as_profile = Profile.objects.filter(id=as_profile).first()
            if as_profile is None:
                # incorrect as_profile
                return False
            else:
                if hasattr(as_profile, 'userprofile'):
                    as_profile = as_profile.userprofile
                else:
                    as_profile = as_profile.communityprofile
                    if as_profile.is_deleted:
                        # incorrect as_profile
                        return False
                if as_profile.owner != user:
                    # incorrect as_profile
                    return False
                # here we have a correct as_profile
                # return True
        else:
            # no as_profile
            if hasattr(user, 'profile'):
                as_profile = user.profile
        # Here we have either a community profile that belongs to the user, or his userprofile or None

        if request.method == 'HEAD' or request.method == 'OPTIONS':
            return True
        if request.method == 'GET':
            if as_profile is not None:
                return True
            return False
        # Should be additional object permission check for update operations
        print request.method
        print 'ALLOW'
        return True

class IsOwnerOrReadOnlyCreateIfAbsent(permissions.BasePermission):
    def has_permission(self, request, view):
        print request.method
        print 'hp'
        if (request.method in permissions.SAFE_METHODS) or not (hasattr(request.user, 'profile')):
            return True
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class ReadCreateAnyPatchOthersDeleteSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'DELETE':
            return obj.request_from.id == request.query_params.get('as_profile', default=request.user.profile.id) \
                   or obj.request_to.id == request.query_params.get('as_profile', default=request.user.profile.id)
        if request.method == 'PATCH':
            return obj.request_to.id == request.query_params.get('as_profile', default=request.user.profile.id)
        return False
