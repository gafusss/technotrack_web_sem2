from rest_framework import serializers

from m_profile.models import Profile


class GetAsProfileMixin(serializers.ModelSerializer):

    def get_as_profile(self):
        request = self.context['request']
        user = request.user
        as_profile = request.query_params.get('as_profile', default=None)

        if as_profile is None:
            if hasattr(user, 'profile'):
                as_profile = user.profile.profile_ptr
            else:
                # FIXME: ? Hack for newly created community profiles by users without personal profile
                if user.community_profile.count() > 0:
                    as_profile = user.community_profile.first().profile_ptr
        else:
            as_profile = Profile.objects.get(id=int(as_profile))
        return as_profile
