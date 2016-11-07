from rest_framework import permissions

from m_photo.models import PhotoAlbum
from m_profile.models import Profile


class HasCorrectForAlbum(permissions.BasePermission):
    def has_permission(self, request, view):
        for_album = request.query_params.get('for_album', default=None)
        if for_album is not None:
            try:
                for_album = int(for_album)
            except (TypeError, ValueError):
                return False
            for_album = PhotoAlbum.objects.filter(id=for_album).filter(is_deleted=False).first()
            if for_album is None:
                return False
            else:
                as_profile = request.query_params.get('as_profile', default=request.user.profile.id)
                as_profile = Profile.objects.get(id=as_profile)
                if for_album.profile == as_profile or for_album.profile.is_friends_with(as_profile):
                    return True
                else:
                    return False
        else:
            return False
