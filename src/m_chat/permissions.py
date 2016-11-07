from rest_framework import permissions

from m_chat.models import Chat
from m_profile.models import Profile


class HasCorrectForChat(permissions.BasePermission):
    def has_permission(self, request, view):
        as_profile = request.query_params.get('as_profile', default=request.user.profile.id)
        as_profile = Profile.objects.get(id=as_profile)

        for_chat = request.query_params.get('for_chat', default=None)
        if for_chat is not None:
            try:
                for_chat = int(for_chat)
            except (TypeError, ValueError):
                return False
            for_chat = Chat.objects.filter(id=for_chat).first()
            if for_chat is None:
                return False
            if not for_chat.is_profile_in_chat(as_profile):
                return False
            return True
        else:
            return False


class HasCorrectForConference(permissions.BasePermission):
    def has_permission(self, request, view):
        as_profile = request.query_params.get('as_profile', default=request.user.profile.id)
        as_profile = Profile.objects.get(id=as_profile)

        for_chat = request.query_params.get('for_conference', default=None)
        if for_chat is not None:
            try:
                for_chat = int(for_chat)
            except (TypeError, ValueError):
                return False
            for_chat = Chat.objects.filter(id=for_chat).first()
            if for_chat is None:
                return False
            if not hasattr(for_chat, 'conference'):
                return False
            if not for_chat.is_profile_in_chat(as_profile):
                return False
            return True
        else:
            return False
