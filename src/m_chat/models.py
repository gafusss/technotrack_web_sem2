# coding=utf-8

from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# TODO: __unicode__ or __str__ (unicode on python2) AND meta verbose_name (_plural) AND unique?
# TODO: on_delete?
# TODO: message read?
#  Create your models here.
from rest_framework import permissions

from core.models import DeletableMixin
from m_post.mixins import PostIncludableMixin


class Chat(models.Model):
    def is_profile_in_chat(self, profile):
        if hasattr(self, 'conference'):
            return self.conference.is_profile_in_chat(profile)
        else:
            return self.dialogue.is_profile_in_chat(profile)

    def get_object_permissions_for_profile(self, method, user, profile):
        if hasattr(self, 'conference'):
            return self.conference.get_object_permissions_for_profile(method, user, profile)
        else:
            return self.dialogue.get_object_permissions_for_profile(method, user, profile)

    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=False,
                                      editable=False,
                                      verbose_name=u'Created at')
    last_message = models.ForeignKey('Message',
                                     db_index=False,
                                     blank=True,
                                     null=True,
                                     editable=False,
                                     verbose_name=u'Last message',
                                     related_name=u'last_message+')


class Conference(Chat):
    def is_profile_in_chat(self, profile):
        return self.is_active and self.membership.filter(is_deleted=False).filter(profile=profile).count() > 0

    def get_object_permissions_for_profile(self, method, user, profile):
        if profile is None or not self.is_active:
            return False
        if method in permissions.SAFE_METHODS:
            return self.is_profile_in_chat(profile)
        return False

    owner = models.ForeignKey('m_profile.Profile',
                              verbose_name=u'Conference owner',
                              related_name='owned_conference',
                              blank=False)
    members = models.ManyToManyField('m_profile.Profile',
                                     verbose_name=u'Conference members',
                                     related_name='conference',
                                     through='ConferenceMembership',
                                     through_fields=('conference', 'profile'))
    # denorm: is_active == (no inactive memberships)
    is_active = models.BooleanField(blank=False,
                                    default=True,
                                    verbose_name=u'Is active')
    member_count = models.PositiveIntegerField(default=0,
                                               blank=False,
                                               null=False,
                                               verbose_name=u'Member count')

    class Meta:
        index_together = [['owner', 'is_active'], ]


class Dialogue(Chat):
    def is_profile_in_chat(self, profile):
        return self.profile1 == profile or self.profile2 == profile

    def get_object_permissions_for_profile(self, method, user, profile):
        if profile is None:
            return False
        if method in permissions.SAFE_METHODS:
            return self.is_profile_in_chat(profile)
        return False

    profile1 = models.ForeignKey('m_profile.Profile',
                                 db_index=True,
                                 verbose_name=u'First person',
                                 related_name='dialogue1',
                                 blank=False)
    profile2 = models.ForeignKey('m_profile.Profile',
                                 db_index=True,
                                 verbose_name=u'Second person',
                                 related_name='dialogue2',
                                 blank=False)


class ConferenceMembership(DeletableMixin):

    def get_object_permissions_for_profile(self, method, user, profile):
        if profile is None or self.is_deleted:
            return False
        if method in permissions.SAFE_METHODS:
            return self.conference.is_profile_in_chat(profile)
        if method == 'DELETE':
            return self.profile == profile or self.conference.owner == profile
        return False

    conference = models.ForeignKey(Conference,
                                   verbose_name=u'Conference',
                                   related_name='membership',
                                   blank=False)
    profile = models.ForeignKey('m_profile.Profile',
                                verbose_name=u'Invited profile',
                                related_name='conference_membership',
                                blank=False)
    invite_from = models.ForeignKey('m_profile.Profile',
                                    related_name='conference_membership_invite',
                                    verbose_name=u'Invite from',
                                    blank=False)


class Message(DeletableMixin, PostIncludableMixin):
    def tt_can_profile_include_in_post(self, profile):
        if self.is_deleted:
            return False
        return self.chat.is_profile_in_chat(profile)

    def get_object_permissions_for_profile(self, method, user, profile):
        if profile is None or self.is_deleted:
            return False
        if method in permissions.SAFE_METHODS:
            return self.sender == profile or self.chat.is_profile_in_chat(profile)
        if method == 'DELETE':
            return self.sender == profile
        return False

    chat = models.ForeignKey(Chat,
                             verbose_name=u'Chat',
                             related_name='message',
                             blank=False)
    sender = models.ForeignKey('m_profile.Profile',
                               verbose_name=u'Sender',
                               related_name='message',
                               blank=False)
    sender_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    verbose_name=u'Sender user',
                                    related_name='message',
                                    blank=False)
    text = models.TextField(blank=True,
                            verbose_name=u'Message text')

    class Meta:
        index_together = [['chat', 'created_at'], ]


# TODO: DRF
class MessageInclude(models.Model):

    def get_object_permissions_for_profile(self, method, user, profile):
        if profile is None or self.message.is_deleted:
            return False
        if method in permissions.SAFE_METHODS:
            return self.message.get_object_permissions_for_profile(method, user, profile)
        return False

    message = models.ForeignKey(Message,
                                db_index=True,
                                verbose_name=u'Message',
                                related_name='include',
                                blank=False)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey(ct_field='content_type',
                               fk_field='object_id')
