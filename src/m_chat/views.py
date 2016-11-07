from django.db.models import Q
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import serializers
from rest_framework import viewsets
from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import GenericViewSet

from core.permissions import HasUserProfile, CorrectAsProfile, ModelObjectPermissions
from m_chat.models import Conference, Dialogue, ConferenceMembership, Message, MessageInclude, Chat
from m_chat.permissions import HasCorrectForChat, HasCorrectForConference
from m_chat.serializers import ConferenceSerializer, DialogueSerializer, ConferenceMembershipSerializer, \
    MessageSerializer
from m_profile.models import Profile


class ConferenceViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    serializer_class = ConferenceSerializer
    queryset = Conference.objects.filter(is_active=True)
    permission_classes = (permissions.IsAuthenticated,
                          CorrectAsProfile,
                          ModelObjectPermissions)

    def perform_create(self, serializer):
        serializer.save(owner=self.tt_get_as_profile())

    def tt_get_as_profile_id(self):
        return self.request.query_params.get('as_profile', default=self.request.user.profile.id)

    def tt_get_as_profile(self):
        return Profile.objects.get(id=self.tt_get_as_profile_id())

    def get_queryset(self):
        qs = super(ConferenceViewSet, self).get_queryset()
        qs = qs.filter(members=self.tt_get_as_profile())
        return qs


class DialogueViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    serializer_class = DialogueSerializer
    queryset = Dialogue.objects.all()
    permission_classes = (
        permissions.IsAuthenticated, CorrectAsProfile, ModelObjectPermissions
    )

    def tt_get_as_profile_id(self):
        return self.request.query_params.get('as_profile', default=self.request.user.profile.id)

    def tt_get_as_profile(self):
        return Profile.objects.get(id=self.tt_get_as_profile_id())

    def perform_create(self, serializer):
        # FIXME: Validate elsewhere?
        profile1 = self.tt_get_as_profile()
        profile2_id = self.request.data.get('profile2')
        profile2 = Profile.objects.filter(id=profile2_id).first()
        if profile2 is None:
            raise serializers.ValidationError('Wrong profile')
        ds = Dialogue.objects.filter(
            (Q(profile1=profile1) & Q(profile2=profile2)) | (Q(profile1=profile2) & Q(profile2=profile1)))
        if not ds.count() == 0:
            raise serializers.ValidationError('Dialogue already exists')
        serializer.save(profile1=profile1)

    def get_queryset(self):
        qs = super(DialogueViewSet, self).get_queryset()
        qs = qs.filter(Q(profile1=self.tt_get_as_profile()) | Q(profile2=self.tt_get_as_profile()))
        return qs


class ConferenceMembershipViewSet(mixins.CreateModelMixin,
                                  mixins.RetrieveModelMixin,
                                  mixins.ListModelMixin,
                                  mixins.DestroyModelMixin,
                                  GenericViewSet):
    serializer_class = ConferenceMembershipSerializer
    queryset = ConferenceMembership.objects.filter(is_deleted=False)
    permission_classes = (permissions.IsAuthenticated,
                          CorrectAsProfile,
                          HasCorrectForConference,
                          ModelObjectPermissions)

    # TODO: Move validation elsewhere?
    def perform_create(self, serializer):
        for_chat_id = self.request.query_params.get('for_conference', default=None)
        for_chat = Chat.objects.get(id=for_chat_id).conference

        profile = self.request.data.get('profile')
        profile = Profile.objects.filter(id=profile).first()

        if profile is None or for_chat.is_profile_in_chat(profile):
            raise serializers.ValidationError('Can\'t invite that profile')

        serializer.save(invite_from=self.tt_get_as_profile(),
                        conference=for_chat)

    def tt_get_as_profile_id(self):
        return self.request.query_params.get('as_profile', default=self.request.user.profile.id)

    def tt_get_as_profile(self):
        return Profile.objects.get(id=self.tt_get_as_profile_id())

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def get_queryset(self):
        for_chat_id = self.request.query_params.get('for_conference', default=None)
        for_chat = Chat.objects.get(id=for_chat_id).conference

        qs = super(ConferenceMembershipViewSet, self).get_queryset()
        qs = qs.filter(conference=for_chat)
        return qs


# TODO: Make editable?
class MessageViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.filter(is_deleted=False).order_by('-created_at')
    permission_classes = (
        permissions.IsAuthenticated, CorrectAsProfile, HasCorrectForChat, ModelObjectPermissions
    )

    def tt_get_as_profile_id(self):
        return self.request.query_params.get('as_profile', default=self.request.user.profile.id)

    def tt_get_as_profile(self):
        return Profile.objects.get(id=self.tt_get_as_profile_id())

    def perform_create(self, serializer):
        for_chat_id = self.request.query_params.get('for_chat', default=None)
        for_chat = Chat.objects.get(id=for_chat_id)
        serializer.save(chat=for_chat,
                        sender=self.tt_get_as_profile(),
                        sender_user=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def get_queryset(self):
        for_chat_id = self.request.query_params.get('for_chat', default=None)
        qs = super(MessageViewSet, self).get_queryset()
        qs = qs.filter(chat__id=for_chat_id)
        return qs