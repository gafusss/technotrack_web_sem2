# coding=utf-8

from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.db.models import Q
from rest_framework import permissions

from core.models import DeletableMixin, EditableMixin
from m_event.models import CreateEventOnCreateMixin
from m_like.models import LikeableMixin

# TODO: __unicode__ or __str__ (unicode on python2) AND meta verbose_name (_plural) AND unique?
# TODO: other fields in profiles
# Create your models here.
from m_post.mixins import PostIncludableMixin


class Profile(EditableMixin, LikeableMixin, PostIncludableMixin):
    tt_is_likeable = False
    tt_is_post_includable = False


    def __unicode__(self):
        if hasattr(self, 'userprofile'):
            return self.userprofile.__unicode__()
        else:
            return self.communityprofile.__unicode__()

    def get_object_permissions_for_profile(self, method, user, profile):
        if hasattr(self, 'userprofile'):
            return self.userprofile.get_object_permissions_for_profile(method, user, profile)
        else:
            return self.communityprofile.get_object_permissions_for_profile(method, user, profile)

    def tt_can_profile_include_in_post(self, profile):
        return False

    def is_friends_with_id(self, other_profile_id):
        f = Friendship.objects \
            .filter(is_active=True) \
            .filter(
            (
                Q(request_from__id=other_profile_id)
                & Q(request_to=self)
            ) | (
                Q(request_to__id=other_profile_id)
                & Q(request_from=self)
            ))
        return f.count() == 1

    def is_friends_with(self, other_profile):
        f = Friendship.objects \
            .filter(is_active=True) \
            .filter(
            (
                Q(request_from=other_profile)
                & Q(request_to=self)
            ) | (
                Q(request_to=other_profile)
                & Q(request_from=self)
            ))
        return f.count() == 1




        # # denorm: active friends
        # friend = models.ManyToManyField('self',
        #                                 verbose_name=u'Friends',
        #                                 related_name='friend',
        #                                 symmetrical=True)
        # # denorm: active chats
        # chat = models.ManyToManyField('m_chat.Chat',
        #                               verbose_name=u'Chats',
        #                               symmetrical=False)
        # TODO: denorm: number of friends, friend requests, other shit, every fucking counter
        # TODO: avatar = foreign key to photos? cut box? wtf?


class UserProfile(Profile):
    tt_is_likeable = True
    tt_is_post_includable = True

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

    def get_object_permissions_for_profile(self, method, user, profile):
        if profile is None:
            return False
        if method in permissions.SAFE_METHODS:
            return True
        if method == 'DELETE':
            return False
        if self.owner == user:
            return True
        return False

    owner = models.OneToOneField(settings.AUTH_USER_MODEL,
                                 verbose_name='Owner',
                                 related_name='profile',
                                 on_delete=models.CASCADE,
                                 blank=False,
                                 db_index=True)

    first_name = models.CharField(max_length=100,
                                  blank=False,
                                  verbose_name=u'First name')
    last_name = models.CharField(max_length=100,
                                 blank=False,
                                 verbose_name=u'Last name')
    gender = models.BooleanField(default=True,
                                 blank=False,
                                 null=False,
                                 verbose_name=u'Gender (male?)')
    birthday = models.DateField(blank=False,
                                null=False,
                                verbose_name=u'Birthday')


class CommunityProfile(DeletableMixin, Profile):
    tt_is_likeable = True
    tt_is_post_includable = True

    def __unicode__(self):
        return 'Community: ' + self.name

    def get_object_permissions_for_profile(self, method, user, profile):
        if profile is None or self.is_deleted:
            return False
        if method in permissions.SAFE_METHODS:
            return True
        if method == 'DELETE':
            return False
        if self.owner == user:
            return True
        return False

    def tt_can_profile_include_in_post(self, profile):
        return not self.is_deleted

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              verbose_name=u'Profile owner',
                              related_name='community_profile',
                              on_delete=models.CASCADE,
                              blank=False)

    name = models.CharField(blank=False,
                            max_length=256,
                            verbose_name=u'Community name')
    description = models.TextField(blank=True,
                                   verbose_name=u'Description')


class Friendship(DeletableMixin, CreateEventOnCreateMixin):
    # is magic
    def get_user_for_event(self):
        return self.request_from_user

    def get_profile_for_event(self):
        return self.request_from

    def get_object_permissions_for_profile(self, method, user, profile):
        if profile is None or self.is_deleted:
            return False
        if method in permissions.SAFE_METHODS:
            if self.request_from == profile or self.request_to == profile:
                return True
            else:
                return False
        if method == 'DELETE':
            if self.request_to == profile or self.request_from == profile:
                return True
            else:
                return False
        # POST, PUT, PATCH
        # Accept incoming only
        if self.request_to == profile:
            return True
        return False

    request_from = models.ForeignKey(Profile,
                                     related_name='friendship_request_sent',
                                     verbose_name=u'Request from',
                                     blank=False)
    request_from_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                          verbose_name=u'By user',
                                          related_name='friendship_request_sent',
                                          blank=False)
    request_to = models.ForeignKey(Profile,
                                   related_name='friendship_request',
                                   verbose_name=u'Request to',
                                   blank=False)
    accepted_by_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                         verbose_name=u'Accepted by user',
                                         related_name='friendship_request',
                                         blank=True,
                                         null=True)
    # is_active == (accepted and not deleted)
    # handled by pre_save signal
    is_active = models.BooleanField(blank=False,
                                    default=False,
                                    verbose_name=u'Is active')

    # is_accepted == (accepted_at is not blank)
    is_accepted = models.BooleanField(blank=False,
                                      default=False,
                                      verbose_name=u'Is accepted')
    # handled by signal
    accepted_at = models.DateTimeField(blank=True,
                                       null=True,
                                       default=None,
                                       verbose_name=u'Accepted at')
    request_text = models.TextField(blank=True,
                                    verbose_name=u'Request text')

    class Meta:
        index_together = [
            ['request_from', 'is_active'],
            ['request_to', 'is_active'],
        ]
